"""« Expliquer » sur une question — cockpit 1.19.

The Product Owner is not technical: a question may use words she does not
know, or ask about a consequence she cannot see. « Expliquer » gives a short
explanation in plain French — never a recommendation.

§1 — what the model reads, and only that, all of it in the prompt:
- the question, its options and its `Défaut:`;
- the passage its `Block:` line names, extracted as « À répondre » shows it
  beside the question (context.resolve: the `### B<n>` section of the
  product file, or the `§n.m` entry of the technical document for the
  Architecte's) — when there is none, the prompt says so;
- the entries of `lexique.md`'s `## Tranché` whose terms appear in the
  question or its options — the entries only, never the whole file.

§2 — the call, as 1.17's measure: the lightest model, one turn, no tool, no
setting, no MCP server, in a scratch folder; 60 s at most; cancellable. Its
cost recorded in the stats, `kind = 'explication'`.
"""
import asyncio
import hashlib
import json
import os
import re
import tempfile
import uuid
from datetime import datetime

import context as context_mod
import runner as runner_mod
import stats as stats_mod
import textfile
import usage as usage_mod

KIND = "explication"
COMMAND = "(explication)"
MODEL = usage_mod.MODEL
TIMEOUT = 60.0
SCRATCH = os.path.join(tempfile.gettempdir(), "cockpit-explication")
LEXICON = "lexique.md"
# A block longer than this is cut, and the prompt says it was.
MAX_PASSAGE = 6000

# 🔴 The instruction, whole (§3). The no-recommendation rule is written here,
# and a test reads it here.
INSTRUCTION = """Tu expliques une question à la Product Owner d'une application. Elle n'est pas technicienne, et c'est elle seule qui décide de la réponse.

Écris en français de tous les jours, sans jargon, en 150 mots au plus, en quatre parties, chacune sous son titre en gras :

**Ce que la question demande** — en mots de tous les jours.
**Pourquoi c'est important** — ce que l'utilisateur de l'application verra ou ne verra pas, selon la réponse.
**Ce que change chaque option** — une ligne par option, qui commence par l'option : ce qu'elle change concrètement pour l'utilisateur. S'il n'y a pas d'options, dis ce que la réponse doit préciser.
**Les mots techniques** — chaque mot technique de la question ou des options, défini en une ligne. S'il n'y en a pas : « Aucun. »

Règle absolue : tu ne recommandes jamais rien. Aucun conseil, aucune préférence, aucun « en général », « d'habitude », « le plus souvent », « il vaut mieux », « le plus simple », aucune option présentée comme meilleure, plus sûre ou plus courante qu'une autre. Le défaut, s'il y en a un, n'est pas un choix à faire : décris-le comme les autres options, sans le mettre en avant. La décision appartient à la Product Owner seule.

Tu n'as que ce qui suit : la question, ses options, son défaut, le passage du document qu'elle nomme et les définitions du lexique de l'application. N'invente rien au-delà. Si cela ne suffit pas pour expliquer un point, dis-le en une phrase : ce qui manque."""


# The rules whose passage is the one `Block:` names (context_rules.md).
BLOCK_RULES = {r for r, _ in context_mod.BLOCK_WRITERS.values()} | {"CTX-ARC"}


class Failed(Exception):
    pass


class Cancelled(Failed):
    """« Annuler »."""


# ------------------------------------------------------------- §1 context

def lexicon_entries(lines, text):
    """The `## Tranché` entries of lexique.md whose terms appear in `text`:
    each entry whole — its head line and its indented lines —, nothing
    else of the file. An entry's terms: those its head line names before
    ` — `, those an indented line names before ` : `, and those a
    `remplace :` line retires."""
    entries, cur, inside = [], None, False
    for line in lines:
        if line.startswith("## "):
            inside = line.strip() == "## Tranché"
            if cur:
                entries.append(cur)
            cur = None
            continue
        if not inside:
            continue
        if not line.strip():
            if cur:
                entries.append(cur)
            cur = None
            continue
        if not line[:1].isspace():
            if cur:
                entries.append(cur)
            cur = [line.rstrip()]
        elif cur is not None:
            cur.append(line.rstrip())
    if cur:
        entries.append(cur)
    out = []
    for e in entries:
        terms = _terms_of(e)
        if any(context_mod.term_pattern(t).search(text) for t in terms):
            out.append("\n".join(e))
    return out


def _clean_term(t):
    t = re.sub(r"\([a-z]\)", "", t).strip().strip('"«» ')
    return t if len(t) >= 2 else ""


def _terms_of(entry):
    terms = []
    head = entry[0].split(" — ", 1)[0]
    terms += [_clean_term(x) for x in re.split(r",\s*", head)]
    for line in entry[1:]:
        s = line.strip()
        m = re.match(r"^remplace\s*:\s*(.+)$", s)
        if m:
            terms.append(_clean_term(re.split(r",\s*(?:dans ce sens seulement|seule?s?)\b", m.group(1))[0]))
            continue
        m = re.match(r"^(?:\([a-z]\)\s*)?([^:]+?)\s*:\s*(.+)$", s)
        if m:
            left, right = m.group(1), m.group(2)
            if s.startswith("("):
                # `(a) <le sens> : <terme>, retenu` — the term is on the right.
                terms.append(_clean_term(right.split(",")[0]))
            elif left.strip() not in ("le concept", "en anglais"):
                terms += [_clean_term(x) for x in re.split(r",\s*", left)]
    return [t for t in terms if t]


def gather(entry, base):
    """What the explanation reads (§1): {question, options, default,
    default_source, passage, passage_missing, lexicon}. `base` is the
    feature folder — where lexique.md sits."""
    out = {"question": entry.question, "options": list(entry.options), "default": entry.default,
           "default_source": entry.default_source, "passage": None, "passage_missing": None, "lexicon": []}
    t = context_mod.target(entry, base)
    if t.get("rule") not in BLOCK_RULES:
        # A lexicographe's question points to words, a technical one to its
        # `Entries:` — neither names a block.
        out["passage_missing"] = "la question ne nomme aucun bloc (pas de ligne « Block: »)"
    elif t["status"] != "ok":
        out["passage_missing"] = t["reason"]
    else:
        r = context_mod.resolve(entry, base)
        if r["status"] != "ok":
            out["passage_missing"] = r.get("reason") or "le passage est introuvable"
        else:
            parts = ["\n".join(r["lines"][m["start"]:m["end"] + 1]) for m in r["matches"]]
            text = "\n\n".join(parts)
            cut = len(text) > MAX_PASSAGE
            out["passage"] = {"doc": r["doc"], "ids": r["ids"], "text": text[:MAX_PASSAGE], "cut": cut,
                              "missing": r.get("missing") or []}
    try:
        lines = textfile.load(os.path.join(base, LEXICON)).lines
    except (OSError, textfile.UnreadableFile):
        lines = []
    seen = "\n".join([entry.question, *entry.options, entry.default or ""])
    out["lexicon"] = lexicon_entries(lines, seen)
    return out


def build_prompt(ctx):
    """The prompt: the context, nothing else — the instruction is the
    system prompt."""
    parts = ["## La question", ctx["question"].strip()]
    if ctx["options"]:
        parts += ["", "## Ses options", *[f"- {o}" for o in ctx["options"]]]
    else:
        parts += ["", "## Ses options", "Aucune : la réponse est libre."]
    if ctx["default"]:
        parts += ["", "## Son défaut", ctx["default"] + (f" — {ctx['default_source']}" if ctx["default_source"] else "")]
    p = ctx["passage"]
    if p:
        parts += ["", f"## Le passage qu'elle nomme ({', '.join(p['ids'])}, dans {p['doc']})", p["text"]]
        if p["cut"]:
            parts.append("[… passage coupé : trop long]")
    else:
        parts += ["", "## Le passage qu'elle nomme",
                  f"Introuvable : {ctx['passage_missing']}. Explique à partir de la question seule, et dis-le."]
    parts += ["", "## Le lexique de l'application, pour ces mots"]
    parts += ([*ctx["lexicon"]] if ctx["lexicon"] else ["Aucune entrée pour les mots de cette question."])
    return "\n".join(parts)


def file_sig(path):
    """The question file's content, hashed: a kept explanation is dropped
    once it changed."""
    try:
        with open(path, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()
    except OSError:
        return None


# --------------------------------------------------------------- §2 call

def build_options(cwd):
    from claude_agent_sdk import ClaudeAgentOptions
    return ClaudeAgentOptions(cwd=cwd, tools=[], setting_sources=[], strict_mcp_config=True,
                              mcp_servers={}, model=MODEL, max_turns=1, thinking={"type": "disabled"},
                              system_prompt=INSTRUCTION, permission_mode="default")


def sdk_client_factory(cwd):
    from claude_agent_sdk import ClaudeSDKClient
    return ClaudeSDKClient(options=build_options(cwd))


class Explainer:
    """One call per question at a time; each cancellable."""

    def __init__(self, store, log_dir, client_factory=None, scratch=None, timeout=None):
        self.store = store
        self.log_dir = log_dir
        self.client_factory = client_factory or sdk_client_factory
        self.scratch = scratch or SCRATCH
        self.timeout = timeout or TIMEOUT
        self.tasks = {}

    def going(self, key):
        t = self.tasks.get(key)
        return bool(t and not t.done())

    def cancel(self, key):
        t = self.tasks.get(key)
        if t and not t.done():
            t.cancel()
            return True
        return False

    async def explain(self, key, prompt, app=None, feature=None, what=""):
        """The explanation's text, its cost and its time — or Failed with
        why, in French; asyncio.CancelledError when « Annuler »."""
        if self.going(key):
            raise Failed("une explication de cette question est déjà en cours")
        task = asyncio.get_running_loop().create_task(self._call(prompt, app, feature, what))
        self.tasks[key] = task
        try:
            try:
                await asyncio.wait({task})
            except asyncio.CancelledError:        # the request itself went away
                task.cancel()
                raise
            if task.cancelled():
                raise Cancelled("explication annulée")
            return task.result()
        finally:
            if self.tasks.get(key) is task:
                del self.tasks[key]

    async def _call(self, prompt, app, feature, what):
        run_id = "explication-" + uuid.uuid4().hex[:10]
        tally = stats_mod.Tally()
        log_path = self._open_log()
        started = runner_mod._now()
        t0 = asyncio.get_running_loop().time()
        texts, limits, api_error = [], [], ""
        outcome, error, result = "terminé", "", None
        try:
            os.makedirs(self.scratch, exist_ok=True)

            async def go():
                nonlocal api_error, result
                client = self.client_factory(self.scratch)
                async with client:
                    await client.query(prompt)
                    async for msg in client.receive_messages():
                        at = runner_mod._now()
                        body = self._log(log_path, msg, at)
                        kind = type(msg).__name__
                        if kind == "AssistantMessage" and isinstance(body, dict):
                            if body.get("error"):
                                api_error = str(body["error"])
                            for b in body.get("content") or []:
                                if isinstance(b, dict) and isinstance(b.get("text"), str):
                                    texts.append(b["text"])
                        for k, x in tally.feed(kind, body, at):
                            if k == "limit":
                                limits.append(x)
                        if kind == "ResultMessage":
                            result = body
                            break
            await asyncio.wait_for(go(), self.timeout)
            if api_error:
                error = runner_mod.API_ERRORS.get(api_error, api_error)
            elif result and result.get("is_error"):
                error = "; ".join(result.get("errors") or []) or result.get("result") or "erreur"
            elif not "".join(texts).strip() and not (result or {}).get("result"):
                error = "Claude n'a rien répondu"
        except asyncio.CancelledError:
            outcome, error = "annulé", "annulée"
            raise
        except asyncio.TimeoutError:
            outcome, error = "délai dépassé", f"pas de réponse en {self.timeout:g} s : l'explication est abandonnée"
        except Exception as e:
            error = usage_mod.describe_failure(e)
        finally:
            seconds = round(asyncio.get_running_loop().time() - t0, 1)
            if error and outcome == "terminé":
                outcome = "erreur"
            cost = self._record(run_id, started, tally, outcome, log_path, limits, app, feature)
            print(f"Expliquer — {what} : {outcome}" + (f" ({error})" if error and outcome != "terminé" else "")
                  + f" en {seconds} s" + (f" · {cost.get('read_tokens')} tokens lus, {cost.get('output_tokens')} écrits"
                                         if cost else ""), flush=True)
        if error:
            raise Failed(error)
        text = ((result or {}).get("result") or "\n".join(texts)).strip()
        return {"text": text, "seconds": seconds, "cost": cost, "run_id": run_id,
                "at": datetime.now().isoformat(timespec="seconds")}

    def _record(self, run_id, started, tally, outcome, log_path, limits, app, feature):
        stats_mod.apply_model_usage(tally)
        ended = runner_mod._now()
        cost = stats_mod.totals_summary(tally.totals, stats_mod._seconds(started, ended))
        if self.store:
            try:
                cost = self.store.record_run(
                    run_id=run_id, feature=feature, work=feature, command=COMMAND, mode=None, started_at=started,
                    ended_at=ended, tally=tally, next_line=None, outcome=outcome, log_path=log_path or None,
                    app=app, kind=KIND) or cost
                for m in limits:
                    self.store.record_limit(run_id, m)
            except Exception as e:
                print(f"Expliquer : coût non enregistré ({e})", flush=True)
        if cost is not None and tally.model_usage:
            cost["usd"] = round(sum((u.get("costUSD") or 0) for u in tally.model_usage.values()), 6)
        return cost

    def _open_log(self):
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            path = os.path.join(self.log_dir, f"{stamp}-explication.jsonl")
            n = 1
            while os.path.exists(path):
                n += 1
                path = os.path.join(self.log_dir, f"{stamp}-explication-{n}.jsonl")
            open(path, "w", encoding="utf-8").close()
            return path
        except OSError:
            return ""

    @staticmethod
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
