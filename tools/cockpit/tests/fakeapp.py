"""A fake application folder served by the real cockpit server, for the
headless-browser tests and the screenshots. The SDK client is a fake: no
chain command runs."""
import asyncio
import os
import threading

from aiohttp import web

import runner as runner_mod
import server
from state import State
from test_runner import FakeClient, script_with_permission
from test_server import build_app_folder


class FakeServer:
    def __init__(self, tmp_path, script=script_with_permission, opened=True, diag_runner=None):
        self.tmp = tmp_path
        self.app_root = tmp_path / "app"
        self.feat = build_app_folder(self.app_root)
        # One command per group of the settings screen, beside those the folder helper writes.
        for name in ("7_lots", "diagnostique", "fusion_compare"):
            (self.app_root / ".claude" / "commands" / f"{name}.md").write_text(
                f'---\ndescription: run {name}\nargument-hint: "<f>"\n---\nbody\n', encoding="utf-8")
        self.state = State(str(tmp_path / "config.json"))
        if opened:
            self.state.open_pair(str(self.app_root), "f")
        self.script = script
        self.clients = []

        def factory(cwd, can_use_tool, **kw):
            c = FakeClient(self.script, can_use_tool)
            c.kw = kw
            self.clients.append(c)
            return c

        self.rn = runner_mod.Runner(
            client_factory=factory, log_dir=str(tmp_path / "logs"),
            on_end=server.make_on_end(self.state), mode_getter=lambda: self.state.mode)
        self.app = server.make_app(self.state, self.rn, picker=lambda initial: str(self.app_root),
                                   **({"diag_runner": diag_runner} if diag_runner else {}))
        self.loop = asyncio.new_event_loop()
        self.url = ""
        self._ready = threading.Event()
        self._stop = None

    def __enter__(self):
        t = threading.Thread(target=self._run, daemon=True)
        t.start()
        assert self._ready.wait(10)
        return self

    def __exit__(self, *exc):
        self.loop.call_soon_threadsafe(self._stop.set)
        self._thread_done.wait(10)

    def _run(self):
        asyncio.set_event_loop(self.loop)
        self._thread_done = threading.Event()

        async def main():
            self._stop = asyncio.Event()
            runner = web.AppRunner(self.app, shutdown_timeout=0.5)
            await runner.setup()
            site = web.TCPSite(runner, "127.0.0.1", 0)
            await site.start()
            port = site._server.sockets[0].getsockname()[1]
            self.url = f"http://127.0.0.1:{port}/"
            self._ready.set()
            await self._stop.wait()
            for run in list(self.rn.runs.values()):
                if run.task and not run.task.done():
                    run.task.cancel()
            await runner.cleanup()

        try:
            self.loop.run_until_complete(main())
        finally:
            self._thread_done.set()

    def call(self, coro):
        """Run a coroutine on the server's loop (to start or stop runs)."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop).result(10)
