
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import UDP, IP, ISAKMP, RandString, ISAKMP_payload_SA, ISAKMP_payload_Proposal


class ike_scanner(TrafficAPI):

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, hosts):

        # Send SYN with random Src Port for each Dst port
        for host in hosts:
            print(host)
            packet = IP(dst=host)/UDP()/ISAKMP(
                init_cookie=RandString(8),
                exch_type="identity prot.")/ISAKMP_payload_SA(prop=ISAKMP_payload_Proposal())
            self.send_receive(packet, timeout=2, verbose=0)
