from __future__ import annotations

from .constants import DIGIT_WORDS, FENCE_RE, HEADING_RE, ID_SEGMENT_RE, WORD_TO_DIGIT


def build_level_list(lines: list[str]) -> list[int]:
    """各行の見出しレベルを返す（非見出し・コードブロック内は 0）。"""
    result = []
    in_fence = False
    fence_char = ""
    for line in lines:
        fm = FENCE_RE.match(line)
        if fm:
            ch = fm.group(1)[0]
            if not in_fence:
                in_fence, fence_char = True, ch
            elif ch == fence_char:
                in_fence = False
            result.append(0)
            continue
        if in_fence:
            result.append(0)
            continue
        m = HEADING_RE.match(line)
        result.append(len(m.group(1)) if m else 0)
    return result


def number_to_id(number_str: str) -> str:
    """'12.2.4' -> '12-2-4'"""
    parts = [part for part in number_str.split(".") if part]
    return "-".join(parts)


def number_to_legacy_id(number_str: str) -> str:
    """'12.2.4' -> 'one-two-two-four'"""
    parts = [DIGIT_WORDS[ch] for ch in number_str.replace(".", "") if ch in DIGIT_WORDS]
    return "-".join(parts)


def legacy_id_to_number(anchor_id: str) -> str | None:
    """旧形式の ID を番号へ戻す。"""
    if not anchor_id:
        return None

    parts = anchor_id.split("-")
    if not all(part in WORD_TO_DIGIT for part in parts):
        return None
    return ".".join(WORD_TO_DIGIT[part] for part in parts)


def id_to_number(anchor_id: str) -> str | None:
    """新旧どちらの ID 形式でも番号表現へ戻す。"""
    if ID_SEGMENT_RE.fullmatch(anchor_id):
        return anchor_id.replace("-", ".")
    return legacy_id_to_number(anchor_id)
