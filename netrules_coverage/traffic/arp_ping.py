
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import Ether, ARP


class arp_ping(TrafficAPI):

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, network):

        # The fastest way to discover hosts on a local ethernet network is to use the ARP Ping method

        packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network)
        answer = self.send_receive(packet, timeout=2, verbose=0, retry=2)


