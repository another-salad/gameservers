"""Contains all the acceptable messages. I don't want to parse user input (ew)."""

from datetime import datetime

from mcipc.rcon.je import Client

from helpers.get_servers import get_servers, get_rcon_pw_from_prop_file

class InvaldMsg(Exception):
    """Raised when an unknown message is requested"""

def get_time() -> datetime:
    return datetime.now().strftime('%H:%M:%S')

def _time(client: Client) -> str:
    client.say(f"The time is currently {get_time()}, are you still playing?")

def _restart(client: Client) -> str:
    client.say(f"Get to a safe place, the server will restart on the hour. The time is now: {get_time()}")

def _return_player_info(client: Client) -> str:
    player_info = client.list()
    return ", ".join(getattr(x, "name", "") for x in getattr(player_info, "players", []))

def _players(client: Client) -> list:
    client.say(f'Current Miners: {_return_player_info(client)}')

def _echo_players(client: Client) -> str:
    print(f"Current Miners on host '{client.host}': {_return_player_info(client)}")

ACCEPTABLE_MESSAGES = {
    "time": _time,
    "players": _players,
    "restart": _restart,
    "echoplayers": _echo_players
}

def interact(msg: str):
    """Sends message via rcon to all servers in the server_conf.json file"""
    server_msg = ACCEPTABLE_MESSAGES.get(msg, False)
    if not server_msg:
        raise InvaldMsg(f"Server message must be in approved list: {ACCEPTABLE_MESSAGES.keys()}")
    for server in get_servers():
        with Client(server.host, server.rconport, passwd=get_rcon_pw_from_prop_file(server.datadir)) as client:
            server_msg(client)
