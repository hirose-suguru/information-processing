from __future__ import annotations

import tomlkit
from pathlib import Path

from modules.cache import SectionCache


class ConfigManager:
    """file_title.toml の読み書きとセクション管理"""

    def __init__(self, config_path: Path | str = Path("file_title.toml")):
        self.config_path = Path(config_path)
        self.sections: dict[int, dict] = {}  # { 1: {file, title}, 2: {...}, ... }
        self.cache = SectionCache()
        self._load()

    def _load(self) -> None:
        """file_title.toml を読み込み"""
        if not self.config_path.exists():
            # デフォルト設定で初期化
            self._init_default()
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            data = tomlkit.parse(f.read())

        # [sections] を読み込み
        sections_data = data.get("sections", {})
        for key, value in sections_data.items():
            section_num = int(key)
            self.sections[section_num] = {
                "file": value.get("file", ""),
                "title": value.get("title", ""),
            }

        # キャッシュを復元
        if "cache" in data:
            self.cache = SectionCache.from_dict(data["cache"])
        else:
            # キャッシュが無ければ sections から生成
            self._regenerate_cache()

    def _init_default(self) -> None:
        """デフォルト設定を作成（既存の note_segments ファイルから）"""
        note_segments_dir = Path("note_segments")
        if not note_segments_dir.exists():
            return

        # 既存ファイルから sections を構成
        section_num = 1
        for md_file in sorted(note_segments_dir.glob("*.md")):
            title = md_file.stem  # ファイル名から拡張子を除いた部分
            self.sections[section_num] = {
                "file": str(md_file),
                "title": title,
            }
            section_num += 1

        self._regenerate_cache()

    def _regenerate_cache(self) -> None:
        """sections からキャッシュを再生成"""
        self.cache = SectionCache()
        for section_num, info in self.sections.items():
            title = info.get("title", "")
            file_path = info.get("file", "")
            if title and file_path:
                self.cache.set_section_file(section_num, title, file_path)

    def get_section_files(self) -> list[tuple[int, str]]:
        """(セクション番号, ファイルパス) のリストを返す"""
        result = []
        for section_num in sorted(self.sections.keys()):
            file_path = self.sections[section_num].get("file", "")
            if file_path:
                result.append((section_num, file_path))
        return result

    def update_id_mapping(self, old_id: str, new_id: str, section_num: int) -> None:
        """ID の変更を記録"""
        title = self.sections.get(section_num, {}).get("title", "")
        self.cache.update_id_mapping(old_id, new_id, title)

    def save(self) -> None:
        """file_title.toml に書き込み"""
        # sections を TOML フォーマットに変換
        sections_dict = tomlkit.table()
        for section_num, info in sorted(self.sections.items()):
            sections_dict[str(section_num)] = tomlkit.table()
            sections_dict[str(section_num)]["file"] = info["file"]
            sections_dict[str(section_num)]["title"] = info["title"]

        cache_dict = tomlkit.table()
        cache_data = self.cache.to_dict()
        cache_dict["id_to_section"] = cache_data["id_to_section"]
        cache_dict["section_to_file"] = cache_data["section_to_file"]
        cache_dict["number_to_section"] = cache_data["number_to_section"]

        data = tomlkit.document()
        data["sections"] = sections_dict
        data["cache"] = cache_dict

        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(tomlkit.dumps(data))
