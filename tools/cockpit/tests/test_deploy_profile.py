"""1.8 — the deploy profile: the contract's examples load, Hyrox's profile is
the one derived from its /deploie with the lines it cites, what is refused,
and the save — written, committed alone, pushed. Every repository is a
scratch one; nothing reaches GitHub."""
import json
import os
import re

import pytest

import deploy_profile
from conftest import fixture_path
from test_chain import commit, git, init, write

DOC = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                   "docs", "app", "DEPLOY_PROFILE.md")


def doc():
    with open(DOC, encoding="utf-8") as f:
        return f.read()


def examples():
    return [json.loads(m) for m in re.findall(r"```json\n(.*?)\n```", doc(), re.S) if '"targets"' in m]


def test_every_example_of_the_contract_loads():
    ex = examples()
    assert len(ex) == 4                     # two per adapter
    for e in ex:
        targets, errors = deploy_profile.check(e)
        assert not deploy_profile.has_errors(errors), (e, errors)
        assert targets
    assert {t["type"] for e in ex for t in e["targets"]} == {"android", "commande"}


def test_hyrox_profile_is_the_one_derived_from_its_deploie():
    hyrox = examples()[0]
    t = {x["name"]: x for x in hyrox["targets"]}
    assert set(t) == {"Téléphone", "Montre"}
    assert t["Téléphone"]["kind"] == "phone" and t["Montre"]["kind"] == "watch"
    assert t["Téléphone"]["install"] == r".\gradlew.bat :app-phone:installDebug"
    assert t["Montre"]["install"] == r".\gradlew.bat :app-wear:installDebug"
    # No {serial}: the device goes in ANDROID_SERIAL, as deploie.md sets it.
    assert all("{serial}" not in x["install"] for x in t.values())
    assert t["Téléphone"]["build"].endswith(":app-phone:assembleDebug")
    assert {x["app_id"] for x in t.values()} == {"com.mgilli.hyroxtracker"}


def test_the_lines_section_5_cites_say_what_it_reads():
    with open(fixture_path("hyrox", "deploie.md"), encoding="utf-8") as f:
        lines = f.read().splitlines()
    at = lambda n: lines[n - 1]
    assert "Phone" in at(20) and "model:SM_S928B" in at(20)
    assert "Watch" in at(21) and "model:SM_L705F" in at(21)
    assert "ANDROID_SERIAL" in at(42) and ":app-phone:installDebug" in at(43)
    assert "ANDROID_SERIAL" in at(45) and ":app-wear:installDebug" in at(46)
    assert "Remove-Item Env:\\ANDROID_SERIAL" in at(48)
    assert "Do not" in at(28) and "install the other one alone" in at(29)
    text = doc()
    for cite in ("deploie.md:20", "deploie.md:21", "deploie.md:42-43", "deploie.md:45-46", "(:28-30)"):
        assert cite in text


def errors_of(targets, **top):
    _, e = deploy_profile.check({"format": 1, "targets": targets, **top})
    return e


def test_what_is_refused():
    ok = {"name": "Site", "type": "commande", "run": "python -m http.server 8000"}
    assert not deploy_profile.has_errors(errors_of([ok]))
    e = errors_of([{**ok, "port": 8000}])
    assert "clé inconnue" in e["targets"][0]["_"] and "port" in e["targets"][0]["_"]
    assert errors_of([ok, {**ok}])["targets"][1]["name"] == "deux cibles ont ce nom"
    assert errors_of([{**ok, "run": " "}])["targets"][0]["run"] == "obligatoire"
    assert "http" in errors_of([{**ok, "url": "localhost:8000"}])["targets"][0]["url"]
    assert errors_of([{**ok, "keeps_running": "oui"}])["targets"][0]["keeps_running"] == "vrai ou faux attendu"
    assert "type inconnu" in errors_of([{**ok, "type": "ios"}])["targets"][0]["type"]
    a = {"name": "T", "type": "android", "kind": "tablet", "install": "x", "app_id": "pas un id"}
    e = errors_of([a])["targets"][0]
    assert "phone" in e["kind"] and "com.exemple" in e["app_id"]
    assert "format" in errors_of([ok], format=2)["general"][0]
    assert "clé inconnue" in errors_of([ok], extra=1)["general"][0]


def test_load_says_a_file_it_cannot_read(tmp_path):
    assert deploy_profile.load(str(tmp_path)) == {"path": ".claude/deploy.json", "exists": False, "targets": [],
                                                  "errors": {"general": [], "targets": {}}}
    write(tmp_path, ".claude/deploy.json", "{ pas du json")
    p = deploy_profile.load(str(tmp_path))
    assert p["exists"] and p["targets"] == [] and "illisible" in p["errors"]["general"][0]


@pytest.fixture
def app_repo(tmp_path):
    remote = tmp_path / "remote.git"
    git(tmp_path, "init", "-q", "--bare", "-b", "master", str(remote))
    app = tmp_path / "app"
    init(app)
    write(app, "README.md", "app\n")
    commit(app, "first")
    git(app, "remote", "add", "origin", str(remote))
    git(app, "push", "-q", "-u", "origin", "master")
    return app, remote


def test_save_writes_commits_alone_and_pushes(app_repo):
    app, remote = app_repo
    # What she staged stays out of the profile's commit.
    write(app, "notes.md", "à moi\n")
    git(app, "add", "notes.md")
    hyrox = examples()[0]["targets"]
    res = deploy_profile.save(str(app), hyrox)
    assert res["commit"] and res["pushed"] and res["push_error"] is None
    assert git(app, "log", "-1", "--format=%s").strip() == "deploy: profil"
    assert git(app, "show", "--name-only", "--format=", "HEAD").split() == [".claude/deploy.json"]
    assert git(app, "status", "--porcelain").strip() == "A  notes.md"
    assert git(remote, "log", "-1", "--format=%s").strip() == "deploy: profil"
    data = json.loads((app / ".claude" / "deploy.json").read_text(encoding="utf-8"))
    assert data == {"format": 1, "targets": hyrox}
    # The keys in the contract's order.
    assert list(data["targets"][0]) == ["name", "type", "build", "kind", "install", "app_id"]
    # Saved again unchanged: no commit.
    again = deploy_profile.save(str(app), hyrox)
    assert again["commit"] is None
    assert deploy_profile.load(str(app))["targets"] == hyrox


def test_save_refuses_a_profile_that_does_not_hold(app_repo):
    app, _ = app_repo
    with pytest.raises(deploy_profile.ProfileError) as e:
        deploy_profile.save(str(app), [{"name": "", "type": "commande", "run": ""}])
    assert e.value.errors["targets"][0] == {"name": "obligatoire", "run": "obligatoire"}
    assert not (app / ".claude" / "deploy.json").exists()


def test_a_push_that_fails_keeps_the_commit_and_says_why(tmp_path):
    app = tmp_path / "app"
    init(app)
    write(app, "README.md", "app\n")
    commit(app, "first")
    git(app, "remote", "add", "origin", str(tmp_path / "nowhere.git"))
    res = deploy_profile.save(str(app), examples()[2]["targets"])
    assert res["commit"] and not res["pushed"] and res["push_error"]


def test_the_chain_install_never_touches_it():
    import chain
    assert not any(deploy_profile.PATH.startswith(p) for p in chain.PATHS)
