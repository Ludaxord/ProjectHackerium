import abc
import getopt
import sys


class Protocol:

    @abc.abstractmethod
    def usage(self):
        return

    def get_tcp_args(self):
        if not len(sys.argv[1:]):
            self.usage()
        try:
            print(sys.argv)
            opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                       ["host", "port", "data", "localhost", "localport", "receive_first"])
            return opts, args
        except getopt.GetoptError as err:
            print(str(err))
            self.usage()

    def get_udp_args(self):
        if not len(sys.argv[1:]):
            self.usage()
        try:
            print(sys.argv)
            opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                       ["host", "port", "data"])
            return opts, args
        except getopt.GetoptError as err:
            print(str(err))
            self.usage()

    def check_args(self, opts):
        temporary_host = ""
        temporary_port = 0
        temporary_localhost = ""
        temporary_localport = 0
        temporary_receive_first = False
        temporary_data = ""
        for option, action in opts:
            if option in ("-h", "--host"):
                temporary_host = action
            elif option in ("-p", "--port"):
                temporary_port = int(action)
            elif option in ("-d", "--data"):
                temporary_data = action
            elif option in ("-lh", "--localhost"):
                temporary_localhost = action
            elif option in ("-lp", "--localport"):
                temporary_localport = action
            elif option in ("-r", "--receivefirst"):
                temporary_receive_first = True
            else:
                assert False, "unsupported option"

        return temporary_host, temporary_port, temporary_data, temporary_localhost, temporary_localport, temporary_receive_first
