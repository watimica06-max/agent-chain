"""« État de l'ordinateur » — cockpit 1.16.

One view of everything that must be current or present for the chain to run
right on this computer. Each item has a state, a rule — it fixes itself, it
notifies, or it blocks — what it stops when it blocks, the time it was
last checked, and the repair the cockpit offers, never PowerShell.

The probes run commands (git, the Claude Code CLI, adb, sdkmanager) and read
files; each is behind a module-level hook the tests replace (`RUN`,
`SDK_CLI`, `ANDROID`, `DEPS_CHECK`). The server builds the context — what it
already knows: the commit it started from, agent-chain's GitHub state, each
application's — and asks for every family at once (`Machine.full`) or for
the families an action needs (`Machine.before`).
"""
import json
import os
import re
import shutil
import subprocess
import threading
from datetime import datetime

import deps
import sync as sync_mod

# ------------------------------------------------------------ vocabulary

OK, WARN, BLOCK, FIXED, FIXING, OPTIONAL, SKIP, UNKNOWN = (
    "ok", "à voir", "bloque", "réparé", "se répare", "facultatif", "non concerné", "inconnu")
# What needs her: the badge counts these.
NEEDS = {WARN, BLOCK}
GOOD = {OK, FIXED, SKIP}

R_FIX, R_NOTIFY, R_BLOCK, R_OPTIONAL = "se répare seul", "signale", "bloque", "facultatif"

# What a blocking item stops.
LAUNCH, TOOL_INSTALL, PUSH, CHAIN_INSTALL, SEND, COMMIT, BATIR, DEPLOY, SAVE = (
    "launch", "tool_install", "push", "chain_install", "send", "commit", "batir", "deploy", "save")
ACTION_TEXT = {LAUNCH: "les lancements", TOOL_INSTALL: "« Installer avec Claude »", PUSH: "les push",
               CHAIN_INSTALL: "l'installation de la chaîne", SEND: "« Envoyer »", COMMIT: "tout ce qui commite",
               BATIR: "« Bâtir »", DEPLOY: "l'écran Déploiement", SAVE: "« Enregistrer »"}
# The actions that commit: identity missing stops each of them.
COMMITS = [LAUNCH, CHAIN_INSTALL, SEND, COMMIT, SAVE]

GROUPS = ["Le cockpit", "Claude Code", "git et GitHub", "Android et builds"]

TIMEOUT = 30
SDKMANAGER_TIMEOUT = 90
PUSH_TIMEOUT = 60
GITHUB_FRESH = 300.0         # a GitHub credentials check younger than this is not run again before a push


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def item(id, group, label, status, rule, detail="", stops=(), repair=None, app=None, rule_text=None):
    return {"id": id, "group": group, "label": label, "status": status, "rule": rule,
            "rule_text": rule_text or rule, "detail": detail, "stops": list(stops) if status not in GOOD else [],
            "repair": repair, "app": app, "checked_at": now_iso()}


def repair(id, label, **args):
    return {"id": id, "label": label, "args": args}


def stops_text(actions):
    return ", ".join(ACTION_TEXT.get(a, a) for a in actions)


# ------------------------------------------------------------ running a command

def system_run(argv, timeout=TIMEOUT, env=None, cwd=None):
    """(code, output) of one command, stdout then stderr. Raises
    FileNotFoundError when the program is not there, TimeoutExpired."""
    exe = argv[0]
    if os.path.isabs(exe):
        if not os.path.exists(exe):
            raise FileNotFoundError(f"{exe} introuvable")
    else:
        found = shutil.which(exe)
        if not found:
            raise FileNotFoundError(f"{exe} introuvable (PATH)")
        exe = found
    p = subprocess.run([exe, *argv[1:]], capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL,
                       env=env, cwd=cwd)
    return p.returncode, (p.stdout.decode("utf-8", "replace") + "\n" + p.stderr.decode("utf-8", "replace")).strip()


RUN = system_run


def _try(argv, timeout=TIMEOUT, env=None, cwd=None):
    """(code, text, missing): `missing` when the program is not there."""
    try:
        code, text = RUN(argv, timeout=timeout, env=env, cwd=cwd)
        return code, text, False
    except FileNotFoundError as e:
        return 127, str(e), True
    except subprocess.TimeoutExpired:
        return 124, f"pas de réponse en {timeout} s", False
    except OSError as e:
        return 126, f"{type(e).__name__}: {e}", False


def first_line(text):
    for line in (text or "").splitlines():
        if line.strip() and not re.fullmatch(r"[-=_*\s]+", line):
            return line.strip()
    return ""


# ------------------------------------------------------------ Claude Code

def find_sdk_cli():
    """The CLI the SDK runs — the bundled one first, then the system's
    (subprocess_cli.py `_find_cli`): (path or None, the SDK's minimum)."""
    minimum = None
    try:
        from claude_agent_sdk._internal.transport import subprocess_cli as sc
        minimum = getattr(sc, "MINIMUM_CLAUDE_CODE_VERSION", None)
        from claude_agent_sdk import ClaudeAgentOptions
        try:
            return sc.SubprocessCLITransport(prompt="", options=ClaudeAgentOptions())._find_cli(), minimum
        except Exception:
            return None, minimum
    except Exception:
        return shutil.which("claude"), minimum


SDK_CLI = find_sdk_cli


def version_of(text):
    m = re.search(r"(\d+\.\d+\.\d+)", text or "")
    return m.group(1) if m else ""


def claude_env():
    """The environment a Claude Code probe runs with: the cockpit's own."""
    return dict(os.environ)


def probe_claude(ctx):
    g = "Claude Code"
    cli, minimum = SDK_CLI()
    out = []
    install = repair("claude_code", "Installer Claude Code")
    if not cli:
        out.append(item("claude_cli", g, "Claude Code — le programme que le SDK lance", BLOCK, R_BLOCK,
                        "introuvable : ni celui du SDK (_bundled), ni claude.exe sur cet ordinateur",
                        [LAUNCH, TOOL_INSTALL], install, rule_text="bloque : " + stops_text([LAUNCH])))
        out.append(item("claude_login", g, "Claude Code — connecté", UNKNOWN, R_BLOCK,
                        "Claude Code d'abord : rien à interroger", [LAUNCH, TOOL_INSTALL],
                        rule_text="bloque : chaque lancement, « Installer avec Claude »"))
        return out
    where = "celui du SDK" if "_bundled" in cli else "celui de l'ordinateur"
    code, text, missing = _try([cli, "--version"], env=claude_env())
    v = version_of(text)
    if code or not v:
        out.append(item("claude_cli", g, "Claude Code — le programme que le SDK lance", BLOCK, R_BLOCK,
                        f"{cli} ne répond pas : {first_line(text) or f'code {code}'}", [LAUNCH, TOOL_INSTALL],
                        install, rule_text="bloque : " + stops_text([LAUNCH])))
    elif minimum and deps._cmp(v, minimum) < 0:
        out.append(item("claude_cli", g, "Claude Code — le programme que le SDK lance", BLOCK, R_BLOCK,
                        f"{v}, sous le minimum du SDK ({minimum}) — {cli}", [LAUNCH, TOOL_INSTALL],
                        repair("claude_code", "Mettre à jour Claude Code"), rule_text="bloque : " + stops_text([LAUNCH])))
    else:
        out.append(item("claude_cli", g, "Claude Code — le programme que le SDK lance", OK, R_BLOCK,
                        f"{v} ({where}) — minimum du SDK : {minimum or '?'} — {cli}",
                        rule_text="bloque : " + stops_text([LAUNCH])))
    code, text, missing = _try([cli, "auth", "status"], env=claude_env())
    info = {}
    try:
        info = json.loads(text[text.index("{"):text.rindex("}") + 1]) if "{" in text else {}
    except ValueError:
        info = {}
    login = repair("claude_login", "Se connecter à Claude")
    rt = "bloque : chaque lancement, « Installer avec Claude »"
    if code == 0 and info.get("loggedIn") is not False:
        how = info.get("authMethod") or "?"
        sub = info.get("subscriptionType")
        out.append(item("claude_login", g, "Claude Code — connecté", OK, R_BLOCK,
                        f"connecté ({how}{', ' + sub if sub else ''})", rule_text=rt))
    elif code == 1 or info.get("loggedIn") is False:
        out.append(item("claude_login", g, "Claude Code — connecté", BLOCK, R_BLOCK,
                        "Claude Code n'est pas connecté sur cet ordinateur (claude auth status : code 1)",
                        [LAUNCH, TOOL_INSTALL], login, rule_text=rt))
    else:
        out.append(item("claude_login", g, "Claude Code — connecté", UNKNOWN, R_BLOCK,
                        f"claude auth status ne répond pas : {first_line(text) or f'code {code}'}", [], login, rule_text=rt))
    return out


# ------------------------------------------------------------ git

def git_run(root, *args, timeout=TIMEOUT):
    return _try(["git", "-C", root, *args], timeout=timeout, env=sync_mod.env())


def probe_identity(ctx):
    g = "git et GitHub"
    root = ctx["chain_root"]
    rt = "bloque : " + stops_text([COMMIT])
    code, text, missing = _try(["git", "--version"])
    if missing or code:
        return [item("git", g, "git", BLOCK, R_BLOCK, f"git ne répond pas : {first_line(text)}", COMMITS + [PUSH],
                     repair("tool", "Installer avec Claude", tool="git"), rule_text=rt),
                item("git_identity", g, "git — identité des commits", UNKNOWN, R_BLOCK, "git d'abord", COMMITS,
                     rule_text=rt)]
    out = [item("git", g, "git", OK, R_BLOCK, first_line(text), rule_text=rt)]
    name = git_run(root, "config", "--get", "user.name")
    mail = git_run(root, "config", "--get", "user.email")
    ident = git_run(root, "var", "GIT_AUTHOR_IDENT")
    fix = repair("identity", "Régler")
    if name[0] == 0 and mail[0] == 0 and name[1].strip() and mail[1].strip():
        out.append(item("git_identity", g, "git — identité des commits", OK, R_BLOCK,
                        f"{name[1].strip()} <{mail[1].strip()}>", rule_text=rt))
    elif ident[0] == 0 and ident[1].strip():
        who = re.sub(r"\s+\d+\s+[+-]\d{4}\s*$", "", ident[1].strip().splitlines()[0])
        out.append(item("git_identity", g, "git — identité des commits", WARN, R_BLOCK,
                        f"non réglée : git la devine — {who} ; « Régler » la fixe dans la configuration globale",
                        [], fix, rule_text=rt))
    else:
        out.append(item("git_identity", g, "git — identité des commits", BLOCK, R_BLOCK,
                        "aucune : git refuse de commiter sans nom ni e-mail (user.name, user.email)", COMMITS, fix,
                        rule_text=rt))
    return out


def probe_github(ctx):
    """Git Credential Manager, the GitHub accounts it holds, then a push
    that sends nothing (`git push --dry-run --porcelain`) on agent-chain:
    GitHub reached, and credentials it accepts."""
    g = "git et GitHub"
    root = ctx["chain_root"]
    out = []
    login = repair("github_login", "Se connecter à GitHub")
    code, text, missing = _try(["git", "credential-manager", "--version"])
    gcm = not missing and code == 0
    out.append(item("gcm", g, "Git Credential Manager", OK if gcm else WARN, R_NOTIFY,
                    first_line(text) if gcm else "absent : git ne garde aucun identifiant GitHub sans lui",
                    repair=None if gcm else repair("tool", "Installer avec Claude", tool="git"),
                    rule_text="signale"))
    accounts = []
    if gcm:
        c, t, _ = _try(["git", "credential-manager", "github", "list"])
        accounts = [x.strip() for x in t.splitlines() if x.strip()] if c == 0 else []
    rt = "bloque : " + stops_text([PUSH, CHAIN_INSTALL, SEND]) + " ; signale pour un lancement"
    reach_rt = "signale ; bloque " + stops_text([CHAIN_INSTALL]) + " tant qu'il dure"
    has_remote = git_run(root, "remote")
    if has_remote[0] != 0 or not has_remote[1].strip():
        out.append(item("github", g, "GitHub — identifiants", SKIP, R_BLOCK, "agent-chain n'a pas de dépôt distant",
                        rule_text=rt))
        out.append(item("github_reach", g, "GitHub — joignable", SKIP, R_NOTIFY, "rien à joindre", rule_text=reach_rt))
        return out
    code, text, _ = git_run(root, "push", "--dry-run", "--porcelain", timeout=PUSH_TIMEOUT)
    who = f" — compte : {', '.join(accounts)}" if accounts else ""
    if code == 0 or sync_mod._REJECTED.search(text or ""):
        out.append(item("github", g, "GitHub — identifiants", OK, R_BLOCK,
                        "acceptés (git push --dry-run sur agent-chain)" + who, rule_text=rt))
        out.append(item("github_reach", g, "GitHub — joignable", OK, R_NOTIFY, "répond", rule_text=reach_rt))
    elif sync_mod.credentials(text):
        out.append(item("github", g, "GitHub — identifiants", BLOCK, R_BLOCK,
                        "aucun identifiant GitHub utilisable sur cet ordinateur"
                        + (f" (Git Credential Manager connaît : {', '.join(accounts)})" if accounts else ""),
                        [PUSH, CHAIN_INSTALL, SEND], login, rule_text=rt))
        out.append(item("github_reach", g, "GitHub — joignable", OK, R_NOTIFY, "répond (il refuse les identifiants)",
                        rule_text=reach_rt))
    else:
        out.append(item("github", g, "GitHub — identifiants", UNKNOWN, R_BLOCK,
                        "non vérifiés : GitHub ne répond pas" + who, rule_text=rt))
        out.append(item("github_reach", g, "GitHub — joignable", WARN, R_NOTIFY,
                        sync_mod.explain(text) or "pas de réponse", [CHAIN_INSTALL], rule_text=reach_rt))
    return out


def longpaths_item(id, group, label, folder, app=None):
    """core.longpaths in the repository's own config — set when it is not
    (the rule: it fixes itself)."""
    if not folder or not os.path.isdir(folder):
        return item(id, group, label, SKIP, R_FIX, "dossier introuvable", app=app)
    if not sync_mod.git(folder, "rev-parse", "--git-dir").ok:
        return item(id, group, label, SKIP, R_FIX, "pas un dépôt git", app=app)
    v = sync_mod.long_paths(folder)
    if v:
        return item(id, group, label, OK, R_FIX, "core.longpaths=true", app=app)
    try:
        sync_mod.set_long_paths(folder)
    except sync_mod.SyncError as e:
        return item(id, group, label, WARN, R_FIX, f"absent, et non réglé : {e}", app=app,
                    repair=repair("longpaths", "Régler", folder=folder))
    return item(id, group, label, FIXED, R_FIX,
                f"core.longpaths={'false' if v is False else 'absent'} → réglé à true à l'instant", app=app)


def probe_longpaths(ctx):
    out = [longpaths_item("longpaths", "git et GitHub", "agent-chain — chemins longs (core.longpaths)",
                          ctx["chain_root"])]
    for a in ctx.get("apps") or []:
        out.append(longpaths_item(f"app:{key(a['folder'])}:longpaths", a["name"], "chemins longs (core.longpaths)",
                                  a["folder"], app=a["folder"]))
    return out


# ------------------------------------------------------------ Android and builds

def sdk_folder():
    """(folder or None, what was looked at): ANDROID_HOME, ANDROID_SDK_ROOT,
    then %LOCALAPPDATA%\\Android\\Sdk — the deploy adapter's order."""
    from adapters import android
    roots = android.sdk_roots()
    for r in roots:
        if os.path.isdir(r):
            return r, roots
    return None, roots


def find_sdkmanager():
    exe = shutil.which("sdkmanager")
    if exe:
        return exe
    root, _ = sdk_folder()
    if not root:
        return None
    name = "sdkmanager.bat" if os.name == "nt" else "sdkmanager"
    base = os.path.join(root, "cmdline-tools")
    cands = []
    if os.path.isdir(base):
        subs = sorted(os.listdir(base), key=lambda s: (s != "latest", [-int(x) if x.isdigit() else 0 for x in s.split(".")]))
        cands += [os.path.join(base, s, "bin", name) for s in subs]
    cands.append(os.path.join(root, "tools", "bin", name))
    return next((c for c in cands if os.path.isfile(c)), None)


def android_lookup():
    """Where each Android tool is: {adb, sdkmanager, emulator, scrcpy, sdk}."""
    from adapters import android
    sdk, roots = sdk_folder()
    return {"adb": android.adb_argv(), "sdkmanager": [p] if (p := find_sdkmanager()) else None,
            "emulator": android.emulator_argv(), "scrcpy": android.scrcpy_argv(), "sdk": sdk, "roots": roots}


ANDROID = android_lookup


def android_apps(apps):
    """The applications that build for Android: a Gradle wrapper, a Flutter
    project, or an android/ folder."""
    out = []
    for a in apps or []:
        f = a.get("folder") or ""
        if any(os.path.exists(os.path.join(f, n)) for n in ("gradlew.bat", "gradlew", "pubspec.yaml", "android")):
            out.append(a)
    return out


def probe_android(ctx):
    g = "Android et builds"
    rt = "signale ; bloque " + stops_text([BATIR, DEPLOY])
    out = []
    # Java, Gradle, Flutter: the open application's diagnostic, as today.
    diag = ctx.get("diagnostic") or {}
    by = {r["id"]: r for r in diag.get("results") or []}
    app_name = ctx.get("app_name") or "l'application ouverte"
    for tid, label, tool in (("java", "Java", "java"), ("gradle", "Gradle", None), ("flutter", "Flutter", "flutter")):
        r = by.get(tid)
        if not r:
            out.append(item(tid, g, label, UNKNOWN if diag else SKIP, R_NOTIFY,
                            "pas encore vérifié" if diag else "aucune application ouverte", rule_text=rt))
            continue
        if r["status"] == "skip":
            out.append(item(tid, g, label, SKIP, R_NOTIFY, f"non concerné — {app_name}", rule_text=rt))
        elif r["status"] == "ok":
            out.append(item(tid, g, label, OK, R_NOTIFY, f"{r['detail']} — {app_name}", rule_text=rt))
        else:
            out.append(item(tid, g, label, WARN, R_NOTIFY, f"{r['detail']} — {app_name}", [BATIR, DEPLOY],
                            repair("tool", "Installer avec Claude", tool=tool) if tool else None, rule_text=rt))
    concerned = android_apps(ctx.get("apps"))
    look = ANDROID()
    none = "aucune application Android dans la liste"
    # adb
    if look.get("adb"):
        code, text, _ = _try([*look["adb"], "version"])
        out.append(item("adb", g, "adb", OK if code == 0 else WARN, R_NOTIFY,
                        f"{first_line(text)} — {look['adb'][0]}" if code == 0 else f"{look['adb'][0]} ne répond pas : {first_line(text)}",
                        [BATIR, DEPLOY], repair("tool", "Installer avec Claude", tool="adb"), rule_text=rt))
    else:
        out.append(item("adb", g, "adb", WARN if concerned else SKIP, R_NOTIFY,
                        "introuvable : ni dans le PATH, ni dans le SDK (platform-tools)" if concerned else none,
                        [BATIR, DEPLOY], repair("tool", "Installer avec Claude", tool="adb"), rule_text=rt))
    # sdkmanager
    if look.get("sdkmanager"):
        code, text, _ = _try([*look["sdkmanager"], "--version"], timeout=SDKMANAGER_TIMEOUT)
        out.append(item("sdkmanager", g, "sdkmanager", OK if code == 0 else WARN, R_NOTIFY,
                        f"{first_line(text)} — {look['sdkmanager'][0]}" if code == 0
                        else f"{look['sdkmanager'][0]} ne répond pas : {first_line(text) or f'code {code}'}",
                        [BATIR, DEPLOY], repair("tool", "Installer avec Claude", tool="sdkmanager"), rule_text=rt))
    else:
        out.append(item("sdkmanager", g, "sdkmanager", WARN if concerned else SKIP, R_NOTIFY,
                        "introuvable : ni dans le PATH, ni dans le SDK (cmdline-tools)" if concerned else none,
                        [BATIR, DEPLOY], repair("tool", "Installer avec Claude", tool="sdkmanager"), rule_text=rt))
    # The SDK folder
    env_home = (os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT") or "").strip().strip('"')
    if look.get("sdk"):
        said = f"{look['sdk']}" + ("" if env_home else " — ANDROID_HOME n'est pas défini, le dossier par défaut est pris")
        out.append(item("android_sdk", g, "SDK Android (ANDROID_HOME)", OK, R_NOTIFY, said, rule_text=rt))
    else:
        out.append(item("android_sdk", g, "SDK Android (ANDROID_HOME)", WARN if concerned else SKIP, R_NOTIFY,
                        (f"ANDROID_HOME pointe vers {env_home}, qui n'existe pas" if env_home
                         else "introuvable : " + ", ".join(look.get("roots") or [])) if concerned else none,
                        [BATIR, DEPLOY], repair("tool", "Installer avec Claude", tool="android_sdk"), rule_text=rt))
    # The optional ones: never an alert.
    for tid, label, flag in (("emulator", "Émulateur Android", "-version"), ("scrcpy", "scrcpy", "--version")):
        argv = look.get(tid)
        if not argv:
            out.append(item(tid, g, label, OPTIONAL, R_OPTIONAL, "non trouvé — facultatif",
                            repair=repair("tool", "Installer avec Claude", tool=tid) if concerned else None,
                            rule_text="facultatif"))
            continue
        code, text, _ = _try([*argv, flag])
        out.append(item(tid, g, label, OK if code == 0 else OPTIONAL, R_OPTIONAL,
                        f"{first_line(text)} — {argv[0]}" if code == 0 else f"trouvé ({argv[0]}), sans réponse",
                        rule_text="facultatif"))
    return out


# ------------------------------------------------------------ the cockpit itself

def probe_cockpit(ctx):
    g = "Le cockpit"
    out = []
    started, head = ctx.get("started"), ctx.get("head")
    restart = ctx.get("restart") or {}
    rt = "se répare seul : redémarre quand rien ne tourne ; signale pendant un run"
    again = repair("restart", "Redémarrer le cockpit")
    if not started or not head or started == head:
        out.append(item("server", g, "Le serveur du cockpit et le code sur le disque", OK, R_FIX,
                        f"le serveur tourne sur {(head or started or '?')[:7]}, le code sur le disque", rule_text=rt))
    elif restart.get("error"):
        out.append(item("server", g, "Le serveur du cockpit et le code sur le disque", WARN, R_FIX,
                        f"le serveur tourne sur {started[:7]}, le disque est à {head[:7]} — le redémarrage a échoué : "
                        f"{restart['error']}", repair=again, rule_text=rt))
    elif ctx.get("busy"):
        out.append(item("server", g, "Le serveur du cockpit et le code sur le disque", WARN, R_FIX,
                        f"le serveur tourne sur {started[:7]}, le disque est à {head[:7]} — il redémarre de lui-même "
                        f"après {ctx['busy']}", repair=again, rule_text=rt))
    else:
        out.append(item("server", g, "Le serveur du cockpit et le code sur le disque", FIXING, R_FIX,
                        f"le serveur tourne sur {started[:7]}, le disque est à {head[:7]} — il redémarre de lui-même",
                        repair=again, rule_text=rt))
    st = ctx.get("chain_sync") or {}
    rt2 = "se répare seul : récupéré au démarrage ; signale « pas encore en service »"
    s = st.get("state")
    label = "agent-chain face à GitHub"
    if s is None:
        out.append(item("chain", g, label, UNKNOWN, R_FIX, st.get("detail") or "pas encore vérifié", rule_text=rt2))
    elif s == sync_mod.UP_TO_DATE:
        pending = started and head and started != head
        out.append(item("chain", g, label, WARN if pending else OK, R_FIX,
                        "à jour — la version récupérée n'est pas encore en service" if pending else "à jour",
                        repair=again if pending else None, rule_text=rt2))
    elif s == sync_mod.BEHIND:
        out.append(item("chain", g, label, FIXING, R_FIX, st.get("summary") or s, rule_text=rt2,
                        repair=repair("cockpit_update", "Mettre à jour le cockpit")))
    elif s == sync_mod.DIVERGED:
        out.append(item("chain", g, label, WARN, R_FIX, st.get("summary") or s, rule_text=rt2,
                        repair=repair("reconcile", "Réconcilier", chain=True)))
    elif s == sync_mod.AHEAD or (s == sync_mod.OFFLINE and st.get("ahead")):
        out.append(item("chain", g, label, WARN, R_FIX, st.get("summary") or s, rule_text=rt2,
                        repair=repair("push", "Envoyer", chain=True)))
    else:
        out.append(item("chain", g, label, WARN if s == sync_mod.OFFLINE else SKIP, R_FIX, st.get("summary") or s,
                        rule_text=rt2))
    res = DEPS_CHECK()
    rt3 = "se répare seul : pip au démarrage ; signale un échec"
    pip_state = ctx.get("pip") or {}
    if res["ok"]:
        detail = f"{res['count']} paquets de requirements.txt, chacun à une version acceptée"
        if pip_state.get("restart"):
            out.append(item("python", g, "Dépendances Python", FIXING, R_FIX,
                            detail + " — installées : prises en compte au redémarrage", repair=again, rule_text=rt3))
        else:
            out.append(item("python", g, "Dépendances Python", OK, R_FIX, detail, rule_text=rt3))
    else:
        out.append(item("python", g, "Dépendances Python", FIXING if pip_state.get("going") else WARN, R_FIX,
                        "manquantes : " + deps.missing_text(res)
                        + (f" — l'installation a échoué : {pip_state['error']}" if pip_state.get("error") else ""),
                        repair=repair("pip", "Installer les dépendances"), rule_text=rt3))
    return out


DEPS_CHECK = deps.check


# ------------------------------------------------------------ each application

def key(folder):
    return os.path.normcase(os.path.abspath(folder or ""))


def conventions_file(folder):
    return os.path.isfile(os.path.join(folder, "docs", "TECHNICAL_CONVENTIONS.md"))


def probe_apps(ctx):
    """Per application: GitHub, the chain installed, BUILD_REPORT against
    the conventions — from what the server already knows (`apps`)."""
    out = []
    for a in ctx.get("apps") or []:
        f, g, k = a["folder"], a["name"], key(a["folder"])
        if not os.path.isdir(f):
            out.append(item(f"app:{k}:github", g, "dossier", WARN, R_NOTIFY, f"introuvable : {f}", app=f))
            continue
        st = a.get("sync") or {}
        s = st.get("state")
        if s is None:
            out.append(item(f"app:{k}:github", g, "GitHub", UNKNOWN, R_NOTIFY, st.get("detail") or "pas encore vérifié",
                            app=f))
        elif s == sync_mod.UP_TO_DATE:
            out.append(item(f"app:{k}:github", g, "GitHub", OK, R_NOTIFY, "à jour", app=f))
        elif s == sync_mod.DIVERGED:
            out.append(item(f"app:{k}:github", g, "GitHub", BLOCK, R_BLOCK, st.get("summary") or s,
                            [LAUNCH, CHAIN_INSTALL, SAVE], repair("reconcile", "Réconcilier", folder=f), app=f,
                            rule_text="bloque : " + stops_text([LAUNCH, CHAIN_INSTALL, SAVE])))
        elif s == sync_mod.AHEAD or (s == sync_mod.OFFLINE and st.get("ahead")):
            out.append(item(f"app:{k}:github", g, "GitHub", WARN, R_NOTIFY, st.get("summary") or s,
                            repair=repair("push", "Envoyer", folder=f), app=f,
                            rule_text="signale, toujours visible, jamais en vert"))
        elif s == sync_mod.BEHIND:
            out.append(item(f"app:{k}:github", g, "GitHub", WARN, R_NOTIFY, st.get("summary") or s,
                            repair=repair("pull", "Récupérer", folder=f), app=f,
                            rule_text="signale ; récupéré avant un lancement"))
        elif s == sync_mod.OFFLINE:
            out.append(item(f"app:{k}:github", g, "GitHub", WARN, R_NOTIFY, st.get("summary") or s, [CHAIN_INSTALL],
                            app=f, rule_text="signale ; bloque " + stops_text([CHAIN_INSTALL]) + " tant qu'il dure"))
        else:
            out.append(item(f"app:{k}:github", g, "GitHub", SKIP, R_NOTIFY, st.get("summary") or s, app=f))
        ch = a.get("chain") or {}
        cs = ch.get("state")
        rt = "signale ; demandé au lancement"
        if cs == "à jour" or cs == "plus récente":
            out.append(item(f"app:{k}:chain", g, "La chaîne installée", OK, R_NOTIFY, ch.get("summary") or cs, app=f,
                            rule_text=rt))
        elif cs:
            out.append(item(f"app:{k}:chain", g, "La chaîne installée", WARN, R_NOTIFY, ch.get("summary") or cs, app=f,
                            repair=repair("chain_install", "Installer la chaîne", folder=f), rule_text=rt))
        else:
            out.append(item(f"app:{k}:chain", g, "La chaîne installée", UNKNOWN, R_NOTIFY,
                            ch.get("summary") or "état inconnu", app=f, rule_text=rt))
        rt = "signale ; « Bâtir » proposé à nouveau"
        if not conventions_file(f):
            out.append(item(f"app:{k}:build", g, "BUILD_REPORT et les conventions", SKIP, R_NOTIFY,
                            "pas encore de conventions", app=f, rule_text=rt))
        else:
            rep, conv = a.get("build"), a.get("conventions")
            if rep is None:
                out.append(item(f"app:{k}:build", g, "BUILD_REPORT et les conventions", WARN, R_NOTIFY,
                                "docs/BUILD_REPORT.md absent : le projet n'a jamais été bâti", app=f, rule_text=rt))
            elif rep.get("commit") and conv and rep["commit"].lower() == conv.lower():
                out.append(item(f"app:{k}:build", g, "BUILD_REPORT et les conventions", OK, R_NOTIFY,
                                f"bâti sur les conventions en vigueur ({conv[:7]})", app=f, rule_text=rt))
            else:
                out.append(item(f"app:{k}:build", g, "BUILD_REPORT et les conventions", WARN, R_NOTIFY,
                                f"bâti sur {(rep.get('commit') or '?')[:7]}, les conventions ont changé depuis"
                                + (f" ({conv[:7]})" if conv else "") + " : « Bâtir » est proposé à nouveau",
                                app=f, rule_text=rt))
    return out


# ------------------------------------------------------------ the whole view

FAMILIES = {"cockpit": probe_cockpit, "claude": probe_claude, "identity": probe_identity, "github": probe_github,
            "longpaths": probe_longpaths, "android": probe_android, "apps": probe_apps}
ORDER = ["cockpit", "claude", "identity", "github", "longpaths", "android", "apps"]
# What each action checks again before it goes: what blocks it.
BEFORE = {LAUNCH: ["claude", "identity"], TOOL_INSTALL: ["claude"], PUSH: ["identity", "github"],
          SEND: ["identity", "github"], CHAIN_INSTALL: ["identity", "github"], COMMIT: ["identity"],
          SAVE: ["identity"], BATIR: ["android"], DEPLOY: ["android"]}


class Machine:
    """The last result of each family; one check at a time."""

    def __init__(self):
        self.families = {}           # family -> {"at", "items"}
        self.at = None               # the last full check
        self.running = False
        self._lock = threading.Lock()
        self._guard = threading.Lock()

    def _family(self, fam, ctx):
        try:
            items = FAMILIES[fam](ctx)
        except Exception as e:       # said on its line, never raised
            items = [item(f"{fam}:erreur", "Le cockpit", f"Vérification « {fam} »", UNKNOWN, R_NOTIFY,
                          f"la vérification a échoué : {type(e).__name__}: {e}")]
        with self._guard:
            self.families[fam] = {"at": now_iso(), "items": items}
        return items

    def full(self, ctx):
        with self._lock:
            self.running = True
            try:
                for fam in ORDER:
                    self._family(fam, ctx)
                self.at = now_iso()
            finally:
                self.running = False
        return self.report()

    def refresh(self, families, ctx):
        with self._lock:
            for fam in families:
                self._family(fam, ctx)
        return self.report()

    def fresh(self, fam, seconds):
        f = self.families.get(fam)
        if not f:
            return False
        try:
            return (datetime.now() - datetime.fromisoformat(f["at"])).total_seconds() < seconds
        except ValueError:
            return False

    def before(self, action, ctx, app=None):
        """The families this action needs, checked again — GitHub's only
        when its last check is older than GITHUB_FRESH —; then what blocks
        it."""
        fams = [f for f in BEFORE.get(action, []) if not (f == "github" and self.fresh("github", GITHUB_FRESH))]
        if fams:
            self.refresh(fams, ctx)
        return self.blockers(action, app)

    def items(self):
        with self._guard:
            fams = dict(self.families)
        return [x for fam in ORDER for x in (fams.get(fam) or {}).get("items", [])]

    def blockers(self, action, app=None):
        """The items that stop `action` now — an application's own only for
        that application."""
        out = []
        for x in self.items():
            if action not in x.get("stops", []):
                continue
            if x.get("app") and (not app or key(x["app"]) != key(app)):
                continue
            out.append(x)
        return out

    def report(self):
        items = self.items()
        block = [x for x in items if x["status"] == BLOCK]
        warn = [x for x in items if x["status"] == WARN]
        return {"at": self.at, "running": self.running, "items": items, "groups": GROUPS,
                "summary": summary(block, warn), "now": now_iso()}


def summary(block, warn):
    """One line for the badge: what blocks, else what needs her."""
    if block:
        first = block[0]
        return {"level": "block", "count": len(block) + len(warn), "block": len(block), "warn": len(warn),
                "text": (f"{first['label']} — {first['detail']}" if len(block) == 1
                         else f"{len(block)} points bloquent") + (f" · {len(warn)} à voir" if warn else "")}
    if warn:
        return {"level": "warn", "count": len(warn), "block": 0, "warn": len(warn),
                "text": f"{warn[0]['label']} — {warn[0]['detail']}" if len(warn) == 1 else f"{len(warn)} points à voir"}
    return {"level": "ok", "count": 0, "block": 0, "warn": 0, "text": "Tout est en ordre"}


def refusal(blockers):
    """The error a refused action returns: what blocks it, and its repair."""
    b = blockers[0]
    more = f" (et {len(blockers) - 1} autre{'s' if len(blockers) > 2 else ''})" if len(blockers) > 1 else ""
    return {"error": f"{b['label']} : {b['detail']}{more} — à réparer dans Paramètres → État de l'ordinateur",
            "machine": blockers}
