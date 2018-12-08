
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import TCP, IP, sr


class ack_scanner(TrafficAPI):

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, hosts, dports=[80, 666]):

        # Send SYN with random Src Port for each Dst port
        for host in hosts:
            print(host)
            packet = IP(dst=host) / TCP(dports, flags="A")
            self.send_receive(packet, timeout=2, verbose=0)
