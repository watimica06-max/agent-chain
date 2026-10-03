"""Read and write a chain file without changing what the chain did not ask
to change: its line endings, its byte-order mark, its final newline."""
from dataclasses import dataclass


class UnreadableFile(Exception):
    """A file the cockpit cannot read. Shown to the Product Owner, never
    taken for an empty file."""


@dataclass
class TextFile:
    path: str
    lines: list[str]
    newline: str = "\n"
    final_newline: bool = True
    bom: bool = False

    def text(self) -> str:
        body = self.newline.join(self.lines)
        if self.final_newline and self.lines:
            body += self.newline
        return body

    def encode(self) -> bytes:
        data = self.text().encode("utf-8")
        return (b"\xef\xbb\xbf" + data) if self.bom else data


def decode(path: str, raw: bytes) -> TextFile:
    bom = raw.startswith(b"\xef\xbb\xbf")
    if bom:
        raw = raw[3:]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise UnreadableFile(f"pas de l'UTF-8 ({e.reason}, octet {e.start})") from e
    newline = "\r\n" if "\r\n" in text else "\n"
    final_newline = text.endswith("\n")
    lines = text.splitlines()
    return TextFile(path, lines, newline, final_newline, bom)


def load(path: str) -> TextFile:
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError as e:
        raise UnreadableFile(f"ouverture impossible : {e.strerror or e}") from e
    return decode(path, raw)


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def write_bytes(path: str, data: bytes) -> None:
    # Written in place, not through a rename: an editor or a worktree may
    # hold the file, and a rename would change its identity under them.
    with open(path, "wb") as f:
        f.write(data)
