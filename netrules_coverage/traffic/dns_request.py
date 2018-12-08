
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import UDP, IP, DNS, DNSQR
import random

class dns_request(TrafficAPI):

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, dns_server, hosts, dport=53):

        # Send SYN with random Src Port for each Dst port
        for host in hosts:
            packet = IP(dst=dns_server) / UDP(dport=dport) / DNS(rd=1, qd=DNSQR(qname=host))
            answer = self.send_receive(packet, timeout=2, verbose=0)
            print(answer[DNS].summary())

