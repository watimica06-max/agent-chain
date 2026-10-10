"""1.21 — what the investigations' tests share: a fake SDK client that plays
the model — it tries tools the way the CLI would, through the PreToolUse hook
and then the permission callback the cockpit gave it, and answers —, and the
scripts it plays. No real Claude call: the options are the cockpit's own,
built by enquete.build_options."""
import asyncio

from claude_agent_sdk import (AssistantMessage, PermissionResultAllow, ResultMessage, TextBlock,
                              ToolPermissionContext)

SONNET = "claude-sonnet-5-5"

ANSWER = ("**En bref** — Le cockpit relance le serveur quand le code change (`tools/cockpit/server.py:3415`).\n\n"
          "**Ce que j'ai trouvé** — Le redémarrage compare deux commits (`tools/cockpit/selfupdate.py:72`).\n\n"
          "**Ce que je n'ai pas pu établir** — Rien.\n\n"
          "**Ce que je conseille d'en faire** — **Rien** : c'est le comportement voulu.")


class FakeEnq:
    def __init__(self, options, script):
        self.options = options
        self.script = script
        self.prompts = []
        self.tried = []                 # [(tool, input, allowed)]
        self.interrupted = asyncio.Event()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def query(self, prompt):
        self.prompts.append(prompt)

    def receive_messages(self):
        return self.script(self)

    def receive_response(self):
        return self.script(self)

    async def interrupt(self):
        self.interrupted.set()

    async def tool(self, name, data):
        """What the CLI does before running a tool: the PreToolUse hooks —
        a deny stops it there —, then the permission callback."""
        allowed = True
        for m in self.options.hooks.get("PreToolUse") or []:
            for h in m.hooks:
                out = await h({"hook_event_name": "PreToolUse", "tool_name": name, "tool_input": data}, "tu", None)
                if ((out or {}).get("hookSpecificOutput") or {}).get("permissionDecision") == "deny":
                    allowed = False
        if allowed:
            r = await self.options.can_use_tool(name, data, ToolPermissionContext(tool_use_id="tu"))
            allowed = isinstance(r, PermissionResultAllow)
        self.tried.append((name, data, allowed))
        return allowed


class Factory:
    """The client factory: one script per call, the last one again after."""

    def __init__(self, *scripts):
        self.scripts = list(scripts)
        self.made = []

    def __call__(self, options):
        s = self.scripts.pop(0) if len(self.scripts) > 1 else self.scripts[0]
        c = FakeEnq(options, s)
        self.made.append(c)
        return c


def result(text, cost=0.0123, read=12000, wrote=800):
    return ResultMessage(subtype="success", duration_ms=4000, duration_api_ms=3900, is_error=False, num_turns=3,
                         session_id="s", result=text, model_usage={SONNET: {
                             "inputTokens": read, "outputTokens": wrote, "cacheReadInputTokens": 0,
                             "cacheCreationInputTokens": 0, "costUSD": cost}})


def answering(text=ANSWER, tools=(), gate=None):
    """Tries `tools` [(name, input)], then answers `text`. `gate`, an
    asyncio.Event: waited for before answering — an investigation that goes."""
    async def script(c):
        for name, data in tools:
            await c.tool(name, data)
        yield AssistantMessage(content=[TextBlock("Je lis.")], model=SONNET)
        if gate is not None:
            await gate.wait()
        yield AssistantMessage(content=[TextBlock(text)], model=SONNET)
        yield result(text)
    return script


def until_cancelled():
    async def script(c):
        yield AssistantMessage(content=[TextBlock("Je lis longtemps.")], model=SONNET)
        await asyncio.Event().wait()
        yield result("jamais")
    return script


def saying(text):
    """A second call's answer (§4)."""
    async def script(c):
        yield AssistantMessage(content=[TextBlock(text)], model=SONNET)
        yield result(text, cost=0.002, read=3000, wrote=200)
    return script


# Every way to write, commit, push, delete or reach the web the tests try.
WRITES = [
    ("Write", {"file_path": "docs/x.md", "content": "x"}),
    ("Edit", {"file_path": "README.md", "old_string": "a", "new_string": "b"}),
    ("NotebookEdit", {"notebook_path": "n.ipynb", "new_source": "x"}),
    ("Bash", {"command": "git commit -am 'x'"}),
    ("Bash", {"command": "git push origin master"}),
    ("Bash", {"command": "rm -rf docs"}),
    ("Bash", {"command": "del README.md"}),
    ("Bash", {"command": "echo x > README.md"}),
    ("WebFetch", {"url": "https://example.com", "prompt": "x"}),
    ("WebSearch", {"query": "x"}),
]
READS = [
    ("Read", {"file_path": "README.md"}),
    ("Grep", {"pattern": "app"}),
    ("Glob", {"pattern": "**/*.md"}),
    ("Bash", {"command": "git log --oneline -5"}),
    ("Bash", {"command": "ls docs"}),
]
