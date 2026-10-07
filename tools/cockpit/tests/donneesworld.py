"""« Données » (1.10) — the application the page tests and the screenshots
open: a git repository with both `donnees/` folders, an index in the format
in each, a text file and an image, and a question carrying `Folder:`
(.claude/formats/donnees.md §5). Every repository is a scratch one; nothing
is pushed."""
import struct
import zlib

from test_chain import commit, git, init

RELEVE = ("date;libellé;montant;catégorie\n"
          "2026-09-01;CARTE 31/08 BOULANGERIE DU PORT;-4,20;alimentation\n"
          "2026-09-02;VIR SEPA SALAIRE SEPTEMBRE;2 480,00;revenu\n"
          "2026-09-03;PRLV SEPA ASSURANCE HABITATION;-31,90;logement\n"
          "2026-09-05;CARTE 04/09 PHARMACIE CENTRALE;-12,35;santé\n"
          "2026-09-08;RETRAIT DAB 08/09;-60,00;espèces\n"
          "2026-09-11;CARTE 10/09 LIBRAIRIE DES QUAIS;-23,50;loisirs\n"
          "2026-09-14;VIR INSTANTANE LOYER;-720,00;logement\n")

FEATURE_INDEX = """# Données

## releve-2026-09-14.csv
What: a statement of operations, as the bank's site exports it
Source: exported from the bank's account page, by the Product Owner
Date: 2026-09-14
Private: no
"""

APP_INDEX = """# Données

## fleche.png
What: the arrow shown beside each item of a list
Source: drawn by the Product Owner
Date: 2026-10-01
Private: no
"""

QUESTION = """
### Q4
Block: B7
Folder: docs/features/f/donnees/
Question: The import reads the statement the bank exports. Which file does
the bank give, exactly as it gives it?
Options:
- Le relevé n'existe pas encore : le bloc dit qu'il manque.
Answer:
"""


def png(width=160, height=96):
    """A small arrow on a soft background — an image to preview."""
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            mid = height // 2
            shaft = 30 <= x < 100 and abs(y - mid) <= 7
            head = 100 <= x < 136 and abs(y - mid) <= (136 - x)
            if shaft or head:
                row += bytes((0x2f, 0x6f, 0xb3))
            else:
                row += bytes((0xf4, 0xf3, 0xef))
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        return c + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def data_world(app_root, question=True):
    """The fake application, made a repository, with its data — committed."""
    init(app_root)
    feat = app_root / "docs" / "features" / "f" / "donnees"
    feat.mkdir(parents=True, exist_ok=True)
    (feat / "releve-2026-09-14.csv").write_bytes(RELEVE.encode("utf-8"))
    (feat / "donnees.md").write_bytes(FEATURE_INDEX.encode("utf-8"))
    emb = app_root / "docs" / "donnees"
    emb.mkdir(parents=True, exist_ok=True)
    (emb / "fleche.png").write_bytes(png())
    (emb / "donnees.md").write_bytes(APP_INDEX.encode("utf-8"))
    (app_root / ".gitignore").write_bytes(b"build/\n")
    if question:
        q = app_root / "docs" / "features" / "f" / "questions-sondeur-02.md"
        q.write_bytes(q.read_bytes() + QUESTION.encode("utf-8"))
    return commit(app_root, "init")


__all__ = ["data_world", "png", "RELEVE", "git", "commit"]
