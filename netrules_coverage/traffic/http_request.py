
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import TCP, IP


class http_request(TrafficAPI):

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, hosts, dport=80):

        # Send SYN packet
        for host in hosts:
            packet = IP(dst=host) / TCP(dport=dport, flags='S')
            answer = self.send_receive(packet, timeout=2, verbose=0)
            print(answer.summary())

    #/ "GET /index.html HTTP/1.0 \n\n"