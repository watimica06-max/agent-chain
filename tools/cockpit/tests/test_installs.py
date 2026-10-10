"""1.16 §3 — the repairs that take a while, against fakes: the sign-ins
(Claude, GitHub), the Python dependencies, Claude Code itself, « Installer
avec Claude ». Both install modes: « Rapide » asks nothing after the start
and lists the licences accepted; « Pas à pas » shows a card per step and per
licence, and a refused licence stops the install. The two real login
checks run only against a throwaway config: CLAUDE_CONFIG_DIR, a Git
Credential Manager store of the test — never the Product Owner's login."""
import json
import os
import shutil
import subprocess
import sys
import time

import pytest
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock
from claude_agent_sdk.types import ToolPermissionContext

import deps
import installs


def wait(pred, timeout=20.0):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        v = pred()
        if v:
            return v
        time.sleep(0.05)
    raise AssertionError("jamais arrivé")


@pytest.fixture
def inst(tmp_path):
    seen = []
    i = installs.Installs(str(tmp_path / "logs"), emit=seen.append)
    i.seen = seen
    return i


def ended(inst, s=None):
    """The session `s` once ended — the one going by default."""
    s = s or inst.current
    return wait(lambda: s if s.status == "ended" and inst.last is s else None, 30)


def card(inst, kind=None):
    def has():
        s = inst.going()
        c = s and s.card
        return c if c and (kind is None or c["kind"] == kind) else None
    return wait(has)


def recorded(tmp_path):
    with open(tmp_path / "logs" / installs.LOG_NAME, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


# ------------------------------------------------------------ the Python dependencies

PKGS = [{"name": "aiohttp", "version": "3.10.5", "licence": "Apache-2.0", "requested": True},
        {"name": "multidict", "version": "6.0.5", "licence": "Apache 2", "requested": False}]


@pytest.fixture
def fake_pip(monkeypatch):
    calls = {"install": 0, "licence": []}
    monkeypatch.setattr(deps, "plan", lambda path=None: {"ok": True, "packages": [dict(p) for p in PKGS], "message": ""})

    def install(path=None):
        calls["install"] += 1
        return {"ok": True, "message": "", "installed": ["aiohttp-3.10.5", "multidict-6.0.5"]}
    monkeypatch.setattr(deps, "install", install)

    def text(name, version):
        calls["licence"].append(name)
        return f"{name} licence — le texte entier.", ""
    monkeypatch.setattr(deps, "licence_text", text)
    return calls


def test_pip_rapide_asks_nothing_and_lists_the_licences(tmp_path, inst, fake_pip):
    inst.start("pip", "Dépendances Python", installs.pip_install(installs.RAPIDE), mode=installs.RAPIDE)
    s = ended(inst)
    assert s.outcome == "installé" and s.restart is True
    assert not any(x.get("card") for x in inst.seen)                       # no card, ever
    first = s.steps[1]["text"]
    assert first.startswith("Rapide — installe : aiohttp 3.10.5 (Apache-2.0), multidict 6.0.5 (Apache 2)")
    assert "licences acceptées d'avance : Apache 2, Apache-2.0" in first
    assert [x["text"] for x in s.steps].index(first) < [x["text"] for x in s.steps].index("pip install --user -r requirements.txt")
    assert s.installed == ["aiohttp-3.10.5", "multidict-6.0.5"]
    assert [l["name"] for l in s.licences] == ["Apache-2.0", "Apache 2"] and fake_pip["licence"] == []
    rec = recorded(tmp_path)[-1]
    assert rec["mode"] == "rapide" and rec["outcome"] == "installé" and rec["licences"] == s.licences


def test_pip_pas_a_pas_a_card_per_step_and_per_licence(tmp_path, inst, fake_pip):
    inst.start("pip", "Dépendances Python", installs.pip_install(installs.PAS_A_PAS), mode=installs.PAS_A_PAS)
    shown = []
    for _ in range(4):
        c = card(inst)
        shown.append((c["kind"], c["title"]))
        if c["kind"] == "licence":
            assert c["text"].endswith("le texte entier.")                # in full
        assert inst.going().answer(c["id"], True)
        wait(lambda: not inst.going() or not inst.going().card or inst.going().card["id"] != c["id"])
    s = ended(inst)
    assert shown == [("étape", "Installer aiohttp 3.10.5"), ("licence", "Licence de aiohttp 3.10.5 : Apache-2.0"),
                     ("étape", "Installer multidict 6.0.5"), ("licence", "Licence de multidict 6.0.5 : Apache 2")]
    assert s.outcome == "installé" and fake_pip["install"] == 1 and len(s.licences) == 2


def test_pip_a_refused_licence_stops_the_install(tmp_path, inst, fake_pip):
    inst.start("pip", "Dépendances Python", installs.pip_install(installs.PAS_A_PAS), mode=installs.PAS_A_PAS)
    c = card(inst, "étape")
    inst.going().answer(c["id"], True)
    c = card(inst, "licence")
    inst.going().answer(c["id"], False)
    s = ended(inst)
    assert s.outcome == "refusé" and "Licence refusée : Apache-2.0" in s.message
    assert fake_pip["install"] == 0 and s.installed == [] and s.licences == []
    assert recorded(tmp_path)[-1]["outcome"] == "refusé"


FAKE_PIP = r'''
import json, sys
args = sys.argv[1:]
if "--dry-run" in args:
    report = args[args.index("--report") + 1]
    json.dump({"install": [{"requested": True, "metadata": {"name": "rich", "version": "13.7.1", "license": "MIT"}},
                           {"requested": False, "metadata": {"name": "pygments", "version": "2.18.0",
                                                             "license_expression": "BSD-2-Clause"}}]},
              open(report, "w"))
    sys.exit(0)
print("Successfully installed pygments-2.18.0 rich-13.7.1")
'''


def test_plan_reads_pips_report_and_installs_nothing(tmp_path, monkeypatch):
    p = tmp_path / "pip.py"
    p.write_text(FAKE_PIP, encoding="utf-8")
    monkeypatch.setattr(deps, "PIP_COMMAND", [sys.executable, str(p)])
    plan = deps.plan()
    assert plan["ok"] and [(x["name"], x["licence"]) for x in plan["packages"]] == [("rich", "MIT"), ("pygments", "BSD-2-Clause")]
    assert deps.install()["installed"] == ["pygments-2.18.0", "rich-13.7.1"]


def test_licence_read_in_full_from_a_wheel(tmp_path):
    import zipfile
    w = tmp_path / "x-1.0-py3-none-any.whl"
    with zipfile.ZipFile(w, "w") as z:
        z.writestr("x-1.0.dist-info/licenses/LICENSE", "MIT License\n\nPermission is hereby granted…")
        z.writestr("x/__init__.py", "")
    assert "Permission is hereby granted" in deps._read_licences(str(w))


def test_requirements_checked_against_what_is_installed(tmp_path):
    req = tmp_path / "requirements.txt"
    req.write_text("aiohttp>=3.9,<4\ncryptography>=42      # commentaire\n-r autre.txt\n", encoding="utf-8")
    got = deps.check(str(req), version_of={"aiohttp": "3.10.5", "cryptography": "41.0.1"}.get)
    assert not got["ok"] and got["missing"] == [{"name": "cryptography", "spec": ">=42", "installed": "41.0.1"}]
    got = deps.check(str(req), version_of=lambda n: None)
    assert [m["name"] for m in got["missing"]] == ["aiohttp", "cryptography"]
    assert "aiohttp>=3.9,<4 (absent)" in deps.missing_text(got)


# ------------------------------------------------------------ « Installer avec Claude »

class ToolClient:
    """A Claude run of an install: a step (Bash), a licence, the result."""

    def __init__(self, can_use_tool, licence, licence_name, result="Résultat : installé — Android Debug Bridge 1.0.41"):
        self.can_use_tool, self.licence = can_use_tool, licence
        self.licence_name, self.result = licence_name, result
        self.prompts, self.answers = [], {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def query(self, prompt):
        self.prompts.append(prompt)

    async def interrupt(self):
        pass

    async def receive_response(self):
        r = await self.can_use_tool("Bash", {"command": "winget show --id Google.PlatformTools"},
                                    ToolPermissionContext())
        self.answers["step"] = type(r).__name__
        if type(r).__name__ != "PermissionResultAllow":
            yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False, num_turns=1,
                                session_id="s", result="Résultat : échec — étape refusée")
            return
        yield AssistantMessage(content=[TextBlock("Je lis la licence.")], model="m")
        ok = await self.licence(self.licence_name, "ANDROID SOFTWARE DEVELOPMENT KIT LICENSE AGREEMENT\n1. …", "sdkmanager --licenses")
        self.answers["licence"] = ok
        text = self.result if ok else "Résultat : échec — licence refusée"
        yield AssistantMessage(content=[TextBlock(text)], model="m")
        yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1, is_error=False, num_turns=1,
                            session_id="s", result=text)


@pytest.fixture
def claude_client(monkeypatch):
    made = []

    def factory(licence_name):
        def make(workdir, can_use_tool, licence):
            c = ToolClient(can_use_tool, licence, licence_name)
            made.append(c)
            return c
        monkeypatch.setattr(installs, "CLIENT_FACTORY", make)
    factory.made = made
    return factory


def with_claude(inst, tmp_path, mode, ok=True):
    return inst.start("tool", "Installer adb", installs.with_claude(
        "adb", mode, str(tmp_path / "work"), str(tmp_path / "logs" / "install-adb.jsonl"),
        lambda: (ok, "adb : Android Debug Bridge version 1.0.41")), mode=mode, target="adb")


def test_claude_rapide_accepts_the_licences_named_before_the_start(tmp_path, inst, claude_client):
    claude_client(installs.ANDROID_SDK)
    with_claude(inst, tmp_path, installs.RAPIDE)
    s = ended(inst)
    c = claude_client.made[0]
    assert c.answers == {"step": "PermissionResultAllow", "licence": True}
    assert not any(x.get("card") for x in inst.seen)
    assert s.outcome == "installé" and s.installed == ["adb (Android SDK Platform-Tools)"]
    assert s.licences == [{"name": installs.ANDROID_SDK, "source": "sdkmanager --licenses"}]
    assert s.steps[0]["text"].startswith("Rapide — installe : adb") and installs.ANDROID_SDK in s.steps[0]["text"]
    # The brief: the tool, its proof, the licences named, the licence tool.
    assert "adb version" in c.prompts[0] and installs.ANDROID_SDK in c.prompts[0] and "mcp__cockpit__licence" in c.prompts[0]
    assert os.path.isfile(tmp_path / "logs" / "install-adb.jsonl")
    assert recorded(tmp_path)[-1]["licences"] == s.licences


def test_claude_rapide_refuses_a_licence_not_named_before_the_start(tmp_path, inst, claude_client):
    claude_client("Licence d'un autre éditeur")
    with_claude(inst, tmp_path, installs.RAPIDE)
    s = ended(inst)
    assert claude_client.made[0].answers["licence"] is False
    assert s.outcome == "refusé" and "Licence refusée : Licence d'un autre éditeur" in s.message and s.licences == []


def test_claude_pas_a_pas_cards_and_a_refused_licence_stops(tmp_path, inst, claude_client):
    claude_client(installs.ANDROID_SDK)
    with_claude(inst, tmp_path, installs.PAS_A_PAS)
    c = card(inst, "étape")
    assert c["title"] == "Bash" and "winget show" in c["text"]
    inst.going().answer(c["id"], True)
    c = card(inst, "licence")
    assert c["title"] == f"Licence : {installs.ANDROID_SDK}" and "LICENSE AGREEMENT" in c["text"]
    inst.going().answer(c["id"], False)
    s = ended(inst)
    assert s.outcome == "refusé" and s.installed == [] and s.licences == []


def test_claude_pas_a_pas_a_refused_step_installs_nothing(tmp_path, inst, claude_client):
    claude_client(installs.ANDROID_SDK)
    with_claude(inst, tmp_path, installs.PAS_A_PAS)
    c = card(inst, "étape")
    inst.going().answer(c["id"], False)
    s = ended(inst)
    assert claude_client.made[0].answers == {"step": "PermissionResultDeny"}
    assert s.outcome == "échec" and s.installed == []


def test_claude_says_installed_but_the_proof_fails(tmp_path, inst, claude_client):
    claude_client(installs.ANDROID_SDK)
    inst.start("tool", "Installer adb", installs.with_claude(
        "adb", installs.RAPIDE, str(tmp_path / "w"), str(tmp_path / "logs" / "a.jsonl"),
        lambda: (False, "adb : introuvable")), mode=installs.RAPIDE)
    s = ended(inst)
    assert s.outcome == "échec" and "introuvable" in s.message


def test_path_changed_asks_for_a_restart(tmp_path, inst, claude_client, monkeypatch):
    claude_client(installs.ANDROID_SDK)
    paths = iter([{"PATH": r"C:\a"}, {"PATH": r"C:\a;C:\sdk\platform-tools"}])
    monkeypatch.setattr(installs, "REGISTRY", lambda: next(paths))
    with_claude(inst, tmp_path, installs.RAPIDE)
    s = ended(inst)
    assert s.restart is True and any("Le PATH de Windows a changé" in x["text"] for x in s.steps)


def test_one_repair_at_a_time(tmp_path, inst, claude_client):
    claude_client(installs.ANDROID_SDK)
    with_claude(inst, tmp_path, installs.PAS_A_PAS)
    card(inst)
    with pytest.raises(RuntimeError, match="une réparation à la fois"):
        inst.start("pip", "x", lambda s: None)
    inst.going().cancel()
    s = ended(inst)
    assert s.outcome == "annulé"


# ------------------------------------------------------------ the sign-ins

FAKE_LOGIN = r'''
import sys
print("Opening browser to sign in…", flush=True)
print("If the browser didn't open, visit: https://claude.com/cai/oauth/authorize?code=true&state=abc", flush=True)
sys.stdout.write("Paste code here if prompted > "); sys.stdout.flush()
code = sys.stdin.readline().strip()
if code == "bon#etat":
    print("Login successful.")
    sys.exit(0)
print("Login failed: Request failed with status code 400")
sys.exit(1)
'''


@pytest.fixture
def fake_login(tmp_path, monkeypatch):
    p = tmp_path / "login.py"
    p.write_text(FAKE_LOGIN, encoding="utf-8")
    monkeypatch.setattr(installs, "CLAUDE_LOGIN", [sys.executable, str(p)])


def test_claude_login_the_page_address_then_the_code(tmp_path, inst, fake_login):
    inst.start("claude_login", "Se connecter à Claude", installs.claude_login("claude", dict(os.environ),
                                                                             lambda: (True, "connecté")))
    s = wait(lambda: inst.going() if inst.going() and inst.going().code_wanted else None)
    assert s.url == "https://claude.com/cai/oauth/authorize?code=true&state=abc" and s.status == "waiting"
    assert installs.send_code(s, "bon#etat")
    s = ended(inst)
    assert s.outcome == "connecté" and s.message == "connecté"


def test_claude_login_with_a_wrong_code_fails_and_says_it(tmp_path, inst, fake_login):
    inst.start("claude_login", "Se connecter à Claude", installs.claude_login(
        "claude", dict(os.environ), lambda: (False, "pas connecté (claude auth status : code 1)")))
    s = wait(lambda: inst.going() if inst.going() and inst.going().code_wanted else None)
    installs.send_code(s, "faux")
    s = ended(inst)
    assert s.outcome == "échec" and "code 1" in s.message and "Login failed" in s.message


def test_github_login_then_the_dry_run_push(tmp_path, inst, monkeypatch):
    monkeypatch.setattr(installs, "GCM_LOGIN", [sys.executable, "-c", "print('ok')"])
    monkeypatch.setenv("GCM_INTERACTIVE", "never")
    seen = {}
    real = subprocess.Popen

    def popen(argv, **kw):
        seen["env"] = kw.get("env")
        return real(argv, **kw)
    monkeypatch.setattr(installs.subprocess, "Popen", popen)
    inst.start("github_login", "Se connecter à GitHub", installs.github_login(lambda: (True, "GitHub accepte")))
    s = ended(inst)
    assert s.outcome == "connecté" and "GCM_INTERACTIVE" not in seen["env"]       # allowed to open the browser
    monkeypatch.setattr(installs, "GCM_LOGIN", [sys.executable, "-c", "import sys; sys.exit(2)"])
    s = ended(inst, inst.start("github_login", "Se connecter à GitHub", installs.github_login(lambda: (False, "GitHub refuse"))))
    assert s.outcome == "échec" and "code 2" in s.message and "GitHub refuse" in s.message


def test_claude_code_install_both_modes(tmp_path, inst, monkeypatch):
    monkeypatch.setattr(installs, "CLAUDE_INSTALL", [sys.executable, "-c", "print('installé')"])
    inst.start("claude_code", "Claude Code", installs.claude_code(installs.PAS_A_PAS, None, lambda: (True, "2.1.300")),
               mode=installs.PAS_A_PAS)
    c = card(inst, "étape")
    assert c["title"] == "Installer Claude Code" and "Aucune licence à accepter" in c["text"]
    s = inst.going()
    s.answer(c["id"], False)
    assert ended(inst, s).outcome == "refusé"
    s = ended(inst, inst.start("claude_code", "Claude Code", installs.claude_code(installs.RAPIDE, None,
                                                                              lambda: (True, "2.1.300")), mode=installs.RAPIDE))
    assert s.outcome == "installé" and s.installed == ["Claude Code"] and s.restart is True


# ------------------------------------------------------------ the real CLIs, logged out, throwaway config only

def test_real_claude_auth_status_logged_out_exits_1(tmp_path):
    """Established with a throwaway CLAUDE_CONFIG_DIR — the Product
    Owner's own login is never touched: logged out, `claude auth status`
    exits 1 and says « loggedIn: false »."""
    cli = shutil.which("claude")
    if not cli:
        pytest.skip("Claude Code absent")
    env = {k: v for k, v in os.environ.items() if not (k.startswith("CLAUDE") or k.startswith("ANTHROPIC"))}
    env["CLAUDE_CONFIG_DIR"] = str(tmp_path / "claude-jetable")
    p = subprocess.run([cli, "auth", "status"], capture_output=True, text=True, env=env, timeout=60)
    assert p.returncode == 1 and json.loads(p.stdout)["loggedIn"] is False


def test_real_gcm_with_a_throwaway_store_knows_no_account(tmp_path):
    p = subprocess.run(["git", "credential-manager", "--version"], capture_output=True, text=True)
    if p.returncode:
        pytest.skip("Git Credential Manager absent")
    env = dict(os.environ, GCM_CREDENTIAL_STORE="plaintext", GCM_PLAINTEXT_STORE_PATH=str(tmp_path / "gcm-jetable"))
    p = subprocess.run(["git", "credential-manager", "github", "list"], capture_output=True, text=True, env=env,
                       timeout=60)
    assert p.returncode == 0 and p.stdout.strip() == ""
