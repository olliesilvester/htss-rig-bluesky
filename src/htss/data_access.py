from pprint import pprint
from typing import Any, Mapping

from tiled.client import from_uri

from .names import server_name


def get_client():
    return from_uri(f"http://{server_name()}:8000")


def print_docs(name: str, doc: Mapping[str, Any]) -> None:
    pprint({"name": name, "doc": doc})
