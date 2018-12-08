
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import TCP, IP, ICMP
import random

class tcp_port_range_scanner(TrafficAPI):

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, host, port_range):

        # Send SYN with random Src Port for each Dst port
        for dstPort in port_range:
            srcPort = random.randint(1025, 65534)
            packet = IP(dst=host)/TCP(sport=srcPort, dport=dstPort, flags="S")
            resp = self.send_receive(packet, timeout=2, verbose=0)

            if resp is None:
                print('{}:{} is filtered (silently dropped).'.format(host, str(dstPort)))

            elif(resp.haslayer(TCP)):
                if(resp.getlayer(TCP).flags == 0x12):
                    # Send a gratuitous RST to close the connection
                    packet = IP(dst=host)/TCP(sport=srcPort, dport=dstPort, flags='R')
                    send_rst = self.send_receive(packet, timeout=2, verbose=0)
                    print('{}:{} is open.'.format(host, str(dstPort)))

                elif (resp.getlayer(TCP).flags == 0x14):
                    print('{}:{} is closed.'.format(host, str(dstPort)))

            elif(resp.haslayer(ICMP)):
                if(int(resp.getlayer(ICMP).type )==3 and int(resp.getlayer(ICMP).code) in [1 ,2 ,3 ,9 ,10 ,13]):
                    print('{}:{} is filtered (silently dropped).'.format(host, str(dstPort)))

