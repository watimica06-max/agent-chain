"""« Private: yes », decided by the Product Owner on 7 October 2026: a private
data file, and every copy a lot makes of it, stay out of git
(.claude/formats/donnees.md §2, §6).

No chain command runs. The moves the chain's files now prescribe are played
here by hand, in a real repository and a real worktree, as those files write
them — /8_code carrying the private files in and back, the Testeur's move 3
and move 6, the Réalisateur's move 5 and move 9, the Relecteur's point 4 on
the file list /8_code computes — and each file is checked to say what is
played. The helpers are written from the chain's text alone, independent of
the cockpit's `donnees` module, so that a cockpit bug cannot hide itself."""
import os
import re
import shutil
import subprocess

import pytest

from test_chain import commit, git, init

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CLAUDE = os.path.join(REPO, ".claude")
SECTION = "# Données privées — .claude/formats/donnees.md"
MARK = "— private, ignored, not committed"
WF, LOT = "budget", "lot-03"


def said(rel):
    """A chain file, its whitespace folded: a rule reads the same across a wrap."""
    with open(os.path.join(CLAUDE, *rel.split("/")), encoding="utf-8") as f:
        return " ".join(f.read().split())


# ------------------------------------------------- the chain's text, played

def index_entry(repo, path):
    """The Testeur's and the Réalisateur's read: the entry of the file in the
    index of the folder its path names, by name — `^## <name>$` and the four
    lines after it, that index only."""
    folder, name = path.rsplit("/donnees/", 1)
    lines = (repo / (folder + "/donnees/donnees.md")).read_text(encoding="utf-8").splitlines()
    i = lines.index("## " + name)
    return dict(l.split(": ", 1) for l in lines[i + 1:i + 5])


def private_section(text):
    """§6: the lines after the opening line, to the first blank line or the end."""
    lines = text.splitlines()
    if SECTION not in lines:
        return []
    out = []
    for l in lines[lines.index(SECTION) + 1:]:
        if not l.strip():
            break
        out.append(l)
    return out


def add_to_section(repo, path):
    """The path into the section — created at the end of the file when absent."""
    gi = repo / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if path in private_section(text):
        return
    lines = text.splitlines()
    if SECTION in lines:
        i = lines.index(SECTION) + 1
        while i < len(lines) and lines[i].strip():
            i += 1
        lines.insert(i, path)
    else:
        lines += ["", SECTION, path] if lines else [SECTION, path]
    gi.write_text("\n".join(lines) + "\n", encoding="utf-8")


def copy_lot_data(repo, paths, dest_folder):
    """Testeur move 3 / Réalisateur move 5: before each copy, the entry; one
    `cp` per file, unaltered; a private one's path into the section, never
    staged. Returns the report's lines and what goes under `## Outside the lot`."""
    lines, outside, stage = [], [], []
    for p in paths:
        private = index_entry(repo, p)["Private"] == "yes"
        copy = dest_folder + "/" + p.rsplit("/", 1)[1]
        (repo / copy).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo / p, repo / copy)
        if private:
            add_to_section(repo, copy)
            lines.append(f"{p} → {copy} {MARK}")
            if ".gitignore" not in outside:
                outside.append(".gitignore")
                stage.append(".gitignore")
        else:
            lines.append(f"{p} → {copy}")
            stage.append(copy)
    return lines, outside, stage


def carry_in(main, wt):
    """/8_code, before entering the worktree: each path of the main checkout's
    section that is on disk there, copied to the same path in the worktree."""
    gi = main / ".gitignore"
    for p in private_section(gi.read_text(encoding="utf-8") if gi.exists() else ""):
        if (main / p).is_file():
            (wt / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(main / p, wt / p)


def carry_back(main, wt):
    """/8_code, step 5: each path of the worktree's section on disk in the
    worktree, copied back to the main checkout, then the worktree removed."""
    for p in private_section((wt / ".gitignore").read_text(encoding="utf-8")):
        if (wt / p).is_file():
            (main / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(wt / p, main / p)
    git(main, "worktree", "remove", str(wt))


def relecteur_point4(changed, declared, outside):
    """Point 4 on /8_code's list (`git diff --name-only <first>^ HEAD`): a
    changed file named nowhere is a finding; a copy declared and absent from
    the list is one too — unless it carries the private mark."""
    findings = []
    named = set(outside)
    for line in declared:
        m = re.match(r"^(\S+) → (\S+)( " + re.escape(MARK) + ")?$", line)
        if m:
            named.add(m.group(2))
            if m.group(2) not in changed and not m.group(3):
                findings.append(f"{m.group(2)}: declared, never committed")
        else:
            named.add(line)
    findings += [f"{f}: changed, named nowhere" for f in changed if f not in named]
    return findings


# ------------------------------------------------- the world

@pytest.fixture
def world(tmp_path):
    """An application whose feature holds two reference files — one private,
    kept out of git as the format says — and whose application folder holds
    a private embedded image. The private ones are in no commit."""
    main = tmp_path / "app"
    init(main)
    F = "docs/features/budget/donnees"
    (main / F).mkdir(parents=True)
    (main / F / "releve.csv").write_text("date;montant\n2026-09-14;-720,00\n", encoding="utf-8")
    (main / F / "tarifs.csv").write_text("zone;prix\nA;1,80\n", encoding="utf-8")
    (main / F / "donnees.md").write_text(
        "# Données\n\n## releve.csv\nWhat: a statement\nSource: the bank\nDate: 2026-09-14\nPrivate: yes\n\n"
        "## tarifs.csv\nWhat: the fares\nSource: the operator's site\nDate: 2026-09-01\nPrivate: no\n", encoding="utf-8")
    (main / "docs" / "donnees").mkdir(parents=True)
    (main / "docs" / "donnees" / "logo.png").write_bytes(b"\x89PNG private logo")
    (main / "docs" / "donnees" / "donnees.md").write_text(
        "# Données\n\n## logo.png\nWhat: the client's logo\nSource: the client\nDate: 2026-10-01\nPrivate: yes\n",
        encoding="utf-8")
    (main / ".gitignore").write_text(f"build/\n\n{SECTION}\n{F}/releve.csv\ndocs/donnees/logo.png\n", encoding="utf-8")
    (main / "app" / "src" / "test" / "kotlin").mkdir(parents=True)
    (main / "app" / "src" / "test" / "kotlin" / "ImportTest.kt").write_text("class ImportTest\n", encoding="utf-8")
    commit(main, "init")
    assert "releve.csv" not in git(main, "ls-files") and "logo.png" not in git(main, "ls-files")
    return main, F


def open_worktree(main, tmp_path):
    wt = tmp_path / "wt"
    git(main, "worktree", "add", "-q", "--detach", str(wt), "HEAD")
    return wt


# ------------------------------------------------- the tests

def test_a_private_file_reaches_no_worktree_unless_the_command_carries_it(world, tmp_path):
    main, F = world
    wt = open_worktree(main, tmp_path)
    assert not (wt / F / "releve.csv").exists()           # in no commit
    carry_in(main, wt)
    assert (wt / F / "releve.csv").read_bytes() == (main / F / "releve.csv").read_bytes()
    assert (wt / "docs" / "donnees" / "logo.png").exists()
    assert git(wt, "status", "--porcelain").strip() == ""   # carried, still ignored
    git(main, "worktree", "remove", str(wt))


def test_the_testeur_copy_of_a_private_file_is_ignored_not_staged_not_a_finding(world, tmp_path):
    main, F = world
    wt = open_worktree(main, tmp_path)
    carry_in(main, wt)
    sheet = [F + "/releve.csv", F + "/tarifs.csv"]           # `## Test data`
    created, outside, stage = copy_lot_data(wt, sheet, "app/src/test/resources")
    (wt / "app/src/test/kotlin/ImportTest.kt").write_text("class ImportTest { /* reads the copies */ }\n", encoding="utf-8")
    report = f"docs/features/{WF}/code/{LOT}/tests.md"
    (wt / report).parent.mkdir(parents=True)
    (wt / report).write_text("## Created\n\n" + "\n".join(created) + "\n\n## Outside the lot\n\n" + "\n".join(outside) + "\n",
                             encoding="utf-8")
    # Move 6: staged explicitly — never the private copy, `.gitignore` in its place.
    git(wt, "add", "app/src/test/kotlin/ImportTest.kt", report, *stage)
    git(wt, "commit", "-q", "-m", f"{WF}/{LOT}: tests")
    # Git itself refuses to stage it, should a hand try.
    p = subprocess.run(["git", "-C", str(wt), "add", "app/src/test/resources/releve.csv"], capture_output=True, text=True)
    assert p.returncode != 0 and "ignored" in p.stderr
    assert "!! app/src/test/resources/releve.csv" in git(wt, "status", "--porcelain", "--ignored")
    assert git(wt, "status", "--porcelain").strip() == ""   # clean: step 1 has nothing left, the remove holds
    # /8_code's list for the Relecteur.
    first = git(wt, "log", "--reverse", "--format=%H", "-1", "--grep", f"^{WF}/{LOT}: ").strip()
    changed = git(wt, "diff", "--name-only", f"{first}^", "HEAD").split()
    assert "app/src/test/resources/tarifs.csv" in changed       # non-private: committed as before
    assert "app/src/test/resources/releve.csv" not in changed
    assert ".gitignore" in changed
    assert private_section((wt / ".gitignore").read_text(encoding="utf-8"))[-1] == "app/src/test/resources/releve.csv"
    declared = created + ["app/src/test/kotlin/ImportTest.kt", report]
    assert relecteur_point4(changed, declared, outside) == []
    # Without the mark, the absent copy is a finding; `.gitignore` unnamed is one too.
    unmarked = [l.replace(" " + MARK, "") for l in created]
    assert relecteur_point4(changed, unmarked + declared[2:], outside) == [
        "app/src/test/resources/releve.csv: declared, never committed"]
    assert relecteur_point4(changed, declared, []) == [".gitignore: changed, named nowhere"]
    # Step 5: the copies back in the main checkout, then the worktree removed —
    # which deletes what git ignores.
    sha = git(wt, "rev-parse", "HEAD").strip()
    git(main, "merge", "-q", "--no-ff", "-m", f"Merge /8_code {WF}", sha)
    carry_back(main, wt)
    assert not wt.exists()
    assert (main / "app/src/test/resources/releve.csv").read_text(encoding="utf-8").startswith("date;montant")
    assert git(main, "check-ignore", "app/src/test/resources/releve.csv").strip() == "app/src/test/resources/releve.csv"
    assert "releve.csv" not in git(main, "log", "--all", "--name-only", "--format=").replace(F + "/releve.csv", "")
    # The next run's worktree gets the copy too: the test runs where the file is.
    wt2 = open_worktree(main, tmp_path)
    carry_in(main, wt2)
    assert (wt2 / "app/src/test/resources/releve.csv").exists()
    git(main, "worktree", "remove", str(wt2))


def test_without_the_carry_back_the_copy_is_lost(world, tmp_path):
    main, F = world
    wt = open_worktree(main, tmp_path)
    carry_in(main, wt)
    copy_lot_data(wt, [F + "/releve.csv"], "app/src/test/resources")
    git(wt, "add", ".gitignore")
    git(wt, "commit", "-q", "-m", f"{WF}/{LOT}: tests")
    git(main, "merge", "-q", "--no-ff", "-m", "m", git(wt, "rev-parse", "HEAD").strip())
    git(main, "worktree", "remove", str(wt))                  # a plain remove: no refusal
    assert not (main / "app/src/test/resources/releve.csv").exists()


def test_the_realisateur_copy_of_a_private_resource(world, tmp_path):
    main, F = world
    wt = open_worktree(main, tmp_path)
    carry_in(main, wt)
    resources, outside, stage = copy_lot_data(wt, ["docs/donnees/logo.png"], "app/src/main/res/drawable")
    assert resources == [f"docs/donnees/logo.png → app/src/main/res/drawable/logo.png {MARK}"] and stage == [".gitignore"]
    git(wt, "add", *stage)
    git(wt, "commit", "-q", "-m", f"{WF}/{LOT}: bodies")
    assert git(wt, "show", "--name-only", "--format=", "HEAD").split() == [".gitignore"]
    assert relecteur_point4([".gitignore"], resources, outside) == []
    git(main, "merge", "-q", "--no-ff", "-m", "m", git(wt, "rev-parse", "HEAD").strip())
    carry_back(main, wt)
    assert (main / "app/src/main/res/drawable/logo.png").read_bytes() == b"\x89PNG private logo"


# ------------------------------------------------- the files say it

def test_the_format_says_private_means_out_of_git_copies_included():
    f = said("formats/donnees.md")
    assert "The file, and every copy a lot makes of it, stay out of git" in f
    assert "never copies a value from it into a document the chain writes" in f      # 1/2's rule kept
    assert "A test built on it runs only where the file is" in f
    assert "the copies a lot makes of it — into a test folder, into a resource folder — are files, not documents" not in f.lower()
    assert "## 6. Out of git — the private section of `.gitignore`" in f
    assert SECTION in f and "never a pattern, never a folder" in f
    assert "`git worktree remove` deletes what git ignores" in f


@pytest.mark.parametrize("agent,move,field", [("testeur", "move 3", "## Created"), ("realisateur", "move 5", "## Resources")])
def test_the_two_copying_agents_read_the_entry_and_keep_a_private_copy_out(agent, move, field):
    f = said(f"agents/{agent}.md")
    assert "The entry of each of those files in its index" in f
    assert "the `donnees.md` of the folder the file's path names, by the file's name, that index only" in f
    assert f"its `Private:` line, read before the copy of {move}" in f
    assert "Before each copy, read the file's entry in its index" in f
    assert "the copy's path goes into the private section of `.gitignore`" in f
    assert "the copy is never staged" in f
    assert "Stage a private copy" in f
    assert "`.gitignore` is written with `Edit`" in f
    assert f"`{MARK}`" in f
    assert "declared like any file you modified" in f or "declared here like any file you modified" in f
    assert "never a `donnees/` folder, never its `donnees.md`" not in f.lower()


def test_the_testeur_skips_a_test_whose_private_copy_is_absent():
    f = said("agents/testeur.md")
    assert "A test that reads a private copy is skipped where the copy is absent, never failed" in f


def test_the_relecteur_reads_a_private_copy_as_no_finding():
    f = said("agents/relecteur.md")
    assert f"A copy followed by `{MARK}`" in f
    assert "is declared and absent from the list" in f and "not a finding" in f
    assert "The `.gitignore` the list names for it is checked like any changed file" in f
    assert "A copy not marked private and absent from the list is a finding of this point" in f


@pytest.mark.parametrize("command", ["8_code", "6_convertit"])
def test_the_commands_whose_agents_open_data_carry_the_private_files_in(command):
    f = said(f"commands/{command}.md")
    assert "Before entering it, carry the private files in" in f
    assert "the private section of the main checkout's `.gitignore` lists" in f


def test_8_code_carries_them_back_before_every_removal():
    f = said("commands/8_code.md")
    assert "Carry the private files back, then `git worktree remove <path>`" in f
    assert "The private files back, then `git worktree remove <path>` — as step 5 of *Git, once it has reported*" in f
