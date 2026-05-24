from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SectionCache:
    """セクション情報のキャッシュ: id ↔ section_title ↔ file_name"""

    id_to_section: dict[str, str] = field(default_factory=dict)
    """アンカーID (one, two, one-one) → セクションタイトル"""

    section_to_file: dict[str, str] = field(default_factory=dict)
    """セクションタイトル → ファイルパス (note_segments/言語理論.md など)"""

    number_to_section: dict[int, str] = field(default_factory=dict)
    """セクション番号 (1, 2, 3) → セクションタイトル"""

    def update_id_mapping(self, old_id: str, new_id: str, section_title: str) -> None:
        """ID の変更を記録（番号リネーム時に使用）"""
        if old_id in self.id_to_section:
            del self.id_to_section[old_id]
        self.id_to_section[new_id] = section_title

    def set_section_file(self, section_num: int, section_title: str, file_path: str) -> None:
        """セクション番号 ↔ タイトル ↔ ファイルパスを同時に設定"""
        self.number_to_section[section_num] = section_title
        self.section_to_file[section_title] = file_path

    def get_file_by_number(self, section_num: int) -> str | None:
        """セクション番号からファイルパスを取得"""
        title = self.number_to_section.get(section_num)
        if title:
            return self.section_to_file.get(title)
        return None

    def to_dict(self) -> dict:
        """TOML への変換用辞書化"""
        return {
            "id_to_section": self.id_to_section,
            "section_to_file": self.section_to_file,
            "number_to_section": {str(k): v for k, v in self.number_to_section.items()},
        }

    @classmethod
    def from_dict(cls, data: dict) -> SectionCache:
        """TOML からの復元"""
        cache = cls()
        cache.id_to_section = data.get("id_to_section", {})
        cache.section_to_file = data.get("section_to_file", {})
        cache.number_to_section = {int(k): v for k, v in data.get("number_to_section", {}).items()}
        return cache
