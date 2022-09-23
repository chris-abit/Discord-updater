"""
Assumes that discord API and interface does not
change. Hurray.

DISCORD_V_PATH: Location where discord version is kept
"""
import pytest
from discord_updater import get_current_version


class Test_get_current_version:
    def test_on_invalid_path_returns_0(self):
        """
        Inability to find the current path will
        assume that discord is not installed.
        """
        version = get_current_version("garbage")
        assert version == 0

    def test_missing_version_raises_ValueError(self, tmp_path):
        d = tmp_path / "test_me"
        d.touch()
        with pytest.raises(ValueError):
            get_current_version(d)
