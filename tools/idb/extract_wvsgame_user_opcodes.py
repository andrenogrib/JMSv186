from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import GENERATED_ROOT, IDB_ROOT, ensure_generated_root, format_ea, open_api, write_text


DEFAULT_SERVER_IDB = IDB_ROOT / "BMS_srv" / "BMS_WvsGame.idb"
TARGET_FUNCTION = "OnPacket@CUser@@QAEXJAAVCInPacket"
FOCUS_OPCODES = [0x56, 0x5F, 0xC4]


def read_dword(api, ea: int) -> int:
    data = api.idc.GetManyBytes(ea, 4)
    return int.from_bytes(data, "little")


def try_get_name(api, ea: int) -> str:
    try:
        name = api.idc.GetFunctionName(ea) or ""
    except Exception:
        name = ""
    if not name:
        name = api.ida_name.get_name(ea) or ""
    return name


def find_target_function(api) -> int:
    for ea in api.idautils.Functions():
        name = try_get_name(api, int(ea))
        if TARGET_FUNCTION.lower() in name.lower():
            return int(ea)
    raise RuntimeError(f"Could not find `{TARGET_FUNCTION}`")


def parse_switch_metadata(api, func_ea: int) -> tuple[int, int, int, int, int]:
    func = api.idaapi.get_func(func_ea)

    opcode_base = None
    opcode_delta_max = None
    byte_table_ea = None
    jump_table_ea = None

    for head in api.idautils.Heads(func.startEA, func.endEA):
        disasm = api.idc.GetDisasm(head)

        if opcode_base is None:
            match = re.search(r"lea\s+eax,\s+\[ebx\s*-\s*(0x[0-9a-fA-F]+)\]", disasm)
            if match:
                opcode_base = int(match.group(1), 16)
                continue

        if opcode_base is not None and opcode_delta_max is None:
            match = re.search(r"cmp\s+eax,\s*(0x[0-9a-fA-F]+)", disasm)
            if match:
                opcode_delta_max = int(match.group(1), 16)
                continue

        if byte_table_ea is None:
            match = re.search(r"movzx\s+eax,\s+byte ptr \[eax \+ (0x[0-9a-fA-F]+)\]", disasm)
            if match:
                byte_table_ea = int(match.group(1), 16)
                continue

        if jump_table_ea is None:
            match = re.search(r"jmp\s+dword ptr \[eax\*4 \+ (0x[0-9a-fA-F]+)\]", disasm)
            if match:
                jump_table_ea = int(match.group(1), 16)
                continue

    if None in (opcode_base, opcode_delta_max, byte_table_ea, jump_table_ea):
        raise RuntimeError("Failed to parse compressed switch metadata from CUser::OnPacket")

    return (
        int(func.startEA),
        int(func.endEA),
        int(opcode_base),
        int(opcode_delta_max),
        int(byte_table_ea),
        int(jump_table_ea),
    )


def resolve_call_target(api, ea: int) -> tuple[int | None, str]:
    operand = api.idc.GetOpnd(ea, 0)
    if operand.startswith("0x"):
        target = int(operand, 16)
        return target, try_get_name(api, target)
    return None, operand


def extract_case_handler(api, case_target: int, dispatch_end: int) -> tuple[int | None, str]:
    max_end = min(case_target + 0x30, dispatch_end)
    for head in api.idautils.Heads(case_target, max_end):
        if api.idc.GetMnem(head).lower() == "call":
            target_ea, target_name = resolve_call_target(api, head)
            if target_ea is not None:
                return target_ea, target_name
            return None, target_name
        if head != case_target and api.idc.GetMnem(head).lower() == "jmp":
            break
    return None, ""


def decode_entries(api, func_start: int, func_end: int, opcode_base: int, opcode_delta_max: int, byte_table_ea: int, jump_table_ea: int) -> list[dict[str, object]]:
    entries = []
    max_opcode = opcode_base + opcode_delta_max
    for opcode in range(opcode_base, max_opcode + 1):
        idx = opcode - opcode_base
        case_index = api.idc.IdbByte(byte_table_ea + idx)
        case_target = read_dword(api, jump_table_ea + case_index * 4)
        handler_ea, handler_name = extract_case_handler(api, case_target, func_end)
        entries.append(
            {
                "opcode": opcode,
                "case_index": case_index,
                "case_target": case_target,
                "handler_ea": handler_ea,
                "handler_name": handler_name,
            }
        )
    return entries


def build_markdown(idb_path: Path) -> str:
    lines: list[str] = []

    with open_api(idb_path) as (_, api):
        func_ea = find_target_function(api)
        func_start, func_end, opcode_base, opcode_delta_max, byte_table_ea, jump_table_ea = parse_switch_metadata(api, func_ea)
        entries = decode_entries(api, func_start, func_end, opcode_base, opcode_delta_max, byte_table_ea, jump_table_ea)
        entry_by_opcode = {entry["opcode"]: entry for entry in entries}

        lines.append("# WvsGame User Packet Switch")
        lines.append("")
        lines.append("This document is extracted from `CUser::OnPacket` in `BMS_WvsGame.idb`.")
        lines.append("")
        lines.append(f"- Function: `{try_get_name(api, func_ea)}`")
        lines.append(f"- Function start: `{format_ea(func_start)}`")
        lines.append(f"- Function end: `{format_ea(func_end)}`")
        lines.append(f"- Opcode base: `0x{opcode_base:02X}`")
        lines.append(f"- Opcode max: `0x{opcode_base + opcode_delta_max:02X}`")
        lines.append(f"- Byte table: `{format_ea(byte_table_ea)}`")
        lines.append(f"- Jump table: `{format_ea(jump_table_ea)}`")
        lines.append("")

        lines.append("## Focus Opcodes")
        lines.append("")
        lines.append("| Opcode | Result | Case | Case Target | Handler |")
        lines.append("| --- | --- | --- | --- | --- |")
        for opcode in FOCUS_OPCODES:
            entry = entry_by_opcode.get(opcode)
            if entry is None:
                lines.append(f"| `0x{opcode:02X}` | Outside primary `CUser::OnPacket` switch |  |  |  |")
                continue
            handler_ea = entry["handler_ea"]
            handler_name = entry["handler_name"] or "_unnamed_"
            handler_text = handler_name
            if handler_ea is not None:
                handler_text = f"`{format_ea(handler_ea)}` `{handler_name or '_unnamed_'}`"
            lines.append(
                f"| `0x{opcode:02X}` | Routed by `CUser::OnPacket` | `{entry['case_index']}` | `{format_ea(int(entry['case_target']))}` | {handler_text} |"
            )
        lines.append("")

        lines.append("## Full Switch Map")
        lines.append("")
        lines.append("| Opcode | Case | Case Target | Handler |")
        lines.append("| --- | --- | --- | --- |")
        for entry in entries:
            handler_ea = entry["handler_ea"]
            handler_name = entry["handler_name"] or "_unnamed_"
            if handler_ea is not None:
                handler_text = f"`{format_ea(handler_ea)}` `{handler_name}`"
            else:
                handler_text = f"`{handler_name}`" if handler_name else "_no direct call found_"
            lines.append(
                f"| `0x{int(entry['opcode']):02X}` | `{entry['case_index']}` | `{format_ea(int(entry['case_target']))}` | {handler_text} |"
            )
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--idb", default=str(DEFAULT_SERVER_IDB))
    args = parser.parse_args()

    idb_path = Path(args.idb)
    ensure_generated_root()
    out = GENERATED_ROOT / "BMS_WvsGame_user_packet_switch.md"
    write_text(out, build_markdown(idb_path))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
