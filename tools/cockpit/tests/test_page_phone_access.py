"""1.15 — the phone through Tailscale, in a headless browser (Microsoft Edge
through Playwright) at 390 × 844 with touch. Between them, what `tailscale
serve` does (phoneproxy.py): HTTPS at the computer's Tailscale name, the
Host kept, the forwarding headers added. The code page, then the
dashboard; a permission over the event stream; a notification tapped opens
its screen; « Déconnecter le téléphone » brings the code page back; five
wrong codes show on the computer. Screenshots go to $COCKPIT_SHOTS when it
is set. No chain command runs. Skipped when Playwright or Edge is missing."""
import json
import os
from urllib.parse import quote

import pytest

pytest.importorskip("playwright")

import phone as phone_mod  # noqa: E402
from fakeapp import FakeServer  # noqa: E402
from phoneproxy import HOST, TailscaleServe  # noqa: E402
from test_page import _wait  # noqa: E402
from test_runner import script_until_interrupted  # noqa: E402

W, H = 390, 844
CODE = "4815162342"


@pytest.fixture(scope="module")
def edge():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        try:
            # The proxy's certificate is made on the spot: trusted, so that the service
            # worker registers, as it does with the real ts.net certificate.
            b = p.chromium.launch(channel="msedge", args=[f"--host-resolver-rules=MAP {HOST} 127.0.0.1",
                                                          "--ignore-certificate-errors"])
        except Exception as e:                      # no Edge on this machine
            pytest.skip(f"Edge indisponible : {e}")
        yield b
        b.close()


def watch(pg):
    pg.js_errors = []
    pg.on("pageerror", lambda e: pg.js_errors.append(str(e)))
    pg.on("console", lambda m: pg.js_errors.append(m.text) if m.type == "error" else None)
    pg.on("dialog", lambda d: d.accept())
    return pg


def errors(pg):
    # A refused code or a revoked cookie answers 401, 403 or 429, a save without a code 400:
    # the browser logs it, the page says it.
    return [e for e in pg.js_errors if "Failed to fetch" not in e and "net::ERR" not in e
            and not any(f"status of {n}" in e for n in (400, 401, 403, 409, 429))]


@pytest.fixture
def phone(edge):
    ctx = edge.new_context(viewport={"width": W, "height": H}, is_mobile=True, has_touch=True, ignore_https_errors=True)
    yield watch(ctx.new_page())
    ctx.close()


def shot(pg, name):
    out = os.environ.get("COCKPIT_SHOTS")
    if out:
        os.makedirs(out, exist_ok=True)
        pg.screenshot(path=os.path.join(out, name + ".png"))


def through_tailscale(s, tmp_path):
    ts = TailscaleServe(s.url, tmp_path)
    ts.__enter__()
    phone_mod.Phone(s.state).configure(True, ts.address, CODE)
    return ts


def code(pg, value):
    pg.fill("#code", value)
    pg.locator("#code-go").tap()


def test_code_page_then_the_dashboard_then_a_permission_over_the_stream(tmp_path, phone):
    with FakeServer(tmp_path) as s:
        ts = through_tailscale(s, tmp_path)
        try:
            pg = phone
            pg.goto(ts.address + "/#dashboard")
            pg.wait_for_selector("#code-form")
            assert pg.locator("#phone-nav").count() == 0 and pg.locator("#scr-dashboard").count() == 0
            assert pg.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
            assert pg.locator("#code").bounding_box()["height"] >= 44 and pg.locator("#code-go").bounding_box()["height"] >= 44
            shot(pg, "1-telephone-code")
            code(pg, "999999")
            pg.wait_for_selector("#code-err:not(.hidden)")
            assert "encore 4 essais" in pg.locator("#code-err").text_content()
            shot(pg, "2-telephone-code-faux")
            code(pg, CODE)
            pg.wait_for_selector("#phone-nav")
            pg.wait_for_selector("#scr-dashboard:not(.hidden)")
            assert pg.url.endswith("#dashboard")
            (ck,) = [c for c in pg.context.cookies() if c["name"] == phone_mod.COOKIE]
            assert ck["httpOnly"] and ck["secure"] and ck["sameSite"] == "Lax" and ck["expires"] > 0
            assert pg.evaluate("document.cookie") == ""             # HttpOnly: no script reads it
            pg.wait_for_timeout(300)
            shot(pg, "3-telephone-tableau")
            # Every request went through the proxy, under the tailnet name.
            assert ts.forwarded and all(host.startswith(HOST) for _, _, host, _ in ts.forwarded)
            # The service worker: registered, controlling the page — the phone can install it.
            assert pg.evaluate("navigator.serviceWorker.ready.then((r) => r.active && r.active.scriptURL)").endswith("/sw.js")
            # The event stream through it: a permission arrives, is granted, the run ends.
            s.call(s.rn.start(str(s.app_root), "f", "f", "1_lexique", "f"))
            pg.wait_for_selector("#perm-banner .perm", timeout=8000)
            shot(pg, "4-telephone-autorisation")
            pg.locator("#perm-banner").get_by_role("button", name="Autoriser").tap()
            pg.wait_for_selector("#perm-banner", state="hidden")
            s.call(_wait(s.rn.current(str(s.app_root)).task))
            assert any(p == "/api/events" for _, p, _, _ in ts.forwarded)
            # Paramètres on the phone: « Sur ce téléphone », and nothing of the computer's.
            pg.evaluate("location.hash = '#settings'")
            pg.wait_for_selector("#sec-notes", state="visible")
            assert pg.locator("#push-title").is_visible() and pg.locator("#set-push").text_content().strip()
            assert not pg.locator("#sec-phone").is_visible() and not pg.locator("#set-notes").is_visible()
            assert pg.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
            shot(pg, "5-telephone-parametres-notifications")
            assert errors(pg) == []
        finally:
            ts.__exit__(None, None, None)


def test_a_notification_tapped_opens_its_screen_and_deconnecter_asks_the_code_again(tmp_path, phone):
    with FakeServer(tmp_path) as s:
        ts = through_tailscale(s, tmp_path)
        try:
            pg = phone
            pg.goto(ts.address + "/#dashboard")
            code(pg, CODE)
            pg.wait_for_selector("#phone-nav")
            # What the service worker opens when no page is: the address with the push in it.
            s.state.open_pair(str(s.app_root), "f")
            push = {"app": str(s.app_root), "work": "f", "screen": "answer"}
            fresh = watch(pg.context.new_page())
            fresh.goto(ts.address + "/#push=" + quote(json.dumps(push)))
            fresh.wait_for_selector("#scr-answer:not(.hidden)")
            assert fresh.evaluate("location.hash") == "#answer"
            assert errors(fresh) == []
            fresh.close()
            # The page open, the same address with the push in its hash.
            pg.evaluate("location.hash = '#push=' + encodeURIComponent(JSON.stringify(%s))" % json.dumps(push))
            pg.wait_for_selector("#scr-answer:not(.hidden)")
            # And what it tells the page already open.
            pg.evaluate("""() => openFromPush({app: %s, work: "f", screen: "dashboard"})""" % json.dumps(str(s.app_root)))
            pg.wait_for_selector("#scr-dashboard:not(.hidden)")
            # « Déconnecter le téléphone », on the computer: the phone's next request asks the code.
            phone_mod.Phone(s.state).disconnect()
            pg.evaluate("refreshState().catch(() => {})")
            pg.wait_for_selector("#code-form", timeout=8000)
            assert pg.locator("#phone-nav").count() == 0
            assert errors(pg) == []
        finally:
            ts.__exit__(None, None, None)


def test_the_computer_sets_the_access_and_shows_five_wrong_codes(tmp_path, phone, edge):
    with FakeServer(tmp_path, script=script_until_interrupted) as s:
        ts = TailscaleServe(s.url, tmp_path)
        with ts:
            desk = watch(edge.new_page(viewport={"width": 1280, "height": 900}))
            desk.goto(s.url + "#settings")
            desk.wait_for_selector("#sec-phone")
            assert not desk.locator("#phone-on").is_checked()
            # Paramètres → « Accès depuis le téléphone »: the address, the code.
            desk.locator("#phone-on").check()
            desk.fill("#phone-address", ts.address)
            desk.locator("#phone-save").click()
            desk.wait_for_function("document.getElementById('phone-msg').textContent.includes('code')")
            desk.fill("#phone-code", CODE)
            desk.locator("#phone-save").click()
            desk.wait_for_function("document.getElementById('phone-msg').textContent.includes('accepté')")
            assert desk.locator("#phone-code").input_value() == ""                   # never shown back
            assert CODE not in desk.content()
            assert "Un code est enregistré" in desk.locator("#set-phone").text_content()
            desk.locator("#sec-phone").scroll_into_view_if_needed()
            shot(desk, "6-ordinateur-acces-telephone")
            # Five wrong codes on the phone.
            pg = phone
            pg.goto(ts.address + "/")
            for _ in range(5):
                code(pg, "000000")
                pg.wait_for_selector("#code-err:not(.hidden)")
            assert "trop de codes faux" in pg.locator("#code-err").text_content()
            shot(pg, "7-telephone-bloque")
            # The computer shows it, whatever the screen.
            desk.wait_for_selector("#phone-lock:not(.hidden)", timeout=8000)
            assert "cinq codes d'accès faux" in desk.locator("#phone-lock").text_content()
            assert desk.locator("#phone-locked").is_visible()
            desk.evaluate("location.hash = '#dashboard'")
            desk.wait_for_selector("#scr-dashboard:not(.hidden)")
            assert desk.locator("#phone-lock").is_visible()
            shot(desk, "8-ordinateur-telephone-bloque")
            # The right code is refused all the same.
            code(pg, CODE)
            pg.wait_for_timeout(300)
            assert pg.locator("#code-form").is_visible()
            # « Déconnecter le téléphone » is there, and no phone is connected.
            desk.evaluate("location.hash = '#settings'")
            assert desk.locator("#phone-disconnect").is_disabled()
            assert errors(pg) == [] and errors(desk) == []
            desk.close()
