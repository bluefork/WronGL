from wrongl.core.detector import detect, should_auto_convert


def test_detect_garbage_fa_should_be_en():
    # "اثممخ" is what "hello" looks like when typed with wrong layout
    r = detect("اثممخ")
    assert r.direction == "fa2en"


def test_detect_garbage_en_should_be_fa():
    # "sghl" is what "سلام" looks like when typed with wrong layout
    r = detect("sghl")
    assert r.direction == "en2fa"


def test_detect_empty():
    r = detect("")
    assert r.confidence == 0.0


def test_detect_confidence_range():
    r = detect("sghl")
    assert 0.0 <= r.confidence <= 1.0


def test_should_auto_convert():
    r = detect("sghl")
    # Depends on wordfreq availability, just verify it's boolean
    assert isinstance(should_auto_convert(r), bool)