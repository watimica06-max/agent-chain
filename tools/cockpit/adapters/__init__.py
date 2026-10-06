"""The deploy adapters, one per kind of target (1.8). Adding a platform is
adding a module here and its line in ADAPTERS — the page and the server read
only what an adapter declares."""
from .android import AndroidAdapter
from .commande import CommandeAdapter

ADAPTERS = {a.TYPE: a for a in (AndroidAdapter, CommandeAdapter)}
