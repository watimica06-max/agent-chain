"""Les enquêtes — cockpit 1.21.

The Product Owner asks a question, in French, about the application or about
the chain and its cockpit; a model reads — and only reads — and answers, for
a reader who is not technical. The answer becomes a report, kept in the
repository it concerns: `docs/enquetes/<date>-<subject>.md`, committed and
pushed by the cockpit.

§1 — read-only, enforced by the cockpit, never asked of the model:
- the tools the model is given: Read, Grep, Glob and Bash — no Write, Edit,
  NotebookEdit, no web tool, no agent, no MCP server, no setting loaded;
- every tool call goes through `gate`, twice: the PreToolUse hook, which the
  CLI runs before any tool whatever the permission mode, and the permission
  callback. A shell command passes only when each of its simple commands is
  one of READ_COMMANDS, with none of the options that write, run a program
  or wait for ever; anything else is refused, and the refusal is kept in the
  report.

§4 — what follows a report: for the chain or the cockpit, a correction
prompt, written by a second call, saved beside the report and marked « à
relire » — never launched from the cockpit; for the application, a bug entry
in the format the Diagnostiqueur reads (.claude/agents/diagnostiqueur.md
« What a gap looks like »: a `G<n>` that opens the gap, what is wrong, what
it should be), written only once she confirmed it.
"""
import asyncio
import json
import os
import re
import sys
import tempfile
import unicodedata
import uuid
from datetime import datetime

import runner as runner_mod
import stats as stats_mod
import usage as usage_mod

KIND = "enquête"
COMMAND = "(enquête)"
FOLDER = "docs/enquetes"
APP, CHAIN = "application", "chaine"
TARGETS = (APP, CHAIN)
# "" — the model the chain's commands run with: none passed, the CLI's own.
MODELS = ("", "opus", "sonnet", "haiku")
TIMEOUT = 45 * 60.0
ASK_TIMEOUT = 5 * 60.0
MAX_QUESTION = 8000
MESSAGE = "enquete: {subject}"
PROMPT_MESSAGE = "enquete: prompt de correction — {subject}"
PROMPT_SUFFIX = "-prompt.md"
PROMPT_MARK = "À relire dans la conversation de conception avant de lancer"
STEPS_KEPT = 40
# Where a second call runs: it reads nothing, it is given everything.
SCRATCH = os.path.join(tempfile.gettempdir(), "cockpit-enquete")


def default_model():
    """The model the chain's commands run with when none is passed: the one
    Claude Code's user settings name — said on the form, never passed."""
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
    try:
        with open(os.path.join(base, "settings.json"), encoding="utf-8") as f:
            m = json.load(f).get("model")
        return m if isinstance(m, str) and m.strip() else None
    except (OSError, ValueError, AttributeError):
        return None

# ------------------------------------------------------------------ §1 read-only

READ_TOOLS = ("Read", "Grep", "Glob")
SHELL = "Bash"
TOOLS = [*READ_TOOLS, SHELL]
# Named as well, so that no setting and no default can bring one back.
NEVER = ["Write", "Edit", "MultiEdit", "NotebookEdit", "WebFetch", "WebSearch", "Agent", "Task", "PowerShell",
         "TodoWrite", "KillShell", "BashOutput", "SlashCommand", "Skill"]

# The shell commands allowed — the list the Product Owner reads (LISEZMOI).
GIT_READS = ("log", "show", "diff", "status", "blame", "grep")
READ_COMMANDS = {
    "git": "git log, git show, git diff, git status, git blame, git grep — lire l'historique",
    "ls": "lister un dossier",
    "find": "chercher des fichiers par leur nom (sans -delete, -exec, -ok, -fprint, -fls)",
    "cat": "lire un fichier",
    "head": "lire le début d'un fichier",
    "tail": "lire la fin d'un fichier (sans -f : rien qui attende)",
    "wc": "compter les lignes",
    "stat": "la taille et la date d'un fichier",
    "grep": "chercher dans les fichiers", "egrep": "chercher dans les fichiers", "fgrep": "chercher dans les fichiers",
    "rg": "chercher dans les fichiers (sans --pre)",
    "sort": "trier ce qu'une autre commande lit (sans -o)",
    "uniq": "dédoublonner ce qu'une autre commande lit (sans fichier de sortie)",
    "cut": "découper des colonnes",
    "pwd": "le dossier courant", "cd": "changer de dossier",
    "basename": "le nom d'un chemin", "dirname": "le dossier d'un chemin", "realpath": "le chemin complet",
}
# Between simple commands: a pipe, and the three ways to chain them.
SEPARATORS = ("|", "||", "&&", ";")
# The only redirections: an error output thrown away, or joined to the output.
_REDIR = re.compile(r"(?:2>&1|[12]?>\s*/dev/null)(?=\s|$|[|;&])")


class Refused(Exception):
    """A tool call the gate refuses — its reason, in French."""


def _words(command):
    """The shell line as simple commands: [[word, ...], ...]. Refused: what
    substitutes a command or a variable, a redirection to a file, a
    background job, a subshell, several lines."""
    out, cur, word, i, n = [], [], None, 0, len(command)

    def flush():
        nonlocal word
        if word is not None:
            cur.append(word)
            word = None
    while i < n:
        c = command[i]
        if c in "\r\n":
            raise Refused("une commande sur plusieurs lignes")
        if c.isspace():
            flush()
            i += 1
            continue
        if word is None:
            m = _REDIR.match(command, i)
            if m:
                i = m.end()
                continue
        if c == "'":
            j = command.find("'", i + 1)
            if j < 0:
                raise Refused("une apostrophe non fermée")
            word = (word or "") + command[i + 1:j]
            i = j + 1
            continue
        if c == '"':
            j, buf = i + 1, ""
            while j < n and command[j] != '"':
                if command[j] in "$`":
                    raise Refused("une substitution ($ ou `) : rien n'est lancé à l'intérieur d'une autre commande")
                if command[j] == "\\" and j + 1 < n:
                    buf += command[j + 1]
                    j += 2
                    continue
                buf += command[j]
                j += 1
            if j >= n:
                raise Refused("un guillemet non fermé")
            word = (word or "") + buf
            i = j + 1
            continue
        if c in "$`":
            raise Refused("une substitution ($ ou `) : rien n'est lancé à l'intérieur d'une autre commande")
        if c == "\\":
            word = (word or "") + (command[i + 1] if i + 1 < n else "")
            i += 2
            continue
        if c in "|&;":
            flush()
            op = command[i:i + 2] if command[i:i + 2] in ("||", "&&") else c
            if op == "&":
                raise Refused("une commande en arrière-plan (&)")
            if not cur:
                raise Refused(f"« {op} » sans commande avant")
            out.append(cur)
            cur = []
            i += len(op)
            continue
        if c in "<>":
            raise Refused("une redirection vers un fichier (> ou <) : rien ne s'écrit")
        if c in "(){}":
            raise Refused(f"« {c} » : ni sous-commande ni bloc")
        word = (word or "") + c
        i += 1
    flush()
    if cur:
        out.append(cur)
    elif out:
        raise Refused("une commande qui finit sur un séparateur")
    if not out:
        raise Refused("une commande vide")
    return out


def _short_has(words, letter):
    """A short option cluster (`-uo`) that holds `letter`."""
    return any(w.startswith("-") and not w.startswith("--") and letter in w[1:] for w in words)


def _check_git(args):
    i = 0
    while i < len(args) and args[i].startswith("-"):
        a = args[i]
        if a == "--no-pager":
            i += 1
            continue
        if a == "-C" and i + 1 < len(args):
            i += 2
            continue
        raise Refused(f"git {a} : seuls --no-pager et -C <dossier> passent avant la sous-commande")
    if i >= len(args):
        raise Refused("git sans sous-commande")
    sub, rest = args[i], args[i + 1:]
    if sub not in GIT_READS:
        raise Refused(f"git {sub} : seuls git {', git '.join(GIT_READS)} lisent sans rien changer")
    for w in rest:
        if w == "--output" or w.startswith("--output="):
            raise Refused(f"git {sub} --output écrit un fichier")
        if w == "--ext-diff":
            raise Refused(f"git {sub} --ext-diff lance un programme")
        if sub == "grep" and (w.startswith("--open-files-in-pager") or (w.startswith("-O") and not w.startswith("--"))):
            raise Refused("git grep -O lance un programme")


def _check_simple(words):
    name, args = words[0], words[1:]
    if "=" in name:
        raise Refused(f"« {name} » : aucune variable d'environnement posée")
    if name not in READ_COMMANDS:
        raise Refused(f"« {name} » n'est pas une commande de lecture")
    if name == "git":
        _check_git(args)
    elif name == "find":
        bad = [w for w in args if w in ("-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprint", "-fprint0",
                                         "-fprintf", "-fls")]
        if bad:
            raise Refused(f"find {bad[0]} écrit, supprime ou lance un programme")
    elif name == "rg":
        if any(w == "--pre" or w.startswith("--pre=") for w in args):
            raise Refused("rg --pre lance un programme")
    elif name == "sort":
        if any(w == "--output" or w.startswith("--output=") for w in args) or _short_has(args, "o"):
            raise Refused("sort -o écrit un fichier")
    elif name == "uniq":
        if len([w for w in args if not w.startswith("-")]) > 1:
            raise Refused("uniq avec un fichier de sortie écrit ce fichier")
    elif name == "tail":
        if any(w in ("--follow", "-F") or w.startswith("--follow=") for w in args) or _short_has(args, "f"):
            raise Refused("tail -f attend sans fin")


def check_shell(command):
    """None when the shell line only reads; else Refused's reason."""
    try:
        for words in _words(command or ""):
            _check_simple(words)
    except Refused as e:
        return str(e)
    return None


def gate(name, data):
    """§1 — None when the tool call only reads; else why it is refused."""
    if name in READ_TOOLS:
        return None
    if name == SHELL:
        why = check_shell((data or {}).get("command") or "")
        return f"lecture seule — {why}" if why else None
    return f"lecture seule — l'outil {name} n'est pas permis à une enquête"


def _tool_text(name, data):
    data = data or {}
    if name == SHELL:
        return data.get("command") or ""
    if name == "Read":
        return data.get("file_path") or ""
    if name in ("Grep", "Glob"):
        return " ".join(str(data.get(k)) for k in ("pattern", "path", "glob") if data.get(k))
    try:
        return json.dumps(data, ensure_ascii=False)[:300]
    except (TypeError, ValueError):
        return str(data)[:300]


# ------------------------------------------------------------------ the instruction

INSTRUCTION = """Tu mènes une enquête pour la Product Owner d'une chaîne d'agents qui écrit des applications. Elle n'est pas technicienne.

Tu lis, tu ne changes rien. Le cockpit ne te donne que des outils de lecture : lire un fichier, chercher, lister, lire l'historique git. Toute autre commande est refusée par le cockpit lui-même : n'insiste pas, cherche autrement, et dis-le si cela t'empêche d'établir un point.

Comment tu réponds :
- En français de tous les jours, pour une lectrice qui n'est pas technicienne. Un mot technique, explique-le en quelques mots la première fois.
- Chaque affirmation cite sa source en `chemin:ligne` — par exemple `tools/cockpit/server.py:1672` — ou le commit, pour ce que dit git. Ce que tu ne peux pas sourcer, tu ne l'affirmes pas.
- Dis ce que tu n'as pas pu établir, et pourquoi.
- `docs/process/` dit pourquoi la chaîne est faite ainsi, règles abandonnées comprises : ce n'est jamais la source de ce qu'elle fait aujourd'hui — les fichiers eux-mêmes le sont.

Ta réponse a quatre parties, chacune sous son titre en gras, dans cet ordre :

**En bref** — trois phrases au plus.
**Ce que j'ai trouvé** — les faits, chacun avec sa source.
**Ce que je n'ai pas pu établir** — et pourquoi ; « Rien. » s'il n'y a rien.
**Ce que je conseille d'en faire** — commence par un seul de ces trois choix, en gras : **Enquêter plus loin** (sur quoi), **Une correction** (de quoi, où), **Rien**. Puis une ou deux phrases."""


def build_prompt(question, target, folder, target_name):
    where = (f"La cible : l'application « {target_name} », dans {folder} — ton dossier de travail."
             if target == APP else
             f"La cible : la chaîne d'agents et son cockpit, dans {folder} — ton dossier de travail. La chaîne est "
             "dans `.claude/` (agents, commandes, formats, grilles), le cockpit dans `tools/cockpit/` "
             "(son mode d'emploi : `tools/cockpit/LISEZMOI.md`).")
    return f"{where}\n\nLa question de la Product Owner :\n\n{question.strip()}"


# ------------------------------------------------------------------ the SDK options

def build_options(cwd, model, can_use_tool, hook, system_prompt=None, tools=None, max_turns=None):
    """The investigation's options — or, with `tools=[]`, a second call's: no
    tool at all, one turn."""
    from claude_agent_sdk import ClaudeAgentOptions, HookMatcher
    kw = {}
    if model:
        kw["model"] = model
    if max_turns:
        kw["max_turns"] = max_turns
    return ClaudeAgentOptions(
        cwd=cwd, tools=list(TOOLS if tools is None else tools), allowed_tools=[], disallowed_tools=list(NEVER),
        setting_sources=[], strict_mcp_config=True, mcp_servers={}, permission_mode="default",
        can_use_tool=can_use_tool, hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[hook])]},
        system_prompt={"type": "preset", "preset": "claude_code", "append": system_prompt or INSTRUCTION},
        env={"CLAUDE_CODE_EMIT_SESSION_STATE_EVENTS": "1"}, **kw)


def sdk_client_factory(options):
    from claude_agent_sdk import ClaudeSDKClient
    return ClaudeSDKClient(options=options)


def make_callbacks(refused_sink=None, seen_sink=None):
    """The permission callback and the PreToolUse hook, both on `gate`."""
    from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny

    def judge(name, data):
        why = gate(name, data)
        if why and refused_sink:
            refused_sink(name, data, why)
        elif not why and seen_sink:
            seen_sink(name, data)
        return why

    async def can_use_tool(name, data, ctx):
        why = gate(name, data)          # already told by the hook
        if why:
            return PermissionResultDeny(message=f"Refusé par le cockpit : {why}.")
        return PermissionResultAllow()

    async def hook(input_data, tool_use_id, context):
        name = (input_data or {}).get("tool_name") or ""
        why = judge(name, (input_data or {}).get("tool_input") or {})
        if not why:
            return {}
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                       "permissionDecisionReason": f"Refusé par le cockpit : {why}."}}
    return can_use_tool, hook


# ------------------------------------------------------------------ the investigation

def _now():
    return datetime.now().isoformat(timespec="seconds")


def console(text):
    """Her text, as the server's console can print it — a character its code
    page lacks (a Windows console's cp1252) replaced, never an error."""
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    return str(text).encode(enc, "replace").decode(enc, "replace")


class Failed(Exception):
    pass


class Investigation:
    def __init__(self, question, target, folder, target_name, model, source=None, computer=""):
        self.id = uuid.uuid4().hex[:10]
        self.question, self.target, self.folder = question, target, folder
        self.target_name, self.model, self.source = target_name, model or "", source or None
        self.computer = computer
        self.status = "going"            # going, ended
        self.outcome = ""                # terminé, erreur, annulé, délai dépassé
        self.error = ""
        self.started_at, self.ended_at = _now(), ""
        self.seconds = None
        self.text = ""
        self.model_used = ""
        self.cost = None
        self.log_path = ""
        self.run_id = ""
        self.refused = []                # [{tool, what, why}]
        self.steps = []                  # [{at, text}]
        self.report = None               # {path, commit, pushed, push_error, error}
        self.task = None
        self.seq = 0

    def snapshot(self):
        return {"id": self.id, "seq": self.seq, "question": self.question, "target": self.target,
                "folder": self.folder, "target_name": self.target_name, "model": self.model,
                "model_used": self.model_used, "status": self.status, "outcome": self.outcome, "error": self.error,
                "started_at": self.started_at, "ended_at": self.ended_at, "seconds": self.seconds,
                "text": self.text, "cost": self.cost, "log_path": self.log_path, "refused": self.refused[-40:],
                "steps": self.steps[-STEPS_KEPT:], "report": self.report, "source": self.source}


class Investigator:
    """One investigation at a time — and none while a run goes (the server
    checks that before `start`)."""

    def __init__(self, store, log_dir, client_factory=None, emit=None, on_end=None, timeout=None):
        self.store = store
        self.log_dir = log_dir
        self.client_factory = client_factory or sdk_client_factory
        self.emit = emit or (lambda snap: None)
        self.on_end = on_end
        self.timeout = timeout or TIMEOUT
        self.current = None
        self.last = None

    def going(self):
        c = self.current
        return c if c is not None and c.status != "ended" else None

    def public(self):
        c = self.going() or self.last
        return c.snapshot() if c else None

    def _tell(self, inv):
        inv.seq += 1
        try:
            self.emit(inv.snapshot())
        except Exception:
            pass

    def start(self, question, target, folder, target_name, model="", source=None, computer=""):
        if self.going():
            raise Failed("une enquête est déjà en cours : une à la fois")
        inv = Investigation(question, target, folder, target_name, model, source, computer)
        self.current = inv
        inv.task = asyncio.get_running_loop().create_task(self._drive(inv))
        self._tell(inv)
        return inv

    def cancel(self):
        inv = self.going()
        if inv and inv.task and not inv.task.done():
            inv.task.cancel()
            return True
        return False

    async def wait(self, timeout=None):
        inv = self.current
        if not inv or not inv.task:
            return True
        try:
            await asyncio.wait_for(asyncio.shield(inv.task), timeout)
        except asyncio.TimeoutError:
            return False
        except BaseException:
            pass
        return True

    async def _drive(self, inv):
        tally = stats_mod.Tally()
        inv.log_path = _open_log(self.log_dir, "enquete")
        inv.run_id = "enquete-" + uuid.uuid4().hex[:10]
        t0 = asyncio.get_running_loop().time()
        texts, limits, api_error, result = [], [], "", None

        def refused(name, data, why):
            inv.refused.append({"tool": name, "what": _tool_text(name, data)[:300], "why": why})
            inv.steps.append({"at": _now(), "text": f"Refusé — {name} : {_tool_text(name, data)[:160]}"})
            self._tell(inv)

        def seen(name, data):
            inv.steps.append({"at": _now(), "text": f"{name} — {_tool_text(name, data)[:160]}"})
            self._tell(inv)
        can_use_tool, hook = make_callbacks(refused, seen)
        try:
            async def go():
                nonlocal api_error, result
                options = build_options(inv.folder, inv.model, can_use_tool, hook)
                client = self.client_factory(options)
                async with client:
                    await client.query(build_prompt(inv.question, inv.target, inv.folder, inv.target_name))
                    async for msg in client.receive_messages():
                        at = runner_mod._now()
                        body = _log(inv.log_path, msg, at)
                        kind = type(msg).__name__
                        if kind == "AssistantMessage" and isinstance(body, dict):
                            if body.get("error"):
                                api_error = str(body["error"])
                            if body.get("model") and not inv.model_used:
                                inv.model_used = str(body["model"])
                            for b in body.get("content") or []:
                                if isinstance(b, dict) and isinstance(b.get("text"), str) and b["text"].strip():
                                    texts.append(b["text"])
                        for k, x in tally.feed(kind, body, at):
                            if k == "limit":
                                limits.append(x)
                        if kind == "ResultMessage":
                            result = body
                            break
            await asyncio.wait_for(go(), self.timeout)
            if api_error:
                inv.error = runner_mod.API_ERRORS.get(api_error, api_error)
            elif result and result.get("is_error"):
                inv.error = "; ".join(result.get("errors") or []) or result.get("result") or "erreur"
            elif not ((result or {}).get("result") or "".join(texts)).strip():
                inv.error = "Claude n'a rien répondu"
            inv.outcome = "erreur" if inv.error else "terminé"
        except asyncio.CancelledError:
            inv.outcome, inv.error = "annulé", "Arrêtée depuis le cockpit."
        except asyncio.TimeoutError:
            inv.outcome, inv.error = "délai dépassé", f"pas de fin en {int(self.timeout / 60)} min : l'enquête est abandonnée"
        except Exception as e:
            inv.outcome, inv.error = "erreur", usage_mod.describe_failure(e)
        finally:
            inv.seconds = round(asyncio.get_running_loop().time() - t0, 1)
            inv.text = ((result or {}).get("result") or (texts[-1] if texts else "")).strip()
            inv.cost = _record(self.store, inv.run_id, inv.started_at, tally, inv.outcome, inv.log_path, limits,
                               inv.folder, inv.seconds)
            inv.ended_at = _now()
            inv.status = "ended"
            self.last = inv
            print(console(f"Enquête — « {inv.question[:80]} » : {inv.outcome}" + (f" ({inv.error})" if inv.error else "")
                          + f" en {inv.seconds} s"), flush=True)
            if self.on_end:
                try:
                    await self.on_end(inv)
                except Exception as e:      # said, never raised
                    inv.report = {"error": f"rapport non écrit : {e}"}
            self._tell(inv)


def _open_log(log_dir, name):
    try:
        os.makedirs(log_dir, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        path = os.path.join(log_dir, f"{stamp}-{name}.jsonl")
        n = 1
        while os.path.exists(path):
            n += 1
            path = os.path.join(log_dir, f"{stamp}-{name}-{n}.jsonl")
        open(path, "w", encoding="utf-8").close()
        return path
    except OSError:
        return ""


def _log(path, msg, at):
    body = runner_mod._body(msg)
    if path:
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"at": at, "type": type(msg).__name__, "message": body},
                                   ensure_ascii=False, default=str) + "\n")
        except (OSError, TypeError, ValueError):
            pass
    return body


def _record(store, run_id, started, tally, outcome, log_path, limits, app, seconds):
    stats_mod.apply_model_usage(tally)
    cost = stats_mod.totals_summary(tally.totals, seconds)
    if store:
        try:
            cost = store.record_run(
                run_id=run_id, feature=None, work=None, command=COMMAND, mode=None, started_at=started,
                ended_at=_now(), tally=tally, next_line=None, outcome=outcome, log_path=log_path or None,
                app=app, kind=KIND) or cost
            for m in limits:
                store.record_limit(run_id, m)
        except Exception as e:
            print(f"Enquête : coût non enregistré ({e})", flush=True)
    if cost is not None:
        cost = dict(cost)
        cost["duration_s"] = seconds
        if tally.model_usage:
            cost["usd"] = round(sum((u.get("costUSD") or 0) for u in tally.model_usage.values()), 6)
    return cost


async def ask(prompt, system, cwd, client_factory=None, store=None, log_dir=None, model="", timeout=None,
              app=None):
    """A second call (§4): one turn, no tool — its text, or Failed."""
    can_use_tool, hook = make_callbacks()
    tally = stats_mod.Tally()
    log_path = _open_log(log_dir, "enquete-suite") if log_dir else ""
    started = _now()
    t0 = asyncio.get_running_loop().time()
    texts, result, api_error, outcome, error = [], None, "", "terminé", ""
    try:
        async def go():
            nonlocal result, api_error
            os.makedirs(cwd, exist_ok=True)
            options = build_options(cwd, model, can_use_tool, hook, system_prompt=system, tools=[], max_turns=1)
            client = (client_factory or sdk_client_factory)(options)
            async with client:
                await client.query(prompt)
                async for msg in client.receive_messages():
                    at = runner_mod._now()
                    body = _log(log_path, msg, at)
                    kind = type(msg).__name__
                    if kind == "AssistantMessage" and isinstance(body, dict):
                        if body.get("error"):
                            api_error = str(body["error"])
                        for b in body.get("content") or []:
                            if isinstance(b, dict) and isinstance(b.get("text"), str):
                                texts.append(b["text"])
                    tally.feed(kind, body, at)
                    if kind == "ResultMessage":
                        result = body
                        break
        await asyncio.wait_for(go(), timeout or ASK_TIMEOUT)
        if api_error:
            error = runner_mod.API_ERRORS.get(api_error, api_error)
        elif result and result.get("is_error"):
            error = "; ".join(result.get("errors") or []) or result.get("result") or "erreur"
    except asyncio.TimeoutError:
        outcome, error = "délai dépassé", "pas de réponse à temps"
    except asyncio.CancelledError:
        outcome, error = "annulé", "annulé"
        raise
    except Exception as e:
        error = usage_mod.describe_failure(e)
    finally:
        seconds = round(asyncio.get_running_loop().time() - t0, 1)
        if error and outcome == "terminé":
            outcome = "erreur"
        _record(store, "enquete-suite-" + uuid.uuid4().hex[:8], started, tally, outcome, log_path, [], app, seconds)
    text = ((result or {}).get("result") or "\n".join(texts)).strip()
    if error or not text:
        raise Failed(error or "Claude n'a rien répondu")
    return text


# ------------------------------------------------------------------ §2 the report

def slug(text, words=7, limit=60):
    t = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii").lower()
    parts = re.findall(r"[a-z0-9]+", t)
    out = "-".join(parts[:words])[:limit].strip("-")
    return out or "enquete"


def report_rel(folder, question, day=None):
    """docs/enquetes/<date>-<subject>.md, never over an existing one."""
    day = day or datetime.now().strftime("%Y-%m-%d")
    base = f"{FOLDER}/{day}-{slug(question)}"
    rel, n = base + ".md", 1
    while os.path.exists(os.path.join(folder, *rel.split("/"))) or \
            os.path.exists(os.path.join(folder, *(rel[:-3] + PROMPT_SUFFIX).split("/"))):
        n += 1
        rel = f"{base}-{n}.md"
    return rel


def fmt_int(n):
    return f"{n:,}".replace(",", " ") if isinstance(n, int) else "inconnu"


def fmt_duration(s):
    if s is None:
        return "durée inconnue"
    s = int(round(s))
    m, r = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h} h {m:02d} min" if h else f"{m} min {r:02d} s" if m else f"{r} s"


def cost_text(cost, seconds=None):
    c = cost or {}
    dur = c.get("duration_s") if c.get("duration_s") is not None else seconds
    parts = [f"{fmt_int(c.get('read_tokens'))} tokens lus · {fmt_int(c.get('output_tokens'))} écrits"
             if c else "tokens inconnus", fmt_duration(dur)]
    if c.get("usd"):
        parts.append(f"≈ {c['usd']:.2f} $ en équivalent API".replace(".", ","))
    return " · ".join(parts)


def target_text(target, target_name):
    return "la chaîne et le cockpit" if target == CHAIN else f"l'application « {target_name} »"


def model_text(inv):
    used = inv.model_used or inv.model or "inconnu"
    return used + (" (choisi pour cette enquête)" if inv.model else " (celui des commandes de la chaîne)")


def title_of(question):
    first = " ".join((question or "").split())
    return first if len(first) <= 110 else first[:107].rstrip() + "…"


def report_md(inv, rel, when=None):
    when = when or datetime.now()
    L = [f"# Enquête — {title_of(inv.question)}", "",
         f"- Date : {when.strftime('%d/%m/%Y à %H:%M')}",
         f"- Ordinateur : {inv.computer}",
         f"- Cible : {target_text(inv.target, inv.target_name)}",
         f"- Modèle : {model_text(inv)}",
         f"- Coût : {cost_text(inv.cost, inv.seconds)}",
         "", "Écrite par le cockpit. L'enquête a lu, rien de plus : aucun fichier modifié, aucune commande "
             "autre que de lecture. Aucun agent de la chaîne ne lit ce dossier.", "",
         "## La question", "", inv.question.strip(), "", "## La réponse", "", inv.text.strip() or "(vide)"]
    if inv.refused:
        L += ["", "## Ce que le cockpit a refusé", "",
              "Des commandes que l'enquête a tentées, refusées parce qu'elles ne lisent pas seulement :", ""]
        L += [f"- `{r['what'] or r['tool']}` — {r['why']}" for r in inv.refused]
    return "\n".join(L).rstrip() + "\n"


_META = re.compile(r"^- (Date|Ordinateur|Cible|Modèle|Coût) : (.*)$")


def parse_report(text):
    lines = (text or "").splitlines()
    out = {"title": "", "date": "", "computer": "", "target": "", "model": "", "cost": "", "question": ""}
    keys = {"Date": "date", "Ordinateur": "computer", "Cible": "target", "Modèle": "model", "Coût": "cost"}
    section = None
    q = []
    for line in lines:
        if line.startswith("# Enquête — ") and not out["title"]:
            out["title"] = line[len("# Enquête — "):].strip()
            continue
        m = _META.match(line)
        if m and section is None:
            out[keys[m.group(1)]] = m.group(2).strip()
            continue
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if section == "La question":
            q.append(line)
    out["question"] = "\n".join(q).strip()
    return out


def list_reports(folder, kind):
    """The reports of `docs/enquetes/`, newest first: [{path, name, …}]."""
    d = os.path.join(folder, *FOLDER.split("/"))
    try:
        names = sorted((n for n in os.listdir(d) if n.endswith(".md") and not n.endswith(PROMPT_SUFFIX)),
                       reverse=True)
    except OSError:
        return []
    out = []
    for n in names:
        p = os.path.join(d, n)
        try:
            with open(p, encoding="utf-8") as f:
                meta = parse_report(f.read())
        except (OSError, UnicodeDecodeError):
            continue
        prompt = n[:-3] + PROMPT_SUFFIX
        out.append({**meta, "name": n, "path": f"{FOLDER}/{n}", "target_kind": kind,
                    "prompt": f"{FOLDER}/{prompt}" if os.path.exists(os.path.join(d, prompt)) else None})
    return out


def safe_rel(rel):
    """A report's path as the page sends it back: inside docs/enquetes/, a
    .md, nothing else."""
    r = (rel or "").replace("\\", "/")
    if not r.startswith(FOLDER + "/") or "/" in r[len(FOLDER) + 1:] or ".." in r or not r.endswith(".md"):
        return None
    return r


# ------------------------------------------------------------------ §3 from a problem

def _human(at):
    try:
        d = datetime.fromisoformat(str(at).replace(" ", "T"))
    except (TypeError, ValueError):
        return str(at or "?")
    return d.strftime("%d/%m à %H:%M")


POINT_ASK = {
    "erreur": "Pourquoi cette commande a-t-elle fini en erreur, et qu'est-ce qui l'éviterait ?",
    "programme": "Pourquoi le programme du pilote automatique s'est-il arrêté sur une erreur ?",
    "blocage": "Pourquoi cet agent bloque-t-il plusieurs fois dans ce cycle : qu'ont ses fichiers de blocage en commun, "
               "et qu'est-ce que la chaîne pourrait faire autrement ?",
    "coût": "Pourquoi cette commande a-t-elle coûté beaucoup plus que d'habitude ?",
    "sur place": "Pourquoi cette commande a-t-elle été relancée plusieurs fois sans que l'étape proposée change ?",
}


def question_from_point(point, ctx):
    """§3 — a point à creuser of the Journal, as a question: what happened,
    where, the files and the run logs to look at. `ctx`: app_name, app,
    feature, cycle, journal (path), logs [(at, command, path)], files
    (paths)."""
    kind = (point or {}).get("kind") or ""
    L = [POINT_ASK.get(kind, "Que s'est-il passé, et pourquoi ?"), "",
         f"Ce qui s'est passé : {(point or {}).get('text') or '?'}",
         f"Où : l'application « {ctx.get('app_name')} » ({ctx.get('app')}), feature « {ctx.get('feature')} », "
         + ("cycle principal" if ctx.get("cycle") in (None, "", "main") else f"correction {ctx.get('cycle')}") + ".",
         "", "À regarder :"]
    L += [f"- le journal de run de {c} ({_human(at)}) : {p}" for at, c, p in ctx.get("logs") or []]
    L += [f"- {p}" for p in ctx.get("files") or []]
    if ctx.get("journal"):
        L.append(f"- le journal de cycle : {ctx['journal']}")
    if not ctx.get("logs"):
        L.append("- le journal de run n'est pas sur cet ordinateur (lancé ailleurs, ou effacé)")
    return {"question": "\n".join(L), "target": CHAIN}


def question_from_run(run, ctx):
    """§3 — a run that ended in error."""
    L = ["Pourquoi cette commande a-t-elle fini en erreur, et qu'est-ce qui l'éviterait ?", "",
         f"Ce qui s'est passé : {run.get('prompt')} a fini en erreur le {_human(run.get('started_at'))}"
         + (f" — « {run.get('error')} »" if run.get("error") else "") + ".",
         f"Où : l'application « {ctx.get('app_name')} » ({ctx.get('app')}), feature « {ctx.get('feature')} ».",
         "", "À regarder :"]
    if run.get("log_path"):
        L.append(f"- le journal de run : {run['log_path']}")
    else:
        L.append("- le journal de run : aucun (le run n'en a pas ouvert)")
    if ctx.get("journal"):
        L.append(f"- le journal de cycle : {ctx['journal']}")
    relay = " ".join((run.get("relay") or "").split())
    if relay:
        L += ["", f"Ses derniers mots : « {relay[-400:]} »"]
    return {"question": "\n".join(L), "target": CHAIN}


# ------------------------------------------------------------------ §4 what follows

PROMPT_INSTRUCTION = """You write a correction prompt for the Product Owner's design conversation — the conversation where the agent chain and its cockpit are designed. That conversation reads it, maybe changes it, and only then sends it to be carried out: never write as if it were launched as it is.

Write it in the shape of the design conversation's prompts, in English — the strings the Product Owner reads on the screen stay in French:

- a first line: what changes, in one sentence;
- what to change and why, from the investigation's findings, each with the file:line the report gives;
- « Quote before changing »: the passages to quote, as they are, before any edit;
- the tests that prove the change — and that would fail without it;
- the last line: « Commit and push: `<subject>` ».

Only what the report establishes: what it could not establish is said as such, never decided. No preamble, no closing words: the prompt alone, in Markdown."""

BUG_INSTRUCTION = """Tu écris une entrée de la liste de bugs d'une application, d'après un rapport d'enquête. L'entrée décrit un comportement de l'application — ce que voit la personne qui s'en sert —, jamais un fichier ni du code.

Réponds en trois lignes exactement, et rien d'autre :
Observé : <ce que l'application fait de travers, en une phrase de tous les jours>
Où : <l'écran, le moment ou l'action où on le voit>
Attendu : <ce qu'elle devrait faire à la place, et quand — une phrase qui complète « Elle devrait »>"""


def prompt_request(report_text):
    return f"Le rapport d'enquête :\n\n{report_text.strip()}"


def prompt_file(report_rel, model_text_):
    name = report_rel.split("/")[-1]
    return (f"> **{PROMPT_MARK}.**\n"
            f"> Écrit par le cockpit d'après l'enquête `{name}` ({model_text_}). Le cockpit ne lance jamais une "
            "correction de la chaîne ou du cockpit : ce prompt passe d'abord par la conversation de conception.\n\n")


def prompt_rel(report_rel):
    return report_rel[:-3] + PROMPT_SUFFIX


_BUG_LINE = re.compile(r"^\s*(Observé|Où|Attendu)\s*:\s*(.+?)\s*$", re.M | re.I)
GAP = re.compile(r"^\s*G(\d+)\b", re.M)


def bug_fields(text):
    out = {}
    for m in _BUG_LINE.finditer(text or ""):
        out[m.group(1).lower().replace("ù", "u")] = m.group(2).strip()
    return out


def next_gap(buglist_text):
    """The next `G<n>` of a bug list — the highest one there, plus one."""
    nums = [int(m.group(1)) for m in GAP.finditer(buglist_text or "")]
    return (max(nums) if nums else 0) + 1


def _sentence(s):
    s = (s or "").strip().rstrip(".")
    return s[:1].upper() + s[1:] if s else s


def bug_entry(fields, n):
    """One gap, as .claude/agents/diagnostiqueur.md « What a gap looks like »
    has it: `G<n> <what the application fails to do>. It should <what it
    should do instead, and when>.` — in French, where it is seen first."""
    where = _sentence(fields.get("ou"))
    seen = (fields.get("observé") or "").strip().rstrip(".")
    seen = (seen[:1].lower() + seen[1:]) if where and seen else _sentence(seen)
    expected = (fields.get("attendu") or "").strip().rstrip(".")
    expected = re.sub(r"^(?:elle\s+devrait\s+)", "", expected, flags=re.I)
    head = f"{where} : {seen}" if where else seen
    return f"G{n:02d} {head}. Elle devrait {expected}."


def renumber(entry, n):
    """Her confirmed entry, opening on the G<n> the list needs now."""
    t = (entry or "").strip()
    if GAP.match(t):
        return GAP.sub(f"G{n:02d}", t, count=1)
    return f"G{n:02d} {t}"


def append_gap(text, entry):
    body = (text or "").rstrip()
    return (body + "\n\n" if body else "") + entry.strip() + "\n"
