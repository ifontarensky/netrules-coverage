
from __future__ import print_function
from scapy.all import sr1, wrpcap

class TrafficAPI:

    def __init__(self):
        self.traffic = []

    def send_receive(self, packet, *args, **kargs):
        self.traffic += packet
        resp = sr1(packet, *args, **kargs)
        self.traffic += resp
        return resp

    def generate_pcap(self, file_path_pcap):
        wrpcap(file_path_pcap, self.traffic, append=True)