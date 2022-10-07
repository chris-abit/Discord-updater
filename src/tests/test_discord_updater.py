"""
Assumes that discord API and interface does not
change. Hurray.

DISCORD_V_PATH: Location where discord version is kept
"""
import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
import pytest
import requests
from discord_updater import get_current_version


SERVER_NAME = "localhost"
SERVER_PORT = 8080
SERVER_URL = f"http://{SERVER_NAME}:{SERVER_PORT}/"


@pytest.fixture(scope="module")
def file_server(tmp_path_factory):
    """
    Start a basic HTTP server wich serves files from a temporary
    directory.
    Create files for the server using the returned server_dir
    which is an instance of Path (see pathlib).
    Relies on os.chdir to ensure that the HTTPServer only works
    out of the tmp_path_factory. This is a quick hack as
    SimpleHTTPRequestHandler relies on os.getcwd() to set the working
    directory.
    Yields a pair of the server instance and a Path object.
    """
    """
    TODO: Consider subclassing HTTPServer with a custom init
    and finish_request. See DualStackServer in server.py.
    """
    handler = SimpleHTTPRequestHandler
    server_address = (SERVER_NAME, SERVER_PORT)
    server_dir = tmp_path_factory.mktemp("server")
    os.chdir(server_dir.resolve())
    with HTTPServer(server_address, handler) as httpd:
        httpd.timeout = 1
        print("Serving at port", SERVER_PORT)
        yield httpd, server_dir
    print("Server is terminated!")


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


def test_server_does_not_serve_local(file_server):
    """
    Verify that the fileserver does not serve local content.
    """
    server, path = file_server
    handle_request(server)
    r = requests.get(SERVER_URL + __file__)
    assert r.status_code == requests.codes.not_found


class Test_get_latest_version:
    def test_retreives_float(self):
        pass
