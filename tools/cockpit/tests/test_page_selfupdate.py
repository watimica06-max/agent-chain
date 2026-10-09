"""1.14 — « Mettre à jour le cockpit » and « Récupérer » on the page, in a
headless browser (Microsoft Edge through Playwright): the notice at the top
of the home screen with its commits, its button and Paramètres' own; the
update refused during a run, said; « Récupérer » on a home row and on the
dashboard. Then the whole restart, for real: two cockpit servers started
from a scratch copy of agent-chain — the old one exits, the new one takes its
port, and the page reloads on its own. Skipped when Playwright or Edge is
missing. GitHub is a bare repository in a temporary folder; no chain command
runs.

With COCKPIT_SHOTS=<folder>, each step's screenshot is written there."""
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request

import pytest

pytest.importorskip("playwright")

import selfupdate  # noqa: E402
import server  # noqa: E402
import startup  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from selfupdateworld import chain_world, fakes, is_alive  # noqa: E402,F401
from syncworld import app_world, bare, change, clone_of, head  # noqa: E402
from test_chain import commit, git, init  # noqa: E402
from test_page import browser, page  # noqa: E402,F401
from test_runner import script_until_interrupted  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def shot(page, name, full=False):
    d = os.environ.get("COCKPIT_SHOTS")
    if d:
        os.makedirs(d, exist_ok=True)
        page.screenshot(path=os.path.join(d, f"{name}.png"), full_page=full)


def page_errors(page):
    return [e for e in page.js_errors if "status of 409" not in e and "Failed to fetch" not in e and "net::ERR" not in e]


@pytest.fixture
def behind(tmp_path, monkeypatch):
    """agent-chain behind GitHub by two commits; fetched when the home
    screen opens."""
    remote, here, other = chain_world(tmp_path)
    change(other, "tools/cockpit/x.py", "cockpit 2\n", "cockpit : se mettre à jour en un clic", push=True)
    change(other, ".claude/agents/a.md", "agent a, two\n", "chaîne : l'agent a relit son relais", push=True)
    monkeypatch.setattr(server, "CHAIN_ROOT", str(here))
    monkeypatch.setattr(server, "SYNC_CHAIN_ON_HOME", True)
    monkeypatch.setattr(server, "CHAIN_HOME_EVERY", 0.0)
    return here, other


def test_notice_button_and_settings(tmp_path, page, behind, fakes):
    here, _ = behind
    with FakeServer(tmp_path / "srv", script=script_until_interrupted) as s:
        page.goto(s.url)
        page.wait_for_selector("#cockpit-update:not(.hidden) li")
        box = page.locator("#cockpit-update")
        assert box.locator("h3").inner_text() == "Nouvelle version du cockpit disponible"
        assert box.locator("li").count() == 2
        assert box.locator("li").nth(0).inner_text().endswith("chaîne : l'agent a relit son relais")
        assert "GitHub a 2 commits du cockpit et de la chaîne" in box.inner_text()
        assert box.get_by_role("button", name="Mettre à jour le cockpit").is_visible()
        # The notice comes first on the home screen.
        top = page.evaluate("document.querySelector('#scr-accueil > :not(.hidden)').id")
        assert top == "cockpit-update"
        shot(page, "1-accueil-nouvelle-version")
        # Paramètres says the same, with its own button.
        page.locator(".home-card").first.click()
        page.wait_for_function("S.open")
        page.locator("#nav-settings").click()
        page.wait_for_selector("#sec-cockpit #cockpit-set-subjects li")
        sec = page.locator("#sec-cockpit")
        assert f"version {server.VERSION}" in sec.inner_text() and "Nouvelle version du cockpit disponible — 2 commits" in sec.inner_text()
        assert sec.locator("#btn-cockpit-update").is_visible()
        sec.scroll_into_view_if_needed()
        shot(page, "2-parametres-version")
        # Refused while a run goes, said.
        r = page.request.post(s.url + "api/run", data=json.dumps({"command": "1_lexique", "args": "f"}),
                              headers={"Content-Type": "application/json"})
        assert r.ok, r.text()
        page.locator("#btn-cockpit-update").click()
        page.wait_for_selector("#cockpit-set-msg .notice.err")
        msg = page.locator("#cockpit-set-msg").inner_text()
        assert "Pas maintenant." in msg and "une commande tourne" in msg and "après sa fin" in msg
        shot(page, "3-parametres-refus-pendant-un-run")
        assert head(here) != head(behind[1]) and fakes.spawned == []
        page.request.post(s.url + "api/stop-now", data="{}", headers={"Content-Type": "application/json"})
        assert s.call(s.rn.wait_ended(str(s.app_root), 10))
        assert not page_errors(page), page.js_errors


def test_the_start_notice_carries_the_button(tmp_path, page, behind, fakes, monkeypatch):
    """1.12's pull at start stays: its notice now carries the button, and the
    home screen says the version is pulled, not yet in service."""
    here, other = behind
    monkeypatch.setattr(server, "SYNC_CHAIN_AT_START", True)
    with FakeServer(tmp_path / "srv") as s:
        page.goto(s.url)
        page.wait_for_selector("#sync-banner:not(.hidden) .cockpit-update-btn")
        banner = page.locator("#sync-banner").inner_text()
        assert server.CHAIN_RESTART in banner and "null" not in banner
        page.wait_for_selector("#cockpit-update:not(.hidden) li")
        assert page.locator("#cockpit-update h3").inner_text() == "Nouvelle version du cockpit récupérée — pas encore en service"
        assert head(here) == head(other)
        shot(page, "0-demarrage-version-recuperee")
        page.locator("#sync-banner .cockpit-update-btn").click()
        page.wait_for_selector("#stopped.restart:not(.hidden)", timeout=30000)
        assert len(fakes.spawned) == 1 and fakes.pip_calls() == []
        assert not page_errors(page), page.js_errors


def test_refused_on_an_overlapping_file_says_which(tmp_path, page, behind, fakes):
    here, _ = behind
    (here / "tools" / "cockpit" / "x.py").write_text("mon essai\n", encoding="utf-8")
    with FakeServer(tmp_path / "srv") as s:
        page.goto(s.url)
        page.wait_for_selector("#cockpit-update:not(.hidden) li")
        page.locator("#btn-cockpit-update-home").click()
        page.wait_for_selector("#cockpit-update-msg .notice.err")
        msg = page.locator("#cockpit-update-msg").inner_text()
        assert "Mise à jour arrêtée." in msg and "tools/cockpit/x.py" in msg
        assert page.locator("#btn-cockpit-update-home").is_enabled()
        shot(page, "4-accueil-refus-fichier-non-commite")
        assert fakes.spawned == []
        assert not page_errors(page), page.js_errors


def test_recuperer_on_the_home_row_and_the_dashboard(tmp_path, page):
    _, a, b = app_world(tmp_path, "hyrox")
    change(b, "README.md", "B\n", "README depuis l'autre ordinateur", push=True)
    _, c, d = app_world(tmp_path, "carnet")
    change(d, "README.md", "D\n", push=True)
    with FakeServer(tmp_path / "srv", opened=False) as s:
        for name, f in (("Hyrox", a), ("Carnet", c)):
            s.state.add_app(str(f))
            s.state.rename_app(str(f), name)
            s.state.open_pair(str(f), "f")
        page.goto(s.url)
        row = page.locator('.home-card[data-name="Hyrox"]')
        row.locator("button.sync-pull").wait_for()
        assert "En retard : GitHub a 1 commit" in row.inner_text()
        shot(page, "5-accueil-recuperer-avant")
        row.locator("button.sync-pull").click()
        page.wait_for_selector("#sync-banner.ok")
        banner = page.locator("#sync-banner").inner_text()
        assert "Hyrox — 1 commit récupéré de GitHub. À jour avec GitHub." in banner and "null" not in banner
        page.wait_for_function("document.querySelector('.home-card[data-name=\"Hyrox\"] .hc-sync .cst').textContent === 'à jour'")
        assert row.locator("button.sync-pull").count() == 0
        shot(page, "6-accueil-recuperer-apres")
        assert head(a) == head(b)
        # The dashboard: the same button in its alert.
        page.locator('.home-card[data-name="Carnet"]').click()
        page.wait_for_selector("#alerts .sync-alert button.sync-pull")
        shot(page, "7-tableau-de-bord-recuperer")
        page.locator("#alerts .sync-alert button.sync-pull").click()
        page.wait_for_selector("#sync-banner.ok")
        page.wait_for_function("!document.querySelector('#alerts .sync-alert button.sync-pull')")
        assert head(c) == head(d)
        assert not page_errors(page), page.js_errors


# ------------------------------------------------------------ the whole restart, for real

IGNORE = shutil.ignore_patterns("tests", "logs", "__pycache__", "*.pyc", "stats.sqlite*", "config.json", "screens")


def scratch_agent_chain(tmp_path):
    """This cockpit's code, as it is on disk, in a scratch agent-chain on a
    bare GitHub: `here` runs it, `other` moves it on."""
    remote = bare(tmp_path / "github" / "agent-chain.git")
    seed = tmp_path / "seed"
    init(seed)
    shutil.copytree(HERE, seed / "tools" / "cockpit", ignore=IGNORE)
    commit(seed, "cockpit")
    git(seed, "remote", "add", "origin", str(remote))
    git(seed, "push", "-q", "-u", "origin", "master")
    return clone_of(remote, tmp_path / "A" / "agent-chain"), clone_of(remote, tmp_path / "B" / "agent-chain")


def get(url, timeout=3):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def end_server(pid, port):
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/shutdown", data=b'{"confirm": true}',
                                     headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=5).read()
    except OSError:
        pass
    for _ in range(50):
        if not is_alive(pid):
            return
        time.sleep(0.2)
    subprocess.run(["taskkill", "/F", "/PID", str(pid)] if os.name == "nt" else ["kill", "-9", str(pid)],
                   capture_output=True)


def test_the_page_reloads_after_a_real_restart(tmp_path, page):
    here, other = scratch_agent_chain(tmp_path)
    port = selfupdate.free_port()
    data = tmp_path / "donnees"
    data.mkdir()
    args = ["--port", str(port), "--config", str(data / "config.json"), "--stats", str(data / "stats.sqlite"),
            "--journaux", str(data / "logs")]
    old = subprocess.Popen([sys.executable, str(here / "tools" / "cockpit" / "server.py"), *args],
                           cwd=str(here / "tools" / "cockpit"), stdin=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    new_pid = None
    try:
        for _ in range(150):
            if startup.ping(port, timeout=0.5):
                break
            time.sleep(0.2)
        first = startup.ping(port)
        assert first and first["pid"] == old.pid and first["version"] == server.VERSION
        url = f"http://127.0.0.1:{port}/"
        # Its fetch at start done, the other computer pushes a new cockpit.
        for _ in range(100):
            cs = get(url + "api/state")["chain_sync"]
            if not cs["checking"] and cs["sync"]:
                break
            time.sleep(0.2)
        assert cs["sync"]["state"] == "à jour"
        p = other / "tools" / "cockpit" / "server.py"
        p.write_text(p.read_text(encoding="utf-8").replace(f'VERSION = "{server.VERSION}"', 'VERSION = "1.14-relève"', 1),
                     encoding="utf-8")
        sha = commit(other, "cockpit : la relève")
        git(other, "push", "-q")

        page.goto(url)
        page.wait_for_selector("#cockpit-update:not(.hidden) li", timeout=30000)
        assert page.locator("#cockpit-update li").inner_text().endswith("cockpit : la relève")
        shot(page, "8-relance-avant")
        page.evaluate("window.__old_page = true")
        page.locator("#btn-cockpit-update-home").click()
        page.wait_for_selector("#stopped.restart:not(.hidden)", timeout=90000)
        assert page.locator("#stopped-title").inner_text() == "Redémarrage du cockpit…"
        shot(page, "9-relance-en-cours")
        # The old server exits; the page reloads on its own, on the new one.
        assert old.wait(30) == 0
        page.wait_for_function("!window.__old_page && document.readyState === 'complete' && typeof S === 'object'",
                               timeout=60000)
        ping = startup.ping(port)
        new_pid = ping["pid"]
        assert ping["version"] == "1.14-relève" and new_pid != old.pid
        assert head(here) == sha
        page.wait_for_selector("#scr-accueil:not(.hidden)")
        assert page.locator("#stopped").is_hidden()
        page.wait_for_function("S.chain_sync && S.chain_sync.cockpit && S.chain_sync.cockpit.state === 'à jour'",
                               timeout=30000)
        assert page.locator("#cockpit-update").is_hidden()
        shot(page, "10-relance-apres")
        # The trial port is closed; the new server's log says how it took over.
        with open(data / "logs" / "server.log", encoding="utf-8") as f:
            log = f.read()
        assert "le nouveau serveur répond" in log and "Relève faite" in log
    finally:
        if old.poll() is None:
            old.kill()
        if new_pid:
            end_server(new_pid, port)
        else:
            got = startup.ping(port)
            if got and got["pid"] != old.pid:
                end_server(got["pid"], port)
