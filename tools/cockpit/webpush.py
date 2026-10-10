"""1.15 — Web Push, by hand: the VAPID key pair (RFC 8292), the payload
encrypted for one subscription (RFC 8291, `aes128gcm` of RFC 8188), the
request a push service takes. `cryptography` alone; the HTTP is aiohttp's.

A subscription is what the phone's browser gives `PushManager.subscribe()`:
{"endpoint": url, "keys": {"p256dh": b64url, "auth": b64url}}."""
import base64
import hashlib
import hmac
import json
import os
import time
from urllib.parse import urlsplit

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

RECORD_SIZE = 4096
TTL = 24 * 3600
JWT_LIFE = 12 * 3600


def b64u(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def unb64u(text: str) -> bytes:
    text = (text or "").strip()
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _public_bytes(key) -> bytes:
    return key.public_key().public_bytes(serialization.Encoding.X962,
                                         serialization.PublicFormat.UncompressedPoint)


def new_vapid() -> dict:
    """The server's key pair, made once: the private scalar and the public
    point — the latter is the page's `applicationServerKey`."""
    key = ec.generate_private_key(ec.SECP256R1())
    d = key.private_numbers().private_value.to_bytes(32, "big")
    return {"private": b64u(d), "public": b64u(_public_bytes(key))}


def _private(vapid: dict):
    return ec.derive_private_key(int.from_bytes(unb64u(vapid["private"]), "big"), ec.SECP256R1())


def check_subscription(sub) -> dict:
    """The subscription as the server keeps it, or ValueError."""
    if not isinstance(sub, dict):
        raise ValueError("abonnement illisible")
    endpoint = sub.get("endpoint")
    keys = sub.get("keys") if isinstance(sub.get("keys"), dict) else {}
    if not isinstance(endpoint, str) or urlsplit(endpoint).scheme not in ("https", "http") \
            or not urlsplit(endpoint).hostname:
        raise ValueError("abonnement sans adresse de service de notification")
    try:
        p256dh, auth = unb64u(keys.get("p256dh", "")), unb64u(keys.get("auth", ""))
        ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), p256dh)
    except (ValueError, TypeError):
        raise ValueError("abonnement aux clés illisibles")
    if len(auth) != 16:
        raise ValueError("abonnement aux clés illisibles")
    return {"endpoint": endpoint, "keys": {"p256dh": keys["p256dh"], "auth": keys["auth"]}}


def _hkdf(salt: bytes, ikm: bytes, info: bytes, length: int) -> bytes:
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    return hmac.new(prk, info + b"\x01", hashlib.sha256).digest()[:length]


def encrypt(payload: bytes, p256dh: str, auth: str, salt: bytes | None = None, sender=None) -> bytes:
    """RFC 8291 §3.4: one record, its header carrying the salt and the
    sender's ephemeral public key."""
    ua_public = unb64u(p256dh)
    ua_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), ua_public)
    sender = sender or ec.generate_private_key(ec.SECP256R1())
    as_public = _public_bytes(sender)
    secret = sender.exchange(ec.ECDH(), ua_key)
    ikm = _hkdf(unb64u(auth), secret, b"WebPush: info\x00" + ua_public + as_public, 32)
    salt = salt or os.urandom(16)
    cek = _hkdf(salt, ikm, b"Content-Encoding: aes128gcm\x00", 16)
    nonce = _hkdf(salt, ikm, b"Content-Encoding: nonce\x00", 12)
    body = AESGCM(cek).encrypt(nonce, payload + b"\x02", None)
    return salt + RECORD_SIZE.to_bytes(4, "big") + bytes([len(as_public)]) + as_public + body


def decrypt(body: bytes, ua_private, auth: str) -> bytes:
    """What the phone's browser does — for the tests' fake push service."""
    salt, idlen = body[:16], body[20]
    as_public = body[21:21 + idlen]
    ua_public = _public_bytes(ua_private)
    secret = ua_private.exchange(ec.ECDH(), ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), as_public))
    ikm = _hkdf(unb64u(auth), secret, b"WebPush: info\x00" + ua_public + as_public, 32)
    cek = _hkdf(salt, ikm, b"Content-Encoding: aes128gcm\x00", 16)
    nonce = _hkdf(salt, ikm, b"Content-Encoding: nonce\x00", 12)
    plain = AESGCM(cek).decrypt(nonce, body[21 + idlen:], None)
    return plain.rstrip(b"\x00")[:-1]


def vapid_jwt(endpoint: str, vapid: dict, subject: str, now=None) -> str:
    u = urlsplit(endpoint)
    head = b64u(json.dumps({"typ": "JWT", "alg": "ES256"}, separators=(",", ":")).encode())
    claims = b64u(json.dumps({"aud": f"{u.scheme}://{u.netloc}", "exp": int((now or time.time()) + JWT_LIFE),
                              "sub": subject}, separators=(",", ":")).encode())
    signing = f"{head}.{claims}".encode("ascii")
    r, s = decode_dss_signature(_private(vapid).sign(signing, ec.ECDSA(hashes.SHA256())))
    return f"{head}.{claims}.{b64u(r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))}"


def request_for(sub: dict, message: dict, vapid: dict, subject: str):
    """(url, headers, body) of one push."""
    body = encrypt(json.dumps(message, ensure_ascii=False).encode("utf-8"), sub["keys"]["p256dh"], sub["keys"]["auth"])
    headers = {"Authorization": f"vapid t={vapid_jwt(sub['endpoint'], vapid, subject)}, k={vapid['public']}",
               "Content-Encoding": "aes128gcm", "Content-Type": "application/octet-stream",
               "TTL": str(TTL), "Urgency": "high"}
    return sub["endpoint"], headers, body


async def send(session, sub: dict, message: dict, vapid: dict, subject: str) -> int:
    """The push service's status: 201 taken; 404 or 410, the subscription is gone."""
    url, headers, body = request_for(sub, message, vapid, subject)
    async with session.post(url, data=body, headers=headers) as r:
        await r.read()
        return r.status
