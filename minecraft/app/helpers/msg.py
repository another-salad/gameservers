"""Contains all the acceptable messages. I don't want to parse user input (ew)."""

from datetime import datetime

from mcipc.rcon.je import Client

from helpers.get_servers import get_servers, get_rcon_pw_from_prop_file

class InvaldMsg(Exception):
    """Raised when an unknown message is requested"""

def get_time() -> datetime:
    return datetime.now().strftime('%H:%M:%S')

def _time() -> str:
    return f"The time is currently {get_time()}, are you still playing?"

def _restart() -> str:
    return f"Get to a safe place, the server will restart on the hour. The time is now: {get_time()}"

def _players(client: Client) -> list:
    player_info = client.list()
    return f'Current Miners: {",".join(getattr(x, "name", "") for x in getattr(player_info, "players", []))}'

ACCEPTABLE_MESSAGES = {
    "time": _time,
    "players": _players,
    "restart": _restart
}

def send_msg(msg: str):
    """Sends message via rcon to all servers in the server_conf.json file"""
    server_msg = ACCEPTABLE_MESSAGES.get(msg, False)
    if not server_msg:
        raise InvaldMsg(f"Server message must be in approved list: {ACCEPTABLE_MESSAGES.keys()}")
    for server in get_servers():
        with Client(server.host, server.rconport, passwd=get_rcon_pw_from_prop_file(server.datadir)) as client:
            # FILTHY HACK
            if server_msg == "players":
                msg_to_send = server_msg(client)
            else:
                msg_to_send = server_msg()

            client.say(msg_to_send)
