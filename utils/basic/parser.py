from argparse import ArgumentParser


def default_tcp_client_args():
    return Parser(args=[{"command": "--host", "type": str, "help": "target host"},
                        {"command": "--port", "type": int, "help": "target port"},
                        {"command": "--data", "type": str, "help": "target data to send"}]).get_args()


def default_tcp_proxy_args():
    return Parser(args=[{"command": "--host", "type": str, "help": "target host"},
                        {"command": "--port", "type": int, "help": "target port"},
                        {"command": "--localhost", "type": str, "help": "target host"},
                        {"command": "--localport", "type": int, "help": "target port"},
                        {"command": "--receivefirst", "type": bool, "help": "bool o receive first"}]).get_args()


def default_udp_client_args():
    return Parser(args=[{"command": "--host", "type": str, "help": "target host"},
                        {"command": "--port", "type": int, "help": "target port"},
                        {"command": "--data", "type": str, "help": "target data to send"}]).get_args()


def default_tcp_server_args():
    return Parser(args=[{"command": "--ip", "type": str, "help": "bind ip"},
                        {"command": "--port", "type": int, "help": "bind port"}]).get_args()


def default_sniffer_args():
    return Parser(args=[{"command": "--ip", "type": str, "help": "bind ip"}]).get_args()


def default_arp_poison_reader_args():
    return Parser(args=[{"command": "--filename", "type": str, "help": "pcap filename"}]).get_args()


def default_arp_poison_args():
    return Parser(args=[{"command": "--target_ip", "type": str, "help": "target ip"},
                        {"command": "--getaway_ip", "type": str, "help": "getaway ip"},
                        {"command": "--interface", "type": str, "help": "interface"},
                        {"command": "--packet", "type": str, "help": "packet count"}]).get_args()


def default_ssh_command_args():
    return Parser(args=[{"command": "--ip", "type": str, "help": "ssh connection ip"},
                        {"command": "--user", "type": str, "help": "ssh connection username"},
                        {"command": "--passwd", "type": str, "help": "ssh connection password"},
                        {"command": "--port", "type": int, "help": "ssh connection port"},
                        {"command": "--cmd", "type": str, "help": "ssh connection command to execute"}]).get_args()


def default_ssh_active_command_args():
    return Parser(args=[{"command": "--ip", "type": str, "help": "ssh connection ip"},
                        {"command": "--user", "type": str, "help": "ssh connection username"},
                        {"command": "--passwd", "type": str, "help": "ssh connection password"},
                        {"command": "--port", "type": int, "help": "ssh connection port"}]).get_args()


class Parser:
    parser = None
    args = []

    def __init__(self, args=None):
        if args is None:
            args = []
        self.parser = self.__init_parser()
        self.__add_args(args)
        self.args = self.parser.parse_args()

    def get_parser(self):
        return self.parser

    def get_args(self):
        return self.args

    def __init_parser(self):
        parser = ArgumentParser()
        return parser

    def __add_args(self, args):
        for arg in args:
            if isinstance(arg, dict):
                arg_command = arg.get("command")
                arg_type = arg.get("type")
                arg_help = arg.get("help")
                self.parser.add_argument(arg_command, type=arg_type, help=arg_help)
