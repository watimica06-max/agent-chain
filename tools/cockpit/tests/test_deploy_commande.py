"""1.8 — the `commande` adapter, for real on this machine: a target whose run
command is `python -m http.server <free port>` on a scratch folder, with its
URL — deployed, its output in the journal, « Ouvrir » offered, a traceback
marked, « Arrêter » stops it. And a script, which ends."""
import socket
import struct
import sys
import time
import urllib.request

import pytest

import deploy
from adapters import commande
from deployworld import write_profile
from state import State

PY = f'"{sys.executable}"'
DEST = "commande:local"


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait(pred, timeout=15.0):
    t0 = time.monotonic()
    while time.monotonic() - t0 < timeout:
        if pred():
            return True
        time.sleep(0.1)
    return False


def answers(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2) as r:
            return r.status == 200
    except OSError:
        return False


@pytest.fixture
def site(tmp_path):
    app = tmp_path / "app"
    (app / "www").mkdir(parents=True)
    (app / "www" / "index.html").write_text("<h1>Site</h1>", encoding="utf-8")
    (app / "www" / "gros.bin").write_bytes(b"\0" * (64 * 1024 * 1024))
    port = free_port()
    write_profile(app, [
        {"name": "Site", "type": "commande", "build": f'{PY} -c "print(\'build du site\')"',
         "run": f"{PY} -m http.server {port} --bind 127.0.0.1 --directory www", "keeps_running": True,
         "url": f"http://127.0.0.1:{port}/"},
        {"name": "Script", "type": "commande", "run": f'{PY} -c "raise ValueError(\'boum\')"'},
    ])
    dep = deploy.Deployer(State(str(tmp_path / "config.json")), str(tmp_path / "logs"))
    events = []
    dep.emit = lambda kind, data: events.append((kind, data))
    yield str(app), port, dep, events
    dep.stop_all()


def card(dep, app):
    g = next(g for g in dep.destinations(app)["groups"] if g["type"] == "commande")
    (d,) = g["destinations"]
    return d


def run_job(dep, app, choice):
    job = dep.start(app, "site", choice)
    assert wait(lambda: job.status != "en cours", 60)
    return job.record()


def reset_request(port):
    """Asks for the big file and drops the connection at once (RST): the
    server's write fails, and socketserver prints a traceback."""
    s = socket.create_connection(("127.0.0.1", port), timeout=5)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    s.sendall(b"GET /gros.bin HTTP/1.0\r\n\r\n")
    s.recv(1024)
    s.close()


def test_a_server_deployed_followed_opened_and_stopped(site):
    app, port, dep, events = site
    d = card(dep, app)
    assert d["name"] == "cet ordinateur" and d["connected"]
    assert dict(d["facts"])["Site"] == "pas lancée depuis l'ouverture du cockpit"
    # Not declared: no screenshot, no mirror.
    assert {a["id"] for a in d["actions"]} == {"journal"}
    rec = run_job(dep, app, {"Site": [DEST]})
    assert [(s["kind"], s["label"], s["status"]) for s in rec["steps"]] == [("build", "Construire", "fait"),
                                                                           ("deploy", "Lancer", "fait")]
    assert rec["steps"][1]["detail"].startswith("en marche (pid ") and f":{port}/" in rec["steps"][1]["detail"]
    assert answers(port)
    # « Ouvrir » offered while it runs, with its URL; « Arrêter » too.
    d = card(dep, app)
    acts = {a["id"]: a for a in d["actions"]}
    assert acts["open"]["kind"] == "link" and acts["open"]["url"] == f"http://127.0.0.1:{port}/"
    assert acts["stop"]["args"] == {"target": "Site"}
    assert "en marche depuis" in dict(d["facts"])["Site"]
    # Its output is the journal.
    j = lambda after=0: dep.journal(app, "commande", DEST, "Site", after)
    assert wait(lambda: any(f'"GET / HTTP/1.1" 200' in x["text"] for x in j()["lines"]))
    assert j()["live"]
    # A traceback, marked as a crash.
    for _ in range(5):
        reset_request(port)
        if wait(lambda: j()["crashes"], 5):
            break
    # socketserver's « Exception occurred … » and the traceback under it: one
    # crash, titled by the exception it ends on.
    assert wait(lambda: j()["crashes"][0]["title"].startswith(("ConnectionResetError", "ConnectionAbortedError")))
    c = j()["crashes"][0]
    assert c["lines"][0].startswith("Exception occurred during processing of request")
    assert c["lines"][1] == "Traceback (most recent call last):" and c["lines"][-1] == c["title"]
    assert any(k == "deploy_crash" and x["dest_name"] == "cet ordinateur" and x["target"] == "Site" for k, x in events)
    assert any(x["crash"] == c["id"] for x in j()["lines"])
    # « Arrêter » stops it, with what it started.
    assert dep.act(app, "commande", "stop", DEST, {"target": "Site"})["message"] == "« Site » arrêtée."
    assert wait(lambda: not answers(port), 10)
    assert dict(card(dep, app)["facts"])["Site"] == "arrêtée"
    assert "open" not in {a["id"] for a in card(dep, app)["actions"]}
    tail = j()
    assert not tail["live"] and tail["lines"][-1]["text"] == "— arrêtée depuis le cockpit —"
    with pytest.raises(commande.ActionError, match="ne tourne pas"):
        dep.act(app, "commande", "stop", DEST, {"target": "Site"})


def test_deployed_again_it_restarts_and_keeps_its_log(site):
    app, port, dep, _ = site
    run_job(dep, app, {"Site": [DEST]})
    first = dep.adapters["commande"].procs[commande._key(app, "Site")].popen.pid
    rec = run_job(dep, app, {"Site": [DEST]})
    assert rec["status"] == "fait"
    p = dep.adapters["commande"].procs[commande._key(app, "Site")]
    assert p.popen.pid != first and answers(port)
    text = [x["text"] for x in dep.journal(app, "commande", DEST, "Site")["lines"]]
    assert sum(1 for x in text if "· $ " in x) == 2


def test_a_script_ends_and_its_exit_code_is_its_result(site):
    app, port, dep, _ = site
    rec = run_job(dep, app, {"Script": [DEST]})
    (s,) = rec["steps"]
    assert (s["label"], s["status"], s["detail"]) == ("Exécuter", "échec", "code 1")
    assert s["tail"][-1] == "ValueError: boum"
    j = dep.journal(app, "commande", DEST, "Script")
    (c,) = j["crashes"]
    assert c["title"] == "ValueError: boum" and len(c["lines"]) >= 3


def test_a_server_that_ends_at_once_has_failed(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    write_profile(app, [{"name": "Site", "type": "commande", "run": f'{PY} -c "print(\'adresse prise\')"',
                         "keeps_running": True}])
    dep = deploy.Deployer(State(str(tmp_path / "c.json")), str(tmp_path / "logs"))
    rec = run_job(dep, str(app), {"Site": [DEST]})
    (s,) = rec["steps"]
    assert s["status"] == "échec" and "aussitôt" in s["detail"] and s["tail"] == ["adresse prise"]


def test_error_lines_at_the_start_of_a_line():
    from adapters.base import LogStream
    st = LogStream(commande.CommandeAdapter.CRASHES)
    for x in ["ok", "Error: listen EADDRINUSE: address already in use :::8000", "    at Server.listen (net.js:1)",
              "suite", "  Error: indented is not one", "TypeError: x is undefined", "Exception in thread main"]:
        st.add(x)
    c = st.since()["crashes"]
    assert [x["title"] for x in c] == ["Error: listen EADDRINUSE: address already in use :::8000",
                                       "TypeError: x is undefined", "Exception in thread main"]
    assert c[0]["lines"][1].strip().startswith("at Server.listen")
