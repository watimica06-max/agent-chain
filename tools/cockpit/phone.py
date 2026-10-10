"""1.15 — the cockpit reached from the Product Owner's phone, through
Tailscale: `tailscale serve` presents it in HTTPS at the computer's
Tailscale name and forwards to the cockpit on 127.0.0.1. The server still
listens on 127.0.0.1 alone.

What a request is:
- « local » — this computer's browser: Host 127.0.0.1 or localhost, and no
  forwarding header. As before 1.15.
- « phone » — Paramètres → « Accès depuis le téléphone » on, and its Host
  is that address (Tailscale's proxy keeps the Host it was given, and adds
  X-Forwarded-Host, -Proto, -For and Tailscale-User-*). It needs the access
  code once, then a cookie.
- anything else — refused, as before.

config.json, `phone`:
- `enabled`, `address` (`https://<computer>.<tailnet>.ts.net`);
- `code`, the access code hashed (PBKDF2-SHA256, its salt and rounds);
- `tokens`, the SHA-256 of each cookie given — « Déconnecter le téléphone »
  empties it, and every cookie is worthless;
- `vapid`, the Web Push key pair, made once;
- `subscriptions`, the phones' push subscriptions.
Five wrong codes in a row lock the code for fifteen minutes — in memory."""
import hashlib
import hmac
import os
import secrets
import time
from datetime import datetime
from urllib.parse import urlsplit

import webpush

LOCAL_NAMES = {"127.0.0.1", "localhost"}
# What a proxy adds: a request carrying one never comes from this computer's browser.
FORWARD_HEADERS = ("X-Forwarded-For", "X-Forwarded-Host", "X-Forwarded-Proto", "Forwarded",
                   "Tailscale-User-Login")
COOKIE = "cockpit_telephone"
COOKIE_AGE = 400 * 24 * 3600          # the longest a browser keeps one
MAX_TOKENS = 20
MIN_CODE = 6
ROUNDS = 200_000
MAX_FAILS = 5
LOCK_SECONDS = 15 * 60
MAX_SUBSCRIPTIONS = 10
# What the lock's fifteen minutes are counted with; the tests put a fake here.
CLOCK = time.time


def host_name(hostport):
    try:
        return urlsplit("//" + (hostport or "")).hostname
    except ValueError:
        return None


def _host_port(hostport, default):
    try:
        u = urlsplit("//" + (hostport or ""))
        return (u.hostname or "").lower(), u.port or default
    except ValueError:
        return None, None


def normalize_address(text) -> str:
    """`https://<name>[:port]` from what she typed — the scheme may be left
    out; a path, a query or another scheme is refused."""
    t = (text or "").strip().rstrip("/")
    if not t:
        raise ValueError("adresse vide")
    if "://" not in t:
        t = "https://" + t
    try:
        u = urlsplit(t)
        port = u.port
    except ValueError:
        raise ValueError("adresse illisible")
    if u.scheme != "https":
        raise ValueError("l'adresse commence par https:// — celle que donne « tailscale serve status »")
    if not u.hostname or u.path not in ("", "/") or u.query or u.fragment or u.username:
        raise ValueError("une adresse seule, sans chemin : https://<ordinateur>.<tailnet>.ts.net")
    if u.hostname in LOCAL_NAMES:
        raise ValueError("l'adresse Tailscale de l'ordinateur, pas la sienne en local")
    return f"https://{u.hostname.lower()}" + (f":{port}" if port and port != 443 else "")


def hash_code(code: str, salt: bytes | None = None, rounds: int = ROUNDS) -> dict:
    salt = salt or os.urandom(16)
    return {"salt": salt.hex(), "rounds": rounds,
            "hash": hashlib.pbkdf2_hmac("sha256", code.encode("utf-8"), salt, rounds).hex()}


def code_matches(code: str, stored) -> bool:
    if not isinstance(stored, dict) or not isinstance(code, str):
        return False
    try:
        got = hash_code(code, bytes.fromhex(stored["salt"]), int(stored["rounds"]))["hash"]
    except (KeyError, ValueError, TypeError):
        return False
    return hmac.compare_digest(got, stored.get("hash", ""))


def _digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class Phone:
    def __init__(self, state, clock=None):
        self.state = state
        self.clock = clock or (lambda: CLOCK())
        self.fails = 0
        self.locked_until = 0.0
        self.last_lock = None      # when the last lock began, for the desktop

    # ------------------------------------------------------------ settings
    @property
    def conf(self):
        return self.state.phone()

    @property
    def enabled(self):
        c = self.conf
        return bool(c.get("enabled")) and bool(c.get("address"))

    @property
    def address(self):
        return self.conf.get("address") or ""

    def public(self):
        """What the page is told — never the code nor a token."""
        c = self.conf
        locked = self.locked()
        return {"enabled": bool(c.get("enabled")), "address": c.get("address") or "",
                "has_code": isinstance(c.get("code"), dict), "phones": len(c.get("tokens") or []),
                "subscriptions": len(c.get("subscriptions") or []),
                "locked": locked, "locked_until": self._iso(self.locked_until) if locked else None,
                "fails": self.fails, "last_lock": self.last_lock,
                "vapid_public": (c.get("vapid") or {}).get("public")}

    def _iso(self, t):
        return datetime.fromtimestamp(t).isoformat(timespec="seconds")

    def configure(self, enabled, address, code=None):
        """Paramètres → « Accès depuis le téléphone ». On needs an address
        and a code — the one stored, or the one given."""
        addr = normalize_address(address) if (address or "").strip() else ""
        if code is not None and code != "":
            if not isinstance(code, str) or len(code) < MIN_CODE:
                raise ValueError(f"le code d'accès a au moins {MIN_CODE} caractères")
        c = self.conf
        if enabled and not addr:
            raise ValueError("l'adresse du cockpit sur le téléphone manque")
        if enabled and not code and not isinstance(c.get("code"), dict):
            raise ValueError("choisissez d'abord un code d'accès")

        def change(p):
            p["enabled"] = bool(enabled)
            p["address"] = addr
            if code:
                p["code"] = hash_code(code)
            if not isinstance(p.get("vapid"), dict):
                p["vapid"] = webpush.new_vapid()
        self.state.update_phone(change)
        if code:
            self.fails, self.locked_until = 0, 0.0
        return self.public()

    def vapid(self):
        """The Web Push key pair — made the first time it is asked for."""
        v = self.conf.get("vapid")
        if isinstance(v, dict) and v.get("private") and v.get("public"):
            return v

        def change(p):
            if not isinstance(p.get("vapid"), dict):
                p["vapid"] = webpush.new_vapid()
            return p["vapid"]
        return self.state.update_phone(change)

    # ------------------------------------------------------------ requests
    def where(self, headers, host) -> str | None:
        """« local », « phone », or None — refused."""
        forwarded = any(h in headers for h in FORWARD_HEADERS)
        if host_name(host) in LOCAL_NAMES and not forwarded:
            return "local"
        if not self.enabled:
            return None
        want = _host_port(urlsplit(self.address).netloc, 443)
        if _host_port(host, 443) != want:
            return None
        fh = headers.get("X-Forwarded-Host")
        if fh and _host_port(fh.split(",")[0].strip(), 443) != want:
            return None
        return "phone"

    def origin_ok(self, origin, where) -> bool:
        if where == "local":
            return host_name(origin.split("://", 1)[-1]) in LOCAL_NAMES
        return origin.rstrip("/").lower() == self.address

    def signed_in(self, token) -> bool:
        if not token or not self.enabled:
            return False
        d = _digest(token)
        return any(hmac.compare_digest(d, t.get("hash", "")) for t in (self.conf.get("tokens") or [])
                   if isinstance(t, dict))

    # ------------------------------------------------------------- the code
    def locked(self) -> bool:
        if self.locked_until and self.clock() >= self.locked_until:
            self.locked_until = 0.0
        return bool(self.locked_until)

    def try_code(self, code):
        """(token or None, what happened): « ok », « faux », « verrouillé »
        — the fifth wrong code in a row —, « bloqué » while the fifteen
        minutes run, whatever the code."""
        if self.locked():
            return None, "bloqué"
        if not code_matches(code, self.conf.get("code")):
            self.fails += 1
            if self.fails >= MAX_FAILS:
                self.fails = 0
                self.locked_until = self.clock() + LOCK_SECONDS
                self.last_lock = self._iso(self.clock())
                return None, "verrouillé"
            return None, "faux"
        self.fails = 0
        token = secrets.token_urlsafe(32)

        def change(p):
            toks = [t for t in (p.get("tokens") or []) if isinstance(t, dict)]
            toks.append({"hash": _digest(token), "at": self._iso(self.clock())})
            p["tokens"] = toks[-MAX_TOKENS:]
        self.state.update_phone(change)
        return token, "ok"

    def disconnect(self):
        """« Déconnecter le téléphone »: every cookie given is worthless, and
        no push goes to a phone any more."""
        def change(p):
            n = len(p.get("tokens") or [])
            p["tokens"] = []
            p["subscriptions"] = []
            return n
        return self.state.update_phone(change)

    # ------------------------------------------------------- subscriptions
    def subscriptions(self):
        return [s for s in (self.conf.get("subscriptions") or []) if isinstance(s, dict) and s.get("endpoint")]

    def subscribe(self, sub):
        clean = webpush.check_subscription(sub)

        def change(p):
            subs = [s for s in (p.get("subscriptions") or []) if isinstance(s, dict)
                    and s.get("endpoint") != clean["endpoint"]]
            subs.append({**clean, "at": self._iso(self.clock())})
            p["subscriptions"] = subs[-MAX_SUBSCRIPTIONS:]
        self.state.update_phone(change)
        return clean

    def unsubscribe(self, endpoint):
        def change(p):
            subs = p.get("subscriptions") or []
            kept = [s for s in subs if not (isinstance(s, dict) and s.get("endpoint") == endpoint)]
            p["subscriptions"] = kept
            return len(subs) - len(kept)
        return self.state.update_phone(change)

    def subscribed(self, endpoint) -> bool:
        return any(s["endpoint"] == endpoint for s in self.subscriptions())
