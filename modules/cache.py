from __future__ import annotations

import json
from pathlib import Path


class CacheManager:
    """.cache/renumber_and_divide 配下のキャッシュファイルを管理"""

    def __init__(self, cache_dir: Path | str = Path(".cache/renumber_and_divide")):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_section_cache_dir(self, section_name: str) -> Path:
        """セクション名からキャッシュディレクトリを取得"""
        return self.cache_dir / section_name

    def load_id_section_title(self, section_name: str) -> dict[str, str]:
        """id_section_title.json を読み込み（old_id → section_title）"""
        cache_dir = self.get_section_cache_dir(section_name)
        cache_file = cache_dir / "id_section_title.json"
        if not cache_file.exists():
            return {}
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_id_section_title(self, section_name: str, mapping: dict[str, str]) -> None:
        """id_section_title.json に保存"""
        cache_dir = self.get_section_cache_dir(section_name)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / "id_section_title.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)

    def load_section_number_title(self, section_name: str) -> dict[str, str]:
        """section_number_title.json を読み込み（section_number → title）"""
        cache_dir = self.get_section_cache_dir(section_name)
        cache_file = cache_dir / "section_number_title.json"
        if not cache_file.exists():
            return {}
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_section_number_title(self, section_name: str, mapping: dict[str, str]) -> None:
        """section_number_title.json に保存"""
        cache_dir = self.get_section_cache_dir(section_name)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / "section_number_title.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)

    def load_split_file_names(self, section_name: str) -> dict[str, str]:
        """split_file_names.json を読み込み（section_N → file_name）"""
        cache_dir = self.get_section_cache_dir(section_name)
        cache_file = cache_dir / "split_file_names.json"
        if not cache_file.exists():
            return {}
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_split_file_names(self, section_name: str, mapping: dict[str, str]) -> None:
        """split_file_names.json に保存"""
        cache_dir = self.get_section_cache_dir(section_name)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / "split_file_names.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)

    def update_id_mapping(self, section_name: str, old_id: str, new_id: str, title: str) -> None:
        """ID の変更をキャッシュに記録"""
        id_mapping = self.load_id_section_title(section_name)
        if old_id in id_mapping:
            del id_mapping[old_id]
        id_mapping[new_id] = title
        self.save_id_section_title(section_name, id_mapping)

    def update_section_number(self, section_name: str, section_num: int, title: str) -> None:
        """セクション番号とタイトルをキャッシュに記録"""
        num_mapping = self.load_section_number_title(section_name)
        num_mapping[str(section_num)] = title
        self.save_section_number_title(section_name, num_mapping)

    def load_input_signature(self, section_name: str) -> str | None:
        """input_signature.txt を読み込み"""
        cache_dir = self.get_section_cache_dir(section_name)
        cache_file = cache_dir / "input_signature.txt"
        if not cache_file.exists():
            return None
        return cache_file.read_text(encoding="utf-8").strip()

    def save_input_signature(self, section_name: str, signature: str) -> None:
        """input_signature.txt に保存"""
        cache_dir = self.get_section_cache_dir(section_name)
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / "input_signature.txt"
        cache_file.write_text(signature + "\n", encoding="utf-8", newline="\n")
