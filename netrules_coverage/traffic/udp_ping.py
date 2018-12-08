
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import UDP, IP


class udp_ping(TrafficAPI):

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, hosts):

        # The fastest way to discover hosts on a local ethernet network is to use the ARP Ping method
        for host in hosts:
            packet = IP(dst=host)/UDP(dport=0)
            answer = self.send_receive(packet)


