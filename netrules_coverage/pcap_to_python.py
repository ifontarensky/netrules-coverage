import argparse

from scapy.all import *



TEMPLATE = """
from __future__ import print_function
from traffic.TrafficAPI import TrafficAPI

from scapy.all import *


class ###NAME###(TrafficAPI):

    CATEGORY = "Exploit"

    def __init__(self):
        TrafficAPI.__init__(self)

    def run(self, hosts, *args, **kargs):
        packets = []
        for host in hosts:
            packets.extend(self.prepare_traffic(host, *args, **kargs))
        self.add_to_pcap(packets)
            
    def prepare_traffic(self, ###ARG###):
"""



def extract_packet_ip(pcap, ids_ip):
    filtered = []
    for pkt in pcap:
        if IP in pkt and (pkt[IP].id in ids_ip):
            filtered.append(pkt)
    return filtered


def rg_Ether_layer(eth_layer):
    src = eth_layer.src
    dst = eth_layer.dst
    type= eth_layer.type
    return 'Ether(src="%s", dst="%s", type=%s)'%(src, dst, type)


def rg_IP_layer(ip_layer):
    args = [
        'version = %s'%ip_layer.version,
        'src = "%s"'%ip_layer.src,
        'dst = "%s"'%ip_layer.dst,
        'chksum = %s'%ip_layer.chksum,
        'proto = %s'%ip_layer.proto,
        'ttl = %s'%ip_layer.ttl,
        'id = %s'%ip_layer.id,
        'len = %s'%ip_layer.len,
        'tos = %s'%ip_layer.tos,
        'ihl = %s'%ip_layer.ihl,
        'options = %s'%ip_layer.options
    ]
    return 'IP(%s)'% ','.join(args)


def rg_TCP_layer(tcp_layer):
    args = [
        'sport = %s' % tcp_layer.sport,
        'dport = %s' % tcp_layer.dport,
        'seq = %s' % tcp_layer.seq,
        'ack = %s'% tcp_layer.ack,
        'dataofs = %s' % tcp_layer.dataofs,
        'reserved = %s' % tcp_layer.reserved,
        'flags = "%s"'%tcp_layer.flags,
        'window = %s'%tcp_layer.window,
        'chksum = %s'%tcp_layer.chksum,
        'urgptr = %s'%tcp_layer.urgptr,
        'options = %s'%tcp_layer.options
    ]
    return 'TCP(%s)'% ','.join(args)


def rg_UDP_layer(udp_layer):
    args = [
        'sport = %s' % udp_layer.sport,
        'dport = %s' % udp_layer.dport,
        'len = %s' % udp_layer.len,
        'chksum = %s'%udp_layer.chksum,
    ]
    return 'UDP(%s)'% ','.join(args)


def rg_DNS_layer(dns_layer):
    args = [
        'id = %s' % dns_layer.id,
        'qr = %s' % dns_layer.qr,
        'opcode = %s' % dns_layer.opcode,
        'aa = %s'%dns_layer.aa,
        'aa = %s'%dns_layer.aa,
        'tc = %s'%dns_layer.tc,
        'rd = %s'%dns_layer.rd,
        'z = %s'%dns_layer.z,
        'ad = %s'%dns_layer.ad,
        'rcode = %s'%dns_layer.rcode,
        'qdcount = %s'%dns_layer.qdcount,
        'ancount = %s'%dns_layer.ancount,
        'nscount = %s'%dns_layer.nscount,
        'arcount = %s'%dns_layer.arcount
    ]
    return 'DNS(%s)'% ','.join(args)


def rg_ARP_layer(arp):
    args = [
        'hwtype = %s' % arp.hwtype,
        'ptype = %s' % arp.ptype,
        'hwlen = %s' % arp.hwlen,
        'plen = %s'%arp.plen,
        'op = %s'%arp.op,
        'hwsrc = %s'%arp.hwsrc,
        'hwdst = %s'%arp.hwdst,
        'pdst = %s'%arp.pdst,
    ]
    return 'ARP(%s)'% ','.join(args)


def rg_Padding_layer(padding_layer):

    return '%s'%padding_layer.load


def process(packet, ret=""):

    svar = packet.name.lower() +"="
    if ret != '':
        ret += '/'

    if packet.name == "Ethernet":
        ret += rg_Ether_layer(packet)
    elif packet.name == "ARP":
        ret += rg_ARP_layer(packet)
    elif packet.name == "IP":
        ret += rg_IP_layer(packet)
    elif packet.name == "TCP":
        ret += rg_TCP_layer(packet)
    elif packet.name == "UDP":
        ret += rg_UDP_layer(packet)
    elif packet.name == "DNS":
        ret += rg_DNS_layer(packet)
    elif "IPv6" in packet.name:
        pass
    elif "DHCP" in packet.name:
        pass
    elif "NBNS" in packet.name:
        pass
    elif "BOOTP" in packet.name:
        pass
    elif "Link Local Multicast Node Resolution - Query" in packet.name:
        pass
    elif "MLDv2" in packet.name:
        pass
    elif packet.name == "Padding":
        ret += rg_Padding_layer(packet)
    elif packet.name == "Raw":
        ret += rg_Padding_layer(packet)
    else:
        print(packet.name)
        packet.show2()
        raise Exception()

    if packet.payload:
        return process(packet.payload, ret)

    return ret

def match_criteria(args, session):
    sip = args.sip
    dip = args.dip
    sport = args.sport
    dport = args.dport

    c1 = "%s:%s > %s:%s"%(sip,sport,dip,dport)
    c2 = "%s:%s > %s:%s" % (dip, dport, sip, sport)
    return (c1 in session or c2 in session)

def is_good_packet(p, args):
    sip = args.sip
    dip = args.dip
    sport = args.sport
    dport = args.dport
    if IP in p and TCP in p:
        if p[IP].src == sip and p[IP].dst == dip and p[TCP].sport == sport and p[TCP].dport == dport:
            return True

        if p[IP].src == dip and p[IP].dst == sip and p[TCP].sport == dport and p[TCP].dport == sport:
            return True

    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Pcap.')
    parser.add_argument('pcapfile', metavar='N', type=str,  help='path to pcapfile')
    parser.add_argument("-sip", type=str, help="Source IP")
    parser.add_argument("-dip", type=str, help="Destination IP")
    parser.add_argument("-sport", type=int, help="Source Port")
    parser.add_argument("-dport", type=int, help="Destination Port")
    parser.add_argument("-name", type=str, help="Name")
    args = parser.parse_args()

    pcap_name=args.name.lower()

    data = args.pcapfile
    pcap = rdpcap(data)

    content = ""
    for p in pcap:
        if is_good_packet(p, args):
            mac1 = p[Ether].src
            mac2 = p[Ether].dst
            content = content + " "*8+"packets.append(" + process(p) +")\n"

    # Prepare arg for generate function
    arg_template = []
    arg_template.append("ip_dst = '%s'" % args.dip)
    arg_template.append("ip_src = '%s'" % args.sip)
    arg_template.append("sport = %d" % args.sport)
    arg_template.append("dport = %d" % args.dport)
    arg_template.append("mac1 = '%s'" % mac1)
    arg_template.append("mac2 = '%s'" % mac2)

    page = TEMPLATE.replace("###ARG###", ", ".join(arg_template).replace(" = ","="))

    content = content.replace('"%s"' % mac1, "mac1")
    content = content.replace('"%s"' % mac2, "mac2")
    content = content.replace('"%s"' % args.sip, "ip_src")
    content = content.replace('"%s"' % args.dip, "ip_dst")
    content = content.replace(' %d' % args.sport, "sport")
    content = content.replace(' %d' % args.dport, "dport")

    page = page + " "*8 + "packets = []\n"
    page = page + content + "\n"

    page = page + " "*8 + "return packets"

    page = page.replace("###NAME###",pcap_name)

    with open("traffic/%s.py" % pcap_name, 'w') as handle:
        handle.write(page)