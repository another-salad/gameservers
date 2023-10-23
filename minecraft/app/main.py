"""Main entry point"""

from argparse import ArgumentParser

from helpers.msg import send_msg

class MainArgs(ArgumentParser):
    """Arg parser"""

    _desc = "Args for sending a message via RCON"

    def __init__(self, description=_desc):
        super().__init__(description=description)
        self.add_argument("--msg", dest="message", type=str, required=True)

if __name__ == "main":
    arg, _ = MainArgs().parse_known_args()
    send_msg(arg)