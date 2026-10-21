from wrongl.core.normalize import (
    en_digits_to_fa,
    fa_digits_to_en,
    normalize_arabic,
)


def test_arabic_to_persian():
    assert normalize_arabic("يك") == "یک"
    assert normalize_arabic("ة") == "ه"


def test_digit_conversion():
    assert en_digits_to_fa("0123456789") == "۰۱۲۳۴۵۶۷۸۹"
    assert fa_digits_to_en("۰۱۲۳۴۵۶۷۸۹") == "0123456789"