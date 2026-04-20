from __future__ import annotations

import sys
from pathlib import Path

from modules import fix_missing_levels, insert_anchors, renumber, update_links


def process_markdown(text: str) -> str:
    lines = text.splitlines()

    lines = fix_missing_levels(lines)       # Pass 1: 欠落レベル補完
    lines, mapping = renumber(lines)        # Pass 2: 連番付与 + 対応表生成
    lines = insert_anchors(lines)           # Pass 3: アンカー挿入
    lines = update_links(lines, mapping)    # Pass 4: インラインリンク更新

    return "\n".join(lines) + "\n"


def main() -> int:
    args = sys.argv[1:]
    if len(args) == 0:
        in_path = Path("information_processing.md")
        out_path = in_path
    elif len(args) == 1:
        in_path = out_path = Path(args[0])
    else:
        in_path, out_path = Path(args[0]), Path(args[1])

    if not in_path.exists():
        print(f"File not found: {in_path}", file=sys.stderr)
        return 1

    original = in_path.read_text(encoding="utf-8")
    updated = process_markdown(original)
    out_path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Processed: {in_path} -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
