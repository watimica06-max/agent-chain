"""1.18 — the automatic mode through the server: the real decision over a
fixture folder, each command a fake run whose relay names the next one; the
programme's runs in « auto », recorded with it; its summary in the stats; the
pushes — at its start and its stop, none at each run's end —; « Arrêter après
la commande en cours » on /8_code, stop.md written by the cockpit where the
command reads it and disarmed after; « Arrêter maintenant »; the stops on
« État de l'ordinateur » and the usage; saved programmes; a programme kept
across a restart. No chain command runs."""
import asyncio
import json
import os
import time
from datetime import datetime, timedelta

from aiohttp.test_utils import TestClient, TestServer
from claude_agent_sdk import AssistantMessage, TextBlock

import autopilot as ap
import nextline
import runner as runner_mod
import server
import stats as stats_mod
import webpush
from state import State
from test_runner import FakeClient, result, script_until_interrupted
from test_server import build_app_folder, post
from test_usage import add_both

CHAIN = {"/1_lexique f": "Next: run /2_structure f", "/2_structure f": "Next: run /3_decoupe f",
         "/3_decoupe f": "Next: answer questions, then run /3_decoupe f"}


def chain_script(relays, stop_file=None):
    """Each command's relay names the next; /8_code ends when stop.md is
    at the feature's root — where it reads it (cmd/8_code.md, step 6)."""
    async def script(c):
        prompt = c.prompts[-1]
        yield AssistantMessage(content=[TextBlock(f"{prompt} tourne.")], model="m")
        if prompt.startswith("/8_code") and stop_file:
            for _ in range(500):
                if os.path.exists(stop_file):
                    break
                await asyncio.sleep(0.01)
            yield result("Arrêt demandé par stop.md après le lot.\nNext: run /8_code f")
            return
        yield result(f"Fait.\n{relays.get(prompt, 'Next: done')}")
    return script


def served(tmp_path, body, script, first="Next: run /1_lexique f", mode="manuel", monkeypatch=None, before=None):
    app_root = tmp_path / "app"
    build_app_folder(app_root)
    for name in ("3_decoupe", "3a_genre", "9_controle", "7_lots"):
        (app_root / ".claude" / "commands" / f"{name}.md").write_text(
            f'---\ndescription: run {name}\nargument-hint: "<f>"\n---\nbody\n', encoding="utf-8")
    st = State(str(tmp_path / "config.json"))
    st.add_app(str(app_root))
    st.open_pair(str(app_root), "f")
    st.set_mode(mode)
    st.set_relay(str(app_root), "f", "/0 f", f"Fait.\n{first}", nextline.parse(first).to_dict(), "terminé")
    # One phone subscribed: what is pushed is kept, never sent.
    st.update_phone(lambda p: p.update(subscriptions=[{"endpoint": "https://push.example/tel", "keys": {
        "p256dh": "x", "auth": "y"}}]))
    pushed = []

    async def send(session, sub, message, vapid, subject):
        pushed.append(message)
        return 201
    monkeypatch.setattr(webpush, "send", send)
    if before:
        before(st)
    store = stats_mod.Store(str(tmp_path / "stats.sqlite"))
    made = []

    def factory(cwd, can_use_tool, **kw):
        c = FakeClient(script, can_use_tool)
        c.kw = kw
        made.append(c)
        return c
    rn = runner_mod.Runner(client_factory=factory, on_end=server.make_on_end(st), mode_getter=lambda: st.mode,
                           log_dir=str(tmp_path / "logs"), stats=store)
    app = server.make_app(st, rn, picker=lambda initial: str(app_root))

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            c.ctx = {"state": st, "store": store, "made": made, "app": app_root, "rn": rn, "pushed": pushed}
            return await body(c)
    return asyncio.run(go())


async def pilot(c):
    return (await (await c.get("/api/pilot")).json())


async def until(cond, timeout=10.0):
    end = time.monotonic() + timeout
    while True:
        got = await cond()
        if got:
            return got
        assert time.monotonic() < end, "condition jamais remplie"
        await asyncio.sleep(0.02)


async def ended(c):
    return await until(lambda: _ended(c))


async def _ended(c):
    p = (await pilot(c))["pilot"]
    return p if p and p["status"] == ap.FINI else None


async def pushes_settled(c, n):
    await until(lambda: _count(c, n))


async def _count(c, n):
    return len(c.ctx["pushed"]) >= n


def test_a_programme_chains_the_real_decision_until_she_is_needed(tmp_path, monkeypatch):
    async def body(c):
        r = await post(c, "/api/pilot/start", {"preset": "besoin"})
        assert r.status == 200, await r.text()
        assert (await r.json())["created"]["name"] == "Maintenant, jusqu'à ce qu'on ait besoin de moi"
        p = await ended(c)
        assert p["reason_kind"] == ap.NEED and p["reason"].startswith("Des réponses vous attendent")
        made = c.ctx["made"]
        assert [m.prompts[0] for m in made] == ["/1_lexique f", "/2_structure f", "/3_decoupe f"]
        # « auto », whatever Paramètres says (« manuel » here).
        assert {m.kw["mode"] for m in made} == {"auto"}
        # The summary, kept in the stats; each run tied to the programme.
        store = c.ctx["store"]
        progs = store.programmes()
        assert len(progs) == 1 and progs[0]["id"] == p["id"] and progs[0]["commands"] == 3
        assert progs[0]["prompts"] == ["/1_lexique f", "/2_structure f", "/3_decoupe f"]
        import sqlite3
        with sqlite3.connect(store.path) as db:
            assert {r[0] for r in db.execute("SELECT programme FROM runs")} == {p["id"]}
            assert {r[0] for r in db.execute("SELECT permission_mode FROM runs")} == {"auto"}
        # The pushes: its start and its stop with the reason — no push at each run's end.
        await pushes_settled(c, 2)
        await asyncio.sleep(0.2)
        kinds = [(m["kind"], m["title"]) for m in c.ctx["pushed"]]
        assert kinds == [("pilote", "app — pilote automatique lancé"), ("pilote", "app — pilote automatique arrêté")]
        assert "Des réponses vous attendent" in c.ctx["pushed"][-1]["body"] and "3 commandes" in c.ctx["pushed"][-1]["body"]
        # Nothing kept as active any more; the state says the last summary.
        assert c.ctx["state"].pilot_active is None
        s = await (await c.get("/api/state")).json()
        assert s["pilot_last"]["id"] == p["id"] and s["pilot"]["status"] == ap.FINI
        # And the Statistiques screen lists it.
        st = await (await c.get("/api/stats?app=&feature=f")).json()
        assert [x["id"] for x in st["programmes"]] == [p["id"]]
    served(tmp_path, body, chain_script(CHAIN), monkeypatch=monkeypatch)


def test_stop_after_the_lot_writes_stop_md_where_8_code_reads_it_and_removes_it(tmp_path, monkeypatch):
    stop_file = str(tmp_path / "app" / "docs" / "features" / "f" / "stop.md")

    async def body(c):
        await post(c, "/api/pilot/start", {"preset": "besoin"})
        await until(lambda: _running(c, "8_code"))
        r = await post(c, "/api/pilot/stop", {"how": "apres"})
        assert (await r.json())["pilot"]["stop_after"]
        p = await ended(c)
        assert p["reason"] == "Arrêté après la commande en cours, à votre demande." and p["lots"] == 1
        assert [m.prompts[0] for m in c.ctx["made"]] == ["/8_code f"]
        # Read by the command, then disarmed by the cockpit: she never handles it.
        await until(lambda: _gone(stop_file))
        assert os.path.exists(os.path.join(os.path.dirname(stop_file), "stop1.md"))
    served(tmp_path, body, chain_script({}, stop_file), first="Next: run /8_code f 3", monkeypatch=monkeypatch)


async def _running(c, cmd):
    p = (await pilot(c))["pilot"]
    return p and p["status"] == ap.LANCE and (p.get("run") or {}).get("command") == cmd


async def _gone(path):
    return not os.path.exists(path)


def test_stop_now_interrupts_the_command(tmp_path, monkeypatch):
    async def body(c):
        await post(c, "/api/pilot/start", {"preset": "besoin"})
        await until(lambda: _running(c, "1_lexique"))
        await post(c, "/api/pilot/stop", {"how": "maintenant"})
        p = await ended(c)
        assert p["reason"] == "Arrêté maintenant, à votre demande." and len(c.ctx["made"]) == 1
        assert c.ctx["made"][0].interrupted.is_set()
    served(tmp_path, body, script_until_interrupted, monkeypatch=monkeypatch)


def test_a_block_of_the_computer_stops_it(tmp_path, monkeypatch, fake_machine):
    fake_machine.logged_in = False

    async def body(c):
        await post(c, "/api/pilot/start", {"preset": "besoin"})
        p = await ended(c)
        assert p["reason_kind"] == ap.MACHINE and p["reason"].startswith("État de l'ordinateur :")
        assert c.ctx["made"] == []
    served(tmp_path, body, chain_script(CHAIN), monkeypatch=monkeypatch)


def test_the_blocking_threshold_stops_it(tmp_path, monkeypatch):
    async def body(c):
        add_both(c.ctx["store"], 0.95, 0.20)
        await post(c, "/api/pilot/start", {"preset": "deux-heures"})
        p = await ended(c)
        assert p["reason_kind"] == ap.USAGE and "jamais outre" in p["reason"] and c.ctx["made"] == []
    served(tmp_path, body, chain_script(CHAIN), monkeypatch=monkeypatch)


def test_a_diverged_application_stops_it(tmp_path, monkeypatch):
    import sync as sync_mod
    monkeypatch.setattr(sync_mod, "before_launch", lambda book, folder: {
        "ok": False, "error": "Divergé : 1 commit ici, 2 sur GitHub — rien ne se lance avant « Réconcilier »",
        "notice": "", "files": [], "reconcile": True, "sync": None, "done": []})

    async def body(c):
        await post(c, "/api/pilot/start", {"preset": "besoin"})
        p = await ended(c)
        assert p["reason_kind"] == ap.GITHUB and "Réconcilier" in p["reason"] and c.ctx["made"] == []
    served(tmp_path, body, chain_script(CHAIN), monkeypatch=monkeypatch)


def test_saved_programmes_and_a_later_start(tmp_path, monkeypatch):
    async def body(c):
        later = (datetime.now() + timedelta(hours=3)).strftime("%H:%M")
        spec = {"name": "Ma nuit", "start": {"mode": "at", "at": later}, "bounds": {"lots": 4, "until": "07:00"}}
        r = await post(c, "/api/pilot/save", {"spec": spec})
        saved = (await r.json())["pilot_saved"]
        assert [x["name"] for x in saved] == ["Ma nuit"]
        assert saved[0]["text"].startswith(f"Démarre à {later}, s'arrête à 07:00 ou après 4 lots encore")
        r = await post(c, "/api/pilot/start", {"saved": "Ma nuit"})
        out = (await r.json())["created"]
        assert out["status"] == ap.PROGRAMME and out["notice"] == "L'ordinateur doit rester allumé et réveillé jusque-là."
        # Kept, so that a cockpit restart finds it; the update waits for it.
        assert c.ctx["state"].pilot_active["id"] == out["id"]
        r = await post(c, "/api/cockpit/update", {})
        assert r.status == 409 and "pilote automatique" in (await r.json())["error"]
        # Another programme is refused while it waits.
        r = await post(c, "/api/pilot/start", {"preset": "besoin"})
        assert r.status == 409 and "déjà actif" in (await r.json())["error"]
        r = await post(c, "/api/pilot/stop", {"how": "apres"})
        p = await ended(c)
        assert p["reason"] == "Annulé avant son démarrage, à votre demande." and c.ctx["made"] == []
        assert c.ctx["state"].pilot_active is None
        r = await post(c, "/api/pilot/forget", {"name": "Ma nuit"})
        assert (await r.json())["pilot_saved"] == []
        r = await post(c, "/api/pilot/start", {"spec": {"bounds": {"lots": 0}}})
        assert r.status == 400 and "nombre de lots" in (await r.json())["error"]
    served(tmp_path, body, chain_script(CHAIN), monkeypatch=monkeypatch)


def test_a_programme_kept_across_a_restart(tmp_path, monkeypatch):
    start = (datetime.now() + timedelta(hours=2)).replace(microsecond=0)

    def keep(st):
        st.set_pilot_active({"id": "prog-gardé", "name": "Gardé", "spec": ap.clean_spec({"start": {"mode": "at", "at": start.strftime("%H:%M")}}),
                             "app": str(tmp_path / "app"), "app_name": "app", "feature": "f", "created_at": "2026-10-10T18:00:00",
                             "start_at": start.isoformat(), "end_at": None, "later": True, "started_at": None,
                             "status": ap.PROGRAMME, "doing": "", "waiting": None, "run": None, "commands": 0, "lots": 0,
                             "prompts": [], "stop_after": False, "stop_now": False, "reason": None, "reason_kind": None,
                             "ended_at": None})

    async def body(c):
        p = (await pilot(c))["pilot"]
        assert p["id"] == "prog-gardé" and p["status"] == ap.PROGRAMME and p["notice"]
        await post(c, "/api/pilot/stop", {"how": "apres"})
        await ended(c)
    served(tmp_path, body, chain_script(CHAIN), monkeypatch=monkeypatch, before=keep)


def test_one_that_was_running_is_summed_up_as_interrupted(tmp_path, monkeypatch):
    def keep(st):
        st.set_pilot_active({"id": "prog-coupé", "name": "", "spec": ap.clean_spec({}), "app": str(tmp_path / "app"),
                             "app_name": "app", "feature": "f", "created_at": "2026-10-10T18:00:00",
                             "start_at": "2026-10-10T18:00:00", "end_at": None, "later": False,
                             "started_at": "2026-10-10T18:00:00", "status": ap.LANCE, "doing": "", "waiting": None,
                             "run": None, "commands": 2, "lots": 0, "prompts": ["/1_lexique f", "/2_structure f"],
                             "stop_after": False, "stop_now": False, "reason": None, "reason_kind": None, "ended_at": None})

    async def body(c):
        p = (await pilot(c))["pilot"]
        assert p["status"] == ap.FINI and p["reason"] == "Le cockpit s'est arrêté pendant le programme."
        assert c.ctx["store"].programmes()[0]["commands"] == 2 and c.ctx["state"].pilot_active is None
        assert c.ctx["made"] == []
    served(tmp_path, body, chain_script(CHAIN), monkeypatch=monkeypatch, before=keep)
