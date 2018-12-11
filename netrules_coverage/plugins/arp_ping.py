
from __future__ import print_function
from plugins.PluginAPI import PluginAPI

from scapy.all import Ether, ARP


class arp_ping(PluginAPI):

    def __init__(self):
        PluginAPI.__init__(self)

    def run(self, network):

        # The fastest way to discover hosts on a local ethernet network is to use the ARP Ping method

        packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network)
        answer = self.send_receive(packet, timeout=2, verbose=0, retry=2)


