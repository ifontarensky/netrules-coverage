
from __future__ import print_function
from plugins.PluginAPI import PluginAPI

from scapy.all import TCP, IP


class xmas_scanner(PluginAPI):

    def __init__(self):
        PluginAPI.__init__(self)

    def run(self, hosts, dports=[255]):

        for host in hosts:
            print(host)
            for dport in dports:
                packet = IP(dst=host) / TCP(dport, flags="FPU")
                answer = self.send_receive(packet, timeout=2, verbose=0)

        # Checking RST responses will reveal closed ports on the target.