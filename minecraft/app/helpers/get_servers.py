"""Gets all the RCON servers from the JSON file"""

from collections import namedtuple
from json import loads
from pathlib import Path
import re


Server = namedtuple("Server", ["host", "rconport", "datadir"])
RCON_PW_RGX = r"rcon.password=(?P<pw>.*)"

class NoPasswordSadness(Exception):
    """Raised when we can't find the password in your RCON file"""

def server_obj(dct) -> Server:
    return Server(**dct)

def get_servers() -> list[Server]:
    return loads(Path(Path(__file__).parent, "servers.json").read_bytes(), object_hook=server_obj)

def get_rcon_pw_from_prop_file(absolute_parent_path: str) -> str:
    prop_file_contents = Path(Path(absolute_parent_path).absolute(), "server.properties").read_text()
    res = re.search(RCON_PW_RGX, prop_file_contents)
    if res:
        return res.group("pw")
    raise NoPasswordSadness("RCON password not found is server.properties")
