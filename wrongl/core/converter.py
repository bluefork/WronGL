"""Bidirectional layout conversion."""
from __future__ import annotations

import logging

from . import normalize
from .layouts import LayoutProfile, get_profile

log = logging.getLogger(__name__)


class Converter:
    def __init__(
        self,
        profile: str = "windows",
        convert_digits: bool = False,
        normalize_arabic: bool = True,
    ) -> None:
        self.profile: LayoutProfile = get_profile(profile)
        self.convert_digits = convert_digits
        self.normalize_arabic = normalize_arabic

    def en_to_fa(self, text: str) -> str:
        if not text:
            return text
        out = "".join(self.profile.en_to_fa.get(ch, ch) for ch in text)
        if self.normalize_arabic:
            out = normalize.normalize_arabic(out)
        if self.convert_digits:
            out = normalize.en_digits_to_fa(out)
        return out

    def fa_to_en(self, text: str) -> str:
        if not text:
            return text
        if self.normalize_arabic:
            text = normalize.normalize_arabic(text)
        out = "".join(self.profile.fa_to_en.get(ch, ch) for ch in text)
        if self.convert_digits:
            out = normalize.fa_digits_to_en(out)
        return out


def convert_text(
    text: str,
    direction: str,
    *,
    profile: str = "windows",
    convert_digits: bool = False,
    normalize_arabic: bool = True,
) -> str:
    conv = Converter(
        profile=profile,
        convert_digits=convert_digits,
        normalize_arabic=normalize_arabic,
    )
    if direction == "en2fa":
        return conv.en_to_fa(text)
    if direction == "fa2en":
        return conv.fa_to_en(text)
    raise ValueError(f"Unknown direction: {direction!r}")