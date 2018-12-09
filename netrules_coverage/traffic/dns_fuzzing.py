
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import UDP, IP, DNS, fuzz


class dns_fuzzing(TrafficAPI):

    CATEGORY = "Fuzzing"

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, hosts, dport=53):

        # Send SYN with random Src Port for each Dst port
        for host in hosts:
            packet = IP(dst=host) / UDP(dport=dport) / fuzz(DNS())
            answer = self.send_receive(packet)


