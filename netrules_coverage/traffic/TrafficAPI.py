
from __future__ import print_function
from scapy.all import sr1, wrpcap,PcapWriter

class TrafficAPI:

    def __init__(self):
        self.traffic = []

    def send_receive(self, packet, funcsr=sr1, *args, **kargs):
        self.traffic += packet
        resp = funcsr(packet, *args, **kargs)
        if resp is not None:
            self.traffic += resp
        return resp

    def generate_pcap(self, file_path_pcap):
        print(self.traffic)
        wrpcap("../output_pcap/"+file_path_pcap, self.traffic, append=True)