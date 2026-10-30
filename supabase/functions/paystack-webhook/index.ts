// WorldLink: Paystack payment checker. Paystack calls this after every payment.
// It checks the signature, asks Paystack to confirm the payment, then records the coins in Firestore.
const PACKS: Record<number, number> = { 500: 100, 1000: 250, 2000: 600, 5000: 1500 }; // naira -> coins
const enc = new TextEncoder();
async function hmac512(key: string, msg: string) {
  const k = await crypto.subtle.importKey("raw", enc.encode(key), { name: "HMAC", hash: "SHA-512" }, false, ["sign"]);
  const s = await crypto.subtle.sign("HMAC", k, enc.encode(msg));
  return [...new Uint8Array(s)].map((b) => b.toString(16).padStart(2, "0")).join("");
}
const ok = (t = "ok") => new Response(t, { status: 200 });
Deno.serve(async (req) => {
  try {
    const body = await req.text();
    const secret = Deno.env.get("PAYSTACK_SECRET") || "";
    if (!secret) { console.error("PAYSTACK_SECRET missing"); return new Response("not set up", { status: 500 }); }
    if ((await hmac512(secret, body)) !== (req.headers.get("x-paystack-signature") || "")) return new Response("bad signature", { status: 401 });
    const ev = JSON.parse(body);
    if (ev.event !== "charge.success") return ok("ignored");
    const d = ev.data || {};
    const ref = String(d.reference || "");
    const uid = String(d.metadata?.uid || "");
    const naira = Math.round(Number(d.amount) / 100);
    const coins = PACKS[naira];
    if (!/^[\w-]{6,60}$/.test(ref) || !uid || !coins || d.currency !== "NGN") return ok("skipped");
    // ask Paystack again, do not trust the message alone
    const v = await (await fetch("https://api.paystack.co/transaction/verify/" + encodeURIComponent(ref), { headers: { Authorization: "Bearer " + secret } })).json();
    if (!v?.status || v.data?.status !== "success" || Number(v.data?.amount) !== Number(d.amount)) return ok("not confirmed");
    // sign in as the payments helper account
    const key = Deno.env.get("FB_API_KEY"), proj = Deno.env.get("FB_PROJECT");
    const lg = await (await fetch("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + key, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: Deno.env.get("SRV_EMAIL"), password: Deno.env.get("SRV_PASSWORD"), returnSecureToken: true }),
    })).json();
    if (!lg.idToken) { console.error("helper sign-in failed:", JSON.stringify(lg).slice(0, 300)); return new Response("helper sign-in failed", { status: 500 }); }
    const r = await fetch(`https://firestore.googleapis.com/v1/projects/${proj}/databases/(default)/documents/credits?documentId=${encodeURIComponent(ref)}`, {
      method: "POST", headers: { Authorization: "Bearer " + lg.idToken, "Content-Type": "application/json" },
      body: JSON.stringify({ fields: {
        uid: { stringValue: uid }, coins: { integerValue: String(coins) }, naira: { integerValue: String(naira) },
        ts: { integerValue: String(Date.now()) }, test: { booleanValue: d.domain === "test" },
      } }),
    });
    if (r.status === 409) return ok("already recorded");
    if (!r.ok) { console.error("could not save credit:", r.status, (await r.text()).slice(0, 300)); return new Response("could not save", { status: 500 }); }
    console.log("credit recorded", ref, coins);
    return ok("recorded");
  } catch (e) {
    console.error("webhook error:", String(e));
    return new Response("error", { status: 500 });
  }
});
