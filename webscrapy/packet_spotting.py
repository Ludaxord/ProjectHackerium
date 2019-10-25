import os
import sys

sys.path.append(os.getcwd())

from utils.basic.parser import default_sniffer_args
from utils.webservices.sniffer import Sniffer

parser = default_sniffer_args()

host = parser.ip

sniffer = Sniffer(host)

sniffer.init_sniffer()
