"""The deploy profile — `.claude/deploy.json` of an application (1.8).

The contract is .claude/formats/deploy-profile.md: what a target holds,
adapter by adapter. It belongs to the application: the chain's install never touches it
(chain.PATHS does not hold it). The Product Owner writes it in Paramètres →
Déploiement; saving it writes the file, commits it alone in the application
(`deploy: profil`) and pushes.

A target is the frame's three fields — `name`, `type`, `build` — and its
adapter's own (`FIELDS`). A key no one declares is refused: a typo is said,
never ignored.
"""
import json
import os

import chain as chain_mod
from adapters import ADAPTERS

PATH = ".claude/deploy.json"
FORMAT = 1
COMMIT_MESSAGE = "deploy: profil"
NAME_MAX = 40
FRAME = ("name", "type", "build")


def path_of(app):
    return os.path.join(app, *PATH.split("/"))


def frame_fields():
    """The fields every target has, as the page renders them."""
    from adapters.base import field_spec
    return [
        field_spec("name", "Nom", required=True, placeholder="Téléphone",
                   help="Le nom que la page montre — « Téléphone », « Montre », « Site »."),
        field_spec("type", "Type", "choice", required=True,
                   choices=[[t, a.LABEL] for t, a in ADAPTERS.items()],
                   help="L'adaptateur : ce qu'il sait faire, et les champs qui suivent."),
        field_spec("build", "Commande de build",
                   placeholder=r".\gradlew.bat :app:assembleDebug",
                   help="Lancée une fois depuis la racine de l'application, avant de déployer sur chaque destination. "
                        "Vide : rien à construire."),
    ]


def check(data):
    """(targets, errors): the profile's targets cleaned — each key in the
    contract's order, texts stripped — and every error, in French:
    `{"general": [...], "targets": {index: {field: text}}}`."""
    errors = {"general": [], "targets": {}}
    if not isinstance(data, dict):
        errors["general"].append("le profil est un objet JSON : { \"format\": 1, \"targets\": [...] }")
        return [], errors
    unknown = sorted(set(data) - {"format", "targets"})
    if unknown:
        errors["general"].append("clé inconnue : " + ", ".join(unknown))
    if data.get("format", FORMAT) != FORMAT:
        errors["general"].append(f"format {data.get('format')!r} : ce cockpit lit le format {FORMAT}")
    targets = data.get("targets")
    if not isinstance(targets, list):
        errors["general"].append("« targets » est une liste")
        return [], errors
    out, names = [], set()
    for i, t in enumerate(targets):
        e = {}
        if not isinstance(t, dict):
            errors["targets"][i] = {"_": "une cible est un objet"}
            continue
        typ = t.get("type")
        adapter = ADAPTERS.get(typ)
        if not adapter:
            e["type"] = "type inconnu : " + ", ".join(ADAPTERS) + " attendu"
        name = t.get("name")
        if not isinstance(name, str) or not name.strip():
            e["name"] = "obligatoire"
        elif len(name.strip()) > NAME_MAX:
            e["name"] = f"{NAME_MAX} caractères au plus"
        elif name.strip().casefold() in names:
            e["name"] = "deux cibles ont ce nom"
        else:
            names.add(name.strip().casefold())
        build = t.get("build", "")
        if build is None:
            build = ""
        if not isinstance(build, str):
            e["build"] = "un texte attendu"
        clean = {"name": name.strip() if isinstance(name, str) else name, "type": typ,
                 "build": build.strip() if isinstance(build, str) else build}
        if adapter:
            allowed = set(FRAME) | {f["key"] for f in adapter.FIELDS}
            extra = sorted(set(t) - allowed)
            if extra:
                e["_"] = "clé inconnue pour « " + typ + " » : " + ", ".join(extra)
            e.update(_check(adapter, t))
            for f in adapter.FIELDS:
                v = t.get(f["key"], f["default"])
                if f["kind"] == "bool":
                    clean[f["key"]] = bool(v)
                else:
                    clean[f["key"]] = (v or "").strip() if isinstance(v, str) or v is None else v
        if e:
            errors["targets"][i] = e
        out.append(clean)
    return out, errors


def _check(adapter_cls, target):
    """An adapter's `check`, which reads only the target: called on a bare
    instance, no server behind it."""
    inst = adapter_cls.__new__(adapter_cls)
    return adapter_cls.check(inst, target)


def has_errors(errors):
    return bool(errors["general"] or errors["targets"])


def load(app):
    """{exists, targets, errors, text}: the profile as the file holds it.
    A file that is not JSON is an error said, never an empty profile."""
    p = path_of(app)
    out = {"path": PATH, "exists": os.path.isfile(p), "targets": [],
           "errors": {"general": [], "targets": {}}}
    if not out["exists"]:
        return out
    try:
        with open(p, encoding="utf-8-sig") as f:
            text = f.read()
        data = json.loads(text)
    except (OSError, ValueError) as e:
        out["errors"]["general"].append(f"{PATH} illisible : {e}")
        return out
    out["targets"], out["errors"] = check(data)
    return out


def text_of(targets):
    return json.dumps({"format": FORMAT, "targets": targets}, ensure_ascii=False, indent=2) + "\n"


class ProfileError(Exception):
    def __init__(self, msg, errors=None):
        super().__init__(msg)
        self.errors = errors


def save(app, targets, push=True):
    """Writes the profile, commits it alone — `deploy: profil`, `--only`, so
    that what the Product Owner staged stays out — and pushes. Nothing
    changed: no commit. Raises ProfileError with the errors when it does not
    hold."""
    clean, errors = check({"format": FORMAT, "targets": targets})
    if has_errors(errors):
        raise ProfileError("le profil ne tient pas", errors)
    text = text_of(clean)
    try:
        crlf = chain_mod._crlf(app)
    except Exception:
        crlf = False
    data = (text.replace("\n", "\r\n") if crlf else text).encode("utf-8")
    p = path_of(app)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    old = None
    if os.path.exists(p):
        with open(p, "rb") as f:
            old = f.read()
    if old != data:
        with open(p, "wb") as f:
            f.write(data)
    res = {"path": PATH, "targets": clean, "commit": None, "pushed": False, "push_error": None}
    try:
        if not chain_mod._dirty(app, [PATH]):
            return res
        chain_mod._git(app, "add", "--", PATH)
        chain_mod._git(app, "commit", "-q", "-m", COMMIT_MESSAGE, "--only", "--", PATH)
        res["commit"] = chain_mod._git(app, "rev-parse", "--short", "HEAD").decode().strip()
    except chain_mod.InstallError as e:
        raise ProfileError(f"profil écrit, mais pas commité : {e}")
    if push:
        try:
            chain_mod.push_branch(app)
            res["pushed"] = True
        except chain_mod.InstallError as e:
            res["push_error"] = str(e)
    return res
