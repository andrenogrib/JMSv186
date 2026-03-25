from __future__ import annotations

import re
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable

import idb


REPO_ROOT = Path(__file__).resolve().parents[2]
IDB_ROOT = REPO_ROOT / "idb_client" / "idb"
DOCS_ROOT = REPO_ROOT / "docs" / "idb"
GENERATED_ROOT = DOCS_ROOT / "generated"

DEFAULT_CLIENT_IDB = IDB_ROOT / "BMS_v24.0_U_DEVM.idb"


def ensure_generated_root() -> Path:
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    return GENERATED_ROOT


@contextmanager
def open_api(path: Path):
    with idb.from_file(str(path)) as db:
        yield db, idb.IDAPython(db)


def sanitize_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_")


def iter_names(api) -> Iterable[tuple[int, str]]:
    for ea, name in api.idautils.Names():
        yield int(ea), str(name)


def find_names_by_substrings(api, substrings: list[str]) -> list[tuple[int, str]]:
    lowered = [s.lower() for s in substrings]
    matches = []
    for ea, name in iter_names(api):
        lname = name.lower()
        if any(pattern in lname for pattern in lowered):
            matches.append((ea, name))
    return matches


def format_ea(ea: int) -> str:
    return f"0x{ea:08X}"


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
