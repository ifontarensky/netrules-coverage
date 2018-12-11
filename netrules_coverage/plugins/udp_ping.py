
from __future__ import print_function
from plugins.PluginAPI import PluginAPI

from scapy.all import UDP, IP


class udp_ping(PluginAPI):

    def __init__(self):
        PluginAPI.__init__(self)

    def run(self, hosts):

        # The fastest way to discover hosts on a local ethernet network is to use the ARP Ping method
        for host in hosts:
            packet = IP(dst=host)/UDP(dport=0)
            answer = self.send_receive(packet)


