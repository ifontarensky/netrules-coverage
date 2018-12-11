
from __future__ import print_function
from plugins.PluginAPI import PluginAPI

from scapy.all import IP, ICMP
import netaddr


class icmp_ping_scanner(PluginAPI):

    def __init__(self):
        PluginAPI.__init__(self)

    def run(self, network, nb_host_to_test=255, delay=0):

        # make list of addresses out of network, set live host counter
        addresses = netaddr.IPNetwork(network)
        nb_host_tested = 0

        # Send ICMP ping request, wait for answer
        for host in addresses:
            nb_host_tested += 1
            if host == addresses.network or host == addresses.broadcast:
                # Skip network and broadcast addresses
                continue

            packet = IP(dst=str(host)) / ICMP()
            resp = self.send_receive(packet, timeout=2, verbose=0)

            if resp is None:
                print(host, 'is down or not responding.')
            elif (
                    int(resp.getlayer(ICMP).type) == 3 and
                    int(resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]
            ):
                print(host, 'is blocking ICMP.')
            else:
                print(host, 'is responding.')

            nb_host_tested += 1
            if nb_host_tested >= nb_host_to_test:
                break



