"""1.15 — what `tailscale serve --bg <port>` does, for the tests and the
screenshots: HTTPS at the computer's Tailscale name, forwarded to the cockpit
on 127.0.0.1, the Host kept as the phone sent it, X-Forwarded-Host, -Proto,
-For and Tailscale-User-* added — as tailscale's ipn/ipnlocal/serve.go does.
Its certificate is made on the spot for that name; the browser is told to
take it, and to resolve the name to this computer."""
import asyncio
import datetime
import ipaddress
import ssl
import threading

import aiohttp
from aiohttp import web
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID

HOST = "cockpit-pc.tail1234.ts.net"
HOP = {"connection", "keep-alive", "transfer-encoding", "te", "trailer", "upgrade", "proxy-authorization",
       "proxy-connection", "content-length"}


def certificate(folder, host=HOST):
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, host)])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=30))
            .add_extension(x509.SubjectAlternativeName([x509.DNSName(host), x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]),
                           critical=False)
            .sign(key, hashes.SHA256()))
    crt, pem = folder / "serve.crt", folder / "serve.key"
    crt.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    pem.write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                      serialization.NoEncryption()))
    return str(crt), str(pem)


class TailscaleServe:
    def __init__(self, target, folder, host=HOST):
        self.target = target.rstrip("/")
        self.host = host
        self.crt, self.key = certificate(folder, host)
        self.loop = asyncio.new_event_loop()
        self.port = None
        self.forwarded = []          # (method, path, Host, X-Forwarded-For) of each request
        self._ready = threading.Event()
        self._done = threading.Event()
        self._stop = None

    @property
    def address(self):
        return f"https://{self.host}:{self.port}"

    async def handle(self, request):
        headers = {k: v for k, v in request.headers.items() if k.lower() not in HOP}
        headers["Host"] = request.host
        headers["X-Forwarded-Host"] = request.host
        headers["X-Forwarded-Proto"] = "https"
        headers["X-Forwarded-For"] = "100.101.102.103"
        headers["Tailscale-User-Login"] = "po@example.com"
        headers["Tailscale-User-Name"] = "Product Owner"
        self.forwarded.append((request.method, request.path, request.host, headers["X-Forwarded-For"]))
        body = await request.read()
        try:
            return await self.forward(request, headers, body)
        except aiohttp.ClientError:            # the cockpit stopped first, at the end of a test
            return web.Response(status=502)

    async def forward(self, request, headers, body):
        async with self.session.request(request.method, self.target + request.path_qs, headers=headers,
                                        data=body or None, allow_redirects=False, auto_decompress=False) as r:
            resp = web.StreamResponse(status=r.status)
            for k, v in r.headers.items():
                if k.lower() not in HOP:
                    resp.headers.add(k, v)
            await resp.prepare(request)
            try:
                async for chunk in r.content.iter_any():
                    await resp.write(chunk)
            except (ConnectionResetError, aiohttp.ClientPayloadError):
                pass
            await resp.write_eof()
            return resp

    def __enter__(self):
        threading.Thread(target=self._run, daemon=True).start()
        assert self._ready.wait(10)
        return self

    def __exit__(self, *exc):
        self.loop.call_soon_threadsafe(self._stop.set)
        self._done.wait(10)

    def _run(self):
        asyncio.set_event_loop(self.loop)

        async def main():
            self._stop = asyncio.Event()
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=None), auto_decompress=False)
            app = web.Application(client_max_size=300 * 1024 * 1024)
            app.router.add_route("*", "/{tail:.*}", self.handle)
            runner = web.AppRunner(app, shutdown_timeout=0.5)
            await runner.setup()
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ctx.load_cert_chain(self.crt, self.key)
            site = web.TCPSite(runner, "127.0.0.1", 0, ssl_context=ctx)
            await site.start()
            self.port = site._server.sockets[0].getsockname()[1]
            self._ready.set()
            await self._stop.wait()
            await self.session.close()
            await runner.cleanup()

        try:
            self.loop.run_until_complete(main())
        finally:
            self._done.set()
