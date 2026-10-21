"""Smart direction detection using wordfreq lexical scoring."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass

log = logging.getLogger(__name__)

_wordfreq = None
_wordfreq_failed = False


def _get_wordfreq():
    global _wordfreq, _wordfreq_failed
    if _wordfreq is not None or _wordfreq_failed:
        return _wordfreq
    try:
        from wordfreq import zipf_frequency  # type: ignore
        _wordfreq = zipf_frequency
    except ImportError as exc:
        log.warning("wordfreq unavailable — falling back to char-based: %s", exc)
        _wordfreq_failed = True
    return _wordfreq


_FA_RE = re.compile(r"[\u0600-\u06FF]")
_EN_RE = re.compile(r"[A-Za-z]")
_WORD_RE = re.compile(r"[\w\u0600-\u06FF]+", re.UNICODE)
_MIN_ZIPF = 2.0


@dataclass(frozen=True)
class DetectionResult:
    direction: str
    confidence: float
    method: str


def _char_scores(text: str) -> tuple[float, float]:
    fa = len(_FA_RE.findall(text))
    en = len(_EN_RE.findall(text))
    total = fa + en
    if total == 0:
        return 0.0, 0.0
    return fa / total, en / total


def _lexical_score(text: str, lang: str) -> float:
    zipf = _get_wordfreq()
    if zipf is None:
        if lang == "fa":
            return min(len(_FA_RE.findall(text)) / max(len(text), 1), 1.0)
        return min(len(_EN_RE.findall(text)) / max(len(text), 1), 1.0)
    tokens = _WORD_RE.findall(text)
    if not tokens:
        return 0.0
    total = 0.0
    hits = 0
    for tok in tokens:
        try:
            f = zipf(tok, lang)
        except Exception:
            continue
        if f >= _MIN_ZIPF:
            hits += 1
        total += f
    avg = total / len(tokens)
    hit_ratio = hits / len(tokens)
    return min(avg / 8.0, 1.0) * hit_ratio


def detect(
    text: str,
    threshold: float = 0.55,
    profile: str = "windows",
) -> DetectionResult:
    """Detect the direction ('en2fa' or 'fa2en') most likely intended."""
    if not text or not text.strip():
        return DetectionResult("en2fa", 0.0, "char")

    # Lazy import to avoid circular dependency
    from .converter import convert_text

    as_fa = convert_text(text, "en2fa", profile=profile, normalize_arabic=True)
    as_en = convert_text(text, "fa2en", profile=profile, normalize_arabic=True)

    orig_fa = _lexical_score(text, "fa")
    orig_en = _lexical_score(text, "en")
    conv_fa = _lexical_score(as_fa, "fa")
    conv_en = _lexical_score(as_en, "en")

    gain_en2fa = conv_fa - orig_fa
    gain_fa2en = conv_en - orig_en

    if gain_en2fa > 0.05 and gain_en2fa >= gain_fa2en:
        return DetectionResult("en2fa", round(min(gain_en2fa, 1.0), 3), "lexical")
    if gain_fa2en > 0.05 and gain_fa2en > gain_en2fa:
        return DetectionResult("fa2en", round(min(gain_fa2en, 1.0), 3), "lexical")

    # No clear winner → char-based, penalized
    fa_ratio, en_ratio = _char_scores(text)
    if fa_ratio > en_ratio:
        return DetectionResult("fa2en", round(fa_ratio * 0.5, 3), "char")
    return DetectionResult("en2fa", round(en_ratio * 0.5, 3), "char")


def should_auto_convert(result: DetectionResult, threshold: float = 0.55) -> bool:
    return result.confidence >= threshold