"""1.16 — the fakes of « État de l'ordinateur »: the commands the probes run
(the Claude Code CLI, git, Git Credential Manager, adb, sdkmanager), where the
SDK finds its CLI, where the Android tools are, the Python dependencies.
Every test gets the all-good computer (conftest.py); a test changes one
thing — Claude Code logged out, no GitHub credentials, adb missing —, and
the probes see that. No probe ever runs a real command in a test."""
import json
import subprocess

import machine

CLI = r"C:\fake\claude.exe"


class FakeMachine:
    def __init__(self):
        self.calls = []
        self.cli = CLI
        self.minimum = "2.0.0"
        self.version = "2.1.285 (Claude Code)"
        self.logged_in = True
        self.git = True
        self.identity = "set"            # set, guessed, missing
        self.gcm = True
        self.accounts = ["quelqu-un"]
        self.github = "ok"               # ok, credentials, offline, rejected
        self.remote = True
        self.adb = [r"C:\fake\sdk\platform-tools\adb.exe"]
        self.sdkmanager = [r"C:\fake\sdk\cmdline-tools\latest\bin\sdkmanager.bat"]
        self.emulator = None
        self.scrcpy = None
        self.sdk = r"C:\fake\sdk"
        self.deps = {"ok": True, "missing": [], "count": 3}
        self.answers = {}                # a command's first words → (code, text), over the defaults

    # ------------------------------------------------------------ hooks
    def sdk_cli(self):
        return (self.cli, self.minimum)

    def android(self):
        return {"adb": self.adb, "sdkmanager": self.sdkmanager, "emulator": self.emulator, "scrcpy": self.scrcpy,
                "sdk": self.sdk, "roots": [r"C:\fake\sdk"]}

    def deps_check(self):
        return self.deps

    def run(self, argv, timeout=30, env=None, cwd=None):
        argv = [str(a) for a in argv]
        self.calls.append(argv)
        for k, v in self.answers.items():
            if " ".join(argv).startswith(k) or " ".join(argv[3:] if argv[:2] == ["git", "-C"] else argv).startswith(k):
                if isinstance(v, BaseException):
                    raise v
                return v
        if argv[0] == self.cli:
            if argv[1:] == ["--version"]:
                return 0, self.version
            if argv[1:3] == ["auth", "status"]:
                if self.logged_in:
                    return 0, json.dumps({"loggedIn": True, "authMethod": "claude.ai", "subscriptionType": "max"})
                return 1, json.dumps({"loggedIn": False, "authMethod": "none"})
        if argv[0] == "git" and not self.git:
            raise FileNotFoundError("git introuvable (PATH)")
        if argv[:2] == ["git", "--version"]:
            return 0, "git version 2.56.0.windows.1"
        if argv[:2] == ["git", "credential-manager"]:
            if not self.gcm:
                return 1, "git: 'credential-manager' is not a git command."
            if argv[2:] == ["--version"]:
                return 0, "2.9.1"
            if argv[2:4] == ["github", "list"]:
                return 0, "\n".join(self.accounts)
        if argv[:2] == ["git", "-C"]:
            rest = argv[3:]
            if rest[:3] == ["config", "--get", "user.name"]:
                return (0, "Product Owner") if self.identity == "set" else (1, "")
            if rest[:3] == ["config", "--get", "user.email"]:
                return (0, "po@example.com") if self.identity == "set" else (1, "")
            if rest[:2] == ["var", "GIT_AUTHOR_IDENT"]:
                if self.identity == "missing":
                    return 128, "Author identity unknown\n*** Please tell me who you are."
                return 0, "PO Devine <po@ordinateur.local> 1791604936 +0800"
            if rest[:1] == ["remote"]:
                return (0, "origin") if self.remote else (0, "")
            if rest[:1] == ["push"]:
                if self.github == "ok":
                    return 0, "To https://github.com/x/agent-chain.git\n=\trefs/heads/master:refs/heads/master\t[up to date]\nDone"
                if self.github == "rejected":
                    return 1, "!\trefs/heads/master:refs/heads/master\t[rejected] (fetch first)"
                if self.github == "credentials":
                    return 128, ("fatal: Cannot prompt because user interactivity has been disabled.\n"
                                 "fatal: could not read Username for 'https://github.com': terminal prompts disabled")
                return 128, "fatal: unable to access 'https://github.com/x/agent-chain.git/': Could not resolve host: github.com"
        if self.adb and argv[0] == self.adb[0]:
            return 0, "Android Debug Bridge version 1.0.41"
        if self.sdkmanager and argv[0] == self.sdkmanager[0]:
            return 0, "12.0"
        if self.emulator and argv[0] == self.emulator[0]:
            return 0, "Android emulator version 35.1"
        if self.scrcpy and argv[0] == self.scrcpy[0]:
            return 0, "scrcpy 2.4"
        raise FileNotFoundError(f"{argv[0]} introuvable (faux)")


def install(monkeypatch, fm=None):
    """The fake computer, everywhere a probe looks."""
    fm = fm or FakeMachine()
    monkeypatch.setattr(machine, "RUN", fm.run)
    monkeypatch.setattr(machine, "SDK_CLI", fm.sdk_cli)
    monkeypatch.setattr(machine, "ANDROID", fm.android)
    monkeypatch.setattr(machine, "DEPS_CHECK", fm.deps_check)
    return fm


def timeout(seconds=30):
    return subprocess.TimeoutExpired("fake", seconds)
