import json
import subprocess
from pathlib import Path
import requests


DISCORD_V_PATH = "/usr/share/discord/resources/build_info.json"
DISCORD_URL = "https://discord.com/api/download?platform=linux&format=deb"


def is_ver_char(char):
    """
    Return True if character is . or numeric, False otherwise.
    """
    return char.isnumeric() or char == "."


def parse_version(string):
    """
    Parse and convert version number to a float.
    Will pad second index number for possible future proofing.
    """
    if not isinstance(string, str):
        raise TypeError
    string = "".join(filter(is_ver_char, string))
    if string == "":
        raise ValueError("String must contain version data")
    string = string.rsplit(".")
    if len(string) != 3:
        raise ValueError("Expecting version in format 0.0.0")
    string = list(map(lambda x: f"{x:0>2}", string))
    major, minor = string[0], "".join(string[1:])
    version = float(f"{major}.{minor}")
    return version


def get_current_version(path):
    """
    Retrieve current version of discord.
    """
    if not Path(path).exists():
        return 0
    with open(path) as f:
        content = json.loads(f.read())
    version = parse_version(content["version"])
    return version


def update():
    c_version = get_current_version(DISCORD_V_PATH)
    r = requests.get(DISCORD_URL, allow_redirects=False)
    source = r.headers["location"]
    version = source.rsplit("-", 1)[1].rpartition(".")[0]
    version = parse_version(version)
    target = Path().home() / "Downloads/Discord.deb"
    if c_version == version:
        print("Discord is the latest version.")
        return
    r = requests.get(source, stream=True)
    with target.open("wb") as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)
    subprocess.run(["sudo", "apt", "install", target])
    print("Discord update complete.")


if __name__ == "__main__":
    update()
