from __future__ import annotations

import argparse
from pathlib import Path

from common import DEFAULT_CLIENT_IDB, GENERATED_ROOT, ensure_generated_root, find_names_by_substrings, format_ea, open_api, sanitize_name, write_text


TARGET_FUNCTION_PATTERNS = [
    "OnPacket@CLogin",
    "OnPacket@CField",
    "OnPacket@CMobPool",
    "OnPacket@CNpcPool",
    "OnPacket@CUserPool",
    "OnUserCommonPacket@CUserPool",
    "OnUserRemotePacket@CUserPool",
    "OnUserLocalPacket@CUserPool",
    "OnPacket@CWvsContext",
]


def decode_call_target(api, ea: int) -> str:
    op0 = api.idc.GetOpnd(ea, 0)
    if op0.startswith("0x"):
        target = int(op0, 16)
        target_name = api.ida_name.get_name(target) or ""
        return f"{format_ea(target)} {target_name}".strip()
    return op0


def render_function(api, ea: int, name: str) -> list[str]:
    func = api.idaapi.get_func(ea)
    lines = []
    lines.append(f"## {name}")
    lines.append("")
    lines.append(f"- Start: `{format_ea(func.startEA)}`")
    lines.append(f"- End: `{format_ea(func.endEA)}`")
    lines.append("")
    lines.append("### Calls")
    lines.append("")
    call_lines = []
    for head in api.idautils.Heads(func.startEA, func.endEA):
        if api.idc.GetMnem(head).lower() == "call":
            call_lines.append(f"- `{format_ea(head)}` -> `{decode_call_target(api, head)}`")
    if call_lines:
        lines.extend(call_lines[:200])
    else:
        lines.append("_No direct call instructions found._")
    lines.append("")
    lines.append("### Disassembly")
    lines.append("")
    lines.append("```asm")
    for head in api.idautils.Heads(func.startEA, func.endEA):
        lines.append(f"{format_ea(head)}  {api.idc.GetDisasm(head)}")
    lines.append("```")
    lines.append("")
    return lines


def build_markdown(idb_path: Path) -> str:
    lines = []
    lines.append(f"# Dispatch Walk: `{idb_path.name}`")
    lines.append("")
    lines.append("This dump focuses on packet-facing functions that are already named in the IDB.")
    lines.append("")
    with open_api(idb_path) as (_, api):
        hits = find_names_by_substrings(api, TARGET_FUNCTION_PATTERNS)
        seen = set()
        ordered_hits = []
        for ea, name in hits:
            if name in seen:
                continue
            seen.add(name)
            ordered_hits.append((ea, name))
        for ea, name in ordered_hits:
            lines.extend(render_function(api, ea, name))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--idb", default=str(DEFAULT_CLIENT_IDB))
    args = parser.parse_args()

    idb_path = Path(args.idb)
    ensure_generated_root()
    out = GENERATED_ROOT / f"{sanitize_name(idb_path.stem)}_dispatch.md"
    write_text(out, build_markdown(idb_path))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
