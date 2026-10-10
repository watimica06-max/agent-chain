"""Several applications — TECHNICAL_V1 §21 (1.6).

What the cockpit asks an application's repository for the « Applications »
screen, and « Tout mettre à jour ». Read-only, but for the bulk update, which
is chain.py's install, one application after the other.

- Adding one never writes in its folder: config.json alone. It must be the
  root of a git repository — what an install needs to commit there.
- Uncommitted changes are counted, as information: the cockpit never
  touches them, and the install refuses its own files when they have some.
- « Tout mettre à jour » updates what is « en retard » only. « modifiée sur
  place » and « absente » are listed with their reason: their own install
  asks before replacing anything, and is run from their row.
"""
import os
import subprocess

import chain as chain_mod
import sync

GIT_TIMEOUT = 30


def _git(folder, *args, timeout=GIT_TIMEOUT):
    env = sync.env()
    return subprocess.run(["git", "-C", folder, "-c", "core.quotepath=off", *args], capture_output=True,
                          timeout=timeout, env=env, stdin=subprocess.DEVNULL)


def check_new_app(folder):
    """Why `folder` cannot join the list, in French — or None."""
    if not folder or not os.path.isdir(folder):
        return "dossier introuvable"
    try:
        p = _git(folder, "rev-parse", "--show-toplevel")
    except (OSError, subprocess.SubprocessError) as e:
        return f"git ne répond pas ({e})"
    if p.returncode:
        return "ce dossier n'est pas un dépôt git : la chaîne s'y installe par un commit"
    top = p.stdout.decode("utf-8", "replace").strip()
    if os.path.normcase(os.path.abspath(top)) != os.path.normcase(os.path.abspath(folder)):
        return f"ce dossier est dans un dépôt git sans en être la racine ({os.path.normpath(top)}) : choisir la racine"
    if os.path.normcase(os.path.abspath(folder)) == os.path.normcase(os.path.abspath(chain_mod.CHAIN_ROOT)):
        return "c'est le dépôt de la chaîne lui-même, pas une application"
    return None


def uncommitted(folder):
    """How many paths git sees changed and not committed — untracked ones
    included —, or None when git cannot say."""
    try:
        p = _git(folder, "--no-optional-locks", "status", "--porcelain", "-z")
    except (OSError, subprocess.SubprocessError):
        return None
    if p.returncode:
        return None
    n, parts, i = 0, p.stdout.split(b"\0"), 0
    while i < len(parts):
        e = parts[i]
        if e:
            n += 1
            if e[:1] in (b"R", b"C"):
                i += 1          # the rename's source follows
        i += 1
    return n


# ------------------------------------------------- « Tout mettre à jour »

UPDATED, SKIPPED, FAILED = "mise à jour", "laissée", "échec"


def update_all(apps, chain_state, install, running, prepare=None):
    """Every application of `apps` ({name, folder}), in the list's order:
    those « en retard » are installed, one after the other; every other is
    said, with why. `chain_state(folder)`, `install(folder)` — chain.py's,
    never with `confirm` — and `running(folder)` are given by the server.
    1.12: `prepare(folder)` — the sync before a launch — runs first, and
    returns why the install may not go, or None. One line per application,
    nothing left out."""
    out = []
    for a in apps:
        folder, line = a["folder"], {"name": a["name"], "folder": a["folder"]}
        out.append(line)
        if not os.path.isdir(folder):
            line.update(outcome=FAILED, text="dossier introuvable")
            continue
        st = chain_state(folder)
        line["state"] = st.get("state")
        if st.get("state") == chain_mod.UP_TO_DATE:
            line.update(outcome=SKIPPED, text="déjà à jour — rien à faire")
            continue
        if st.get("state") == chain_mod.NEWER:
            # 1.12: never an older chain over a newer one.
            line.update(outcome=SKIPPED, text=st.get("refused") or st["summary"])
            continue
        if st.get("state") in (chain_mod.MODIFIED, chain_mod.ABSENT):
            # Never in bulk: its own install asks, file by file, before
            # replacing anything.
            line.update(outcome=SKIPPED, own_install=True,
                        text=f"{st['summary']} — jamais en bloc : son installation demande avant de remplacer quoi que ce soit")
            continue
        if st.get("state") != chain_mod.BEHIND:
            line.update(outcome=FAILED, text=st.get("summary") or "état de la chaîne inconnu")
            continue
        if running(folder):
            line.update(outcome=SKIPPED, text="une commande tourne dans cette application : rien n'est installé pendant un run")
            continue
        if prepare:
            why = prepare(folder)
            if why:
                line.update(outcome=SKIPPED, text=why)
                continue
            st = chain_state(folder)
            if st.get("state") != chain_mod.BEHIND:
                # What GitHub brought changed it: said, never installed blind.
                line.update(outcome=SKIPPED, state=st.get("state"),
                            text=f"après la récupération depuis GitHub : {st.get('summary')} — rien d'installé en bloc")
                continue
        try:
            res = install(folder)
        except chain_mod.NeedsConfirm as e:
            line.update(outcome=SKIPPED, own_install=True, files=e.files,
                        text="l'installation remplacerait des fichiers que la chaîne n'a pas laissés tels quels : "
                             + ", ".join(e.files) + " — elle demande d'abord, depuis sa ligne")
            continue
        except chain_mod.InstallError as e:
            line.update(outcome=FAILED, text=str(e))
            continue
        except Exception as e:          # said, never hidden, and the next one goes on
            line.update(outcome=FAILED, text=f"{type(e).__name__} : {e}")
            continue
        # 1.16: a commit GitHub did not get is never said like a success.
        line.update(outcome=UPDATED, result=res, unpushed=bool(res["app_commit"] and not res["pushed"]),
                    text=(f"chaîne {res['commit']} du {res['date']} — commit {res['app_commit']} « {res.get('message', '')} »"
                          + (", poussé" if res["pushed"] else f", non poussé : {res['push_error']}" if res["push_error"] else ", non poussé")
                          if res["app_commit"] else f"chaîne {res['commit']} du {res['date']} — rien n'avait changé, aucun commit"))
    return out
