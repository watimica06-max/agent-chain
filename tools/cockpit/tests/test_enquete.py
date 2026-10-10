"""1.21 — enquete.py alone: the read-only gate (§1) — the allowed reading
commands pass, every write, commit, push, deletion and web call is refused,
through the hook and the permission callback both —; the options the call
is given; the report and its listing (§2); the question written from a point
à creuser and from a failed run (§3); the correction prompt's mark and the
bug entry in the Diagnostiqueur's format (§4). No real Claude call."""
import asyncio
import os

import pytest
from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny, ToolPermissionContext

import enquete

# ------------------------------------------------------------------ §1 the gate

ALLOWED = [
    "git log --oneline -20",
    "git log -p -- tools/cockpit/server.py",
    "git show HEAD~2:tools/cockpit/runner.py",
    "git diff HEAD~3 HEAD -- .claude/agents",
    "git status --short",
    "git blame -L 10,40 tools/cockpit/journal.py",
    "git grep -n computer_name",
    "git --no-pager log -3",
    "git -C C:/Dev/app log --oneline -5",
    "ls -la docs/features",
    "find . -name '*.md' -path '*bugfix*'",
    "cat docs/features/f/bug-list.md",
    "head -n 40 tools/cockpit/LISEZMOI.md",
    "tail -n 20 logs/run.jsonl",
    "wc -l tools/cockpit/server.py",
    "stat README.md",
    "grep -rn \"Next:\" .claude/commands 2>/dev/null",
    "rg -n 'def gate' tools",
    "grep -c x a.md | sort -n | uniq -c | head -5",
    "cut -d: -f1 a.txt",
    "pwd",
    "cd tools/cockpit && git log -3",
    "basename C:/Dev/app; dirname C:/Dev/app",
    "realpath .",
    "grep 'a$' a.md",
]

REFUSED = [
    "git commit -am 'x'",
    "git push origin master",
    "git push --force",
    "git checkout -- README.md",
    "git reset --hard HEAD~1",
    "git rm README.md",
    "git clean -fdx",
    "git stash",
    "git branch -D x",
    "git merge x",
    "git pull",
    "git fetch",
    "git add -A",
    "git tag v1",
    "git config user.name x",
    "git -c core.pager=evil log",
    "git log --output=x.txt",
    "git diff --output x.txt",
    "git diff --ext-diff",
    "git grep -O x",
    "rm -rf docs",
    "rm README.md",
    "del README.md",
    "rmdir docs",
    "mv a b",
    "cp a b",
    "touch x",
    "mkdir x",
    "echo x > README.md",
    "echo x >> README.md",
    "cat a > b",
    "tee x",
    "sed -i s/a/b/ README.md",
    "find . -name x -delete",
    "find . -exec rm {} ;",
    "find . -fprint out.txt",
    "sort -o out.txt a",
    "sort --output=out.txt a",
    "uniq a out.txt",
    "rg --pre evil x",
    "tail -f logs/server.log",
    "curl https://example.com",
    "wget https://example.com",
    "python -c 'print(1)'",
    "powershell -Command Remove-Item x",
    "cmd /c del x",
    "ls $(rm x)",
    "ls `rm x`",
    "cat \"$(rm x)\"",
    "ls & rm x",
    "ls; rm x",
    "ls && git commit -m x",
    "ls || git push",
    "ls | xargs rm",
    "ls\nrm x",
    "FOO=1 ls",
    "(rm x)",
    "",
]


@pytest.mark.parametrize("command", ALLOWED)
def test_the_allowed_reading_commands_pass(command):
    assert enquete.check_shell(command) is None
    assert enquete.gate("Bash", {"command": command}) is None


@pytest.mark.parametrize("command", REFUSED)
def test_anything_else_is_refused(command):
    why = enquete.gate("Bash", {"command": command})
    assert why and why.startswith("lecture seule — ")


@pytest.mark.parametrize("tool", ["Write", "Edit", "MultiEdit", "NotebookEdit", "WebFetch", "WebSearch", "Agent",
                                  "Task", "PowerShell", "TodoWrite", "mcp__cockpit__licence", "Skill"])
def test_every_tool_but_reading_is_refused(tool):
    assert "n'est pas permis" in enquete.gate(tool, {"file_path": "x"})


@pytest.mark.parametrize("tool", ["Read", "Grep", "Glob"])
def test_the_reading_tools_pass(tool):
    assert enquete.gate(tool, {"file_path": "x", "pattern": "x"}) is None


def test_the_list_of_reading_commands_is_the_one_the_gate_applies():
    """The list LISEZMOI gives is READ_COMMANDS: each named command passes
    with a plain argument, and nothing outside it does."""
    for name in enquete.READ_COMMANDS:
        line = f"git log -1" if name == "git" else f"{name} x" if name not in ("pwd",) else name
        assert enquete.check_shell(line) is None, name
    assert set(enquete.GIT_READS) == {"log", "show", "diff", "status", "blame", "grep"}


def callbacks():
    refused, seen = [], []
    can, hook = enquete.make_callbacks(lambda n, d, w: refused.append((n, w)), lambda n, d: seen.append(n))
    return can, hook, refused, seen


def test_the_hook_and_the_permission_callback_refuse_alike():
    async def go():
        can, hook, refused, seen = callbacks()
        for name, data in [("Write", {"file_path": "a", "content": "x"}), ("Bash", {"command": "git commit -m x"}),
                           ("Bash", {"command": "git push"}), ("Bash", {"command": "rm -rf ."}),
                           ("WebFetch", {"url": "https://x"})]:
            out = await hook({"tool_name": name, "tool_input": data}, "t", None)
            assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
            assert out["hookSpecificOutput"]["permissionDecisionReason"].startswith("Refusé par le cockpit")
            r = await can(name, data, ToolPermissionContext())
            assert isinstance(r, PermissionResultDeny) and "lecture seule" in r.message
        assert len(refused) == 5 and not seen
        for name, data in [("Read", {"file_path": "a"}), ("Bash", {"command": "git log -3"})]:
            assert await hook({"tool_name": name, "tool_input": data}, "t", None) == {}
            assert isinstance(await can(name, data, ToolPermissionContext()), PermissionResultAllow)
        assert seen == ["Read", "Bash"]
    asyncio.run(go())


def test_the_options_give_reading_tools_only_whatever_the_settings():
    can, hook, _, _ = callbacks()
    o = enquete.build_options("C:/x", "", can, hook)
    assert o.tools == ["Read", "Grep", "Glob", "Bash"]
    assert {"Write", "Edit", "NotebookEdit", "WebFetch", "WebSearch", "Agent", "PowerShell"} <= set(o.disallowed_tools)
    assert o.allowed_tools == [] and o.setting_sources == [] and o.mcp_servers == {} and o.strict_mcp_config
    assert o.permission_mode == "default" and o.can_use_tool is can
    # The hook stands before every tool — its matcher none: the CLI runs it in
    # every permission mode, an allow rule or « bypass » included.
    (m,) = o.hooks["PreToolUse"]
    assert m.matcher is None and m.hooks == [hook]
    assert o.system_prompt["append"] == enquete.INSTRUCTION
    assert o.model is None                      # the chain's commands' model: none passed
    assert enquete.build_options("C:/x", "opus", can, hook).model == "opus"
    second = enquete.build_options("C:/x", "", can, hook, system_prompt="s", tools=[], max_turns=1)
    assert second.tools == [] and second.max_turns == 1


def test_the_instruction():
    i = enquete.INSTRUCTION
    assert "français" in i and "pas technicienne" in i
    assert "`chemin:ligne`" in i and "Ce que je n'ai pas pu établir" in i
    assert "**Ce que je conseille d'en faire**" in i
    for choice in ("**Enquêter plus loin**", "**Une correction**", "**Rien**"):
        assert choice in i


# ------------------------------------------------------------------ §2 the report

class Inv:
    def __init__(self, **kw):
        self.question = "Pourquoi le serveur redémarre-t-il après un commit de rapport ?"
        self.target, self.target_name, self.model, self.model_used = "chaine", "la chaîne et le cockpit", "", "claude-sonnet-5-5"
        self.computer, self.text, self.seconds = "travail", "**En bref** — Il ne redémarre pas.", 72.4
        self.cost = {"read_tokens": 1234567, "output_tokens": 4321, "duration_s": 72.4, "usd": 0.4213}
        self.refused = [{"tool": "Bash", "what": "git commit -m x", "why": "lecture seule — git commit : …"}]
        self.__dict__.update(kw)


def test_the_report_and_its_listing(tmp_path):
    from datetime import datetime
    inv = Inv()
    rel = enquete.report_rel(str(tmp_path), inv.question, day="2026-10-10")
    assert rel == "docs/enquetes/2026-10-10-pourquoi-le-serveur-redemarre-t-il-apres.md"
    text = enquete.report_md(inv, rel, when=datetime(2026, 10, 10, 21, 14))
    assert text.startswith("# Enquête — Pourquoi le serveur redémarre-t-il après un commit de rapport ?\n")
    for line in ("- Date : 10/10/2026 à 21:14", "- Ordinateur : travail", "- Cible : la chaîne et le cockpit",
                 "- Modèle : claude-sonnet-5-5 (celui des commandes de la chaîne)",
                 "- Coût : 1 234 567 tokens lus · 4 321 écrits · 1 min 12 s · ≈ 0,42 $ en équivalent API",
                 "## La question", "## La réponse", "**En bref** — Il ne redémarre pas.",
                 "## Ce que le cockpit a refusé", "- `git commit -m x` — lecture seule"):
        assert line in text, line
    p = tmp_path / rel
    p.parent.mkdir(parents=True)
    p.write_text(text, encoding="utf-8")
    # Never over an existing one.
    assert enquete.report_rel(str(tmp_path), inv.question, day="2026-10-10").endswith("-apres-2.md")
    (tmp_path / enquete.prompt_rel(rel)).write_text("x", encoding="utf-8")
    (rows,) = enquete.list_reports(str(tmp_path), "chaine")
    assert rows["title"] == inv.question and rows["computer"] == "travail" and rows["date"] == "10/10/2026 à 21:14"
    assert rows["cost"].startswith("1 234 567 tokens lus") and rows["question"] == inv.question
    assert rows["prompt"] == enquete.prompt_rel(rel) and rows["target_kind"] == "chaine"
    app = enquete.report_md(Inv(target="application", target_name="Hyrox", model="opus", model_used=""), rel)
    assert "- Cible : l'application « Hyrox »" in app and "- Modèle : opus (choisi pour cette enquête)" in app


@pytest.mark.parametrize("bad", ["../x.md", "docs/enquetes/../../x.md", "docs/enquetes/a/b.md", "docs/x.md",
                                 "docs/enquetes/x.txt", "", None])
def test_a_report_path_stays_in_docs_enquetes(bad):
    assert enquete.safe_rel(bad) is None
    assert enquete.safe_rel("docs/enquetes/2026-10-10-x.md") == "docs/enquetes/2026-10-10-x.md"


# ------------------------------------------------------------------ §3 from a problem

CTX = {"app_name": "Hyrox", "app": "C:/Dev/hyrox", "feature": "f", "cycle": "main",
       "journal": "C:/Dev/hyrox/docs/features/f/journal.md",
       "logs": [("2026-10-08T02:00", "/8_code f", "C:/cockpit/logs/2026-10-08-020000-8_code.jsonl")],
       "files": ["C:/Dev/hyrox/docs/features/f/code/lot-01/blocked_realisateur-01.md"]}


@pytest.mark.parametrize("kind,ask", [
    ("erreur", "Pourquoi cette commande a-t-elle fini en erreur"),
    ("programme", "Pourquoi le programme du pilote automatique"),
    ("blocage", "Pourquoi cet agent bloque-t-il plusieurs fois"),
    ("coût", "beaucoup plus que d'habitude"),
    ("sur place", "relancée plusieurs fois"),
])
def test_the_question_from_each_kind_of_point(kind, ask):
    q = enquete.question_from_point({"kind": kind, "text": "Ce qui est arrivé.", "at": "2026-10-08T02:00"}, CTX)
    assert q["target"] == "chaine"
    t = q["question"]
    assert t.startswith("Pourquoi") and ask in t
    assert "Ce qui s'est passé : Ce qui est arrivé." in t
    assert "Où : l'application « Hyrox » (C:/Dev/hyrox), feature « f », cycle principal." in t
    assert "- le journal de run de /8_code f (08/10 à 02:00) : C:/cockpit/logs/2026-10-08-020000-8_code.jsonl" in t
    assert "- C:/Dev/hyrox/docs/features/f/code/lot-01/blocked_realisateur-01.md" in t
    assert "- le journal de cycle : C:/Dev/hyrox/docs/features/f/journal.md" in t


def test_a_point_whose_run_log_is_elsewhere_says_so():
    q = enquete.question_from_point({"kind": "erreur", "text": "x"}, {**CTX, "logs": [], "cycle": "bugfix-01"})
    assert "correction bugfix-01" in q["question"]
    assert "le journal de run n'est pas sur cet ordinateur" in q["question"]


def test_the_question_from_a_failed_run():
    run = {"prompt": "/8_code f", "started_at": "2026-10-08T02:00:10", "error": "Claude Code n'est pas connecté",
           "log_path": "C:/cockpit/logs/x.jsonl", "relay": "Je n'ai pas pu continuer.\n"}
    q = enquete.question_from_run(run, CTX)
    assert q["target"] == "chaine"
    t = q["question"]
    assert "/8_code f a fini en erreur le 08/10 à 02:00 — « Claude Code n'est pas connecté »." in t
    assert "- le journal de run : C:/cockpit/logs/x.jsonl" in t and "Ses derniers mots : « Je n'ai pas pu continuer. »" in t


# ------------------------------------------------------------------ §4 what follows

def test_the_prompt_file_is_marked_to_be_read_first():
    head = enquete.prompt_file("docs/enquetes/2026-10-10-x.md", "claude-sonnet-5-5")
    assert head.startswith("> **À relire dans la conversation de conception avant de lancer.**\n")
    assert "Le cockpit ne lance jamais une correction de la chaîne ou du cockpit" in head
    assert enquete.prompt_rel("docs/enquetes/2026-10-10-x.md") == "docs/enquetes/2026-10-10-x-prompt.md"
    assert "Quote before changing" in enquete.PROMPT_INSTRUCTION and "Commit and push" in enquete.PROMPT_INSTRUCTION


def test_the_bug_entry_in_the_diagnostiqueurs_format():
    said = ("Observé : le chrono de la Roxzone repart de zéro après une pause.\n"
            "Où : sur l'écran de course\n"
            "Attendu : Elle devrait reprendre où il en était quand la course reprend.")
    f = enquete.bug_fields(said)
    assert f == {"observé": "le chrono de la Roxzone repart de zéro après une pause.",
                 "ou": "sur l'écran de course", "attendu": "Elle devrait reprendre où il en était quand la course reprend."}
    e = enquete.bug_entry(f, 3)
    # .claude/agents/diagnostiqueur.md: `G03 <what the application fails to do>. It should <…>.`
    assert e == ("G03 Sur l'écran de course : le chrono de la Roxzone repart de zéro après une pause. "
                 "Elle devrait reprendre où il en était quand la course reprend.")
    lst = "G01 Le bouton ne répond pas. Elle devrait répondre.\n\nG02 L'export est vide (B4). Elle devrait remplir.\n"
    assert enquete.next_gap(lst) == 3 and enquete.next_gap("") == 1
    assert enquete.renumber("G09 x. Elle devrait y.", 3) == "G03 x. Elle devrait y."
    assert enquete.renumber("x. Elle devrait y.", 3) == "G03 x. Elle devrait y."
    assert enquete.append_gap(lst, "G03 z.") == lst.rstrip() + "\n\nG03 z.\n"
    assert enquete.append_gap("", "G01 z.") == "G01 z.\n"


def test_default_model_is_read_from_claude_codes_settings(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    assert enquete.default_model() is None
    (tmp_path / "settings.json").write_text('{"model": "sonnet"}', encoding="utf-8")
    assert enquete.default_model() == "sonnet"
    os.remove(tmp_path / "settings.json")


def test_her_text_is_printed_whatever_the_consoles_code_page(monkeypatch):
    """A Windows console in cp1252: a character it lacks is replaced, never
    an error that would fail the request that printed it."""
    import io
    import sys
    out = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
    monkeypatch.setattr(sys, "stdout", out)
    line = enquete.console("bug-list.md ← G01 « écart » ≈ 2 ✓")
    print(line)
    assert line == "bug-list.md ? G01 « écart » ? 2 ?"
