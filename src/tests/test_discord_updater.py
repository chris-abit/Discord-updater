"""
Assumes that discord API and interface does not
change. Hurray.

DISCORD_V_PATH: Location where discord version is kept
"""
from discord_updater import get_current_version


class Test_get_current_version:
    def test_on_invalid_path_returns_0():
        """
        Inability to find the current path will
        assume that discord is not installed.
        """
        version = get_current_version("garbage")
        assert version == 0
