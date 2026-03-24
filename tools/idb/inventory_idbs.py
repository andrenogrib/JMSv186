from __future__ import annotations

from pathlib import Path

from common import DOCS_ROOT, IDB_ROOT, write_text


def collect_entries() -> list[Path]:
    paths = []
    for path in sorted(IDB_ROOT.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".idb", ".i64", ".exe", ".zip"}:
            paths.append(path)
    return paths


def build_markdown() -> str:
    lines = []
    lines.append("# IDB Inventory")
    lines.append("")
    lines.append("This inventory is generated from `idb_client/idb`.")
    lines.append("")
    lines.append("| Path | Size (bytes) |")
    lines.append("| --- | ---: |")
    for path in collect_entries():
        rel = path.relative_to(DOCS_ROOT.parent.parent)
        size = path.stat().st_size
        lines.append(f"| `{rel.as_posix()}` | {size} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    out = DOCS_ROOT / "idb_inventory.md"
    write_text(out, build_markdown())
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
