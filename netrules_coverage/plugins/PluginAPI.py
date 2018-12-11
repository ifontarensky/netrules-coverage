
from __future__ import print_function
from scapy.all import sr1, wrpcap, PcapWriter, send

class PluginAPI:

    def __init__(self):
        self.traffic = []

    def send(self, packet, *args, **kargs):
        self.traffic += packet
        try:
            send(packet, *args, **kargs)
        except SystemExit:
            pass
        except KeyboardInterrupt:
            pass
        except OSError:
            pass

    def send_receive(self, packet, *args, **kargs):
        self.traffic += packet
        resp = sr1(packet, *args, **kargs)
        if resp is not None:
            self.traffic += resp
        return resp

    def add_to_pcap(self, packet):
        self.traffic += packet

    def generate_pcap(self, file_path_pcap):
        wrpcap("../output_pcap/"+file_path_pcap, self.traffic, append=False)