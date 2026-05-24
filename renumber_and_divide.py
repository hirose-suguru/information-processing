from __future__ import annotations

import sys
from pathlib import Path

from modules import fix_missing_levels, insert_anchors, renumber, update_links
from modules.config import ConfigManager


def process_markdown(text: str) -> tuple[str, dict[str, str]]:
    lines = text.splitlines()

    lines = fix_missing_levels(lines)               # Pass 1: 欠落レベル補完
    lines, mapping, id_to_title, old_id_to_new_id = renumber(lines)  # Pass 2: 連番付与 + 対応表生成
    lines = insert_anchors(lines)                   # Pass 3: アンカー挿入
    lines = update_links(lines, mapping, id_to_title, old_id_to_new_id)  # Pass 4: インラインリンク更新

    return "\n".join(lines) + "\n", old_id_to_new_id


def process_all_files(config: ConfigManager) -> int:
    """information_processing.md と全セクションファイルを処理"""
    # メインファイル処理
    main_path = Path("information_processing.md")
    if not main_path.exists():
        print(f"File not found: {main_path}", file=sys.stderr)
        return 1

    original = main_path.read_text(encoding="utf-8")
    updated, old_id_to_new_id = process_markdown(original)
    main_path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Processed: {main_path}")

    # セクションファイルを処理
    for section_num, file_path in config.get_section_files():
        section_file = Path(file_path)
        if not section_file.exists():
            print(f"Warning: Section file not found: {section_file}", file=sys.stderr)
            continue

        original = section_file.read_text(encoding="utf-8")
        updated, section_old_id_to_new_id = process_markdown(original)
        section_file.write_text(updated, encoding="utf-8", newline="\n")
        print(f"Processed: {section_file}")

        # ID マッピングをキャッシュに記録
        for old_id, new_id in section_old_id_to_new_id.items():
            config.update_id_mapping(old_id, new_id, section_num)

    # config.toml を更新
    config.save()
    print(f"Updated: {config.config_path}")
    return 0


def main() -> int:
    args = sys.argv[1:]

    if len(args) == 0:
        print("Usage: python renumber_and_divide.py <file.md> [output.md]", file=sys.stderr)
        print("  1 arg:   process single file in-place", file=sys.stderr)
        print("  2 args:  process input.md and write to output.md", file=sys.stderr)
        return 1

    # 引数がある場合は単一ファイル処理
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

    original = in_path.read_text(encoding="utf-8")
    updated, _ = process_markdown(original)
    out_path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Processed: {in_path} -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
