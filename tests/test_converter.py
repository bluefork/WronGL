import pytest
from wrongl.core.converter import Converter, convert_text


@pytest.fixture
def conv():
    return Converter(profile="windows", convert_digits=False, normalize_arabic=True)


def test_en_to_fa_hello(conv):
    assert conv.en_to_fa("hello") == "اثممخ"


def test_en_to_fa_salam(conv):
    assert conv.en_to_fa("sghl") == "سلام"


def test_fa_to_en_hello(conv):
    assert conv.fa_to_en("اثممخ") == "hello"


def test_fa_to_en_salam(conv):
    assert conv.fa_to_en("سلام") == "sghl"


def test_empty(conv):
    assert conv.en_to_fa("") == ""
    assert conv.fa_to_en("") == ""


def test_spaces_preserved(conv):
    assert conv.en_to_fa("a b") == "ش ذ"


def test_digits():
    c = Converter(convert_digits=True)
    assert c.en_to_fa("123") == "۱۲۳"
    assert c.fa_to_en("۱۲۳") == "123"


def test_arabic_yeh_normalization():
    c = Converter(normalize_arabic=True)
    # Arabic yeh (ي) → Persian ی → d
    assert c.fa_to_en("ي") == "d"


def test_uppercase():
    c = Converter()
    assert c.en_to_fa("S") == "س"
    assert c.en_to_fa("H") == "آ"


def test_unknown_direction():
    with pytest.raises(ValueError):
        convert_text("x", "xx2yy")


def test_round_trip_latin():
    c = Converter()
    for s in ["hello", "world", "test", "abc"]:
        assert c.fa_to_en(c.en_to_fa(s)) == s


def test_round_trip_persian():
    c = Converter()
    for s in ["سلام", "خوبی", "دنیا"]:
        assert c.en_to_fa(c.fa_to_en(s)) == s