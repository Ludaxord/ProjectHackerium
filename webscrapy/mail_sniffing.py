import threading
from scapy.all import *

# our packet callback
from scapy.layers.inet import TCP, IP


def packet_callback(packet):
    print(packet.show())
    if packet[TCP].payload:

        mail_packet = str(packet[TCP].payload)

        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print("[*] Server: %s" % packet[IP].dst)
            print("[*] %s" % packet[TCP].payload)


def call_back(packet):
    print(packet.show())


# fire up our sniffer
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)
# test function
sniff(filter="", prn=call_back, count=1)
