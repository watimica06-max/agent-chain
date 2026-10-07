"""1.10 — « Données »: the index in `.claude/formats/donnees.md`'s format, a
file joined, an entry edited, a file removed with its entry, a private file
kept out of git — new, and already committed —, the commit and what it
leaves alone; « Joindre un fichier » on a question carrying `Folder:`, its
answer as §5 writes it and read as answered by the command's own test. Every
repository is a scratch one; nothing is pushed."""
import base64
import json

import pytest

import donnees
import server
from cmdtests import unanswered_questions
from donneesworld import FEATURE_INDEX, RELEVE, data_world, png
from test_chain import commit, git, init
from test_server import open_pair, post, with_client

F = "docs/features/f/donnees"


@pytest.fixture(autouse=True)
def _no_push(monkeypatch):
    monkeypatch.setattr(server, "DONNEES_PUSH", False)


def b64(data):
    return base64.b64encode(data).decode()


def entry(name, private="no", **kw):
    return {"name": name, "what": kw.get("what", f"what {name} is"), "source": kw.get("source", "the Product Owner"),
            "date": kw.get("date", "2026-10-07"), "private": private}


def section(app_root):
    return donnees.section_paths((app_root / ".gitignore").read_text(encoding="utf-8"))


def tracked(app_root):
    return set(git(app_root, "ls-files").split())


# ------------------------------------------------------------ the format

def test_the_index_reads_and_writes_in_the_format():
    entries, errors = donnees.parse_index(FEATURE_INDEX)
    assert not errors
    assert [e.to_dict() for e in entries] == [{
        "name": "releve-2026-09-14.csv", "what": "a statement of operations, as the bank's site exports it",
        "source": "exported from the bank's account page, by the Product Owner", "date": "2026-09-14",
        "private": "no"}]
    assert donnees.index_text(entries) == FEATURE_INDEX
    # §2: every line, in that order — an absent line and a forgotten one read the same.
    _, errors = donnees.parse_index("# Données\n\n## a.csv\nWhat: x\nDate: 2026-01-01\nSource: y\nPrivate: maybe\n")
    assert any("Source:" in e for e in errors) and any("yes ou no" in e for e in errors)
    _, errors = donnees.parse_index("## a.csv\nWhat: x\nSource: y\nDate: 2026-01-01\nPrivate: no\n")
    assert errors == ["le titre « # Données » manque"]
    # An index with no entry is its title alone.
    assert donnees.index_text([]) == "# Données\n"


def test_the_private_section_of_gitignore():
    text = "build/\n*.log\n"
    a = donnees.with_section(text, add=["docs/donnees/x.png"])
    assert a == "build/\n*.log\n\n# Données privées — .claude/formats/donnees.md\ndocs/donnees/x.png\n"
    b = donnees.with_section(a, add=["docs/donnees/x.png", "app/src/test/resources/x.png"])
    assert donnees.section_paths(b) == ["docs/donnees/x.png", "app/src/test/resources/x.png"]
    assert b.count(donnees.SECTION) == 1                       # never twice
    # A line out of the section stays; the section empty goes with its title.
    c = donnees.with_section(b + "\ndist/\n", drop=["docs/donnees/x.png", "app/src/test/resources/x.png"])
    assert c == "build/\n*.log\n\ndist/\n"
    assert donnees.with_section("a\r\n", add=["p"]) == "a\r\n\r\n" + donnees.SECTION + "\r\np\r\n"


def test_a_question_marker_names_one_of_the_two_folders(tmp_path):
    (tmp_path / "docs" / "features" / "f").mkdir(parents=True)
    assert donnees.folder_of_marker(str(tmp_path), "docs/features/f/donnees/") == F
    assert donnees.folder_of_marker(str(tmp_path), "docs/donnees/") == "docs/donnees"
    for bad in ("docs/features/g/donnees/", "docs/features/f/donnees", "docs/autre/", "../x/"):
        with pytest.raises(donnees.DataError):
            donnees.folder_of_marker(str(tmp_path), bad)


@pytest.mark.parametrize("name", ["", " a.csv", "a/b.csv", "a\\b.csv", "donnees.md", "#a.csv", "!a.csv",
                                  "a[1].csv", "a*.csv", "a?.csv", "a.csv."])
def test_a_name_that_is_not_one_file_is_refused(name):
    with pytest.raises(donnees.DataError):
        donnees.check_name(name)


# ------------------------------------------------------------ « Données »

def test_join_edit_remove_and_the_commit(tmp_path):
    async def body(c, app_root, feat, rn):
        data_world(app_root, question=False)
        # What she staged herself stays staged, and out of the commit.
        (app_root / "brouillon.txt").write_text("x", encoding="utf-8")
        git(app_root, "add", "brouillon.txt")
        await open_pair(c, app_root)
        r = await c.get("/api/donnees?tab=feature")
        d = await r.json()
        assert d["folder"] == F + "/" and [e["name"] for e in d["entries"]] == ["releve-2026-09-14.csv"]
        assert d["entries"][0]["kind"] == "text" and d["entries"][0]["tracked"] and not d["running"]
        # Joined: copied as it came, not in the index until « Enregistrer ».
        r = await post(c, "/api/donnees/join", {"tab": "feature", "name": "export.json", "data": b64(b'{"a": 1}\n')})
        assert r.status == 200, await r.text()
        assert (app_root / F / "export.json").read_bytes() == b'{"a": 1}\n'
        d = await (await c.get("/api/donnees?tab=feature")).json()
        assert [x["name"] for x in d["loose"]] == ["export.json"]
        r = await post(c, "/api/donnees/join", {"tab": "feature", "name": "export.json", "data": b64(b"{}")})
        assert r.status == 409 and (await r.json())["exists"]
        # Incomplete: refused, nothing written.
        r = await post(c, "/api/donnees/save", {"tab": "feature", "entries": [
            {**entry("releve-2026-09-14.csv"), "what": "a statement"}, {**entry("export.json"), "source": ""}]})
        assert r.status == 400 and "Source:" in (await r.json())["error"]
        assert (app_root / F / "donnees.md").read_text(encoding="utf-8") == FEATURE_INDEX
        r = await post(c, "/api/donnees/save", {"tab": "feature", "entries": [
            {**entry("releve-2026-09-14.csv", date="2026-09-14"), "what": "a statement"}, entry("export.json")]})
        res = await r.json()
        assert r.status == 200, res
        assert res["message"] == "donnees: export.json joint, releve-2026-09-14.csv modifié"
        assert git(app_root, "log", "-1", "--format=%s").strip() == res["message"]
        assert set(git(app_root, "show", "--name-only", "--format=", "HEAD").split()) == {
            F + "/donnees.md", F + "/export.json"}
        assert "A  brouillon.txt" in git(app_root, "status", "--porcelain")
        idx = (app_root / F / "donnees.md").read_text(encoding="utf-8")
        assert idx.startswith("# Données\n\n## releve-2026-09-14.csv\nWhat: a statement\n")
        assert "## export.json\nWhat: what export.json is\nSource: the Product Owner\nDate: 2026-10-07\nPrivate: no\n" in idx
        assert not donnees.parse_index(idx)[1]
        # Removed: the file and its entry, together.
        r = await post(c, "/api/donnees/save", {"tab": "feature", "entries": [
            {**entry("releve-2026-09-14.csv", date="2026-09-14"), "what": "a statement"}], "removed": ["export.json"]})
        res = await r.json()
        assert res["message"] == "donnees: export.json retiré"
        assert not (app_root / F / "export.json").exists() and "export.json" not in (app_root / F / "donnees.md").read_text(encoding="utf-8")
        assert F + "/export.json" not in tracked(app_root)
        # Nothing changed: no commit.
        head = git(app_root, "rev-parse", "HEAD")
        r = await post(c, "/api/donnees/save", {"tab": "feature", "entries": [
            {**entry("releve-2026-09-14.csv", date="2026-09-14"), "what": "a statement"}]})
        assert (await r.json())["commit"] is None and git(app_root, "rev-parse", "HEAD") == head
    with_client(tmp_path, body)


def test_private_a_new_file_and_one_already_committed(tmp_path):
    async def body(c, app_root, feat, rn):
        data_world(app_root, question=False)
        await open_pair(c, app_root)
        await post(c, "/api/donnees/join", {"tab": "feature", "name": "releve-2026-10-01.csv", "data": b64(RELEVE.encode())})
        r = await post(c, "/api/donnees/save", {"tab": "feature", "entries": [
            entry("releve-2026-09-14.csv", private="yes", date="2026-09-14"),
            entry("releve-2026-10-01.csv", private="yes")]})
        res = await r.json()
        assert r.status == 200, res
        # The new one never committed; the committed one out of git's index,
        # and the page told it stays in the history.
        assert res["history"] == ["releve-2026-09-14.csv"]
        assert section(app_root) == [F + "/releve-2026-09-14.csv", F + "/releve-2026-10-01.csv"]
        files = tracked(app_root)
        assert F + "/releve-2026-09-14.csv" not in files and F + "/releve-2026-10-01.csv" not in files
        assert (app_root / F / "releve-2026-09-14.csv").exists() and (app_root / F / "releve-2026-10-01.csv").exists()
        assert set(git(app_root, "show", "--name-status", "--format=", "HEAD").splitlines()) == {
            "M\t.gitignore", "M\t" + F + "/donnees.md", "D\t" + F + "/releve-2026-09-14.csv"}
        assert git(app_root, "status", "--porcelain").strip() == ""
        assert git(app_root, "check-ignore", F + "/releve-2026-10-01.csv").strip() == F + "/releve-2026-10-01.csv"
        # It stays in the history.
        assert "2026-09-14;VIR INSTANTANE LOYER" in git(app_root, "show", "HEAD~1:" + F + "/releve-2026-09-14.csv")
        d = await (await c.get("/api/donnees?tab=feature")).json()
        assert [(e["name"], e["private"], e["ignored"], e["tracked"]) for e in d["entries"]] == [
            ("releve-2026-09-14.csv", "yes", True, False), ("releve-2026-10-01.csv", "yes", True, False)]
        # No longer private: its line leaves the section, the file is committed.
        r = await post(c, "/api/donnees/save", {"tab": "feature", "entries": [
            entry("releve-2026-09-14.csv", private="yes", date="2026-09-14"), entry("releve-2026-10-01.csv")]})
        res = await r.json()
        assert res["message"] == "donnees: releve-2026-10-01.csv n'est plus privé"
        assert section(app_root) == [F + "/releve-2026-09-14.csv"] and F + "/releve-2026-10-01.csv" in tracked(app_root)
    with_client(tmp_path, body)


def test_the_app_tab_previews_text_and_image(tmp_path):
    async def body(c, app_root, feat, rn):
        data_world(app_root, question=False)
        await open_pair(c, app_root)
        d = await (await c.get("/api/donnees?tab=app")).json()
        assert d["folder"] == "docs/donnees/" and d["entries"][0]["kind"] == "image"
        r = await c.get("/api/donnees/file?tab=app&name=fleche.png")
        assert r.status == 200 and r.content_type == "image/png" and (await r.read()) == png()
        p = await (await c.get("/api/donnees/preview?tab=feature&name=releve-2026-09-14.csv")).json()
        assert p["kind"] == "text" and p["lines"][0] == "date;libellé;montant;catégorie" and not p["truncated"]
        r = await c.get("/api/donnees/file?tab=app&name=../../.gitignore")
        assert r.status == 404
        r = await c.get("/api/donnees?tab=autre")
        assert r.status == 400
    with_client(tmp_path, body)


def test_refused_while_a_run_goes_in_the_application(tmp_path):
    async def body(c, app_root, feat, rn):
        data_world(app_root)
        await open_pair(c, app_root)
        r = await post(c, "/api/run", {"command": "1_lexique", "args": "f"})
        assert r.status == 200
        d = await (await c.get("/api/donnees?tab=feature")).json()
        assert d["running"]
        r = await post(c, "/api/donnees/save", {"tab": "feature", "entries": [entry("releve-2026-09-14.csv")]})
        assert r.status == 409 and "/1_lexique f" in (await r.json())["error"]
        forms = await (await c.get("/api/forms")).json()
        q4 = next(q for q in forms["questions"] if q["number"] == 4 and q["rel"] == "questions-sondeur-02.md")
        r = await post(c, "/api/donnees/answer", {"id": q4["id"], "fingerprint": q4["fingerprint"], "name": "r.csv",
                                                  "data": b64(b"x"), "entry": entry("r.csv")})
        assert r.status == 409
        assert git(app_root, "log", "--format=%s").split("\n")[0] == "init"
        await rn.stop_now(str(app_root))
        await rn.wait_ended(str(app_root), 5)
    with_client(tmp_path, body)


# ------------------------------------------------------------ « À répondre »

def test_a_question_with_folder_takes_a_file(tmp_path):
    async def body(c, app_root, feat, rn):
        data_world(app_root)
        await open_pair(c, app_root)
        forms = await (await c.get("/api/forms")).json()
        q4 = next(q for q in forms["questions"] if q["number"] == 4 and q["rel"] == "questions-sondeur-02.md")
        assert q4["folder"] == {"folder": F + "/", "error": None}
        # The question's other options stay; the others carry no folder.
        assert q4["options"] == ["Le relevé n'existe pas encore : le bloc dit qu'il manque."]
        assert all(q["folder"] is None for q in forms["questions"] if q["id"] != q4["id"])
        qfile = feat / "questions-sondeur-02.md"
        assert 4 in unanswered_questions(str(qfile))
        r = await post(c, "/api/donnees/answer", {"id": q4["id"], "fingerprint": q4["fingerprint"],
                                                  "name": "releve-2026-09-30.csv", "data": b64(RELEVE.encode()),
                                                  "entry": entry("releve-2026-09-30.csv", private="yes")})
        res = await r.json()
        assert r.status == 200, res
        # The file in the folder the marker names, as it came; its entry in the index.
        assert (app_root / F / "releve-2026-09-30.csv").read_bytes() == RELEVE.encode()
        entries, errors = donnees.parse_index((app_root / F / "donnees.md").read_text(encoding="utf-8"))
        assert not errors and [e.name for e in entries] == ["releve-2026-09-14.csv", "releve-2026-09-30.csv"]
        assert entries[1].private == "yes" and section(app_root) == [F + "/releve-2026-09-30.csv"]
        assert res["message"] == "donnees: releve-2026-09-30.csv joint, privé — questions-sondeur-02.md Q4"
        assert F + "/releve-2026-09-30.csv" not in tracked(app_root)
        # §5: the answer names the file, as the index names it.
        text = qfile.read_text(encoding="utf-8")
        q = text[text.index("### Q4"):]
        assert q.splitlines()[-1] == "Answer: releve-2026-09-30.csv"
        assert "Folder: docs/features/f/donnees/" in q
        # The command's own test reads it as answered.
        assert 4 not in unanswered_questions(str(qfile))
        forms = await (await c.get("/api/forms")).json()
        assert not any(q["id"] == q4["id"] for q in forms["questions"])
    with_client(tmp_path, body)


def test_the_marker_to_the_application_folder_and_refusals(tmp_path):
    async def body(c, app_root, feat, rn):
        data_world(app_root)
        qfile = feat / "questions-sondeur-02.md"
        qfile.write_text(qfile.read_text(encoding="utf-8").replace("Folder: docs/features/f/donnees/", "Folder: docs/donnees/")
                         + "\n### Q5\nBlock: B8\nFolder: docs/ailleurs/\nQuestion: Which?\nAnswer:\n", encoding="utf-8")
        git(app_root, "add", "-A")
        git(app_root, "commit", "-q", "-m", "q")
        await open_pair(c, app_root)
        forms = await (await c.get("/api/forms")).json()
        by = {q["number"]: q for q in forms["questions"] if q["rel"] == "questions-sondeur-02.md"}
        assert by[4]["folder"]["folder"] == "docs/donnees/"
        assert by[5]["folder"]["folder"] is None and "docs/ailleurs/" in by[5]["folder"]["error"]
        r = await post(c, "/api/donnees/answer", {"id": by[5]["id"], "fingerprint": by[5]["fingerprint"],
                                                  "name": "x.png", "data": b64(png()), "entry": entry("x.png")})
        assert r.status == 400
        # A question with no marker takes no file.
        q1 = by[1]
        r = await post(c, "/api/donnees/answer", {"id": q1["id"], "fingerprint": q1["fingerprint"], "name": "x.png",
                                                  "data": b64(png()), "entry": entry("x.png")})
        assert r.status == 400 and "ne demande pas" in (await r.json())["error"]
        # An entry not filled: nothing written.
        r = await post(c, "/api/donnees/answer", {"id": by[4]["id"], "fingerprint": by[4]["fingerprint"],
                                                  "name": "fleche.png", "data": b64(png()), "entry": {**entry("fleche.png"), "date": "hier"}})
        assert r.status == 400
        # A name already there asks first.
        r = await post(c, "/api/donnees/answer", {"id": by[4]["id"], "fingerprint": by[4]["fingerprint"],
                                                  "name": "fleche.png", "data": b64(png(10, 10)), "entry": entry("fleche.png")})
        assert r.status == 409 and (await r.json())["exists"]
        assert (app_root / "docs" / "donnees" / "fleche.png").read_bytes() == png()
        r = await post(c, "/api/donnees/answer", {"id": by[4]["id"], "fingerprint": by[4]["fingerprint"],
                                                  "name": "fleche.png", "data": b64(png(10, 10)), "entry": entry("fleche.png"),
                                                  "replace": True})
        res = await r.json()
        assert r.status == 200, res
        assert (app_root / "docs" / "donnees" / "fleche.png").read_bytes() == png(10, 10)
        assert git(app_root, "show", "--name-only", "--format=", "HEAD").split() == [
            "docs/donnees/donnees.md", "docs/donnees/fleche.png"]
        assert 4 not in unanswered_questions(str(qfile))
    with_client(tmp_path, body)


def test_a_large_file_is_accepted(tmp_path):
    async def body(c, app_root, feat, rn):
        data_world(app_root, question=False)
        await open_pair(c, app_root)
        big = b"x;y\n" * (3 * 1024 * 1024 // 4)
        r = await c.post("/api/donnees/join", data=json.dumps({"tab": "feature", "name": "gros.csv", "data": b64(big)}),
                         headers={"Content-Type": "application/json"})
        assert r.status == 200, await r.text()
        assert (app_root / F / "gros.csv").stat().st_size == len(big)
    with_client(tmp_path, body)


def test_a_repository_with_crlf_keeps_its_line_endings(tmp_path):
    app = tmp_path / "a"
    init(app, crlf=True)
    (app / F).mkdir(parents=True)
    (app / ".gitignore").write_bytes(b"build/\r\n")
    (app / F / "a.csv").write_bytes(b"x\n")
    commit(app, "init")
    res = donnees.save(str(app), F, [entry("a.csv", private="yes")], push=False)
    assert res["commit"]
    assert (app / F / "donnees.md").read_bytes().startswith(b"# Donn\xc3\xa9es\r\n\r\n## a.csv\r\n")
    assert (app / ".gitignore").read_bytes().endswith(b"\r\n" + F.encode() + b"/a.csv\r\n")
