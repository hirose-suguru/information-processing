from __future__ import annotations

import re
from pathlib import Path

from .cache import CacheManager
from .config import ConfigManager
from .splitter import Splitter


class SplitManager:
    """information_processing.md を分割して note_segments に保存"""

    def __init__(self, main_file: Path | str = Path("information_processing.md"),
                 output_dir: Path | str = Path("note_segments"),
                 config_path: Path | str = Path("file_title.toml")):
        self.main_file = Path(main_file)
        self.file_key = self.main_file.stem
        self.output_dir = Path(output_dir)
        self.config = ConfigManager(config_path)
        self.cache = CacheManager()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_section_from_content(self, text: str) -> list[tuple[str, str]]:
        """# で始まる見出しごとにセクションを分割"""
        return Splitter.extract_sections(text)

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Windows で使えない文字を除去し、末尾の空白/ドットを避ける。"""
        sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f`]', "_", name)
        sanitized = re.sub(r"\s+", " ", sanitized).strip(" .")
        return sanitized or "untitled"

    @staticmethod
    def _normalize_section_title(title: str) -> str:
        """見出しから分割ファイル用のタイトルを取り出す。"""
        clean_title = re.sub(r"^\d+(?:\.\d+)*\.\s*", "", title).strip()
        letter_dash_match = re.match(r"^([A-Za-z])\s+―(?:\s.*)?$", clean_title)
        if letter_dash_match is not None:
            return letter_dash_match.group(1)
        return clean_title

    @staticmethod
    def _format_section_number(section_number: int) -> str:
        """分割ファイルの番号は 2 桁でゼロ埋めする。"""
        return f"{section_number:02d}"

    def _build_file_name(self, section_number: int, title: str) -> str:
        formatted_number = self._format_section_number(section_number)
        return f"{formatted_number}_{self._sanitize_filename(title)}"

    def auto_generate_section_map(self) -> dict[str, str]:
        """TOML に [sections.information_processing] がない場合、
        実際の # 見出しから section_N → file_name を自動生成
        """
        if not self.main_file.exists():
            return {}

        text = self.main_file.read_text(encoding="utf-8")
        sections = self.extract_section_from_content(text)

        section_map = {}
        for i, (title, _) in enumerate(sections, 1):
            clean_title = self._normalize_section_title(title)
            file_name = self._build_file_name(i, clean_title)
            section_map[f"section_{i}"] = file_name
            self.config.set_section(self.file_key, f"section_{i}", clean_title)

        self.config.save()
        return section_map

    def split(self) -> None:
        """分割処理を実行"""
        if not self.main_file.exists():
            print(f"File not found: {self.main_file}")
            return

        text = self.main_file.read_text(encoding="utf-8")
        sections = self.extract_section_from_content(text)

        existing_section_map = self.config.get_sections(self.file_key)
        existing_section_keys = [
            key for key in existing_section_map.keys() if re.match(r"^section_\d+$", key)
        ]
        prefer_config_titles = len(existing_section_keys) == len(sections)
        resolved_section_titles: dict[str, str] = {}
        for i, (title, _) in enumerate(sections, 1):
            section_key = f"section_{i}"
            extracted_title = self._normalize_section_title(title)
            if prefer_config_titles and section_key in existing_section_map:
                resolved_title = existing_section_map[section_key]
            else:
                resolved_title = extracted_title
            resolved_section_titles[section_key] = resolved_title
            self.config.set_section(self.file_key, section_key, resolved_title)

        self.config.prune_sections(self.file_key, len(sections))
        self.config.save()

        section_to_file = {}
        for i in range(1, len(sections) + 1):
            section_key = f"section_{i}"
            if section_key in resolved_section_titles:
                clean_title = resolved_section_titles[section_key]
                file_name = self._build_file_name(i, clean_title)
                section_to_file[section_key] = file_name

        cached_file_names = self.cache.load_split_file_names(self.file_key)
        Splitter.split_and_save(self.main_file, self.output_dir, section_to_file, cached_file_names)
        self.cache.save_split_file_names(self.file_key, section_to_file)

        section_number_title = {}
        for i in range(1, len(sections) + 1):
            section_key = f"section_{i}"
            if section_key in resolved_section_titles:
                section_number_title[str(i)] = resolved_section_titles[section_key]
        self.cache.save_section_number_title(self.file_key, section_number_title)

        # 分割結果をログ
        for i, (title, _) in enumerate(sections, 1):
            section_key = f"section_{i}"
            if section_key in section_to_file:
                file_name = section_to_file[section_key]
                print(f"Split: {title} -> {self.output_dir / file_name}.md")
