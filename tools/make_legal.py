import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","assets","pwa")
UP="2 November 2026"
def page(title,body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · WorldLink</title><meta name="robots" content="index,follow">
<style>:root{{--bg:#fff;--fg:#17202e;--mu:#5b6678;--ac:#12307F;--or:#FF7A1A}}@media(prefers-color-scheme:dark){{:root{{--bg:#0e1420;--fg:#e8edf6;--mu:#9aa6ba;--ac:#8fb0ff}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,Segoe UI,Roboto,Arial,sans-serif}}main{{max-width:720px;margin:auto;padding:24px 16px 60px}}
h1{{font-size:28px;margin:.2em 0}}h2{{font-size:19px;margin:1.6em 0 .3em;color:var(--ac)}}p,li{{color:var(--fg)}}.mu{{color:var(--mu);font-size:14px}}a{{color:var(--ac)}}
.top a.b{{font-weight:800;text-decoration:none;color:var(--or);font-size:20px}}nav.f{{margin-top:40px;font-size:14px;display:flex;gap:16px;flex-wrap:wrap}}.btn{{display:inline-block;background:var(--or);color:#fff;text-decoration:none;padding:12px 22px;border-radius:999px;font-weight:700}}</style></head><body><main>
<div class="top"><a class="b" href="/">🌍 WorldLink</a></div><h1>{title}</h1><p class="mu">Last updated: {UP}</p>{body}
<nav class="f"><a href="/privacy.html">Privacy policy</a><a href="/terms.html">Terms of use</a><a href="/delete-account.html">Delete account</a><a href="mailto:hello@worldlink.app">hello@worldlink.app</a></nav></main></body></html>'''

privacy='''<p>WorldLink ("we", "us") is a social video app and website at worldlink.app, run from Nigeria. This policy explains what we collect, why, who helps us run the app, and the choices you have. Questions: <a href="mailto:hello@worldlink.app">hello@worldlink.app</a>.</p>
<h2>1. What we collect</h2><ul>
<li><b>Account details</b>: your email address (or phone number if you sign in by phone), your name and password. Passwords are handled by Google Firebase Authentication; we never see or store them.</li>
<li><b>Profile and content you post</b>: profile picture, bio, videos, photos, posts, stories, series, music, listings, events, comments, likes, follows and gifts.</li>
<li><b>Messages</b>: private chats and group chats, including voice messages, photos and videos you send.</li>
<li><b>Payments</b>: when you buy coins or boost a video, payment is taken by Paystack. We receive a confirmation and the amount, not your card number. Gifts and coin balances are kept in your account.</li>
<li><b>Device permissions you allow</b>: camera and microphone (to record videos, calls and voice messages), photos and files (to upload), location (only when you use "near me" features, and only at that moment), and notifications.</li>
<li><b>Technical data</b>: basic usage and error information such as device type, app version and approximate region, used to keep the service working and fight abuse.</li></ul>
<h2>2. How we use it</h2><ul><li>To run the app: show your content, deliver messages, calls, gifts and alerts.</li><li>To send you email about your account, and updates from WorldLink (you can unsubscribe in any update email).</li><li>To keep people safe: handle reports, block abuse and enforce our <a href="/terms.html">Terms</a>.</li><li>To process payments and prevent fraud.</li></ul>
<p>We do not sell your personal data and we do not show third-party advertising profiles built from it.</p>
<h2>3. Who can see what</h2><p>Videos, posts, series, profile and comments you publish are visible to other WorldLink users and, for videos, may be visible to anyone with the link. Private chats are visible only to the people in them. You can use Privacy settings in the app to control who finds and contacts you, and you can block or report any account.</p>
<h2>4. Service providers</h2><p>We use trusted providers to run WorldLink: Google Firebase (sign-in and database), Supabase (file storage and alerts), Cloudflare (website delivery and security), Resend (email), Paystack (payments), and web push services of your browser or phone maker (alerts). Music search may query Audius and Apple iTunes, and some videos play from YouTube; those services have their own policies. Data may be processed in countries outside Nigeria.</p>
<h2>5. How long we keep it</h2><p>We keep your data while your account is active. When you delete your account (see below), we remove your profile, content, messages, followers and saved email and alert settings. Payment records may be kept as long as the law requires. Backups and caches can take a short time to clear.</p>
<h2>6. Your rights and choices</h2><ul><li>See and edit your profile in the app.</li><li><b>Delete your account and data</b>: Profile → ☰ → Delete my account, or see <a href="/delete-account.html">worldlink.app/delete-account.html</a>.</li><li>Ask us for a copy of your data, correction or deletion at hello@worldlink.app. We reply within 30 days.</li><li>Turn off notifications in the app, your browser or your phone settings.</li><li>Withdraw permissions (camera, microphone, location) in your phone settings at any time.</li></ul>
<p>We handle personal data in line with the Nigeria Data Protection Act 2023. If you are not satisfied, you may complain to the Nigeria Data Protection Commission.</p>
<h2>7. Children</h2><p>WorldLink is for people aged 13 and over (or the minimum age in your country, if higher). We do not knowingly collect data from younger children. If you think a child has an account, email us and we will remove it.</p>
<h2>8. Security</h2><p>Data travels over encrypted connections and is protected by access rules in our database. No system is perfectly secure, so please use a strong password.</p>
<h2>9. Changes</h2><p>If we change this policy in a meaningful way we will tell you in the app or by email. The date at the top shows the latest version.</p>
<h2>10. Contact</h2><p>WorldLink, Nigeria · <a href="mailto:hello@worldlink.app">hello@worldlink.app</a></p>'''

terms='''<p>By creating an account or using WorldLink (app and worldlink.app) you agree to these terms. If you do not agree, please do not use it.</p>
<h2>1. Your account</h2><p>You must be 13 or older. Give true information, keep your password safe, and do not let others use your account. You are responsible for what happens under it.</p>
<h2>2. Your content</h2><p>You keep ownership of what you post. You give WorldLink a non-exclusive, worldwide licence to host, show, share and (for downloads) watermark it so the service can work. Only post content you made or have the right to use, including music and film clips.</p>
<h2>3. Rules</h2><p>Do not post or send: content that sexualises or endangers children; nudity or sexual content; violence, threats, hate or harassment; scams or fake giveaways; illegal goods; other people's private information; spam; malware; or content that infringes copyright. Do not impersonate others or try to break or overload the service. We may remove content and suspend or end accounts that break these rules.</p>
<h2>4. Reporting and blocking</h2><p>You can report any video, post, series, comment or account and block anyone from inside the app. Moderators review reports. To report a copyright problem or urgent abuse, email hello@worldlink.app.</p>
<h2>5. Coins, gifts, boosts and payments</h2><p>Coins are bought through Paystack and used for gifts and boosts. Coins and gifts have no cash value outside WorldLink, are not transferable except as gifts, and are non-refundable unless the law says otherwise. Creator cash-out is subject to the minimums and checks shown in the app, and we may withhold payouts linked to fraud or rule breaking.</p>
<h2>6. Series downloads</h2><p>Downloads from Series carry a WorldLink watermark. Personal viewing only: do not re-upload or sell other people's series.</p>
<h2>7. Service</h2><p>WorldLink is provided "as is". We try to keep it running but cannot promise it will always be available or error-free. To the extent the law allows, we are not liable for indirect losses or for what other users post.</p>
<h2>8. Ending your account</h2><p>You can delete your account at any time (Profile → ☰ → Delete my account). We may suspend or close accounts that break these terms.</p>
<h2>9. Changes and law</h2><p>We may update these terms and will tell you about important changes. These terms are governed by the laws of the Federal Republic of Nigeria.</p>
<h2>10. Contact</h2><p><a href="mailto:hello@worldlink.app">hello@worldlink.app</a></p>'''

delete='''<p>You can delete your WorldLink account and the data linked to it at any time.</p>
<h2>In the app or website</h2><ol><li>Open WorldLink and log in.</li><li>Go to <b>Profile</b>, tap <b>☰</b>, then <b>Delete my account</b>.</li><li>Type your password and tap <b>Delete everything</b>.</li></ol>
<p><a class="btn" href="/">Open WorldLink</a></p>
<h2>What is deleted</h2><p>Your sign-in, profile, videos, posts, stories, series and episodes, music and listings you added, messages, notifications, followers and following, saved email address and phone-alert settings. Deletion starts immediately. Cached copies can take a short time to disappear.</p>
<h2>What may be kept</h2><p>Payment and gift records that we must keep by law, and reports about rule-breaking, for as long as required. Coins you have not used and gifts cannot be refunded after deletion.</p>
<h2>Cannot log in?</h2><p>Email <a href="mailto:hello@worldlink.app">hello@worldlink.app</a> from the address you signed up with, with the subject "Delete my account". We will verify and delete your account within 30 days.</p>'''
for n,t,b in [("privacy.html","Privacy policy",privacy),("terms.html","Terms of use",terms),("delete-account.html","Delete your account",delete)]:
    open(os.path.join(D,n),"w",encoding="utf8").write(page(t,b))
print("ok")
