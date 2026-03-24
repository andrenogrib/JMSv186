from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from common import DEFAULT_CLIENT_IDB, GENERATED_ROOT, ensure_generated_root, find_names_by_substrings, format_ea, open_api, sanitize_name, write_text


DEFAULT_GROUPS = {
    "packet_core": [
        "CClientSocket",
        "CInPacket",
        "COutPacket",
        "SendPacket",
        "ProcessPacket",
        "Decode",
        "Encode",
    ],
    "login": [
        "CLogin",
        "CheckPassword",
        "WorldInformation",
    ],
    "user_and_context": [
        "CUserPool",
        "CWvsContext",
        "CFuncKeyMappedMan",
        "CScriptMan",
        "CShopDlg",
        "CStoreBankDlg",
    ],
    "field_objects": [
        "CField",
        "CMobPool",
        "CNpcPool",
        "CDropPool",
        "CReactorPool",
        "CTownPortalPool",
        "CAffectedAreaPool",
        "CMessageBoxPool",
        "CEmployeePool",
    ],
}


def render_group(title: str, hits: list[tuple[int, str]]) -> list[str]:
    lines = []
    lines.append(f"## {title}")
    lines.append("")
    if not hits:
        lines.append("_No matches found._")
        lines.append("")
        return lines

    lines.append("| Address | Name |")
    lines.append("| --- | --- |")
    for ea, name in hits:
        lines.append(f"| `{format_ea(ea)}` | `{name}` |")
    lines.append("")
    return lines


def build_markdown(idb_path: Path) -> str:
    lines = []
    lines.append(f"# Named Functions And Symbols: `{idb_path.name}`")
    lines.append("")
    with open_api(idb_path) as (_, api):
        for group_name, patterns in DEFAULT_GROUPS.items():
            hits = find_names_by_substrings(api, patterns)
            lines.extend(render_group(group_name, hits[:200]))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--idb", default=str(DEFAULT_CLIENT_IDB))
    args = parser.parse_args()

    idb_path = Path(args.idb)
    ensure_generated_root()
    out = GENERATED_ROOT / f"{sanitize_name(idb_path.stem)}_names.md"
    write_text(out, build_markdown(idb_path))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
