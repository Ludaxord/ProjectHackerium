from argparse import ArgumentParser


def default_tcp_client_args():
    return Parser(args=[{"command": "--host", "type": str, "help": "target host"},
                        {"command": "--port", "type": int, "help": "target port"}]).get_args()


def default_udp_client_args():
    return Parser(args=[{"command": "--host", "type": str, "help": "target host"},
                        {"command": "--port", "type": int, "help": "target port"},
                        {"command": "--data", "type": str, "help": "target data to send"}]).get_args()


class Parser:
    parser = None
    args = []

    def __init__(self, args=None):
        if args is None:
            args = []
        self.parser = self.init_parser()
        self.add_args(args)
        self.args = self.parser.parse_args()

    def get_parser(self):
        return self.parser

    def get_args(self):
        return self.args

    def init_parser(self):
        parser = ArgumentParser()
        return parser

    def add_args(self, args):
        for arg in args:
            if isinstance(arg, dict):
                arg_command = arg.get("command")
                arg_type = arg.get("type")
                arg_help = arg.get("help")
                self.parser.add_argument(arg_command, type=arg_type, help=arg_help)
