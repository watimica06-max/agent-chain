"""1.21 — « Enquêtes », at 1280 × 800 and on a phone (390 × 844).

    python tests/shots121.py <out-dir>

A scratch application with a dated story (journalworld.py) and a scratch
agent-chain; the model a fake (enqueteworld.py) that tries a few writes —
refused — and reads, then answers. The screen, a new investigation, one
going, its report, the bug entry, the correction prompt « à relire »,
« Enquêter sur ce point » from the Journal and from a run in error, this
computer's nickname asked and in Paramètres, the phone reading. Not a test:
run by hand, like shots120.py. No chain command, no real Claude call.
"""
import asyncio
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from playwright.sync_api import sync_playwright  # noqa: E402

import copies  # noqa: E402
import diagnostic  # noqa: E402
import journalworld  # noqa: E402
import server  # noqa: E402
from claude_agent_sdk import ResultMessage  # noqa: E402
from enqueteworld import READS, WRITES, Factory, answering, saying  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from test_mode_diagnostic import ALL_GOOD, fake_exec  # noqa: E402

server.DIAG_RUNNER = lambda app: diagnostic.run_diagnostic(app, fake_exec(ALL_GOOD), env={})
diagnostic.FIND = lambda tool: None
server.MEASURE_USAGE = False
server.SYNC_CHAIN_AT_START = server.SYNC_APPS_AT_START = server.SYNC_CHAIN_ON_HOME = False
server.MACHINE_AT_START = server.AUTO_RESTART = False
server.JOURNAL = False
server.ASK_COMPUTER = True
server.chain_state = lambda app: {"state": "à jour", "summary": "Chaîne à jour — 4fab4b8 du 2026-10-10",
                                  "commit": "4fab4b8", "date": "2026-10-10", "chain_commit": "4fab4b8",
                                  "chain_date": "2026-10-10", "behind": None, "subjects": [], "modified": []}

APP_ANSWER = """**En bref** — Le chrono repart de zéro parce que la reprise recrée le minuteur au lieu de le relancer (`app/src/main/java/run/RunTimer.kt:88`).

**Ce que j'ai trouvé**
- Mettre en pause arrête le minuteur et garde le temps écoulé (`app/src/main/java/run/RunTimer.kt:61`).
- « Reprendre » crée un nouveau minuteur, qui part de zéro (`app/src/main/java/run/RunTimer.kt:88`) ; le temps gardé n'est relu nulle part (`git grep elapsedAtPause` : une seule ligne).
- Le document produit dit que la course reprend « là où elle s'était arrêtée » (`docs/features/f/desc-produit.md:42`).

**Ce que je n'ai pas pu établir** — Si cela arrive aussi après un appel téléphonique : aucun test ne le couvre.

**Ce que je conseille d'en faire** — **Une correction** : un comportement de l'application, à passer par la liste de bugs."""

CHAIN_ANSWER = """**En bref** — Le journal écrivait le nom de l'ordinateur sur le réseau ; depuis 1.21, il écrit son nom court (`tools/cockpit/journal.py:84`).

**Ce que j'ai trouvé**
- Une ligne du journal reçoit `computer=state.computer_label` (`tools/cockpit/server.py:1797`).
- Sans nom donné, « ordinateur » (`tools/cockpit/state.py:49`).

**Ce que je n'ai pas pu établir** — Rien.

**Ce que je conseille d'en faire** — **Rien** : c'est déjà corrigé."""

BUG = ("Observé : le chrono de la course repart de zéro après une pause.\nOù : sur l'écran de course\n"
       "Attendu : reprendre là où il en était quand la course reprend.")
PROMPT = """Cockpit 1.22 — the journal's computer column says the nickname everywhere it is shown.

## 1 — What to change, and why

The report (`docs/enquetes/2026-10-10-pourquoi-le-journal-ecrit-il-le-nom.md`) finds the journal line writes `state.computer_label` (`tools/cockpit/server.py:1797`) …

## Quote before changing

- `tools/cockpit/journal.py:80-84` — as it is.

## Tests

- A journal line written with no nickname says « ordinateur »; with one, the nickname.

Commit and push: `Cockpit 1.22 — le nom court partout`"""


def snap(page, out, name, full=False):
    page.wait_for_timeout(400)
    page.screenshot(path=str(out / f"{name}.png"), full_page=full)
    print("shot", name)


def scroll_to(page, sel):
    page.locator(sel).evaluate("e => e.scrollIntoView({block: 'start'})")


def top(page):
    page.locator("#main").evaluate("m => m.scrollTo(0, 0)")


def open_eq(page, s):
    page.goto(s.url + "#enquetes")
    page.wait_for_selector("#eq-list")
    page.wait_for_timeout(300)


def desk(page, out, s, gate):
    open_eq(page, s)
    page.locator("#eq-new").click()
    page.locator("#eq-question").fill("Pourquoi le chrono de la course repart-il de zéro après une pause ?")
    snap(page, out, "01-nouvelle-enquete")
    page.locator("#eq-launch").click()
    page.wait_for_function("document.querySelectorAll('#eq-current .eq-steps div').length >= 7")
    snap(page, out, "02-enquete-en-cours-refus-en-rouge")
    page.locator("#computer-ask-name").fill("travail")
    page.locator("#computer-ask-save").click()
    s.loop.call_soon_threadsafe(gate.set)
    page.wait_for_selector("#eq-current .notice.ok")
    page.locator("#eq-current").get_by_role("button", name="Lire le rapport").click()
    page.wait_for_selector("#eq-reader .mdoc")
    top(page)
    snap(page, out, "03-enquete-finie-et-son-rapport")
    scroll_to(page, "#eq-reader .eq-next")
    page.locator("#eq-bug").click()
    page.wait_for_selector("#eq-bug-entry")
    scroll_to(page, "#eq-reader .eq-next")
    snap(page, out, "04-ajouter-a-la-liste-de-bugs-avant-confirmation")
    page.locator("#eq-bug-add").click()
    page.wait_for_selector("#eq-reader .notice.ok")
    scroll_to(page, "#eq-reader .eq-next")
    snap(page, out, "05-entree-de-bug-ecrite")
    # The chain and the cockpit: the prompt, marked, never launched.
    page.locator("#eq-reader").get_by_role("button", name="Fermer").click()
    page.locator("#eq-new").click()
    page.locator("#eq-question").fill("Pourquoi le journal écrit-il le nom réseau de l'ordinateur ?")
    page.locator("input[name=eq-target][value=chaine]").check()
    page.locator("#eq-launch").click()
    page.wait_for_function("(() => { const c = document.querySelector('#eq-current'); "
                           "return c.textContent.includes('nom réseau') && c.querySelector('.notice.ok'); })()")
    page.locator("#eq-current").get_by_role("button", name="Lire le rapport").click()
    page.wait_for_selector("#eq-prompt")
    page.locator("#eq-prompt").click()
    page.wait_for_selector("#eq-reader .eq-mark")
    scroll_to(page, "#eq-reader .eq-next")
    snap(page, out, "06-prompt-de-correction-a-relire")
    top(page)
    page.locator("#eq-reader").get_by_role("button", name="Fermer").click()
    scroll_to(page, "#eq-list")
    snap(page, out, "07-liste-des-rapports")
    # From a point à creuser.
    page.goto(s.url + "#journal")
    page.wait_for_selector("#jn-points .eq-go")
    snap(page, out, "08-journal-enqueter-sur-ce-point")
    page.locator("#jn-points .jn-point", has_text="n'était pas connecté").get_by_role(
        "button", name="Enquêter sur ce point").click()
    page.wait_for_selector("#eq-form:not(.hidden)")
    top(page)
    snap(page, out, "09-question-ecrite-depuis-le-point")
    page.locator("#eq-form-cancel").click()
    # A run in error.
    page.goto(s.url + "#chaine")
    page.wait_for_selector("#side")
    s.call(s.rn.start(str(s.app_root), "f", "f", "2_structure", "f"))
    page.wait_for_selector("#run-enquete")
    page.locator("#run-end").evaluate("e => e.scrollIntoView({block: 'center'})")
    snap(page, out, "10-run-en-erreur-enqueter")
    page.goto(s.url + "#settings")
    page.wait_for_selector("#sec-computer")
    scroll_to(page, "#sec-computer")
    snap(page, out, "11-parametres-cet-ordinateur")
    page.evaluate("document.documentElement.dataset.theme = 'dark'")
    open_eq(page, s)
    page.evaluate("document.documentElement.dataset.theme = 'dark'")
    snap(page, out, "12-enquetes-sombre")


def ask_shot(browser, out, s):
    """The nickname asked, on a computer that has none yet."""
    s.state.data.pop("computer", None)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(s.url + "#dashboard")
    page.wait_for_selector("#side")
    page.evaluate("postRun('1_lexique', 'f')")
    page.wait_for_selector("#computer-ask:not(.hidden)")
    snap(page, out, "13-nom-de-cet-ordinateur-demande-une-fois")
    page.close()


def on_phone(browser, out, s):
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    ph = ctx.new_page()
    ph.goto(s.url + "#dashboard")
    ph.wait_for_selector("#phone-nav")
    ph.locator("#phone-more").click()
    ph.wait_for_selector("#phone-enquetes")
    snap(ph, out, "14-telephone-plus-enquetes")
    ph.locator("#phone-enquetes").click()
    ph.wait_for_selector("#eq-list .eq-item")
    snap(ph, out, "15-telephone-enquetes")
    ph.locator("#eq-list .eq-item").last.click()
    ph.wait_for_selector("#eq-reader .mdoc")
    scroll_to(ph, "#eq-reader")
    snap(ph, out, "16-telephone-rapport")
    ctx.close()


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        copies.ROOT = str(t / "modeles")
        copies.SHARED = str(t / "partages")
        os.makedirs(copies.SHARED)
        from selfupdateworld import chain_world
        _, here, _ = chain_world(t / "c")
        server.CHAIN_ROOT = str(here)
        gate = asyncio.Event()

        async def failing(c):
            yield ResultMessage(subtype="error_during_execution", duration_ms=1, duration_api_ms=1, is_error=True,
                                num_turns=1, session_id="s", result="Je n'ai pas pu lire la fiche du lot 3.",
                                errors=["docs/features/f/code/lot-03/fiche.md introuvable"])
        server.ENQUETE_CLIENT = Factory(answering(APP_ANSWER, tools=WRITES[:5] + READS, gate=gate), saying(BUG), answering(CHAIN_ANSWER), saying(PROMPT))
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge")
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            with FakeServer(t / "w", script=failing) as s:
                s.state.rename_app(str(s.app_root), "Hyrox Tracker")
                journalworld.make(s.app_root)
                desk(page, out, s, gate)
                ask_shot(browser, out, s)
                on_phone(browser, out, s)
            browser.close()
            if errors:
                print("erreurs de la page :", *errors, sep="\n  ")


if __name__ == "__main__":
    main(sys.argv[1])
