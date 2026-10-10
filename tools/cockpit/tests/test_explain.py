"""1.19 — « Expliquer » on a question: what the model reads, and only that
(§1); the call — the fake client, the timeout, « Annuler », its cost
recorded and marked, 1.17's threshold and its override (§2); the instruction
and its no-recommendation rule (§3); the explanation kept for the question,
given at once the second time, dropped when the question's file changes
(§4). No real Claude call."""
import asyncio
import json
import sqlite3
import time

import pytest
from aiohttp.test_utils import TestClient, TestServer
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

import explain
import questions
import runner as runner_mod
import server
import stats as stats_mod
import usage
from state import State
from test_runner import FakeClient, script_quick
from test_server import build_app_folder, post
from test_usage import add_both

HAIKU = "claude-haiku-5-5"

PRODUCT = """# Fiche produit

### B1 — La course
La course compte 8 ateliers et 8 courses de 1 km.

### B2 — La Roxzone
Entre une course et un atelier, l'athlète traverse la Roxzone. La montre
marque ROX_IN et ROX_OUT.

Défaut affiché : le temps de la Roxzone est compté à part.

### B3 — L'export
L'export se fait en CSV.
"""

QUESTIONS = """### Q1
Block: B2
Question: Le temps de la Roxzone compte-t-il dans le segment de l'atelier, ou à part ?
Options:
- Dans le segment de l'atelier
- À part, comme une transition
Défaut: À part, comme une transition — B2 « compté à part »
Answer:

### Q2
Block: B9
Question: Faut-il un mode atténué pendant l'export ?
Answer:

### Q3
Block: -
Question: Quelle couleur pour la zone 5 ?
Answer:
"""

LEXIQUE = """## Tranché

Roxzone — retenu, la zone de transition
  ROX_IN, ROX_OUT : ses deux temps, retenus aussi

transition — deux sens, tranchés
  (a) la Roxzone : transition, retenu
  (b) fermer le segment précédent et ouvrir le suivant : marquage, retenu
    remplace : transition, dans ce sens seulement

segment — deux sens, gardés tous deux
  (a) l'un des 30 moments de la course : segment, retenu

mode atténué — retenu
  remplace : mode veille

Rowing — retenu
  remplace : Rameur

## Non tranché

écran, page — 12 et 7 occurrences

## Relevé

Roxzone — 113
segment — 59
"""

ENTRY_ROX = """Roxzone — retenu, la zone de transition
  ROX_IN, ROX_OUT : ses deux temps, retenus aussi"""
ENTRY_TRANSITION = """transition — deux sens, tranchés
  (a) la Roxzone : transition, retenu
  (b) fermer le segment précédent et ouvrir le suivant : marquage, retenu
    remplace : transition, dans ce sens seulement"""
ENTRY_SEGMENT = """segment — deux sens, gardés tous deux
  (a) l'un des 30 moments de la course : segment, retenu"""
BLOCK_B2 = """### B2 — La Roxzone
Entre une course et un atelier, l'athlète traverse la Roxzone. La montre
marque ROX_IN et ROX_OUT.

Défaut affiché : le temps de la Roxzone est compté à part."""

ANSWER = ("**Ce que la question demande** — Où ranger le temps passé entre deux épreuves.\n"
          "**Pourquoi c'est important** — L'athlète verra ce temps dans l'atelier ou sur sa propre ligne.\n"
          "**Ce que change chaque option**\n- Dans le segment de l'atelier : un seul temps.\n"
          "- À part : une ligne de plus.\n**Les mots techniques** — Roxzone : la zone de passage.")


def feature_folder(tmp_path):
    root = tmp_path / "app"
    feat = build_app_folder(root)
    (feat / "desc-produit.md").write_text(PRODUCT, encoding="utf-8")
    (feat / "questions-sondeur-01.md").write_text(QUESTIONS, encoding="utf-8")
    (feat / "lexique.md").write_text(LEXIQUE, encoding="utf-8")
    return root, feat


def entry(feat, n):
    parsed = questions.parse_file(str(feat / "questions-sondeur-01.md"), str(feat))
    return next(e for e in parsed.entries if e.number == n)


def answering(text=ANSWER, wait=0.0):
    async def script(c):
        if wait:
            await asyncio.sleep(wait)
        yield AssistantMessage(content=[TextBlock(text)], model=HAIKU, message_id="m1",
                               usage={"input_tokens": 900, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0})
        yield ResultMessage(subtype="success", duration_ms=4000, duration_api_ms=3900, is_error=False, num_turns=1,
                            session_id="s", result=text, model_usage={HAIKU: {
                                "inputTokens": 900, "outputTokens": 180, "cacheReadInputTokens": 0,
                                "cacheCreationInputTokens": 0, "costUSD": 0.0018}})
    return script


class Factory:
    def __init__(self, script=None):
        self.script = script or answering()
        self.clients, self.cwds = [], []

    def __call__(self, cwd):
        self.cwds.append(cwd)
        c = FakeClient(self.script, None)
        self.clients.append(c)
        return c


# ---------------------------------------------------- §1 what it reads

def test_exactly_the_question_its_options_its_block_and_the_matching_lexicon(tmp_path):
    _, feat = feature_folder(tmp_path)
    ctx = explain.gather(entry(feat, 1), str(feat))
    assert ctx["passage"] == {"doc": "desc-produit.md", "ids": ["B2"], "text": BLOCK_B2, "cut": False, "missing": []}
    # The entries whose terms are in the question or its options — never the rest of the file.
    assert ctx["lexicon"] == [ENTRY_ROX, ENTRY_TRANSITION, ENTRY_SEGMENT]
    prompt = explain.build_prompt(ctx)
    assert prompt == "\n".join([
        "## La question",
        "Le temps de la Roxzone compte-t-il dans le segment de l'atelier, ou à part ?",
        "", "## Ses options", "- Dans le segment de l'atelier", "- À part, comme une transition",
        "", "## Son défaut", "À part, comme une transition — B2 « compté à part »",
        "", "## Le passage qu'elle nomme (B2, dans desc-produit.md)", BLOCK_B2,
        "", "## Le lexique de l'application, pour ces mots", ENTRY_ROX, ENTRY_TRANSITION, ENTRY_SEGMENT])
    # Nothing else: not B1 nor B3, not the unmatched entries, not « Non tranché » nor « Relevé ».
    for absent in ("8 ateliers", "CSV", "mode atténué", "Rowing", "écran, page", "— 113", "Answer"):
        assert absent not in prompt


def test_a_missing_block_is_said_and_the_question_alone_is_used(tmp_path):
    _, feat = feature_folder(tmp_path)
    ctx = explain.gather(entry(feat, 2), str(feat))
    assert ctx["passage"] is None and ctx["passage_missing"] == "B9 introuvable dans desc-produit.md"
    prompt = explain.build_prompt(ctx)
    assert "Introuvable : B9 introuvable dans desc-produit.md. Explique à partir de la question seule, et dis-le." in prompt
    assert "## Ses options\nAucune : la réponse est libre." in prompt
    assert ctx["lexicon"] == ["mode atténué — retenu\n  remplace : mode veille"]
    ctx = explain.gather(entry(feat, 3), str(feat))
    assert ctx["passage_missing"].startswith("« Block: - »") and ctx["lexicon"] == []
    assert "Aucune entrée pour les mots de cette question." in explain.build_prompt(ctx)


def test_a_question_with_no_block_line(tmp_path):
    _, feat = feature_folder(tmp_path)
    (feat / "questions-lexicographe-01.md").write_text(
        "### Q1\nTerms: Roxzone\nQuestion: Roxzone ou zone de transition ?\nAnswer:\n", encoding="utf-8")
    e = questions.parse_file(str(feat / "questions-lexicographe-01.md"), str(feat)).entries[0]
    ctx = explain.gather(e, str(feat))
    assert ctx["passage"] is None and "pas de ligne « Block: »" in ctx["passage_missing"]
    assert ctx["lexicon"] == [ENTRY_ROX, ENTRY_TRANSITION]


# ---------------------------------------------------- §3 the instruction

def test_the_instruction_forbids_any_recommendation():
    i = explain.INSTRUCTION
    assert "Règle absolue : tu ne recommandes jamais rien." in i
    for words in ("aucune préférence", "« en général »", "« d'habitude »", "« il vaut mieux »",
                  "Le défaut, s'il y en a un, n'est pas un choix à faire",
                  "La décision appartient à la Product Owner seule."):
        assert words in i
    for part in ("**Ce que la question demande**", "**Pourquoi c'est important**", "ce que l'utilisateur de l'application verra",
                 "**Ce que change chaque option**", "**Les mots techniques**", "défini en une ligne", "150 mots au plus",
                 "dis-le en une phrase : ce qui manque"):
        assert part in i
    # It is the system prompt of the call; the prompt itself holds the context alone.
    o = explain.build_options("C:/x")
    assert o.system_prompt == i and o.tools == [] and o.setting_sources == [] and o.max_turns == 1
    assert o.model == "haiku" and o.strict_mcp_config and o.mcp_servers == {} and o.thinking == {"type": "disabled"}


# ------------------------------------------------------------ §2 the call

def test_the_call_its_text_and_its_cost_recorded_and_marked(tmp_path):
    store = stats_mod.Store(str(tmp_path / "s.sqlite"))
    f = Factory()
    ex = explain.Explainer(store, str(tmp_path / "logs"), client_factory=f, scratch=str(tmp_path / "scratch"))
    got = asyncio.run(ex.explain("k", "## La question\nx", "C:/app", "f", "Q1"))
    assert got["text"] == ANSWER and got["cost"]["read_tokens"] == 900 and got["cost"]["output_tokens"] == 180
    assert got["cost"]["usd"] == 0.0018
    assert f.cwds == [str(tmp_path / "scratch")] and f.clients[0].prompts == ["## La question\nx"]
    with sqlite3.connect(store.path) as db:
        db.row_factory = sqlite3.Row
        r = dict(db.execute("SELECT * FROM runs").fetchone())
    assert r["kind"] == "explication" and r["command"] == "(explication)" and r["outcome"] == "terminé"
    assert r["app"] == "C:/app" and r["feature"] == "f" and r["log_path"].endswith("-explication.jsonl")
    # Never a command's estimate.
    assert usage.estimates(store.path, "C:/app") == {}


def test_the_timeout_says_so(tmp_path):
    store = stats_mod.Store(str(tmp_path / "s.sqlite"))
    ex = explain.Explainer(store, str(tmp_path / "logs"), client_factory=Factory(answering(wait=5)),
                           scratch=str(tmp_path / "scratch"), timeout=0.3)
    t0 = time.monotonic()
    with pytest.raises(explain.Failed, match="pas de réponse en 0.3 s : l'explication est abandonnée"):
        asyncio.run(ex.explain("k", "x"))
    assert time.monotonic() - t0 < 3
    assert explain.TIMEOUT == 60.0
    with sqlite3.connect(store.path) as db:
        assert db.execute("SELECT outcome, kind FROM runs").fetchone() == ("délai dépassé", "explication")


# ----------------------------------------------------- through the server

def served(tmp_path, body, factory, monkeypatch):
    root, feat = feature_folder(tmp_path)
    st = State(str(tmp_path / "config.json"))
    st.add_app(str(root))
    st.open_pair(str(root), "f")
    store = stats_mod.Store(str(tmp_path / "stats.sqlite"))
    rn = runner_mod.Runner(client_factory=lambda *a, **k: FakeClient(script_quick, None), on_end=server.make_on_end(st),
                           mode_getter=lambda: st.mode, log_dir=str(tmp_path / "logs"), stats=store)
    ex = explain.Explainer(store, str(tmp_path / "logs"), client_factory=factory, scratch=str(tmp_path / "scratch"))
    app = server.make_app(st, rn, picker=lambda initial: str(root), explainer=ex)

    async def go():
        async with TestClient(TestServer(app, host="127.0.0.1")) as c:
            c.ctx = {"store": store, "feat": feat, "ex": ex, "state": st}
            return await body(c)
    return asyncio.run(go())


QID = "q:questions-sondeur-01.md#1"


async def forms_q(c, qid=QID):
    f = await (await c.get("/api/forms")).json()
    return next(q for q in f["questions"] if q["id"] == qid)


def test_kept_given_at_once_the_second_time_and_dropped_when_the_file_changes(tmp_path, monkeypatch):
    f = Factory()

    async def body(c):
        assert (await forms_q(c))["explanation"] is None
        r = await post(c, "/api/explain", {"id": QID})
        out = await r.json()
        assert r.status == 200 and out["kept"] is False and out["explanation"]["text"] == ANSWER
        assert out["explanation"]["used"] == {"passage": {"doc": "desc-produit.md", "ids": ["B2"]},
                                              "passage_missing": None, "lexicon": 3}
        # What the model got: exactly the gathered context.
        assert f.clients[0].prompts == [explain.build_prompt(explain.gather(entry(c.ctx["feat"], 1), str(c.ctx["feat"])))]
        # The second time: at once, no call.
        r = await post(c, "/api/explain", {"id": QID})
        out = await r.json()
        assert out["kept"] is True and out["explanation"]["text"] == ANSWER and len(f.clients) == 1
        assert (await forms_q(c))["explanation"]["text"] == ANSWER
        # « Réexpliquer »: asked again.
        r = await post(c, "/api/explain", {"id": QID, "again": True})
        assert (await r.json())["kept"] is False and len(f.clients) == 2
        # Kept in the cockpit's store, never in the application.
        assert "Roxzone" not in "".join(p.read_text(encoding="utf-8", errors="ignore")
                                        for p in (tmp_path / "app").rglob("*") if p.is_file() and p.suffix != ".md")
        # The question's file changes — another question of it answered: dropped.
        p = c.ctx["feat"] / "questions-sondeur-01.md"
        p.write_text(p.read_text(encoding="utf-8").replace("Answer:\n\n### Q3", "Answer: Non\n\n### Q3", 1),
                     encoding="utf-8")
        assert (await forms_q(c))["explanation"] is None
        with sqlite3.connect(c.ctx["store"].path) as db:
            assert db.execute("SELECT COUNT(*) FROM explanations").fetchone()[0] == 0
        r = await post(c, "/api/explain", {"id": QID})
        assert (await r.json())["kept"] is False and len(f.clients) == 3
    served(tmp_path, body, f, monkeypatch)


def test_annuler(tmp_path, monkeypatch):
    f = Factory(answering(wait=10))

    async def body(c):
        req = asyncio.ensure_future(post(c, "/api/explain", {"id": QID}))
        end = time.monotonic() + 5
        while not (await forms_q(c))["explaining"]:
            assert time.monotonic() < end
            await asyncio.sleep(0.02)
        r = await post(c, "/api/explain/cancel", {"id": QID})
        assert (await r.json())["cancelled"] is True
        r = await req
        assert r.status == 409 and (await r.json())["cancelled"] is True
        assert (await forms_q(c))["explanation"] is None and not (await forms_q(c))["explaining"]
        with sqlite3.connect(c.ctx["store"].path) as db:
            assert db.execute("SELECT outcome FROM runs WHERE kind='explication'").fetchone() == ("annulé",)
    served(tmp_path, body, f, monkeypatch)


def test_the_blocking_threshold_and_its_override(tmp_path, monkeypatch):
    f = Factory()

    async def body(c):
        add_both(c.ctx["store"], 0.95, 0.20)
        r = await post(c, "/api/explain", {"id": QID})
        b = await r.json()
        assert r.status == 409 and b["usage_block"]["windows"][0]["window"] == "five_hour" and f.clients == []
        r = await post(c, "/api/explain", {"id": QID, "usage_ok": True})
        assert r.status == 200 and len(f.clients) == 1
        line = (tmp_path / "logs" / usage.OVERRIDE_LOG).read_text(encoding="utf-8")
        assert "« Lancer quand même » : « Expliquer » sur Q1 de questions-sondeur-01.md" in line
    served(tmp_path, body, f, monkeypatch)


def test_a_failure_says_why(tmp_path, monkeypatch):
    async def not_logged_in(c):
        yield AssistantMessage(content=[TextBlock("Not logged in")], model=HAIKU, error="authentication_failed")
        yield ResultMessage(subtype="success", duration_ms=1, duration_api_ms=0, is_error=True, num_turns=1,
                            session_id="s", result="Not logged in")

    async def body(c):
        r = await post(c, "/api/explain", {"id": QID})
        assert r.status == 502 and (await r.json())["error"] == \
            "Pas d'explication : Claude Code n'est pas connecté sur cet ordinateur."
        assert (await forms_q(c))["explanation"] is None
    served(tmp_path, body, Factory(not_logged_in), monkeypatch)
