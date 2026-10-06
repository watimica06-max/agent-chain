"""What the page shows of a run, read from its messages — cockpit 1.5.

One reader for the live run and for its log: `Reader.feed` takes a message
as the log holds it — its type name and its `asdict` body — and returns the
page's events (`text`, `tool`, `agent_started`, `agent_background`,
`agent_ended`). The runner feeds it every message as it comes, and logs the
same body; a page opened later is given the same events rebuilt from the
log (`replay`), so what it shows does not depend on what the server kept in
memory.

The usage an agent hands back with is the stats `Tally`'s, fed alongside.
"""
import json
import os
import re

import stats as stats_mod

AGENT_TOOLS = {"Agent", "Task"}
# What the Agent tool's result says when the subagent was started in the background.
BACKGROUND_RESULT = re.compile(r"async_launched|in the background|agentId", re.I)
TERMINAL_STATUSES = {"completed", "failed", "stopped", "killed"}


class Reader:
    def __init__(self):
        self.agents = {}          # tool_use_id -> subagent type
        self.active = []          # tool_use_ids running
        self.tasks = {}           # task_id -> tool_use_id
        self.background = set()   # tool_use_ids started in the background
        self.inputs = {}          # tool_use_id -> the Agent tool's input
        self.last_text = ""       # the orchestrator's last text

    def label(self, parent_id):
        if not parent_id:
            return "orchestrateur"
        return self.agents.get(parent_id, "agent")

    def feed(self, kind, body, tally=None):
        """The page's events for one message: [(type, data)]."""
        if not isinstance(body, dict):
            return []
        out = []
        if kind == "AssistantMessage":
            parent = body.get("parent_tool_use_id")
            who = self.label(parent)
            for block in body.get("content") or []:
                if not isinstance(block, dict):
                    continue
                if "text" in block and "id" not in block:
                    if not parent:
                        self.last_text = block["text"]
                    out.append(("text", {"agent": who, "text": block["text"]}))
                elif "name" in block and "id" in block and "input" in block:
                    if block["name"] in AGENT_TOOLS:
                        inp = block.get("input") or {}
                        name = inp.get("subagent_type") or "agent"
                        self.agents[block["id"]] = name
                        self.inputs[block["id"]] = inp
                        self.active.append(block["id"])
                        out.append(("agent_started", {"agent": name, "description": inp.get("description") or "",
                                                      "by": who, "id": block["id"]}))
                    else:
                        out.append(("tool", {"agent": who, "tool": block["name"],
                                             "summary": summary(block["name"], block.get("input"))}))
        elif kind == "UserMessage":
            content = body.get("content")
            for block in content if isinstance(content, list) else []:
                if not (isinstance(block, dict) and "tool_use_id" in block):
                    continue
                tid = block["tool_use_id"]
                if tid not in self.active:
                    continue
                if BACKGROUND_RESULT.search(text_of(block.get("content"))):
                    # Started in the background: still pending until its
                    # completion notification.
                    self.background.add(tid)
                    out.append(("agent_background", {"agent": self.agents.get(tid), "id": tid}))
                else:
                    self.active.remove(tid)
                    out.append(("agent_ended", {"agent": self.agents.get(tid), "id": tid,
                                                "usage": _usage(tally, tid)}))
        elif kind == "TaskStartedMessage":
            if body.get("tool_use_id"):
                self.tasks[body.get("task_id")] = body["tool_use_id"]
        elif kind in ("TaskNotificationMessage", "TaskUpdatedMessage"):
            status = body.get("status") or (body.get("patch") or {}).get("status")
            if status in TERMINAL_STATUSES:
                tid = body.get("tool_use_id") or self.tasks.get(body.get("task_id"))
                if tid in self.active:
                    self.active.remove(tid)
                    self.background.discard(tid)
                    out.append(("agent_ended", {"agent": self.agents.get(tid), "id": tid, "late": True,
                                                "status": status, "usage": _usage(tally, tid)}))
        return out


def _usage(tally, tid):
    p = tally.passes.get(tid) if tally else None
    return p.summary() if p else None


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)
    return str(content or "")


def summary(tool, inp):
    inp = inp or {}
    for k in ("command", "file_path", "path", "pattern", "description", "url", "skill"):
        v = inp.get(k)
        if isinstance(v, str) and v:
            v = v.replace("\n", " ")
            return v if len(v) <= 160 else v[:160] + "…"
    return ""


class Replay:
    """The events of a run rebuilt from its log, read incrementally: a page
    opened again reads only what was written since the last opening."""

    def __init__(self, path):
        self.path = path
        self.offset = 0
        self.reader = Reader()
        self.tally = stats_mod.Tally()
        self.events = []          # (line, at, type, data): line, its rank among the log's lines
        self.lines = 0

    def catch_up(self):
        try:
            with open(self.path, "rb") as f:
                f.seek(self.offset)
                chunk = f.read()
        except OSError:
            return self.events
        end = chunk.rfind(b"\n")
        if end < 0:
            return self.events
        self.offset += end + 1
        for raw in chunk[:end].split(b"\n"):
            raw = raw.strip()
            if not raw:
                continue
            try:
                line = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                continue
            if not isinstance(line, dict) or line.get("probe"):
                continue
            kind, body, at = line.get("type") or "", line.get("message"), line.get("at")
            self.tally.feed(kind, body, at)
            for t, d in self.reader.feed(kind, body, self.tally):
                self.events.append((self.lines, at or "", t, d))
            self.lines += 1
        return self.events


def replay(path, cache=None):
    """`(events, replay)` — the message events of the log at `path`, as
    `(line, at, type, data)`, reusing `cache` when it reads the same file."""
    r = cache if cache is not None and cache.path == path else Replay(path)
    if not path or not os.path.isfile(path):
        return [], r
    return r.catch_up(), r
