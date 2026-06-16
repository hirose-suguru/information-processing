from __future__ import annotations

import re

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*$")
EXISTING_NUMBER_RE = re.compile(r"^\s*\d+(?:\.\d+)*\.?\s*")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
ANCHOR_TAG_RE = re.compile(r'^<a id="[^"]+">(</a>|<a/>)$')
INLINE_LINK_RE = re.compile(r'\[([^\]]*)\]\(#([\w-]+)\)')
ID_SEGMENT_RE = re.compile(r"^\d+(?:-\d+)*$")

DIGIT_WORDS = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
}
WORD_TO_DIGIT = {word: digit for digit, word in DIGIT_WORDS.items()}

# DIGIT_WORDS の値セット（id が数字由来かの判定用）
_DIGIT_WORD_SET = set(DIGIT_WORDS.values())


def is_numeric_id(anchor_id: str) -> bool:
    """新旧どちらの数値由来 ID 形式か判定。"""
    return bool(ID_SEGMENT_RE.fullmatch(anchor_id)) or all(
        part in _DIGIT_WORD_SET for part in anchor_id.split("-")
    )
