"""The next step, decided in this order — cockpit 1.3, §2:

1. a run is going → that run;
2. a run has just ended → its `Next:`, as printed, trusted without a check;
3. at every other moment, the stored `Next:` is checked against the files:
   it holds → shown, « dit par la chaîne »; `answer …, then run X` with
   nothing left to answer → X, same label; the files contradict it →
   dropped, the scan's proposal takes its place, « déduite du dossier »,
   with « Le dernier relais disait <X> ; les fichiers disent <Y>. »;
4. no stored `Next:` → the scan's proposal, labelled.

Pure: the caller writes the dropped `Next:` to the run's log.
"""
import scan as scan_mod

CHAIN = "dit par la chaîne"
FOLDER = "déduite du dossier"
QUESTION_KINDS = {"questions": {"questions", "technique"},
                  "blocking": {"blocking", "redecoupage"},
                  "questions and blocking": {"questions", "technique", "blocking", "redecoupage"}}


def _chain_steps(sc, chain):
    if chain == "main":
        return sc["main"]
    for c in sc["corrections"]:
        if c["name"] == chain:
            return c["steps"]
    return []


def chain_of(sc, command):
    """Which flow a command acts on: the highest correction cycle for the
    commands whose working folder it is, the main chain otherwise."""
    sid = scan_mod.step_of_command(command)
    hb = next((c["name"] for c in sc["corrections"] if c["highest"]), None)
    if hb and (sid == "diagnostique" or sid in ("7_lots", "8_code", "9_controle")):
        return hb, sid
    if sid == "diagnostique":
        return None, None
    return ("main", sid) if sid else (None, None)


def proposal_next(sc, prop, feature):
    """The scan's proposal (§1.4), as a `Next:` the page can show."""
    if not prop or prop["step"] is None:
        return {"kind": "done", "command": None, "args": "", "french": "Toutes les étapes de la chaîne sont faites."}
    steps = _chain_steps(sc, prop["chain"])
    st = next((s for s in steps if s["id"] == prop["step"]), None)
    why = (st["why"][-1]["text"] if st and st["why"] else "")
    where = "" if prop["chain"] == "main" else f" — {prop['chain']}"
    if prop["state"] == scan_mod.ATTEND:
        kinds = {o["kind"] for o in sc["opens"] if o["id"] in (st or {}).get("waiting", [])}
        q = bool(kinds & {"questions", "technique"})
        b = bool(kinds & {"blocking", "redecoupage"})
        what = "questions and blocking" if q and b else ("blocking" if b else "questions")
        fr = {"questions": "aux questions", "blocking": "aux fichiers de blocage",
              "questions and blocking": "aux questions et aux fichiers de blocage"}[what]
        return {"kind": "answer", "what": what, "command": prop["command"], "args": feature,
                "french": f"Répondre {fr} de « {prop['name']} »{where}, puis lancer /{prop['command']} {feature}."}
    if prop["state"] == scan_mod.A_FAIRE:
        if st and st["why"] and st["why"][-1]["rule"] == "DIA-1":
            # Nothing for /diagnostique to read yet: the bug-list is hers to write.
            return {"kind": "manual", "command": "diagnostique", "args": feature,
                    "text": f"écrire {prop['chain']}/bug-list.md",
                    "french": f"À faire à la main : écrire {prop['chain']}/bug-list.md, puis lancer /diagnostique {feature}."}
        if prop["step"] == "test":
            return {"kind": "manual", "command": None, "args": "",
                    "text": "tester sur l'émulateur, puis décider d'une bug-list ou de /fusion",
                    "french": "À faire à la main : tester sur l'émulateur, puis décider d'une bug-list ou de /fusion."}
        return {"kind": "run", "command": prop["command"], "args": feature,
                "french": f"Lancer /{prop['command']} {feature}{where}."}
    if prop["state"] == scan_mod.BLOQUEE:
        return {"kind": "blocked", "command": None, "args": "",
                "french": f"L'étape « {prop['name']} »{where} est bloquée : {why}"}
    if prop["state"] == scan_mod.EN_COURS:
        return {"kind": "running", "command": prop["command"], "args": feature,
                "french": f"« {prop['name']} » est en cours."}
    return {"kind": "unknown_step", "command": None, "args": "",
            "french": f"Le dossier ne dit pas où en est « {prop['name']} »{where} : {why}"}


def _contradiction(sc, nxt, stored, head_now):
    """The first reason the files contradict a stored `Next:`, or None."""
    if stored.get("head") and head_now and stored["head"] != head_now:
        return ("G-HEAD", f"le dépôt a bougé depuis ce relais sans run du cockpit "
                          f"(HEAD {stored['head'][:7]} → {head_now[:7]})")
    if nxt.get("kind") != "run":
        return None
    chain, sid = chain_of(sc, nxt["command"])
    if not sid:
        return None
    steps = _chain_steps(sc, chain)
    for s in steps:
        if s["id"] == sid:
            last = s["why"][-1] if s["why"] else {"rule": "", "text": ""}
            # `G-AMONT` says no command tests the step past the split; the
            # command that named it just did — /7_lots on /batir when the
            # conventions changed since the last build (cmd/7_lots.md:87-97),
            # in a correction or on a split sent back.
            if s["state"] == scan_mod.FAITE and last["rule"] != "G-AMONT":
                return ("X-FAITE", f"« {s['name']} » a déjà tourné — {last['text']} ({last['rule']})")
            if s["state"] == scan_mod.BLOQUEE:
                return ("X-BLOQUEE", f"« {s['name']} » est bloquée — {last['text']} ({last['rule']})")
            return None
        if s["state"] == scan_mod.ATTEND:
            files = sorted({o["rel"] for o in sc["opens"] if o["id"] in s["waiting"]})
            return ("X-AMONT", f"« {s['name']} », avant /{nxt['command']}, attend des réponses "
                               f"({', '.join(files)[:200]})")
    return None


def decide(sc, feature, run=None, stored=None, fresh=False, head_now=None):
    """§2. `sc` is `scan.run_scan`'s result; `run` the runner's snapshot;
    `stored` the last relay remembered for this feature."""
    prop = sc["proposal"]
    scanned = proposal_next(sc, prop, feature)
    base = {"proposal": prop, "scanned": scanned, "dropped": None, "message": None}

    if run and run.get("status") != "ended":
        sid = scan_mod.step_of_command(run.get("command"))
        return {**base, "source": "run", "label": None,
                "next": {"kind": "running", "command": run.get("command"), "args": run.get("args", ""),
                         "french": f"Une commande tourne : {run.get('prompt')}"},
                "step": sid, "chain": chain_of(sc, run.get("command"))[0]}

    def folder(note=None):
        out = {**base, "source": "dossier", "label": FOLDER, "next": scanned,
               "step": prop.get("step"), "chain": prop.get("chain")}
        if note:
            out["note"] = note
        return out

    if not stored or not stored.get("next"):
        return folder()
    nxt = dict(stored["next"])

    def chain_says(n):
        chain, sid = chain_of(sc, n.get("command")) if n.get("command") else (None, None)
        return {**base, "source": "chaine", "label": CHAIN, "next": n, "step": sid, "chain": chain}

    if fresh:
        return {**chain_says(nxt), "fresh": True}   # 2 — trusted, right after its run
    if nxt.get("kind") == "unknown":
        return folder("Le dernier relais ne finissait pas par une ligne Next:.")

    if nxt.get("kind") == "answer":
        kinds = QUESTION_KINDS.get(nxt.get("what"), set())
        left = [o for o in sc["opens"] if o["kind"] in kinds]
        if not left:
            if not nxt.get("command"):
                return folder("Les réponses demandées par le dernier relais sont enregistrées.")
            nxt = {"kind": "run", "command": nxt["command"], "args": nxt.get("args", ""),
                   "raw": nxt.get("raw", ""), "from_answer": True,
                   "french": f"Lancer /{nxt['command']} {nxt.get('args', '')}".rstrip() + " — les réponses sont enregistrées."}

    bad = _contradiction(sc, nxt, stored, head_now)
    if not bad:
        return chain_says(nxt)
    rule, reason = bad
    said = stored["next"].get("raw") or stored["next"].get("french") or "?"
    out = folder()
    out["dropped"] = {"said": said, "rule": rule, "reason": reason, "says": scanned["french"],
                      "relay_at": stored.get("at"), "relay_command": stored.get("command")}
    out["message"] = f"Le dernier relais disait « {said} » ; les fichiers disent « {scanned['french']} »."
    return out
