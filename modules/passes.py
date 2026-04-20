from __future__ import annotations

import re

from .constants import (
    ANCHOR_TAG_RE, EXISTING_NUMBER_RE, HEADING_RE, INLINE_LINK_RE, is_numeric_id,
)
from .helpers import build_level_list, number_to_id


# ---------------------------------------------------------------------------
# Pass 1: 欠落レベルの補完
#   レベル L の見出し直下に L+1 がなく L+2 以下だけある場合、
#   その子孫見出しを全て1段階上げる。収束するまで繰り返す。
# ---------------------------------------------------------------------------

def _fix_levels_once(levels: list[int]) -> tuple[list[int], bool]:
    n = len(levels)
    new_levels = list(levels)
    changed = False

    for i, lv in enumerate(levels):
        if lv == 0:
            continue
        child_levels = []
        for j in range(i + 1, n):
            clv = levels[j]
            if clv == 0:
                continue
            if clv <= lv:
                break
            child_levels.append(clv)

        if not child_levels or min(child_levels) <= lv + 1:
            continue

        for j in range(i + 1, n):
            clv = levels[j]
            if clv == 0:
                continue
            if clv <= lv:
                break
            new_levels[j] = clv - 1
            changed = True

    return new_levels, changed


def fix_missing_levels(lines: list[str]) -> list[str]:
    levels = build_level_list(lines)
    for _ in range(10):
        levels, changed = _fix_levels_once(levels)
        if not changed:
            break

    result = []
    for line, lv in zip(lines, levels):
        m = HEADING_RE.match(line)
        if m is None or lv == 0:
            result.append(line)
        else:
            result.append(f"{'#' * lv} {m.group(2)}")
    return result


# ---------------------------------------------------------------------------
# Pass 2: 連番付与
#   戻り値: (変換後行リスト, {旧番号文字列: (新番号文字列, 新タイトル)} の対応表)
# ---------------------------------------------------------------------------

def renumber(lines: list[str]) -> tuple[list[str], dict[str, tuple[str, str]], dict[str, str]]:
    counters = [0, 0, 0, 0, 0, 0]
    result: list[str] = []
    mapping: dict[str, tuple[str, str]] = {}  # 旧番号 -> (新番号, 新タイトル)
    id_to_title: dict[str, str] = {}           # 新ID -> 新タイトル
    levels = build_level_list(lines)

    for line, lv in zip(lines, levels):
        if lv == 0:
            result.append(line)
            continue

        m = HEADING_RE.match(line)
        hashes, title = m.groups()
        old_number_m = re.match(r"(\d+(?:\.\d+)*)\.", title.lstrip())
        old_number = old_number_m.group(1) if old_number_m else None
        clean_title = EXISTING_NUMBER_RE.sub("", title)

        counters[lv - 1] += 1
        for i in range(lv, 6):
            counters[i] = 0

        new_number = ".".join(str(counters[i]) for i in range(lv))
        numbered_prefix = new_number + "."
        result.append(f"{hashes} {numbered_prefix} {clean_title}")

        if old_number:
            mapping[old_number] = (new_number, clean_title)
        id_to_title[number_to_id(new_number)] = clean_title

    return result, mapping, id_to_title


# ---------------------------------------------------------------------------
# Pass 3: アンカー挿入
# ---------------------------------------------------------------------------

def insert_anchors(lines: list[str]) -> list[str]:
    cleaned = [l for l in lines if not ANCHOR_TAG_RE.match(l)]
    levels = build_level_list(cleaned)

    result: list[str] = []
    for line, lv in zip(cleaned, levels):
        if lv == 0:
            result.append(line)
            continue

        m = HEADING_RE.match(line)
        title = m.group(2)
        number_match = re.match(r"(\d+(?:\.\d+)*)\.?\s*", title)
        if number_match:
            result.append(f'<a id="{number_to_id(number_match.group(1))}"></a>')
        result.append(line)

    return result


# ---------------------------------------------------------------------------
# Pass 4: インラインリンクの更新
#   [text](#old-id) の old-id が数字由来なら新 id に置換。
#   text が旧タイトルと一致すれば新タイトルにも置換。
# ---------------------------------------------------------------------------

def update_links(lines: list[str], mapping: dict[str, tuple[str, str]], id_to_title: dict[str, str]) -> list[str]:
    # mapping は 旧番号("5.2.2") -> (新番号("6.2.3"), 新タイトル)、IDが変わった場合の追跡用
    id_to_old: dict[str, str] = {}
    for old_num in mapping:
        old_id = number_to_id(old_num)
        id_to_old[old_id] = old_num

    def replace_link(match: re.Match) -> str:
        text, anchor_id = match.group(1), match.group(2)
        if not is_numeric_id(anchor_id):
            return match.group(0)

        # IDが変わった場合は新IDへ
        if anchor_id in id_to_old:
            old_num = id_to_old[anchor_id]
            new_num, new_title = mapping[old_num]
            new_id = number_to_id(new_num)
        elif anchor_id in id_to_title:
            new_id = anchor_id
            new_title = id_to_title[anchor_id]
        else:
            return match.group(0)

        new_text = new_title if text == "" else text
        return f"[{new_text}](#{new_id})"

    return [INLINE_LINK_RE.sub(replace_link, line) for line in lines]
