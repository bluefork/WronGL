"""Keyboard layout definitions (Windows/Linux use the same ISIRI 9147 base)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LayoutProfile:
    name: str
    en_to_fa: dict[str, str]
    fa_to_en: dict[str, str]


def _build_en_to_fa() -> dict[str, str]:
    lower = {
        'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف',
        'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
        '[': 'ج', ']': 'چ',
        'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل',
        'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م', ';': 'ک', "'": 'گ',
        'z': 'ظ', 'x': 'ط', 'c': 'ز', 'v': 'ر', 'b': 'ذ',
        'n': 'د', 'm': 'ئ', ',': 'و', '.': '.', '/': '/', '\\': 'پ',
    }
    upper = {
        'Q': 'ض', 'W': 'ص', 'E': 'ث', 'R': 'ق', 'T': 'ف',
        'Y': 'غ', 'U': 'ع', 'I': 'ه', 'O': 'خ', 'P': 'ح',
        '{': 'ج', '}': 'چ',
        'A': 'ش', 'S': 'س', 'D': 'ی', 'F': 'ب', 'G': 'ل',
        'H': 'آ', 'J': 'ت', 'K': 'ن', 'L': 'م', ':': 'ک', '"': 'گ',
        'Z': 'ظ', 'X': 'ط', 'C': 'ز', 'V': 'ر', 'B': 'ذ',
        'N': 'د', 'M': 'ئ', '<': 'و', '>': '.', '?': '/', '|': 'ژ',
    }
    return {**lower, **upper}


def _build_fa_to_en(en_to_fa: dict[str, str]) -> dict[str, str]:
    reverse: dict[str, str] = {}
    for k, v in en_to_fa.items():
        reverse.setdefault(v, k)
    # prefer shifted variants for specific letters
    reverse['آ'] = 'H'
    reverse['ژ'] = '|'
    # Arabic lookalikes → shift keys
    reverse['أ'] = 'H'
    reverse['إ'] = 'H'
    reverse['ؤ'] = 'M'
    reverse['ۀ'] = 'M'
    return reverse


_EN2FA = _build_en_to_fa()
_FA2EN = _build_fa_to_en(_EN2FA)

PROFILES: dict[str, LayoutProfile] = {
    "windows": LayoutProfile("windows", _EN2FA, _FA2EN),
    "linux": LayoutProfile("linux", _EN2FA, _FA2EN),
}

DEFAULT_PROFILE = "windows"


def get_profile(name: str) -> LayoutProfile:
    if name not in PROFILES:
        raise ValueError(f"Unknown profile: {name}. Available: {list(PROFILES)}")
    return PROFILES[name]