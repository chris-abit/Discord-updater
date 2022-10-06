"""
Assumes that discord API and interface does not
change. Hurray.

DISCORD_V_PATH: Location where discord version is kept
"""
import pytest
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
import requests
from discord_updater import get_current_version


SERVER_NAME = "localhost"
SERVER_PORT = 8080
SERVER_URL = f"http://{SERVER_NAME}:{SERVER_PORT}/"


@pytest.fixture(scope="module")
def file_server(tmp_path_factory):
    handler = SimpleHTTPRequestHandler
    server_address = (SERVER_NAME, SERVER_PORT)
    server_dir = tmp_path_factory.mktemp("server")
    tmp_files = sorted(server_dir.glob("*"))
    with HTTPServer(server_address, handler) as httpd:
        httpd.timeout = 1
        print("Serving at port", SERVER_PORT)
        yield httpd
    print("Server is dead!")


def handle_request(server):
    """
    Creates a thread which runs handle_request on the server.
    """
    x = Thread(target=server.handle_request)
    x.start()


class Test_get_current_version:
    def test_on_invalid_path_returns_0(self):
        """
        Inability to find the current path will
        assume that discord is not installed.
        """
        version = get_current_version("garbage")
        assert version == 0

    def test_missing_version_raises_ValueError(self, tmp_path):
        """
        Assert that if version is missing from file a
        ValueError is raised.
        """
        d = tmp_path / "test_me"
        d.touch()
        with pytest.raises(ValueError):
            get_current_version(d)

    def test_returns_version(self, tmp_path):
        """
        Test if get_current_version returns a float
        with the current version.
        """
        f = tmp_path / "build_info.json"
        expected_version = 0.0020
        version = "0.0.20"
        f.write_text(json.dumps({"version": version}))
        assert expected_version == get_current_version(f)


def test_serve(file_server, tmp_path):
    f = tmp_path / "a_random_file.txt"
    f.touch()
    handle_request(file_server)
    r = requests.get(SERVER_URL + "index.html")
    print(f"{r=}")
    assert False
