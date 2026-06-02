from __future__ import annotations

import re
from pathlib import Path


class Splitter:
    """information_processing.md を # レベルのセクションで分割"""

    @staticmethod
    def extract_sections(text: str) -> list[tuple[str, str]]:
        """# で始まる見出しでセクションを分割

        Returns:
            [(section_title, section_content), ...]
        """
        lines = text.split("\n")
        sections = []
        current_title = None
        current_lines = []
        in_fence = False
        fence_char = ""

        for line in lines:
            fence_match = re.match(r"^(`{3,}|~{3,})", line)
            if fence_match:
                ch = fence_match.group(1)[0]
                if not in_fence:
                    in_fence = True
                    fence_char = ch
                elif ch == fence_char:
                    in_fence = False
                if current_title is not None:
                    current_lines.append(line)
                continue

            if (not in_fence) and line.startswith("# "):
                # 新しいセクション開始
                if current_title is not None:
                    sections.append((current_title, "\n".join(current_lines).strip()))
                # タイトルを抽出（"# 1. タイトル" → "1. タイトル"）
                current_title = line[2:].strip()
                current_lines = [line]
            else:
                if current_title is not None:
                    current_lines.append(line)

        # 最後のセクションを追加
        if current_title is not None:
            sections.append((current_title, "\n".join(current_lines).strip()))

        return sections

    @staticmethod
    def create_section_file(section_content: str, file_path: Path) -> None:
        """セクションをファイルに保存"""
        file_path.write_text(section_content + "\n", encoding="utf-8", newline="\n")

    @staticmethod
    def remove_cached_section_files(output_dir: Path, cached_file_names: dict[str, str]) -> None:
        """前回作成した分割ファイルを削除"""
        for file_name in sorted(set(cached_file_names.values())):
            file_path = output_dir / f"{file_name}.md"
            if file_path.exists():
                file_path.unlink()

    @staticmethod
    def split_and_save(
        main_file: Path,
        output_dir: Path,
        section_map: dict[str, str],
        cached_file_names: dict[str, str] | None = None,
    ) -> None:
        """information_processing.md を分割して note_segments に保存

        Args:
            main_file: information_processing.md
            output_dir: 出力ディレクトリ（note_segments など）
            section_map: {"section_1": "file_name"} の対応
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        if cached_file_names:
            Splitter.remove_cached_section_files(output_dir, cached_file_names)

        text = main_file.read_text(encoding="utf-8")
        sections = Splitter.extract_sections(text)

        # section_1, section_2... の順番で対応
        for i, (title, content) in enumerate(sections, 1):
            section_key = f"section_{i}"
            if section_key not in section_map:
                continue
            file_name = section_map[section_key]
            file_path = output_dir / f"{file_name}.md"
            Splitter.create_section_file(content, file_path)
