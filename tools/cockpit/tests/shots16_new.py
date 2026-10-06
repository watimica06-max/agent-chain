"""1.6 — the new screens, for shots16.py « apres »: « Applications » with
three applications, its feature card, « Ajouter une application »; the top
bar's switcher open; « Tout mettre à jour » run for real on scratch
repositories (a chain repository, one application « en retard » with a bare
remote, one « modifiée sur place », one « absente »); a run going in another
application, seen from the active one. Nothing leaves the temporary folder."""
import subprocess

import chain
import server
from fakeapp import FakeServer
from test_apps import second_app
from test_chain import CHAIN_FILES, commit, git, init, write
from test_runner import script_until_interrupted


def snap(page, out, name):
    page.wait_for_timeout(500)
    page.screenshot(path=str(out / f"{name}.png"))
    print("shot", name)


def scratch(t):
    """A chain repository at its second commit, and three applications."""
    root = t / "agent-chain"
    init(root)
    for rel, text in CHAIN_FILES.items():
        write(root, rel, text)
    commit(root, "Chaîne — un")

    def app(name, install):
        repo = t / name
        init(repo)
        write(repo, ".claude/commands/deploie.md", f"{name}'s own\n")
        write(repo, "docs/features/premiere-app/idees.md", "idea\n")
        commit(repo, "app")
        remote = t / f"{name}.git"
        subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
        git(repo, "remote", "add", "origin", str(remote))
        git(repo, "push", "-q", "-u", "origin", "master")
        if install:
            chain.install(str(repo), str(root), push=True)
        return repo

    late = app("hyrox_tracker", True)
    modified = app("atelier", True)
    absent = app("nutrition_app", False)
    write(modified, ".claude/agents/b.md", "changed in the application\n")
    commit(modified, "edited the chain in place")
    write(root, ".claude/agents/a.md", "agent a, two\n")
    commit(root, "Chaîne — deux")
    chain._chain_cache.clear()
    chain._behind_cache.clear()
    return root, late, modified, absent


def main(page, out, t):
    real_state = server.chain_state
    root, late, modified, absent = scratch(t)
    server.CHAIN_ROOT = str(root)
    server.CHAIN_PUSH = True
    server.chain_state = lambda app: chain.state(app, str(root))
    try:
        with FakeServer(t / "s") as s:
            for r in (late, modified, absent):
                s.state.add_app(str(r))
            s.state.rename_app(str(absent), "Belivo")
            # The fake application stays the active one, its feature open.
            page.goto(s.url + "#apps")
            page.wait_for_selector(".app-row")
            snap(page, out, "apres-10-applications")
            page.get_by_role("button", name="Ajouter une application").click()
            page.locator("#app-path").fill(str(t / "pas-un-depot"))
            (t / "pas-un-depot").mkdir()
            page.locator("#btn-app").click()
            page.wait_for_selector("#apps-msg:not(.hidden)")
            snap(page, out, "apres-11-ajouter-refuse")
            page.locator("#btn-app-add").click()
            page.on("dialog", lambda d: d.accept())
            page.get_by_role("button", name="Tout mettre à jour").click()
            page.wait_for_selector("#apps-report .line", timeout=120000)
            page.evaluate("document.getElementById('main').scrollTo(0, 0)")
            snap(page, out, "apres-12-tout-mettre-a-jour")
            page.locator("#apps-list").scroll_into_view_if_needed()
            page.evaluate("document.getElementById('apps-list').scrollIntoView({block: 'start'})")
            snap(page, out, "apres-12b-applications-apres-mise-a-jour")
            # The top bar's switcher, open.
            page.get_by_role("link", name="Tableau de bord").first.click()
            page.locator("#tb-app").click()
            page.wait_for_selector("#app-menu:not(.hidden)")
            snap(page, out, "apres-13-changer-d-application")
            # Belivo active: no feature opens there — its card says so, its install is on its row.
            page.locator("#app-menu button", has_text="Belivo").click()
            page.wait_for_selector("#work-card:not(.hidden)")
            snap(page, out, "apres-14-belivo-active-choisir-la-feature")
            page.locator("#tb-app").click()
            page.locator("#app-menu button", has_text="app").first.click()
            page.wait_for_function("document.getElementById('tb-app').textContent.startsWith('app')")
        server.chain_state = lambda app: {"state": "à jour", "summary": "Chaîne à jour — 93d18fc du 2026-10-06",
                                          "subjects": [], "modified": [], "chain_commit": "93d18fc", "chain_date": "2026-10-06"}
        with FakeServer(t / "r", script=script_until_interrupted) as s:
            b = t / "r" / "belivo"
            second_app(b)
            s.state.add_app(str(b))
            s.state.rename_app(str(b), "Belivo")
            s.state.open_pair(str(b), "g")
            page.goto(s.url + "#dashboard")
            page.wait_for_function("document.getElementById('next-text').textContent !== '—'")
            s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
            page.wait_for_selector("#busy-banner:not(.hidden)")
            snap(page, out, "apres-15-run-dans-une-autre-application")
            page.get_by_role("link", name="Chaîne").first.click()
            page.wait_for_selector("#flow-main li.step")
            snap(page, out, "apres-15b-chaine-run-ailleurs")
            s.call(s.rn.stop_now(str(s.app_root)))
    finally:
        server.chain_state = real_state
