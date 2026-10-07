"""« Bâtir » — the files /batir reads and the Bâtisseur writes, after their
templates (agents/batisseur.md « What you write », « When you cannot
produce », « When the conventions fall short »), on a feature whose
upstream is closed and whose conventions are written. Shared by test_scan,
the page tests and shots_batir.py. Nothing runs."""
import json

COMMIT = "4f7c2a91d0b3e5f6a7b8c9d0e1f2a3b4c5d6e7f8"
OLDER = "0a1b2c3d4e5f60718293a4b5c6d7e8f901234567"

PART = "### B1 — Une séance\nGenre: comportement\nNature: model\n\nLa séance a une date et une durée.\n"
NATURES = ["model", "persistence", "calculation", "transition", "external exchange",
           "synchronisation", "presentation", "access"]
GENRES = ["comportements", "transverses", "directives", "references", "hors-perimetre", "recette"]

# G2.1, G4.4 and G12.6: the three tables /batir greps (batir.md:75).
CONVENTIONS = """# Technical conventions

## G2.1 — Commands

| Name | Command |
|---|---|
| build | .\\gradlew.bat build |
| test | .\\gradlew.bat test |
| assemble app | .\\gradlew.bat :app:assembleDebug |

## G4.4 — Modules

| Module | Builds as | Depends on | Runs on | Application id |
|---|---|---|---|---|
| app | application | domain | phone | com.exemple.seances |
| domain | library | — | — | — |

## G12.6 — Build

| Fact | Value |
|---|---|
| Build system | Gradle 8.9, through its wrapper |
| Toolchain | JDK 17 |
| Android | compileSdk 35, minSdk 26 |
"""

# Conventions written before the grid declared the structure: no table.
CONVENTIONS_OLD = "# Technical conventions\n\n## G1.1 — Naming\n\nClasses in PascalCase.\n"


def write(path, text=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def upstream_done(app, name="premiere", conventions=CONVENTIONS):
    """A feature at the end of /conventions: every upstream step done, the
    conventions written with their three tables, `couverture.md` there."""
    feat = app / "docs" / "features" / name
    write(feat / "idees.md", "# Idées\n\nSuivre mes séances.\n")
    write(feat / "desc-produit.md", "# Produit\n\n" + PART)
    for g in GENRES:
        write(feat / "par-genre" / f"{g}.md", PART if g == "comportements" else "")
    others = "".join(f"## {n}\n\n*(none)*\n\n" for n in NATURES[1:])
    write(feat / "desc-par-nature.md", f"# Product file by nature\n\n## model\n\n{PART}\n{others}")
    write(feat / "convertisseur" / "model-input.md", PART)
    write(feat / "convertisseur" / "model.md", "## model\n\nR1.\n")
    write(feat / "spec-technique.md", "# Preamble\n\n### §1 — Séance\n")
    write(feat / "tracabilite.md", "B1 → §1\n")
    for n in ("sondeur", "existant"):
        write(feat / "questions" / n / f"questions-{n}-01.md", "")
    write(feat / "couverture.md", "§1 — G2.1, G4.4, G12.6\n")
    if conventions is not None:
        write(app / "docs" / "TECHNICAL_CONVENTIONS.md", conventions)
    return feat


def report(feat, commit=COMMIT, status="built", created=None):
    """`docs/BUILD_REPORT.md`, the application's, whole (agents/batisseur.md
    « What you write »), as the run of feature `feat` writes it."""
    created = created or ["settings.gradle.kts", "build.gradle.kts", "gradle/libs.versions.toml",
                          "app/build.gradle.kts", "app/src/main/AndroidManifest.xml",
                          "app/src/main/kotlin/com/exemple/seances/MainActivity.kt",
                          "domain/build.gradle.kts", ".gitignore", ".claude/deploy.json"]
    ok = status == "built"
    rows = [("build", ".\\gradlew.bat build", "0" if ok else "1", "84"),
            ("test", ".\\gradlew.bat test", "0" if ok else "not run", "31" if ok else "—"),
            ("assemble app", ".\\gradlew.bat :app:assembleDebug", "0" if ok else "not run", "12" if ok else "—")]
    write(feat.parent.parent / "BUILD_REPORT.md", "\n".join([
        f"# Bâtisseur — {feat.name}", "", "## Conventions", "", commit, "",
        "## Created", "", *created, "",
        "## Commands", "", "| Name | Command | Result | Duration |", "|---|---|---|---|",
        *[f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows], "",
        "## Packages", "", "app — app/build/outputs/apk/debug/app-debug.apk" if ok else "—", "",
        "## Installed", "", "—", "",
        "## Deploy profile", "", "Téléphone — app" if ok else "—", "",
        "## Decision applied", "", "—", "",
        f"## Status: {status}", ""]))


def profile(app):
    """`.claude/deploy.json`, the target move 6 adds (agents/batisseur.md)."""
    write(app / ".claude" / "deploy.json", json.dumps({"format": 1, "targets": [
        {"name": "Téléphone", "type": "android", "build": ".\\gradlew.bat :app:assembleDebug",
         "kind": "phone", "install": "adb -s {serial} install -r app\\build\\outputs\\apk\\debug\\app-debug.apk",
         "app_id": "com.exemple.seances"}]}, ensure_ascii=False, indent=2) + "\n")


# A build tool it cannot obtain: `## To resume` is a tutorial, in French,
# step by step, ending on what to write under `## Decision`
# (agents/batisseur.md « When you cannot produce »).
TUTORIAL = """## What blocks

Le JDK 17 que G12.6 demande n'est pas sur cette machine, et l'installer demande les droits d'administrateur.

## Where

JDK 17 — G12.6, ligne « Toolchain »

## To resume

1. Ouvrez https://adoptium.net/fr/temurin/releases/?version=17 dans votre navigateur.
2. Choisissez « Windows », « x64 » et « JDK », puis cliquez sur le fichier `.msi` pour le télécharger.
3. Ouvrez le fichier téléchargé, dans `C:\\Users\\vous\\Downloads`, et suivez l'installation.
4. À l'écran « Custom Setup », cliquez sur « Set JAVA_HOME variable » et choisissez « Will be installed on local hard drive ».
5. Terminez l'installation, puis ouvrez l'« Invite de commandes » et tapez :

       java -version

6. Vérifiez que la première ligne affichée commence par `openjdk version "17`.
7. Écrivez *fait* sous `## Decision`, puis relancez `/batir premiere`.

## Decision

"""


def blocked(feat, decision=""):
    write(feat / "blocked_batisseur.md", TUTORIAL + (decision + "\n" if decision else ""))


def request(feat, verdict=""):
    """`architecte/batisseur.md`, one `# Request N` (agents/batisseur.md
    « When the conventions fall short »)."""
    write(feat / "architecte" / "batisseur.md", "\n".join([
        "# Request 1", "", "## What I need", "", "The application id of module `app`.", "",
        "## Why the lot cannot proceed", "", "The build: `app` builds as an application and has none.", "",
        "## Where I met it", "", "G4.4, line `app`, column `Application id`.", "",
        "## What I think it is", "", "add", "", "## Verdict", "", verdict, ""]))
