from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from modules import CacheManager, fix_missing_levels, insert_anchors, renumber, update_links
from modules.split import SplitManager


def process_markdown(text: str) -> tuple[str, dict[str, tuple[str, str]], dict[str, str]]:
    """markdown を4パスで処理"""
    lines = text.splitlines()

    lines = fix_missing_levels(lines)
    lines, mapping, id_to_title = renumber(lines)
    lines = insert_anchors(lines)
    lines = update_links(lines, mapping, id_to_title)

    return "\n".join(lines) + "\n", mapping, id_to_title


def main() -> int:
    args = sys.argv[1:]

    if len(args) == 0:
        print("Usage: python renumber_and_divide.py <file.md> [output.md]", file=sys.stderr)
        print("  1 arg:   process single file in-place", file=sys.stderr)
        print("  2 args:  process input.md and write to output.md", file=sys.stderr)
        return 1

    if len(args) == 1:
        in_path = out_path = Path(args[0])
    elif len(args) == 2:
        in_path, out_path = Path(args[0]), Path(args[1])
    else:
        print("Usage: python renumber_and_divide.py <file.md> [output.md]", file=sys.stderr)
        return 1

    if not in_path.exists():
        print(f"File not found: {in_path}", file=sys.stderr)
        return 1

    cache = CacheManager()
    config_path = Path("file_title.toml")
    original = in_path.read_text(encoding="utf-8")
    config_text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    signature_source = "\n".join([str(in_path.resolve()), original, config_text])
    signature = hashlib.sha256(signature_source.encode("utf-8")).hexdigest()
    cached_signature = cache.load_input_signature(out_path.stem)
    if cached_signature == signature and out_path.exists():
        print(f"Skipped (cache hit): {in_path}")
        return 0

    updated, _, id_to_title = process_markdown(original)
    out_path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Processed: {in_path} -> {out_path}")

    # 見出しIDとタイトルの対応をキャッシュ
    cache.save_id_section_title(out_path.stem, id_to_title)

    # 分割処理を実行
    splitter = SplitManager(out_path)
    splitter.split()
    cache.save_input_signature(out_path.stem, signature)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
