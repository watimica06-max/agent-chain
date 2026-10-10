"""1.16 — « État de l'ordinateur »: each item in each of its states, each
rule of §2 — what it blocks and what it does not —, the badge's summary.
Every probe sees the fake computer (machinefakes.py); git's core.longpaths
is read and set in scratch repositories. No real command of this computer
runs, no real login is touched."""
import os
import subprocess

import pytest

import machine
from machine import (BATIR, BLOCK, CHAIN_INSTALL, COMMIT, DEPLOY, FIXED, FIXING, LAUNCH, OK, OPTIONAL, PUSH,
                     SAVE, SEND, SKIP, TOOL_INSTALL, UNKNOWN, WARN)


def git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=True).stdout


def repo(path):
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q")
    return path


@pytest.fixture
def ctx(tmp_path):
    root = repo(tmp_path / "agent-chain")
    git(root, "config", "--local", "core.longpaths", "true")
    return {"chain_root": str(root), "started": "a" * 40, "head": "a" * 40, "apps": [], "diagnostic": None,
            "chain_sync": {"state": "à jour", "summary": "À jour avec GitHub"}}


def items(fam, ctx):
    return {x["id"]: x for x in machine.FAMILIES[fam](ctx)}


def check(ctx, *fams):
    m = machine.Machine()
    if fams:
        m.refresh(list(fams), ctx)
    else:
        m.full(ctx)
    return m


# ------------------------------------------------------------ Claude Code

def test_claude_ok_logged_in(ctx, fake_machine):
    it = items("claude", ctx)
    assert it["claude_cli"]["status"] == OK and "2.1.285" in it["claude_cli"]["detail"]
    assert "minimum du SDK : 2.0.0" in it["claude_cli"]["detail"] and fake_machine.cli in it["claude_cli"]["detail"]
    assert it["claude_login"]["status"] == OK and "claude.ai" in it["claude_login"]["detail"]
    # The probes ran with the CLI the SDK runs.
    assert [fake_machine.cli, "auth", "status"] in fake_machine.calls


def test_claude_logged_out_blocks_every_launch_and_the_installs(ctx, fake_machine):
    fake_machine.logged_in = False
    m = check(ctx, "claude")
    it = {x["id"]: x for x in m.items()}
    x = it["claude_login"]
    assert x["status"] == BLOCK and x["repair"]["id"] == "claude_login" and x["repair"]["label"] == "Se connecter à Claude"
    assert "n'est pas connecté" in x["detail"]
    assert set(x["stops"]) == {LAUNCH, TOOL_INSTALL}
    assert [b["id"] for b in m.blockers(LAUNCH)] == ["claude_login"]
    assert [b["id"] for b in m.blockers(TOOL_INSTALL)] == ["claude_login"]
    assert m.blockers(PUSH) == [] and m.blockers(CHAIN_INSTALL) == [] and m.blockers(BATIR) == []


def test_claude_missing_or_below_its_minimum_blocks_launches(ctx, fake_machine):
    fake_machine.cli = None
    it = items("claude", ctx)
    assert it["claude_cli"]["status"] == BLOCK and LAUNCH in it["claude_cli"]["stops"]
    assert it["claude_cli"]["repair"]["label"] == "Installer Claude Code"
    assert it["claude_login"]["status"] == UNKNOWN and "Claude Code d'abord" in it["claude_login"]["detail"]
    fake_machine.cli = machinefakes_cli()
    fake_machine.version = "1.9.0 (Claude Code)"
    it = items("claude", ctx)
    assert it["claude_cli"]["status"] == BLOCK and "sous le minimum du SDK (2.0.0)" in it["claude_cli"]["detail"]
    assert it["claude_cli"]["repair"]["label"] == "Mettre à jour Claude Code"


def machinefakes_cli():
    import machinefakes
    return machinefakes.CLI


def test_claude_status_that_does_not_answer_is_unknown_and_blocks_nothing(ctx, fake_machine):
    fake_machine.answers[f"{fake_machine.cli} auth status"] = subprocess.TimeoutExpired("claude", 30)
    m = check(ctx, "claude")
    x = {i["id"]: i for i in m.items()}["claude_login"]
    assert x["status"] == UNKNOWN and "pas de réponse" in x["detail"] and m.blockers(LAUNCH) == []


# ------------------------------------------------------------ git

def test_identity_set_guessed_missing(ctx, fake_machine):
    it = items("identity", ctx)
    assert it["git"]["status"] == OK and it["git_identity"]["status"] == OK
    assert it["git_identity"]["detail"] == "Product Owner <po@example.com>"
    fake_machine.identity = "guessed"
    m = check(ctx, "identity")
    x = {i["id"]: i for i in m.items()}["git_identity"]
    assert x["status"] == WARN and "git la devine" in x["detail"] and "PO Devine <po@ordinateur.local>" in x["detail"]
    assert x["repair"]["id"] == "identity" and m.blockers(COMMIT) == [] and m.blockers(LAUNCH) == []
    fake_machine.identity = "missing"
    m = check(ctx, "identity")
    x = {i["id"]: i for i in m.items()}["git_identity"]
    assert x["status"] == BLOCK and x["repair"]["label"] == "Régler"
    # Anything that commits: a launch, an install of the chain, « Envoyer mes réponses », Données…
    for action in (LAUNCH, CHAIN_INSTALL, SEND, COMMIT, SAVE):
        assert [b["id"] for b in m.blockers(action)] == ["git_identity"], action
    # … not a push, nor « Bâtir »'s tools.
    assert m.blockers(PUSH) == [] and m.blockers(DEPLOY) == []


def test_git_missing_blocks_what_commits(ctx, fake_machine):
    fake_machine.git = False
    it = items("identity", ctx)
    assert it["git"]["status"] == BLOCK and it["git"]["repair"]["id"] == "tool"
    assert it["git_identity"]["status"] == UNKNOWN


def test_github_credentials_ok_missing_offline_rejected(ctx, fake_machine):
    it = items("github", ctx)
    assert it["gcm"]["status"] == OK and it["github"]["status"] == OK and it["github_reach"]["status"] == OK
    assert "compte : quelqu-un" in it["github"]["detail"]
    # Missing: blocks what pushes — a push, an install of the chain, « Envoyer » —, never a launch.
    fake_machine.github = "credentials"
    fake_machine.accounts = []
    m = check(ctx, "github")
    x = {i["id"]: i for i in m.items()}["github"]
    assert x["status"] == BLOCK and x["repair"]["label"] == "Se connecter à GitHub"
    assert set(x["stops"]) == {PUSH, CHAIN_INSTALL, SEND}
    assert m.blockers(LAUNCH) == [] and [b["id"] for b in m.blockers(PUSH)] == ["github"]
    assert "signale pour un lancement" in x["rule_text"]
    # Unreachable: credentials not checked; chain installs blocked while it lasts.
    fake_machine.github = "offline"
    m = check(ctx, "github")
    it = {i["id"]: i for i in m.items()}
    assert it["github"]["status"] == UNKNOWN and it["github_reach"]["status"] == WARN
    assert "GitHub injoignable" in it["github_reach"]["detail"]
    assert [b["id"] for b in m.blockers(CHAIN_INSTALL)] == ["github_reach"] and m.blockers(PUSH) == []
    # Rejected (GitHub has more): it answered and took the credentials.
    fake_machine.github = "rejected"
    assert items("github", ctx)["github"]["status"] == OK


def test_gcm_missing_notifies(ctx, fake_machine):
    fake_machine.gcm = False
    it = items("github", ctx)
    assert it["gcm"]["status"] == WARN and it["gcm"]["stops"] == [] and it["gcm"]["repair"]["id"] == "tool"


def test_longpaths_fixes_itself_agent_chain_included(ctx, tmp_path):
    app = repo(tmp_path / "app")
    git(app, "config", "--local", "core.longpaths", "false")
    root = ctx["chain_root"]
    git(root, "config", "--local", "--unset", "core.longpaths")
    ctx["apps"] = [{"name": "App", "folder": str(app)}]
    it = items("longpaths", ctx)
    assert it["longpaths"]["status"] == FIXED and "absent → réglé à true" in it["longpaths"]["detail"]
    k = f"app:{machine.key(str(app))}:longpaths"
    assert it[k]["status"] == FIXED and "false → réglé" in it[k]["detail"] and it[k]["app"] == str(app)
    assert git(root, "config", "--local", "--get", "core.longpaths").strip() == "true"
    assert git(app, "config", "--local", "--get", "core.longpaths").strip() == "true"
    it = items("longpaths", ctx)
    assert it["longpaths"]["status"] == OK and it[k]["status"] == OK


# ------------------------------------------------------------ Android and builds

def android_app(tmp_path):
    a = tmp_path / "android-app"
    a.mkdir()
    (a / "gradlew.bat").write_text("@echo off")
    return {"name": "Montre", "folder": str(a)}


def test_android_tools_notify_and_block_batir_and_the_deploy_screen_only(ctx, tmp_path, fake_machine):
    ctx["apps"] = [android_app(tmp_path)]
    it = items("android", ctx)
    assert it["adb"]["status"] == OK and r"platform-tools\adb.exe" in it["adb"]["detail"]
    assert it["sdkmanager"]["status"] == OK and it["android_sdk"]["status"] == OK
    assert it["emulator"]["status"] == OPTIONAL and it["scrcpy"]["status"] == OPTIONAL
    fake_machine.adb = None
    fake_machine.sdkmanager = None
    fake_machine.sdk = None
    m = check(ctx, "android")
    it = {i["id"]: i for i in m.items()}
    for k in ("adb", "sdkmanager", "android_sdk"):
        assert it[k]["status"] == WARN and set(it[k]["stops"]) == {BATIR, DEPLOY}, k
        assert it[k]["repair"] == {"id": "tool", "label": "Installer avec Claude", "args": {"tool": k}}
    assert {b["id"] for b in m.blockers(BATIR)} == {"adb", "sdkmanager", "android_sdk"}
    assert {b["id"] for b in m.blockers(DEPLOY)} == {"adb", "sdkmanager", "android_sdk"}
    assert m.blockers(LAUNCH) == [] and m.blockers(PUSH) == []
    # Optional ones never alert.
    assert it["emulator"]["stops"] == [] and it["emulator"]["status"] == OPTIONAL


def test_android_tools_not_concerned_without_an_android_application(ctx, fake_machine):
    fake_machine.adb = None
    fake_machine.sdkmanager = None
    fake_machine.sdk = None
    it = items("android", ctx)
    assert it["adb"]["status"] == SKIP and it["sdkmanager"]["status"] == SKIP and it["android_sdk"]["status"] == SKIP


def test_java_gradle_flutter_from_the_open_applications_diagnostic(ctx):
    ctx["diagnostic"] = {"results": [
        {"id": "java", "status": "fail", "detail": "java introuvable (PATH)"},
        {"id": "gradle", "status": "ok", "detail": "Gradle 8.7"},
        {"id": "flutter", "status": "skip", "detail": "non concerné"}]}
    ctx["app_name"] = "Montre"
    m = check(ctx, "android")
    it = {i["id"]: i for i in m.items()}
    assert it["java"]["status"] == WARN and "Montre" in it["java"]["detail"] and set(it["java"]["stops"]) == {BATIR, DEPLOY}
    assert it["java"]["repair"]["args"] == {"tool": "java"}
    assert it["gradle"]["status"] == OK and it["flutter"]["status"] == SKIP
    assert [b["id"] for b in m.blockers(BATIR)] == ["java"] and m.blockers(LAUNCH) == []


# ------------------------------------------------------------ the cockpit itself

def test_server_against_the_disk(ctx):
    assert items("cockpit", ctx)["server"]["status"] == OK
    ctx["head"] = "b" * 40
    x = items("cockpit", ctx)["server"]
    assert x["status"] == FIXING and "il redémarre de lui-même" in x["detail"] and x["repair"]["id"] == "restart"
    ctx["busy"] = "la fin de /8_code f"
    x = items("cockpit", ctx)["server"]
    assert x["status"] == WARN and "après la fin de /8_code f" in x["detail"]
    ctx["busy"] = None
    ctx["restart"] = {"error": "le nouveau serveur n'a pas répondu"}
    x = items("cockpit", ctx)["server"]
    assert x["status"] == WARN and "le redémarrage a échoué" in x["detail"]


def test_agent_chain_against_github(ctx):
    for st, want in (({"state": "à jour"}, OK), ({"state": "en retard", "summary": "En retard : 2"}, FIXING),
                     ({"state": "divergé", "summary": "Divergé"}, WARN),
                     ({"state": "non envoyé", "ahead": 1, "summary": "Non envoyé : 1"}, WARN),
                     ({"state": "GitHub injoignable", "ahead": 2, "summary": "GitHub injoignable · 2 non envoyés"}, WARN)):
        ctx["chain_sync"] = st
        x = items("cockpit", ctx)["chain"]
        assert x["status"] == want, st
    # Pulled, not yet in service.
    ctx["chain_sync"] = {"state": "à jour"}
    ctx["head"] = "b" * 40
    x = items("cockpit", ctx)["chain"]
    assert x["status"] == WARN and "pas encore en service" in x["detail"]


def test_python_dependencies(ctx, fake_machine):
    assert items("cockpit", ctx)["python"]["status"] == OK
    fake_machine.deps = {"ok": False, "count": 3, "missing": [{"name": "aiohttp", "spec": ">=3.9,<4", "installed": None}]}
    x = items("cockpit", ctx)["python"]
    assert x["status"] == WARN and "aiohttp>=3.9,<4 (absent)" in x["detail"] and x["repair"]["id"] == "pip"
    assert x["stops"] == [] and x["rule"] == machine.R_FIX
    ctx["pip"] = {"going": True}
    assert items("cockpit", ctx)["python"]["status"] == FIXING


# ------------------------------------------------------------ each application

def test_each_application(ctx, tmp_path):
    a = tmp_path / "app"
    (a / "docs").mkdir(parents=True)
    (a / "docs" / "TECHNICAL_CONVENTIONS.md").write_text("# C\n")
    row = {"name": "Carnet", "folder": str(a), "sync": {"state": "divergé", "summary": "Divergé : 1 ici, 1 là"},
           "chain": {"state": "en retard", "summary": "Chaîne en retard"},
           "build": {"commit": "1111111aaaa"}, "conventions": "2222222bbbb"}
    ctx["apps"] = [row]
    m = check(ctx, "apps")
    k = machine.key(str(a))
    it = {i["id"]: i for i in m.items()}
    gh = it[f"app:{k}:github"]
    assert gh["status"] == BLOCK and set(gh["stops"]) == {LAUNCH, CHAIN_INSTALL, SAVE}
    assert gh["repair"] == {"id": "reconcile", "label": "Réconcilier", "args": {"folder": str(a)}}
    # Its own application only.
    assert [b["id"] for b in m.blockers(LAUNCH, str(a))] == [f"app:{k}:github"]
    assert m.blockers(LAUNCH, str(tmp_path / "autre")) == [] and m.blockers(LAUNCH) == []
    assert it[f"app:{k}:chain"]["status"] == WARN and it[f"app:{k}:chain"]["stops"] == []
    b = it[f"app:{k}:build"]
    assert b["status"] == WARN and "« Bâtir » est proposé à nouveau" in b["detail"]
    # Not sent: never green; unreachable with commits not sent: said.
    row["sync"] = {"state": "non envoyé", "ahead": 2, "summary": "Non envoyé : 2 commits"}
    assert items("apps", ctx)[f"app:{k}:github"]["status"] == WARN
    row["sync"] = {"state": "GitHub injoignable", "ahead": 2, "summary": "GitHub injoignable · 2 non envoyés"}
    x = items("apps", ctx)[f"app:{k}:github"]
    assert x["status"] == WARN and "2 non envoyés" in x["detail"] and x["repair"]["id"] == "push"
    row["sync"] = {"state": "GitHub injoignable", "ahead": 0, "summary": "GitHub injoignable"}
    x = items("apps", ctx)[f"app:{k}:github"]
    assert x["status"] == WARN and x["stops"] == [CHAIN_INSTALL]
    row["sync"] = {"state": "en retard", "behind": 1, "summary": "En retard"}
    assert items("apps", ctx)[f"app:{k}:github"]["repair"]["id"] == "pull"
    row["build"], row["conventions"] = {"commit": "2222222bbbb"}, "2222222bbbb"
    assert items("apps", ctx)[f"app:{k}:build"]["status"] == OK
    row["build"] = None
    assert "jamais été bâti" in items("apps", ctx)[f"app:{k}:build"]["detail"]
    os.remove(a / "docs" / "TECHNICAL_CONVENTIONS.md")
    assert items("apps", ctx)[f"app:{k}:build"]["status"] == SKIP


# ------------------------------------------------------------ the whole view

def test_full_check_summary_and_badge_levels(ctx, fake_machine):
    m = check(ctx)
    r = m.report()
    assert r["at"] and r["summary"] == {"level": "ok", "count": 0, "block": 0, "warn": 0, "text": "Tout est en ordre"}
    assert all(x["checked_at"] for x in r["items"])
    fake_machine.identity = "guessed"
    m = check(ctx)
    sm = m.report()["summary"]
    assert sm["level"] == "warn" and sm["count"] == 1 and sm["text"].startswith("git — identité des commits")
    fake_machine.logged_in = False
    m = check(ctx)
    sm = m.report()["summary"]
    assert sm["level"] == "block" and sm["block"] == 1 and "n'est pas connecté" in sm["text"] and "1 à voir" in sm["text"]


def test_a_probe_that_raises_is_said_on_its_line(ctx, monkeypatch):
    def boom(ctx):
        raise RuntimeError("panne")
    monkeypatch.setitem(machine.FAMILIES, "android", boom)
    m = check(ctx)
    x = [i for i in m.items() if i["id"] == "android:erreur"]
    assert x and x[0]["status"] == UNKNOWN and "panne" in x[0]["detail"]


def test_before_an_action_checks_again_what_blocks_it(ctx, fake_machine):
    m = check(ctx)
    fake_machine.calls.clear()
    fake_machine.logged_in = False
    assert [b["id"] for b in m.before(LAUNCH, ctx)] == ["claude_login"]
    ran = [" ".join(c) for c in fake_machine.calls]
    assert any("auth status" in c for c in ran) and not any("push" in c for c in ran)      # GitHub not for a launch
    # Before a push, GitHub again — unless checked a moment ago.
    fake_machine.calls.clear()
    m.before(PUSH, ctx)
    assert not any("push" in " ".join(c) for c in fake_machine.calls)
    m.families["github"]["at"] = "2000-01-01T00:00:00"
    fake_machine.github = "credentials"
    assert [b["id"] for b in m.before(PUSH, ctx)] == ["github"]


def test_refusal_names_the_item_and_where_to_repair(ctx, fake_machine):
    fake_machine.logged_in = False
    m = check(ctx, "claude")
    r = machine.refusal(m.blockers(LAUNCH))
    assert r["error"].startswith("Claude Code — connecté : Claude Code n'est pas connecté")
    assert "Paramètres → État de l'ordinateur" in r["error"] and r["machine"][0]["repair"]["id"] == "claude_login"
