
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import TCP, IP


class ip_scanner(TrafficAPI):

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, hosts, message="SCAPY"):

        # A lower level IP Scan can be used to enumerate supported protocols
        for host in hosts:
            print(host)
            packet = IP(dst=host,proto=(0,255))/ message
            answer = self.send_receive(packet, timeout=2, verbose=0, retry=2)


