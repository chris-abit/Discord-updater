from discord_update import parse_version


@pytest.mark.parametrize(
    "data",
    [1, 2.0, list(), dict(), set(), None]
)
def test_parse_version_invalid_type_raises_TypeError(data):
    """ Assert that invalid types result in a TypeError. """
    with pytest.raises(TypeError):
        parse_version(data)
