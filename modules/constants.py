from __future__ import annotations

import re

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*$")
EXISTING_NUMBER_RE = re.compile(r"^\s*\d+(?:\.\d+)*\.?\s*")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
ANCHOR_TAG_RE = re.compile(r'^<a id="[^"]+"></a>$')
INLINE_LINK_RE = re.compile(r'\[([^\]]*)\]\(#([\w-]+)\)')

DIGIT_WORDS = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
}

# DIGIT_WORDS の値セット（id が数字由来かの判定用）
_DIGIT_WORD_SET = set(DIGIT_WORDS.values())


def is_numeric_id(anchor_id: str) -> bool:
    """'five-two-two' のように数字由来の単語だけで構成されているか判定。"""
    return all(part in _DIGIT_WORD_SET for part in anchor_id.split("-"))
