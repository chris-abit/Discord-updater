import json


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
    pass
