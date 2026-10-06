"""1.8 — « Déploiement » through the server: the frame the page reads, the
profile saved and committed from Paramètres, the refusals while a chain run
goes in the same application — both ways —, and the destinations showing
only what their adapter declares. No chain command runs; adb is a fake."""
import asyncio
import json
import sys

import pytest

import server
from deployworld import hyrox_targets, use_fake_adb, write_profile
from test_chain import commit, git, init
from test_runner import script_until_interrupted
from test_server import open_pair, post, with_client

PY = f'"{sys.executable}"'


@pytest.fixture(autouse=True)
def _no_push(monkeypatch):
    monkeypatch.setattr(server, "PROFILE_PUSH", False)


@pytest.fixture
def fa(tmp_path, monkeypatch):
    f = use_fake_adb(tmp_path / "adb", monkeypatch)
    yield f
    f.close()


async def get(c, path):
    r = await c.get(path)
    return r.status, await r.json()


def test_the_frame_without_a_profile(tmp_path, fa):
    async def body(c, app_root, feat, rn):
        await open_pair(c, app_root)
        st, d = await get(c, "/api/deploy")
        assert st == 200 and d["profile"]["exists"] is False and d["job"] is None and d["run"] is None
        assert [a["type"] for a in d["describe"]["adapters"]] == ["android", "commande"]
        assert [f["key"] for f in d["describe"]["frame"]] == ["name", "type", "build"]
        st, r = await get(c, "/api/deploy/destinations")
        assert [g["type"] for g in r["groups"]] == ["android", "commande"]
        r = await post(c, "/api/deploy/start", {"choice": {"Téléphone": ["android:R5CT10AB1234"]}})
        assert r.status == 409 and "Paramètres → Déploiement" in (await r.json())["error"]
    with_client(tmp_path, body)


def test_only_what_the_adapter_declares(tmp_path, fa):
    async def body(c, app_root, feat, rn):
        write_profile(app_root, hyrox_targets(fa) + [
            {"name": "Site", "type": "commande", "run": f"{PY} -m http.server 0", "keeps_running": True}])
        await open_pair(c, app_root)
        _, r = await get(c, "/api/deploy/destinations")
        g = {x["type"]: x for x in r["groups"]}
        (here,) = g["commande"]["destinations"]
        # No screenshot, no mirror on « cet ordinateur »: not declared.
        assert {a["id"] for a in here["actions"]} == {"journal"}
        phone = g["android"]["destinations"][0]
        assert {"screenshot", "mirror"} <= {a["id"] for a in phone["actions"]}
        r = await c.get("/api/deploy/image?type=commande&action=screenshot&dest=commande:local")
        assert r.status == 409
        r = await c.get("/api/deploy/image?type=android&action=screenshot&dest=android:R5CT10AB1234")
        assert r.status == 200 and r.content_type == "image/png" and (await r.read()).startswith(b"\x89PNG")
    with_client(tmp_path, body)


def test_the_profile_saved_from_parametres(tmp_path, fa):
    async def body(c, app_root, feat, rn):
        init(app_root)
        commit(app_root, "first")
        await open_pair(c, app_root)
        targets = hyrox_targets(fa)
        r = await post(c, "/api/deploy/profile", {"targets": targets})
        res = await r.json()
        assert r.status == 200 and res["commit"] and res["profile"]["targets"] == targets
        assert git(app_root, "log", "-1", "--format=%s").strip() == "deploy: profil"
        r = await post(c, "/api/deploy/profile", {"targets": [{"name": "X", "type": "android"}]})
        res = await r.json()
        # `kind` absent takes its default, `any`; `install` has none.
        assert r.status == 400 and res["errors"]["targets"]["0"] == {"install": "obligatoire"}
        # The choice is remembered per application.
        r = await post(c, "/api/deploy/choice", {"choice": {"Montre": ["android:RFAX20WATCH9"]}})
        assert (await r.json())["choice"] == {"Montre": ["android:RFAX20WATCH9"]}
        _, d = await get(c, "/api/deploy")
        assert d["choice"] == {"Montre": ["android:RFAX20WATCH9"]}
    with_client(tmp_path, body)


def test_refused_while_a_chain_run_goes_in_the_same_application(tmp_path, fa):
    async def body(c, app_root, feat, rn):
        write_profile(app_root, hyrox_targets(fa))
        await open_pair(c, app_root)
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 200
        _, d = await get(c, "/api/deploy")
        assert d["run"]["prompt"] == "/1_lexique f"
        r = await post(c, "/api/deploy/start", {"choice": {"Téléphone": ["android:R5CT10AB1234"]}})
        res = await r.json()
        assert r.status == 409 and "/1_lexique f" in res["error"] and "course avec son merge" in res["error"]
        r = await post(c, "/api/deploy/profile", {"targets": hyrox_targets(fa)})
        assert r.status == 409 and "/1_lexique f" in (await r.json())["error"]
        await rn.stop_now(str(app_root))
        await rn.wait_ended(str(app_root), 5)
        # Once it ended, the deploy goes.
        r = await post(c, "/api/deploy/start", {"choice": {"Téléphone": ["android:R5CT10AB1234"]}})
        assert r.status == 200, await r.text()
        for _ in range(100):
            _, j = await get(c, "/api/deploy/job")
            if not j["job"]["going"]:
                break
            await asyncio.sleep(0.1)
        assert j["job"]["status"] == "fait"
    with_client(tmp_path, body, script=script_until_interrupted)


def test_a_chain_run_waits_for_a_deploy_building_here(tmp_path, fa):
    async def body(c, app_root, feat, rn):
        t = hyrox_targets(fa)[:1]
        t[0]["build"] = f'{PY} -c "import time; time.sleep(3)"'
        write_profile(app_root, t)
        await open_pair(c, app_root)
        r = await post(c, "/api/deploy/start", {"choice": {"Téléphone": ["android:R5CT10AB1234"]}})
        assert r.status == 200
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 409 and "déploiement construit" in (await r.json())["error"]
        r = await post(c, "/api/deploy/start", {"choice": {"Téléphone": ["android:R5CT10AB1234"]}})
        assert r.status == 409 and "un seul à la fois" in (await r.json())["error"]
        for _ in range(100):
            _, j = await get(c, "/api/deploy/job")
            if not j["job"]["going"]:
                break
            await asyncio.sleep(0.1)
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 200
        await rn.stop_now(str(app_root))
    with_client(tmp_path, body, script=script_until_interrupted)


def test_the_journal_and_its_save(tmp_path, fa):
    async def body(c, app_root, feat, rn):
        write_profile(app_root, hyrox_targets(fa))
        await open_pair(c, app_root)
        st, j = await get(c, "/api/deploy/journal?type=android&dest=android:R5CT10AB1234")
        assert st == 200 and j["live"] and j["target"] == "Téléphone"
        st, j = await get(c, "/api/deploy/journal?type=android&dest=android:R3CN70UNAUTH")
        assert st == 409 and "n'est pas connecté" in j["error"]
        r = await post(c, "/api/deploy/journal/save", {"dest": "android:R5CT10AB1234"})
        path = (await r.json())["path"]
        assert r.status == 200 and "journal-SM-S928B-" in path
        assert open(path, encoding="utf-8").read().startswith("— com.mgilli.hyroxtracker tourne")
        server_app = c.server.app
        server_app[server.DEPLOY_KEY].stop_all()
    with_client(tmp_path, body)
