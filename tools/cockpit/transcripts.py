"""What each agent wrote, read from the transcripts Claude Code keeps — cockpit 1.4.1.

Claude Code writes every session under `<config>/projects/<folder>/`
(`<config>` is `CLAUDE_CONFIG_DIR`, else `~/.claude`):

- `<session_id>.jsonl` — the main session;
- `<session_id>/subagents/agent-<id>.jsonl` and `agent-<id>.meta.json` —
  one pair per subagent, nested ones included.

`<folder>` is the session's working directory, flattened. The orchestrator
enters a worktree, so it may be the worktree's: a session is found by its
id, in every folder — never from the cockpit's own directory.

What the files hold (checked on the 1.4 probe, TECHNICAL_V1 §13.1):
- an assistant message is written once per content block, every line with
  the same `message.id`; its `usage.output_tokens` goes from a placeholder
  to the final count, which the last line of that id carries;
- a subagent's `meta.json` names `toolUseId`, the id of the Agent tool call
  that started it — the id `stats.Pass` is keyed on.

All or nothing: the figures are kept only when the main session plus every
subagent equals exactly the output of the latest result's `model_usage`.
A transcript missing, or a sum that differs, leaves every figure unknown —
never a partial set, never one derived by subtraction.

Read only: nothing is ever written under the config folder.
"""
import glob
import json
import os
import re

SESSION_ID = re.compile(r"^[A-Za-z0-9-]+$")


def config_dir() -> str:
    return os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")


def projects_dir(root: str | None = None) -> str:
    return os.path.join(root or config_dir(), "projects")


def find(session_id: str, root: str | None = None):
    """The session's files, in whichever project folders hold them:
    `{"main": [paths], "agents": {toolUseId: path}, "unnamed": [paths]}`,
    or None when no main transcript exists."""
    if not session_id or not SESSION_ID.match(session_id):
        return None
    base = glob.escape(projects_dir(root))
    mains = sorted(glob.glob(os.path.join(base, "*", session_id + ".jsonl")))
    if not mains:
        return None
    agents, unnamed = {}, []
    for p in sorted(glob.glob(os.path.join(base, "*", session_id, "subagents", "agent-*.jsonl"))):
        try:
            with open(p[:-len(".jsonl")] + ".meta.json", encoding="utf-8") as f:
                tid = (json.load(f) or {}).get("toolUseId")
        except (OSError, ValueError, AttributeError):
            tid = None
        if tid and tid not in agents:
            agents[tid] = p
        else:
            unnamed.append(p)
    return {"main": mains, "agents": agents, "unnamed": unnamed}


def outputs(path: str, sidechain: bool | None = None):
    """Message id -> its final output count, the last line of each id.
    `sidechain=False` keeps the main session's own lines only. None when
    the file cannot be read."""
    out = {}
    try:
        with open(path, encoding="utf-8") as f:
            for raw in f:
                try:
                    d = json.loads(raw)
                except ValueError:
                    continue
                if not isinstance(d, dict) or d.get("type") != "assistant":
                    continue
                if sidechain is not None and bool(d.get("isSidechain")) != sidechain:
                    continue
                m = d.get("message") or {}
                u = m.get("usage") or {}
                if m.get("id") is None or "output_tokens" not in u:
                    continue
                out[m["id"]] = u.get("output_tokens") or 0
    except OSError:
        return None
    return out


def agent_outputs(session_id: str, total_output, pass_ids, root: str | None = None):
    """{tool_use_id: output tokens} for every pass named, or None — then
    every figure of the run stays unknown."""
    if total_output is None:
        return None
    f = find(session_id, root)
    if f is None:
        return None
    main = {}
    for p in f["main"]:
        got = outputs(p, sidechain=False)
        if got is None:
            return None
        main.update(got)          # a session split across folders: one id counted once
    per = {}
    for tid, p in f["agents"].items():
        got = outputs(p)
        if got is None:
            return None
        per[tid] = sum(got.values())
    rest = 0
    for p in f["unnamed"]:        # in the sum; no pass can be given its figure
        got = outputs(p)
        if got is None:
            return None
        rest += sum(got.values())
    if any(t not in per for t in pass_ids):
        return None               # a pass of the run has no transcript
    if sum(main.values()) + sum(per.values()) + rest != total_output:
        return None
    return {t: per[t] for t in pass_ids}
