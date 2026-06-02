from __future__ import annotations

import re
import tomlkit
from pathlib import Path


class ConfigManager:
    """file_title.toml の読み書き"""

    def __init__(self, config_path: Path | str = Path("file_title.toml")):
        self.config_path = Path(config_path)
        self.data = tomlkit.document()
        self._load()

    def _load(self) -> None:
        """file_title.toml を読み込み"""
        if not self.config_path.exists():
            # デフォルト構造を初期化
            self.data["sections"] = tomlkit.table()
            self.data["sections"]["information_processing"] = tomlkit.table()
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.data = tomlkit.parse(f.read())

    def get_sections(self, file_key: str = "information_processing") -> dict[str, str]:
        """セクション定義を取得（section_N → title）"""
        if "sections" not in self.data:
            return {}
        if file_key not in self.data["sections"]:
            return {}
        return dict(self.data["sections"][file_key])

    def set_section(self, file_key: str, section_key: str, title: str) -> None:
        """セクション定義を設定"""
        if "sections" not in self.data:
            self.data["sections"] = tomlkit.table()
        if file_key not in self.data["sections"]:
            self.data["sections"][file_key] = tomlkit.table()
        self.data["sections"][file_key][section_key] = title

    def prune_sections(self, file_key: str, max_section_number: int) -> None:
        """section_1..max_section_number 以外の section_N を削除"""
        if "sections" not in self.data or file_key not in self.data["sections"]:
            return
        table = self.data["sections"][file_key]
        keys_to_remove = []
        for key in table.keys():
            match = re.match(r"^section_(\d+)$", str(key))
            if match is None:
                continue
            if int(match.group(1)) > max_section_number:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del table[key]

    def save(self) -> None:
        """file_title.toml に書き込み"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(tomlkit.dumps(self.data))
