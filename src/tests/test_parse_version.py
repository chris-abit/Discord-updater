from discord_update import parse_version


@pytest.mark.parametrize(
    "data",
    [1, 2.0, list(), dict(), set(), None]
)
def test_parse_version_invalid_type_raises_TypeError(data):
    """ Assert that invalid types result in a TypeError. """
    with pytest.raises(TypeError):
        parse_version(data)


def test_parse_version_handles_missing_0_second_slot():
    """
    Test that if in a possible future the version uses
    no leading 0 for second index number one will be added.
    """
    version = "0.9.20"
    expected = 0.0920
    assert expected == parse_version(version)


def test_parse_version_does_not_pad_two_digit_slots():
    """
    Assert that no padding for second index of version
    is done when it is already two digit.
    """
    version = "0.19.20"
    expected = 0.1920
    assert expected == parse_version(version)


def test_parse_version_ignores_alphabet_chars():
    """
    Assert that any characters from the alphabet is ignored.
    """
    version = "0.0.20a"
    expected = 0.0020
    assert expected == parse_version(version)


def test_parse_version_empty_string_is_invalid():
    with pytest.raises(ValueError):
        parse_version("")
