from __future__ import annotations

import re
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*$")
EXISTING_NUMBER_RE = re.compile(r"^\s*\d+(?:\.\d+)*\.?\s*")


def renumber_markdown(text: str) -> str:
    counters = [0, 0, 0, 0, 0, 0]
    output_lines: list[str] = []

    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if not match:
            output_lines.append(line)
            continue

        hashes, title = match.groups()
        level = len(hashes)
        clean_title = EXISTING_NUMBER_RE.sub("", title)

        counters[level - 1] += 1
        for i in range(level, 6):
            counters[i] = 0

        number_parts = [str(counters[i]) for i in range(level) if counters[i] > 0]
        numbered_prefix = ".".join(number_parts) + "."
        output_lines.append(f"{hashes} {numbered_prefix} {clean_title}")

    return "\n".join(output_lines) + "\n"


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("information_processing.md")
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    original = path.read_text(encoding="utf-8")
    updated = renumber_markdown(original)
    path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Renumbered headings in: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
