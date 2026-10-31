// WorldLink: email sender (hello@worldlink.app via Resend).
//  POST {a:"hello"}                 -> saves the signed-in person's email privately and sends the welcome email once
//  POST {a:"test",subject,text}     -> moderator only: sends the message to the moderator's own email
//  POST {a:"broadcast",subject,text}-> moderator only: sends to everyone who has not unsubscribed
//  GET  ?u=<uid>&t=<signature>      -> unsubscribe link inside every update email
// Callers prove who they are with their WorldLink (Firebase) sign-in token in the x-wl-token header.
import { createRemoteJWKSet, jwtVerify } from "npm:jose@5.9.6";

const JWKS = createRemoteJWKSet(new URL("https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com"));
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type, apikey, x-client-info, x-wl-token",
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
};
const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { ...CORS, "Content-Type": "application/json" } });
const enc = new TextEncoder();
const FROM = "WorldLink <hello@worldlink.app>";
const PROJ = Deno.env.get("FB_PROJECT")!;
const DOC = `https://firestore.googleapis.com/v1/projects/${PROJ}/databases/(default)/documents`;
const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

async function sign(msg: string) {
  const k = await crypto.subtle.importKey("raw", enc.encode(Deno.env.get("SRV_PASSWORD") || "x"), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const s = await crypto.subtle.sign("HMAC", k, enc.encode("unsub:" + msg));
  return [...new Uint8Array(s)].map((b) => b.toString(16).padStart(2, "0")).join("").slice(0, 32);
}
async function helperToken(): Promise<string> {
  const lg = await (await fetch("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + Deno.env.get("FB_API_KEY"), {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: Deno.env.get("SRV_EMAIL"), password: Deno.env.get("SRV_PASSWORD"), returnSecureToken: true }),
  })).json();
  if (!lg.idToken) throw new Error("helper sign-in failed");
  return lg.idToken;
}
const dec = (f: any) => ({ email: f?.email?.stringValue || "", name: f?.name?.stringValue || "", unsub: !!f?.unsub?.booleanValue });
async function getMail(tok: string, uid: string) {
  const r = await fetch(`${DOC}/mails/${encodeURIComponent(uid)}`, { headers: { Authorization: "Bearer " + tok } });
  if (r.status === 404) return null;
  if (!r.ok) throw new Error("read mail " + r.status);
  return dec((await r.json()).fields);
}
async function putMail(tok: string, uid: string, m: { email: string; name: string; unsub: boolean }) {
  const r = await fetch(`${DOC}/mails/${encodeURIComponent(uid)}`, {
    method: "PATCH", headers: { Authorization: "Bearer " + tok, "Content-Type": "application/json" },
    body: JSON.stringify({ fields: { email: { stringValue: m.email }, name: { stringValue: m.name }, unsub: { booleanValue: m.unsub }, ts: { integerValue: String(Date.now()) } } }),
  });
  if (!r.ok) throw new Error("save mail " + r.status);
}
async function isMod(tok: string, uid: string) {
  const r = await fetch(`${DOC}/admin/mods`, { headers: { Authorization: "Bearer " + tok } });
  if (!r.ok) return false;
  const j = await r.json();
  return (j.fields?.list?.arrayValue?.values || []).some((v: any) => v.stringValue === uid);
}
async function sendBatch(items: any[]) {
  const r = await fetch("https://api.resend.com/emails/batch", {
    method: "POST", headers: { Authorization: "Bearer " + Deno.env.get("RESEND_KEY"), "Content-Type": "application/json" },
    body: JSON.stringify(items),
  });
  if (!r.ok) throw new Error("resend " + r.status + " " + (await r.text()).slice(0, 200));
}
const wrap = (inner: string, foot: string) => `<div style="background:#f4f6fb;padding:24px 12px;font-family:Arial,sans-serif"><div style="max-width:520px;margin:auto;background:#fff;border-radius:14px;padding:24px;color:#14213d;line-height:1.55"><div style="font-size:22px;font-weight:700;color:#12307F;margin-bottom:12px">🌍 WorldLink</div>${inner}</div><p style="max-width:520px;margin:12px auto 0;font-size:12px;color:#6b7280;text-align:center">${foot}</p></div>`;
const WELCOME = (name: string) => wrap(`<p>Hi ${esc(name)}, welcome to WorldLink! 🎉</p><p>Here is what each part of the app does:</p>
<p><b>⌂ Home</b>: watch videos from people around the world. Swipe up for the next one.</p>
<p><b>☺ Friends</b>: find people, follow them, and see who follows you.</p>
<p><b>＋ Create</b>: record or upload your own video, add a caption and post it.</p>
<p><b>✉ Inbox</b>: your messages, statuses that disappear after 24 hours, and your activity.</p>
<p><b>◉ Profile</b>: your videos, followers, wallet, privacy settings and Boost, which pushes your video to more people.</p>
<p><b>🎁 Gifts and 🪙 coins</b>: send gifts to creators you love. Creators can cash out their gifts.</p>
<p>Tip: turn on alerts so you never miss a message or gift.</p>
<p><a href="https://worldlink.app" style="display:inline-block;background:#FF7A1A;color:#fff;text-decoration:none;padding:12px 22px;border-radius:999px;font-weight:700">Open WorldLink</a></p>`, "You are getting this because you created a WorldLink account.");

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  try {
    const url = new URL(req.url);
    if (req.method === "GET") {
      const u = url.searchParams.get("u") || "", t = url.searchParams.get("t") || "";
      const page = (m: string) => new Response(`<!doctype html><meta name=viewport content="width=device-width,initial-scale=1"><body style="font-family:Arial;padding:40px;text-align:center"><h2>${m}</h2><p><a href="https://worldlink.app">Back to WorldLink</a></p>`, { headers: { "Content-Type": "text/html; charset=utf-8" } });
      if (!u || t !== (await sign(u))) return page("This link is not valid.");
      const tok = await helperToken(), m = await getMail(tok, u);
      if (m) await putMail(tok, u, { ...m, unsub: true });
      return page("You have been unsubscribed from WorldLink updates.");
    }
    const { payload } = await jwtVerify(req.headers.get("x-wl-token") || "", JWKS, { issuer: "https://securetoken.google.com/" + PROJ, audience: PROJ });
    const uid = String(payload.sub), email = String((payload as any).email || "");
    const b = await req.json();
    const tok = await helperToken();
    if (b.a === "hello") {
      if (!email) return json({ ok: false });
      const old = await getMail(tok, uid);
      const name = String(b.name || (payload as any).name || email.split("@")[0]).slice(0, 40);
      await putMail(tok, uid, { email, name, unsub: old?.unsub || false });
      if (!old) { try { await sendBatch([{ from: FROM, to: [email], subject: "Welcome to WorldLink 🌍", html: WELCOME(name) }]) } catch (e) { console.error(String(e)) } }
      return json({ ok: true, welcome: !old });
    }
    if (b.a === "test" || b.a === "broadcast") {
      if (!(await isMod(tok, uid))) return json({ ok: false, why: "moderators only" }, 403);
      const subject = String(b.subject || "").trim().slice(0, 150), text = String(b.text || "").trim().slice(0, 5000);
      if (!subject || !text) return json({ ok: false, why: "write a subject and a message" }, 400);
      const body = esc(text).split(/\n{2,}/).map((p) => `<p>${p.replace(/\n/g, "<br>")}</p>`).join("");
      const mk = async (to: string, id: string) => ({
        from: FROM, to: [to], subject,
        html: wrap(body + `<p><a href="https://worldlink.app" style="display:inline-block;background:#FF7A1A;color:#fff;text-decoration:none;padding:12px 22px;border-radius:999px;font-weight:700">Open WorldLink</a></p>`,
          `You get this because you have a WorldLink account. <a href="${Deno.env.get("SUPABASE_URL")}/functions/v1/send-mail?u=${encodeURIComponent(id)}&t=${await sign(id)}">Unsubscribe</a>`),
      });
      if (b.a === "test") { await sendBatch([await mk(email, uid)]); return json({ ok: true, sent: 1 }); }
      // everyone who saved an email and has not unsubscribed
      const all: { id: string; email: string }[] = [];
      let pt = "";
      for (let i = 0; i < 20; i++) {
        const r = await fetch(`${DOC}/mails?pageSize=300${pt ? "&pageToken=" + encodeURIComponent(pt) : ""}`, { headers: { Authorization: "Bearer " + tok } });
        if (!r.ok) throw new Error("list mails " + r.status);
        const j = await r.json();
        for (const d of j.documents || []) { const m = dec(d.fields); if (m.email && !m.unsub) all.push({ id: String(d.name).split("/").pop()!, email: m.email }); }
        if (!j.nextPageToken) break; pt = j.nextPageToken;
      }
      const cap = Math.min(all.length, 2500);
      let sent = 0;
      for (let i = 0; i < cap; i += 100) {
        const chunk = await Promise.all(all.slice(i, Math.min(i + 100, cap)).map((x) => mk(x.email, x.id)));
        try { await sendBatch(chunk); sent += chunk.length; } catch (e) { console.error(String(e)); return json({ ok: false, sent, total: all.length, why: "stopped: " + String(e).slice(0, 120) }); }
      }
      return json({ ok: true, sent, total: all.length });
    }
    return json({ ok: false }, 400);
  } catch (e) {
    console.error("send-mail error:", String(e));
    return json({ ok: false, why: "error" }, 500);
  }
});
