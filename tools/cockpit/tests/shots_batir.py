"""« Bâtir » — the screens the step changes, at 1280 × 800, before and after.

    python tests/shots_batir.py <out-dir> avant
    python tests/shots_batir.py <out-dir> apres

The same folders both times: a feature whose conventions are written and
not built yet; the same once built, with its report and its profile; the
dashboard of an application without conventions (« À fournir avant le
code »); a blocking file of the Bâtisseur's, a tutorial, beside a request
to the Architecte; the statistics of a /batir run. Not a test: run by hand,
like shots18.py. No chain command runs — the SDK client is a fake — and
every folder is a scratch one.
"""
import os
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from playwright.sync_api import sync_playwright  # noqa: E402

import diagnostic  # noqa: E402
import server  # noqa: E402
import stats  # noqa: E402
import batirworld as bw  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402

server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
diagnostic.FIND = lambda tool: None
# The commit that last changed the conventions: the server reads it with git;
# a scratch folder is no repository.
server.conventions_commit = lambda app: bw.COMMIT
UP = {"state": "à jour", "summary": "Chaîne à jour — f1b473d du 2026-10-06", "commit": "f1b473d", "date": "2026-10-06",
      "chain_commit": "f1b473d", "chain_date": "2026-10-06", "behind": None, "subjects": [], "modified": []}


def snap(page, out, name):
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / f"{name}.png"))
    print("shot", name)


def premiere(t, sub):
    s = FakeServer(t / sub)
    bw.upstream_done(s.app_root)
    s.state.open_pair(str(s.app_root), "premiere")
    return s


def batir_store(path):
    """One /batir run: the Bâtisseur, the Architecte on its request, the
    Bâtisseur again."""
    store = stats.Store(path)
    t = datetime.now() - timedelta(minutes=30)
    iso = lambda x: x.isoformat(timespec="seconds")  # noqa: E731
    db = sqlite3.connect(path)
    with db:
        db.execute("INSERT INTO runs (id, feature, work, command, permission_mode, session_id, started_at, ended_at,"
                   " duration_s, input_tokens, cache_read_tokens, cache_creation_tokens, output_tokens, next_line,"
                   " outcome, log_path) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   ("b1", "premiere", "premiere", "/batir premiere", "auto", "s-b1", iso(t), iso(t + timedelta(seconds=740)),
                    740, 40, 61000, 9000, 5200, "Next: run /7_lots premiere", "terminé", None))
        for k, (agent, model, off, dur, (i, cr, cc), out, tools) in enumerate([
                ("batisseur", "claude-sonnet-5-5", 20, 260, (12, 18000, 3000), None, 41),
                ("architecte", "claude-opus-5-5", 300, 140, (6, 9000, 1500), 1400, 9),
                ("batisseur", "claude-sonnet-5-5", 450, 280, (14, 21000, 2500), None, 37)]):
            st = t + timedelta(seconds=off)
            db.execute("INSERT INTO agent_passes (run_id, tool_use_id, agent, description, model, started_at,"
                       " ended_at, duration_s, input_tokens, cache_read_tokens, cache_creation_tokens,"
                       " output_tokens, tool_calls) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       ("b1", f"tb{k}", agent, "Build premiere" if agent == "batisseur" else "Requests premiere",
                        model, iso(st), iso(st + timedelta(seconds=dur)), dur, i, cr, cc, out, tools))
    db.close()
    return store


def flow(page, s, out, name, why=False):
    page.goto(s.url + "#chaine")
    page.wait_for_selector("#step-main-conventions")
    target = "#step-main-batir" if page.locator("#step-main-batir").count() else "#step-main-conventions"
    if why:
        page.locator(target).get_by_role("button", name="Pourquoi ?").click()
    page.evaluate(f"document.querySelector('{target}').scrollIntoView({{block: 'start'}}); window.scrollBy(0, -90)")
    snap(page, out, name)


def main(out_dir, phase):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    server.chain_state = lambda app: dict(UP)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            # 1. Conventions written, nothing built yet.
            with premiere(t, "a") as s:
                flow(page, s, out, f"{phase}-01-chaine-a-batir", why=True)
            # 2. Built: the report and the profile.
            with premiere(t, "b") as s:
                feat = s.app_root / "docs" / "features" / "premiere"
                bw.report(feat)
                bw.profile(s.app_root)
                flow(page, s, out, f"{phase}-02-chaine-batie", why=True)
            # 3. The dashboard of an application with no conventions yet.
            with FakeServer(t / "c") as s:
                page.goto(s.url + "#dashboard")
                page.wait_for_selector("#next-text")
                page.wait_for_timeout(400)
                if page.locator("#provide-card:not(.hidden)").count():
                    page.locator("#provide-card").scroll_into_view_if_needed()
                else:
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                snap(page, out, f"{phase}-03-tableau-de-bord")
            # 4. « À répondre »: the Bâtisseur's tutorial, a request beside it.
            with premiere(t, "d") as s:
                feat = s.app_root / "docs" / "features" / "premiere"
                bw.report(feat, status="blocked")
                bw.blocked(feat)
                bw.request(feat)
                page.goto(s.url + "#answer")
                page.wait_for_selector("#form .entry")
                page.locator("#form .entry").first.scroll_into_view_if_needed()
                snap(page, out, f"{phase}-04-a-repondre-tutoriel")
                page.evaluate("document.querySelector('#form .entry').scrollIntoView({block: 'end'}); window.scrollBy(0, 120)")
                snap(page, out, f"{phase}-05-a-repondre-fait")
            # 5. Statistiques: the passes of a /batir run.
            with FakeServer(t / "e", stats=batir_store(str(t / "stats.sqlite"))) as s:
                page.goto(s.url + "#stats")
                page.wait_for_selector("#st-tiles .tile")
                page.locator("#st-period button[data-p='tout']").click()
                page.locator("#st-feature").select_option("*")
                page.wait_for_function("document.querySelectorAll('#tbl-agent tbody tr td').length > 1")
                page.evaluate("document.querySelector('#tbl-agent').scrollIntoView({block: 'center'})")
                snap(page, out, f"{phase}-06-statistiques-par-agent")
        browser.close()
        if errors:
            print("erreurs de la page :", *errors, sep="\n  ")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
