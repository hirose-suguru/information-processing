from __future__ import annotations

from .constants import DIGIT_WORDS, FENCE_RE, HEADING_RE


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
    """'5.2.2' -> 'five-two-two'"""
    parts = [DIGIT_WORDS[ch] for ch in number_str.replace(".", "") if ch in DIGIT_WORDS]
    return "-".join(parts)
