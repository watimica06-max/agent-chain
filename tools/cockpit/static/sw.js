// 1.15 — the cockpit's service worker, registered only when the page is
// reached through the phone's address: it makes the page installable on the
// home screen, and shows the Web Push notifications the server sends. It
// caches nothing — the cockpit is live — and has no fetch handler: every
// request, the event stream and the uploads included, goes as before.
"use strict";

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));

// {kind, title, body, app, work, screen, tag} — server.py's push_message.
self.addEventListener("push", (e) => {
  let m = {};
  try { m = e.data ? e.data.json() : {}; } catch (err) { m = {body: e.data ? e.data.text() : ""}; }
  e.waitUntil(self.registration.showNotification(m.title || "Cockpit", {
    body: m.body || "", tag: m.tag || undefined, icon: "/icons/icon-192.png", badge: "/icons/icon-192.png",
    data: {app: m.app || "", work: m.work || "", screen: m.screen || "dashboard"},
  }));
});

// A tap opens the cockpit on the right screen: the page already open is
// brought forward and told; otherwise a new one opens with it in its address.
self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  const open = e.notification.data || {};
  e.waitUntil((async () => {
    const wins = await self.clients.matchAll({type: "window", includeUncontrolled: true});
    const w = wins.find((c) => new URL(c.url).origin === self.location.origin);
    if (w) {
      await w.focus();
      w.postMessage({type: "cockpit-push", open});
      return;
    }
    await self.clients.openWindow("/#push=" + encodeURIComponent(JSON.stringify(open)));
  })());
});
