// WorldLink: phone alerts (Web Push). Saves a phone's alert address and sends alerts to it.
// Callers prove who they are with their WorldLink (Firebase) sign-in token in the x-wl-token header.
import webpush from "npm:web-push@3.6.7";
import { createRemoteJWKSet, jwtVerify } from "npm:jose@5.9.6";

const JWKS = createRemoteJWKSet(new URL("https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com"));
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type, apikey, x-client-info, x-wl-token",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...CORS, "Content-Type": "application/json" } });
const SB = Deno.env.get("SUPABASE_URL")!, KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const H = { apikey: KEY, Authorization: "Bearer " + KEY, "Content-Type": "application/json" };
const recent = new Map<string, number[]>();

webpush.setVapidDetails(Deno.env.get("VAPID_SUBJECT") || "https://worldlink.app", Deno.env.get("VAPID_PUBLIC")!, Deno.env.get("VAPID_PRIVATE")!);

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  try {
    const proj = Deno.env.get("FB_PROJECT")!;
    const { payload } = await jwtVerify(req.headers.get("x-wl-token") || "", JWKS, { issuer: "https://securetoken.google.com/" + proj, audience: proj });
    const me = String(payload.sub);
    const b = await req.json();
    if (b.a === "sub") {
      const s = b.sub;
      if (!s || typeof s.endpoint !== "string" || !s.endpoint.startsWith("https://")) return json({ ok: false }, 400);
      const r = await fetch(SB + "/rest/v1/push_subs?on_conflict=uid", {
        method: "POST", headers: { ...H, Prefer: "resolution=merge-duplicates" },
        body: JSON.stringify({ uid: me, sub: s, updated: new Date().toISOString() }),
      });
      return json({ ok: r.ok });
    }
    if (b.a === "send") {
      const to = String(b.to || "");
      if (!to || to === me) return json({ ok: false });
      // at most 30 alerts a minute per sender
      const now = Date.now(), L = (recent.get(me) || []).filter((t) => now - t < 60000);
      if (L.length >= 30) return json({ ok: false, why: "slow down" }, 429);
      L.push(now); recent.set(me, L);
      const rs = await (await fetch(SB + "/rest/v1/push_subs?uid=eq." + encodeURIComponent(to) + "&select=sub", { headers: H })).json();
      if (!Array.isArray(rs) || !rs.length) return json({ ok: false, why: "no phone" });
      const msg = JSON.stringify({ t: String(b.t || "WorldLink").slice(0, 60), b: String(b.b || "").slice(0, 140), tag: String(b.tag || "wl").slice(0, 30) });
      try {
        await webpush.sendNotification(rs[0].sub, msg, { TTL: 120, urgency: "high" });
        return json({ ok: true });
      } catch (e) {
        const sc = (e as { statusCode?: number }).statusCode;
        if (sc === 404 || sc === 410) await fetch(SB + "/rest/v1/push_subs?uid=eq." + encodeURIComponent(to), { method: "DELETE", headers: H });
        return json({ ok: false, why: "gone" });
      }
    }
    return json({ ok: false }, 400);
  } catch (e) {
    return json({ ok: false, why: "not allowed" }, 401);
  }
});
