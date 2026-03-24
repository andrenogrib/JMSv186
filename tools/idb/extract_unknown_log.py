from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

from common import GENERATED_ROOT, ensure_generated_root, sanitize_name, write_text


HEADER_RE = re.compile(r"@([0-9A-Fa-f]{4})(?:\s+(.*))?$")


def parse_lines(text: str) -> tuple[Counter, dict[str, Counter]]:
    opcode_counts: Counter[str] = Counter()
    payload_counts: dict[str, Counter] = defaultdict(Counter)

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("@"):
            continue
        match = HEADER_RE.match(line)
        if not match:
            continue
        opcode = match.group(1).upper()
        payload = (match.group(2) or "").strip()
        opcode_counts[opcode] += 1
        payload_counts[opcode][payload] += 1

    return opcode_counts, payload_counts


def build_markdown(source_name: str, text: str) -> str:
    opcode_counts, payload_counts = parse_lines(text)

    lines = []
    lines.append(f"# Unknown Packet Summary: `{source_name}`")
    lines.append("")
    lines.append("| Opcode | Count |")
    lines.append("| --- | ---: |")
    for opcode, count in opcode_counts.most_common():
        lines.append(f"| `@{opcode}` | {count} |")
    lines.append("")

    for opcode, variants in payload_counts.items():
        lines.append(f"## `@{opcode}`")
        lines.append("")
        lines.append("| Payload | Count |")
        lines.append("| --- | ---: |")
        for payload, count in variants.most_common():
            payload_text = payload if payload else "(no payload)"
            lines.append(f"| `{payload_text}` | {count} |")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file")
    args = parser.parse_args()

    path = Path(args.log_file)
    ensure_generated_root()
    text = path.read_text(encoding="utf-8")
    out = GENERATED_ROOT / f"{sanitize_name(path.stem)}_unknown_packets.md"
    write_text(out, build_markdown(path.name, text))
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
