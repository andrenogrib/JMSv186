from __future__ import annotations

import argparse
from pathlib import Path

from common import DEFAULT_CLIENT_IDB, GENERATED_ROOT, ensure_generated_root, format_ea, open_api, sanitize_name, write_text


def iter_function_names(api):
    for ea in api.idautils.Functions():
        try:
            name = api.idc.GetFunctionName(ea) or ""
        except Exception:
            name = ""
        if name:
            yield int(ea), str(name)


def build_markdown(idb_path: Path, patterns: list[str], title: str) -> str:
    lowered = [pattern.lower() for pattern in patterns]
    hits: list[tuple[int, str]] = []

    with open_api(idb_path) as (_, api):
        for ea, name in iter_function_names(api):
            lname = name.lower()
            if any(pattern in lname for pattern in lowered):
                hits.append((ea, name))

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- IDB: `{idb_path}`")
    lines.append(f"- Patterns: `{', '.join(patterns)}`")
    lines.append(f"- Match count: `{len(hits)}`")
    lines.append("")

    if not hits:
        lines.append("_No matches found._")
        lines.append("")
        return "\n".join(lines)

    lines.append("| Address | Function |")
    lines.append("| --- | --- |")
    for ea, name in hits:
        lines.append(f"| `{format_ea(ea)}` | `{name}` |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--idb", default=str(DEFAULT_CLIENT_IDB))
    parser.add_argument("--pattern", action="append", required=True)
    parser.add_argument("--title")
    parser.add_argument("--out-name")
    args = parser.parse_args()

    idb_path = Path(args.idb)
    ensure_generated_root()

    if args.out_name:
        out = GENERATED_ROOT / args.out_name
    else:
        out = GENERATED_ROOT / f"{sanitize_name(idb_path.stem)}_function_matches.md"

    title = args.title or f"Function Matches: {idb_path.name}"
    write_text(out, build_markdown(idb_path, args.pattern, title))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
