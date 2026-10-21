"""Persian/Arabic text normalization helpers."""
from __future__ import annotations

ZWNJ = "\u200c"
ZWJ = "\u200d"

_ARABIC_TO_PERSIAN = {
    'ي': 'ی', 'ى': 'ی', 'ك': 'ک', 'ة': 'ه', 'ۀ': 'ه',
    'أ': 'ا', 'إ': 'ا', 'ؤ': 'و', 'ٱ': 'ا',
}

_FA_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
_AR_DIGITS = '٠١٢٣٤٥٦٧٨٩'
_EN_DIGITS = '0123456789'
_FA_TO_EN_DIGITS = str.maketrans(_FA_DIGITS + _AR_DIGITS, _EN_DIGITS * 2)
_EN_TO_FA_DIGITS = str.maketrans(_EN_DIGITS, _FA_DIGITS)


def normalize_arabic(text: str) -> str:
    return "".join(_ARABIC_TO_PERSIAN.get(ch, ch) for ch in text)


def fa_digits_to_en(text: str) -> str:
    return text.translate(_FA_TO_EN_DIGITS)


def en_digits_to_fa(text: str) -> str:
    return text.translate(_EN_TO_FA_DIGITS)


def strip_zwj(text: str) -> str:
    return text.replace(ZWJ, "")