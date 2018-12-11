
from __future__ import print_function
from plugins.PluginAPI import PluginAPI

from scapy.all import UDP, IP, DNS, DNSQR

class dns_request(PluginAPI):

    def __init__(self):
        PluginAPI.__init__(self)

    def run(self, dns_server, hosts, dport=53):

        # Send SYN with random Src Port for each Dst port
        for host in hosts:
            packet = IP(dst=dns_server) / UDP(dport=dport) / DNS(rd=1, qd=DNSQR(qname=host))
            answer = self.send_receive(packet, timeout=2, verbose=0)
            print(answer[DNS].summary())

