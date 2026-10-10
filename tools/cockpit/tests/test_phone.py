"""1.15 — the cockpit reached from the phone through Tailscale, end to end on
the real routes. Every phone request is what `tailscale serve` forwards: the
Host it was given (the computer's Tailscale name), X-Forwarded-Host, -Proto,
-For and Tailscale-User-Login. The push service is a fake that decrypts what
it receives with the subscription's own key. No chain command runs."""
import asyncio
import base64
import json
import os
import shutil

from aiohttp import DummyCookieJar, web
from aiohttp.test_utils import TestClient, TestServer
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature

import phone as phone_mod
import runner as runner_mod
import server
import webpush
from donneesworld import data_world, png
from state import State
from test_runner import result, script_until_interrupted, script_with_permission
from test_server import build_app_folder

HOST = "cockpit-pc.tail1234.ts.net"
ADDR = "https://" + HOST
CODE = "4815162342"


def ph_headers(cookie=None, origin=ADDR, host=HOST, **extra):
    h = {"Host": host, "X-Forwarded-Host": host, "X-Forwarded-Proto": "https",
         "X-Forwarded-For": "100.101.102.103", "Tailscale-User-Login": "po@example.com"}
    if origin:
        h["Origin"] = origin
    if cookie:
        h["Cookie"] = f"{phone_mod.COOKIE}={cookie}"
    h.update(extra)
    return h


def world(tmp_path, scripts=None, data=False):
    """The cockpit on a fake application; `scripts`, the runs' scripts in turn."""
    app_root = tmp_path / "app"
    feat = build_app_folder(app_root)
    if data:
        data_world(app_root, question=False)
    state = State(str(tmp_path / "config.json"))
    state.open_pair(str(app_root), "f")
    queue = list(scripts or [])

    def factory(cwd, can_use_tool, **kw):
        from test_runner import FakeClient
        return FakeClient(queue.pop(0) if queue else script_until_interrupted, can_use_tool)

    rn = runner_mod.Runner(client_factory=factory, on_end=server.make_on_end(state), mode_getter=lambda: state.mode)
    app = server.make_app(state, rn, picker=lambda initial: str(app_root))
    return app, state, rn, app_root, feat


def serve(tmp_path, body, **kw):
    app, state, rn, app_root, feat = world(tmp_path, **kw)

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1"), cookie_jar=DummyCookieJar()) as c:
            return await body(c, state=state, rn=rn, app_root=app_root, feat=feat)
    return asyncio.run(go())


async def post(c, path, data, headers=None):
    return await c.post(path, data=json.dumps(data), headers={"Content-Type": "application/json", **(headers or {})})


async def turn_on(c, code=CODE, address=HOST):
    r = await post(c, "/api/phone/settings", {"enabled": True, "address": address, "code": code})
    assert r.status == 200, await r.text()
    return await r.json()


async def login(c, code=CODE):
    r = await post(c, "/api/phone/login", {"code": code}, ph_headers())
    assert r.status == 200, await r.text()
    return r.cookies[phone_mod.COOKIE].value


# ------------------------------------------------------------ the gate

def test_the_tailnet_address_is_refused_while_the_setting_is_off(tmp_path):
    async def body(c, **_):
        for path in ("/", "/api/state", "/api/events", "/manifest.webmanifest"):
            r = await c.get(path, headers=ph_headers(origin=None))
            assert r.status == 403 and (await r.json())["error"] == "hôte refusé", path
        r = await post(c, "/api/phone/login", {"code": CODE}, ph_headers())
        assert r.status == 403
        # The setting on, then off again: refused again.
        await turn_on(c)
        assert (await c.get("/", headers=ph_headers(origin=None))).status == 200
        r = await post(c, "/api/phone/settings", {"enabled": False, "address": HOST})
        assert r.status == 200 and not (await r.json())["enabled"]
        assert (await c.get("/", headers=ph_headers(origin=None))).status == 403
    serve(tmp_path, body)


def test_a_proxied_request_under_a_local_host_is_never_local(tmp_path):
    """What a proxy forwards never passes for this computer's browser, even
    when it says Host: 127.0.0.1 — on or off."""
    async def body(c, **_):
        for _ in range(2):
            for extra in ({"X-Forwarded-For": "100.1.2.3"}, {"Tailscale-User-Login": "x@y"},
                          {"X-Forwarded-Host": HOST}, {"Forwarded": "for=100.1.2.3"}):
                r = await c.get("/api/state", headers=extra)
                assert r.status == 403, extra
            await turn_on(c)
        # Another tailnet name, or a forwarded host that is not hers: refused.
        assert (await c.get("/api/state", headers=ph_headers(host="autre.tail1234.ts.net", origin=None))).status == 403
        assert (await c.get("/api/state", headers=ph_headers(origin=None, **{"X-Forwarded-Host": "evil.example"}))).status == 403
    serve(tmp_path, body)


def test_the_code_once_then_the_cookie_and_local_never_asked(tmp_path):
    async def body(c, state, **_):
        out = await turn_on(c, address=f" https://{HOST.upper()}/ ")
        assert out["address"] == ADDR and out["enabled"] and out["has_code"]
        # The code is stored hashed — never as typed, never given back.
        raw = open(state.path, encoding="utf-8").read()
        assert CODE not in raw and "pbkdf2" not in raw and '"hash"' in raw
        assert "code" not in out and CODE not in json.dumps(await (await c.get("/api/phone")).json())
        # The phone, no cookie: the code page; everything else asks for it.
        r = await c.get("/", headers=ph_headers(origin=None))
        page = await r.text()
        assert r.status == 200 and 'id="code-form"' in page and "scr-dashboard" not in page
        for path in ("/api/state", "/api/forms", "/api/events", "/sw.js", "/api/donnees/file"):
            r = await c.get(path, headers=ph_headers(origin=None))
            assert r.status == 401 and (await r.json())["code"] is True, path
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"}, ph_headers())
        assert r.status == 401
        # The manifest and the icons, before the code: the code page shows them.
        assert (await c.get("/manifest.webmanifest", headers=ph_headers(origin=None))).status == 200
        assert (await c.get("/icons/icon-192.png", headers=ph_headers(origin=None))).status == 200
        # A wrong code, then the right one: a long-lived, secure, HttpOnly cookie.
        r = await post(c, "/api/phone/login", {"code": "000000"}, ph_headers())
        assert r.status == 403 and "encore 4 essais" in (await r.json())["error"]
        r = await post(c, "/api/phone/login", {"code": CODE}, ph_headers())
        assert r.status == 200
        sc = r.headers["Set-Cookie"]
        assert "Secure" in sc and "HttpOnly" in sc and "SameSite=Lax" in sc and f"Max-Age={400 * 86400}" in sc
        token = r.cookies[phone_mod.COOKIE].value
        assert token not in open(state.path, encoding="utf-8").read()
        r = await c.get("/", headers=ph_headers(cookie=token, origin=None))
        assert 'id="scr-dashboard"' in await r.text()
        for path in ("/api/state", "/api/forms", "/sw.js"):
            assert (await c.get(path, headers=ph_headers(cookie=token, origin=None))).status == 200, path
        assert (await (await c.get("/api/phone", headers=ph_headers(cookie=token, origin=None))).json())["here"] == "phone"
        # A cookie made up, or of no use here: asked again.
        assert (await c.get("/api/state", headers=ph_headers(cookie="x" * 43, origin=None))).status == 401
        # The phone's access is set on the computer only, cookie or not.
        for path in ("/api/phone/settings", "/api/phone/disconnect"):
            r = await post(c, path, {"enabled": False, "address": ""}, ph_headers(cookie=token))
            assert r.status == 403 and (await r.json())["error"] == "sur l'ordinateur", path
        # A page of another site, or of this computer, posting to the phone's address: refused.
        for origin in ("https://evil.example", "http://127.0.0.1:8765", ADDR.replace("https", "http")):
            r = await post(c, "/api/mode", {"mode": "manuel"}, ph_headers(cookie=token, origin=origin))
            assert r.status == 403 and (await r.json())["error"] == "origine refusée", origin
        assert (await post(c, "/api/mode", {"mode": "manuel"}, ph_headers(cookie=token))).status == 200
        # This computer's page: never asked, and the phone's origin is not its own.
        for path in ("/", "/api/state", "/api/forms", "/api/phone"):
            assert (await c.get(path)).status == 200, path
        assert 'id="scr-dashboard"' in await (await c.get("/")).text()
        r = await post(c, "/api/mode", {"mode": "auto"}, {"Origin": ADDR})
        assert r.status == 403
        assert (await post(c, "/api/phone/login", {"code": CODE})).status == 400
        # A new code: the new one opens, the old one no longer does.
        r = await post(c, "/api/phone/settings", {"enabled": True, "address": HOST, "code": "nouveau-code"})
        assert r.status == 200
        assert (await post(c, "/api/phone/login", {"code": CODE}, ph_headers())).status == 403
        await login(c, "nouveau-code")
    serve(tmp_path, body)


def test_the_settings_say_what_is_missing(tmp_path):
    async def body(c, **_):
        for data, said in (({"enabled": True, "address": HOST}, "code d'accès"),
                           ({"enabled": True, "address": "", "code": CODE}, "adresse"),
                           ({"enabled": True, "address": HOST, "code": "123"}, "au moins 6"),
                           ({"enabled": True, "address": "http://" + HOST, "code": CODE}, "https://"),
                           ({"enabled": True, "address": ADDR + "/cockpit", "code": CODE}, "sans chemin"),
                           ({"enabled": True, "address": "https://127.0.0.1", "code": CODE}, "Tailscale")):
            r = await post(c, "/api/phone/settings", data)
            assert r.status == 400 and said in (await r.json())["error"], data
        # Off with nothing: fine — it is the default.
        r = await post(c, "/api/phone/settings", {"enabled": False, "address": ""})
        assert r.status == 200
    serve(tmp_path, body)


def test_five_wrong_codes_lock_fifteen_minutes_and_the_computer_shows_it(tmp_path, monkeypatch):
    now = [1_800_000_000.0]
    monkeypatch.setattr(phone_mod, "CLOCK", lambda: now[0])

    async def body(c, **_):
        await turn_on(c)
        events = await c.get("/api/events")
        for left in (4, 3, 2, 1):
            r = await post(c, "/api/phone/login", {"code": "faux-faux"}, ph_headers())
            assert r.status == 403 and f"encore {left} essai" in (await r.json())["error"]
        r = await post(c, "/api/phone/login", {"code": "faux-faux"}, ph_headers())
        assert r.status == 429 and "trop de codes faux" in (await r.json())["error"]
        # Locked: even the right code.
        r = await post(c, "/api/phone/login", {"code": CODE}, ph_headers())
        assert r.status == 429
        # The computer's page is told, and its state says it.
        ev = await next_data(events, "phone")
        assert ev["data"]["locked"] and ev["data"]["locked_until"]
        st = await (await c.get("/api/state")).json()
        assert st["phone"]["locked"] and st["phone"]["last_lock"]
        events.close()
        # Fifteen minutes later: the right code opens.
        now[0] += 14 * 60
        assert (await post(c, "/api/phone/login", {"code": CODE}, ph_headers())).status == 429
        now[0] += 60 + 1
        await login(c)
        assert not (await (await c.get("/api/state")).json())["phone"]["locked"]
        # A right code resets the count: four wrong ones again do not lock.
        for _ in range(4):
            await post(c, "/api/phone/login", {"code": "faux-faux"}, ph_headers())
        await login(c)
        for _ in range(4):
            assert (await post(c, "/api/phone/login", {"code": "faux-faux"}, ph_headers())).status == 403
    serve(tmp_path, body)


def test_deconnecter_revokes_every_cookie(tmp_path):
    async def body(c, state, **_):
        await turn_on(c)
        a, b = await login(c), await login(c)
        for t in (a, b):
            assert (await c.get("/api/state", headers=ph_headers(cookie=t, origin=None))).status == 200
        assert (await (await c.get("/api/phone")).json())["phones"] == 2
        r = await post(c, "/api/phone/disconnect", {})
        assert r.status == 200 and (await r.json())["revoked"] == 2
        for t in (a, b):
            assert (await c.get("/api/state", headers=ph_headers(cookie=t, origin=None))).status == 401
            r = await c.get("/", headers=ph_headers(cookie=t, origin=None))
            assert 'id="code-form"' in await r.text()
        assert state.phone()["tokens"] == []
        # The code asked again, and it opens again.
        c2 = await login(c)
        assert (await c.get("/api/state", headers=ph_headers(cookie=c2, origin=None))).status == 200
        # The setting off: a cookie is no use either.
        await post(c, "/api/phone/settings", {"enabled": False, "address": HOST})
        assert (await c.get("/api/state", headers=ph_headers(cookie=c2, origin=None))).status == 403
    serve(tmp_path, body)


# --------------------------------------- the stream, uploads, downloads

async def next_data(resp, kind, timeout=5):
    async def read():
        while True:
            line = await resp.content.readline()
            if not line:
                raise AssertionError("flux fermé")
            if line.startswith(b"data: "):
                ev = json.loads(line[6:])
                if ev["type"] == kind:
                    return ev
    return await asyncio.wait_for(read(), timeout)


def test_the_event_stream_an_upload_and_a_download_through_the_phone(tmp_path):
    async def body(c, rn, app_root, **_):
        await turn_on(c)
        token = await login(c)
        h = ph_headers(cookie=token)
        events = await c.get("/api/events", headers=ph_headers(cookie=token, origin=None))
        assert events.status == 200 and events.headers["Content-Type"].startswith("text/event-stream")
        # A run's permission reaches the phone through the stream.
        run = await rn.start(str(app_root), "f", "f", "1_lexique", "f")
        perm = await next_data(events, "permission")
        r = await post(c, "/api/permission", {"id": perm["data"]["id"], "allow": True}, h)
        assert r.status == 200
        assert (await next_data(events, "run_ended"))["data"]["outcome"] == "terminé"
        await run.task
        events.close()
        # « Joindre un fichier » from the phone's camera: a photo of some weight.
        photo = os.urandom(3 * 1024 * 1024)
        r = await post(c, "/api/donnees/join", {"tab": "feature", "name": "photo-du-releve.jpg",
                                                "data": base64.b64encode(photo).decode()}, h)
        assert r.status == 200, await r.text()
        assert (app_root / "docs" / "features" / "f" / "donnees" / "photo-du-releve.jpg").read_bytes() == photo
        # And an image back: a download through the same address.
        img = png()
        await post(c, "/api/donnees/join", {"tab": "feature", "name": "fleche.png",
                                            "data": base64.b64encode(img).decode()}, h)
        r = await c.get("/api/donnees/file", params={"tab": "feature", "name": "fleche.png"},
                        headers=ph_headers(cookie=token, origin=None))
        assert r.status == 200 and await r.read() == img
        r = await c.get("/api/stats/csv", params={"which": "runs"}, headers=ph_headers(cookie=token, origin=None))
        assert r.status in (200, 404)        # served, or nothing to give — never refused
    serve(tmp_path, body, scripts=[script_with_permission], data=True)


# ------------------------------------------------------------- Web Push

class PushService:
    """A push service: every request kept, decrypted with the subscriber's
    own private key; the paths in `gone` answer 410."""
    def __init__(self):
        self.got = []
        self.gone = set()
        self.subs = {}

    def subscriber(self, name, base):
        key = ec.generate_private_key(ec.SECP256R1())
        auth = webpush.b64u(os.urandom(16))
        pub = webpush._public_bytes(key)
        self.subs[f"/push/{name}"] = (key, auth)
        return {"endpoint": f"{base}/push/{name}", "expirationTime": None,
                "keys": {"p256dh": webpush.b64u(pub), "auth": auth}}

    async def handle(self, request):
        body = await request.read()
        key, auth = self.subs[request.path]
        self.got.append({"path": request.path, "headers": dict(request.headers),
                         "message": json.loads(webpush.decrypt(body, key, auth))})
        return web.Response(status=410 if request.path in self.gone else 201)

    def to(self, name):
        return [g["message"] for g in self.got if g["path"] == f"/push/{name}"]


async def until(cond, timeout=5):
    for _ in range(int(timeout / 0.05)):
        if cond():
            return
        await asyncio.sleep(0.05)
    raise AssertionError("jamais arrivé")


def check_vapid(headers, vapid, endpoint_base):
    auth = headers["Authorization"]
    assert auth.startswith("vapid t=") and f", k={vapid['public']}" in auth
    jwt = auth[len("vapid t="):].split(",")[0]
    head, claims, sig = jwt.split(".")
    body = json.loads(webpush.unb64u(claims))
    assert body["aud"] == endpoint_base and body["sub"] == ADDR
    raw = webpush.unb64u(sig)
    pub = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), webpush.unb64u(vapid["public"]))
    pub.verify(encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big")),
               f"{head}.{claims}".encode(), ec.ECDSA(hashes.SHA256()))
    assert headers["Content-Encoding"] == "aes128gcm" and int(headers["TTL"]) > 0


def test_push_on_each_of_the_three_moments_and_a_dead_subscription_removed(tmp_path):
    feat_box = {}

    async def leaves_questions(c):
        await asyncio.sleep(0.2)
        shutil.copyfile(feat_box["feat"] / "questions-sondeur-02.md", feat_box["feat"] / "questions-sondeur-05.md")
        yield result("Deux questions pour vous.\nNext: answer questions, then run /4_grille f")

    async def fails(c):
        raise RuntimeError("le CLI s'est arrêté")
        yield  # pragma: no cover

    svc = PushService()

    async def body(c, state, rn, app_root, feat):
        feat_box["feat"] = feat
        fake = TestServer(web.Application())
        fake.app.router.add_post("/push/{name}", svc.handle)
        await fake.start_server()
        base = f"http://127.0.0.1:{fake.port}"
        try:
            await turn_on(c)
            token = await login(c)
            h = ph_headers(cookie=token)
            live, dead = svc.subscriber("telephone", base), svc.subscriber("ancien", base)
            svc.gone.add("/push/ancien")
            for sub in (live, dead):
                r = await post(c, "/api/push/subscribe", {"subscription": sub}, h)
                assert r.status == 200, await r.text()
            stored = state.phone()["subscriptions"]
            assert [s["endpoint"] for s in stored] == [live["endpoint"], dead["endpoint"]]
            assert (await (await post(c, "/api/push/status", {"endpoint": live["endpoint"]}, h)).json())["subscribed"]
            r = await post(c, "/api/push/subscribe", {"subscription": {"endpoint": "x"}}, h)
            assert r.status == 400

            # 1 — a permission waits.
            run = await rn.start(str(app_root), "f", "f", "1_lexique", "f")
            await until(lambda: svc.to("telephone"))
            (m,) = svc.to("telephone")
            assert m["kind"] == "autorisation" and m["title"] == "app — une autorisation attend"
            assert m["body"].startswith("Write — demandé par lexicographe") and m["screen"] == "run"
            assert m["app"] == str(app_root) and m["work"] == "f"
            check_vapid(svc.got[0]["headers"], state.phone()["vapid"], base)
            # The dead one was tried once, and is gone.
            await until(lambda: len(state.phone()["subscriptions"]) == 1)
            assert svc.to("ancien") and state.phone()["subscriptions"][0]["endpoint"] == live["endpoint"]
            # 2 — the run ends, done.
            rn.answer_permission(str(app_root), run.permissions and next(iter(run.permissions)) or "", True)
            await run.task
            await until(lambda: len(svc.to("telephone")) == 2)
            m = svc.to("telephone")[1]
            assert m["kind"] == "fin" and m["title"] == "app — /1_lexique f — terminé"
            assert m["body"].startswith("Ensuite : ") and m["screen"] == "run"
            # 3 — a run ends with new questions for her: « À répondre ».
            run = await rn.start(str(app_root), "f", "f", "4_grille", "f")
            await run.task
            await until(lambda: len(svc.to("telephone")) == 3)
            m = svc.to("telephone")[2]
            assert m["kind"] == "reponse" and m["screen"] == "answer"
            assert "réponses vous attendent" in m["title"] and "questions-sondeur-05.md" in m["body"]
            assert "/4_grille f — terminé" in m["body"]
            # Stopped, then failed: each said.
            run = await rn.start(str(app_root), "f", "f", "8_code", "f")
            await asyncio.sleep(0.1)
            await rn.stop_now(str(app_root))
            await run.task
            await until(lambda: len(svc.to("telephone")) == 4)
            assert svc.to("telephone")[3]["title"] == "app — /8_code f — interrompu"
            run = await rn.start(str(app_root), "f", "f", "2_structure", "f")
            await run.task
            await until(lambda: len(svc.to("telephone")) == 5)
            m = svc.to("telephone")[4]
            assert m["kind"] == "erreur" and "s'est arrêté sur une erreur" in m["title"] and "le CLI" in m["body"]
            assert len(svc.to("ancien")) == 1
            # « Essayer », from the phone.
            r = await post(c, "/api/push/test", {"endpoint": live["endpoint"]}, h)
            assert (await r.json())["sent"] == 1 and svc.to("telephone")[-1]["kind"] == "essai"
            # « Déconnecter le téléphone »: no push goes any more.
            await post(c, "/api/phone/disconnect", {})
            assert state.phone()["subscriptions"] == []
            n = len(svc.got)
            run = await rn.start(str(app_root), "f", "f", "1_lexique", "f")
            await asyncio.sleep(0.3)
            await rn.stop_now(str(app_root))
            await run.task
            await asyncio.sleep(0.3)
            assert len(svc.got) == n
        finally:
            await fake.close()
    serve(tmp_path, body, scripts=[script_with_permission, leaves_questions, script_until_interrupted, fails,
                                   script_with_permission])


def test_the_service_worker_is_served_and_shows_each_push(tmp_path):
    async def body(c, **_):
        r = await c.get("/sw.js")
        js = await r.text()
        assert r.status == 200 and r.headers["Content-Type"].startswith("text/javascript")
        assert 'addEventListener("push"' in js and "showNotification" in js and 'addEventListener("notificationclick"' in js
        assert "#push=" in js and "cockpit-push" in js
    serve(tmp_path, body)


def test_encryption_round_trip_and_the_rfc8291_example():
    # RFC 8291 §5: the example's keys and salt give its exact message.
    ua_private = ec.derive_private_key(int.from_bytes(webpush.unb64u("q1dXpw3UpT5VOmu_cf_v6ih07Aems3njxI-JWgLcM94"), "big"),
                                       ec.SECP256R1())
    as_private = ec.derive_private_key(int.from_bytes(webpush.unb64u("yfWPiYE-n46HLnH0KqZOF1fJJU3MYrct3AELtAQ-oRw"), "big"),
                                       ec.SECP256R1())
    auth = "BTBZMqHH6r4Tts7J_aSIgg"
    body = webpush.encrypt(b"When I grow up, I want to be a watermelon",
                           "BCVxsr7N_eNgVRqvHtD0zTZsEc6-VV-JvLexhqUzORcxaOzi6-AYWXvTBHm4bjyPjs7Vd8pZGH6SRpkNtoIAiw4",
                           auth, salt=webpush.unb64u("DGv6ra1nlYgDCS1FRnbzlw"), sender=as_private)
    assert webpush.b64u(body) == ("DGv6ra1nlYgDCS1FRnbzlwAAEABBBP4z9KsN6nGRTbVYI_c7VJSPQTBtkgcy27mlmlMoZIIgDll6e3vCYLocInmYWAmS6TlzAC8wEqKK6PBru3jl7A_yl95bQpu6cVPTpK4Mqgkf1CXztLVBSt2Ks3oZwbuwXPXLWyouBWLVWGNWQexSgSxsj_Qulcy4a-fN")
    assert webpush.decrypt(body, ua_private, auth) == b"When I grow up, I want to be a watermelon"
