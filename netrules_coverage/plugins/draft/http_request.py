
from __future__ import print_function
from traffic.PluginAPI import PluginAPI

#from scapy.all import TCP, IP, sr1, send, sr

from scapy.all import *
import logging


from plugin import http

import random



class http_request(PluginAPI):

    def __init__(self):
        PluginAPI.__init__(self)

    def initSYN(self, pktIP, srcPort, dstPort, orig_seq_num):
        #print("!!! Sending SYN")
        this_seq_num = orig_seq_num
        this_ack_num = 0
        syn = pktIP / TCP(sport=srcPort, dport=dstPort, seq=this_seq_num, ack=this_ack_num, flags='S')
        print(syn.sprintf(
            '\033[1m\033[94m>>>\033[0m %IP.dst%    %TCP.flags%:    seq=\033[1m\033[92m%TCP.seq%\033[0m    ack=\033[1m\033[35m%TCP.ack%\033[0m'))
        syn_ack = sr1(syn)
        print(syn_ack.sprintf(
            '%IP.dst% \033[1m\033[91m<<<\033[0m    %TCP.flags%:    seq=\033[1m\033[35m%TCP.seq%\033[0m    ack=\033[1m\033[92m%TCP.ack%\033[0m\n'))
        return syn_ack

    def initACK(self, pktIP, srcPort, dstPort, last_seq_num, last_ack_num):
        this_seq_num = last_ack_num
        this_ack_num = last_seq_num + 1
        ack = pktIP / TCP(sport=srcPort, dport=dstPort, seq=this_seq_num, ack=this_ack_num, flags='A')
        print(ack.sprintf(
            '\033[1m\033[94m>>>\033[0m %IP.dst%    %TCP.flags%:    seq=\033[1m\033[92m%TCP.seq%\033[0m    ack=\033[1m\033[35m%TCP.ack%\033[0m\n'))
        send(ack)
        return ack

    def pshACK(self, pktIP, srcPort, dstPort, last_seq_num, last_ack_num, http_payload):
        this_seq_num = last_seq_num
        this_ack_num = last_ack_num
        http_request = pktIP / TCP(sport=srcPort, dport=dstPort, seq=this_seq_num, ack=this_ack_num,
                                   flags='PA') / http_payload
        print(http_request.sprintf(
            '\033[1m\033[94m>>>\033[0m %IP.dst%    %TCP.flags%:    seq=\033[1m\033[92m%TCP.seq%\033[0m    ack=\033[1m\033[35m%TCP.ack%\033[0m   '),
              "len=%s" % len(http_payload))
        print('\033[1m\033[94m>>>\033[0m PAYLOAD: %s' % http_request.sprintf('%TCP.payload%').replace('\n', '\n\t'))
        http_reply = sr(http_request, multi=2, timeout=1)
        ans, unans = http_reply
        result = None
        if len(ans) >= 1:
            if len(ans[0]) >= 2:
                i = 0
                while i < len(ans):
                    response = ans[i][1]
                    if response.sprintf('%TCP.flags%') == 'A':
                        pass
                    elif response.sprintf('%IP.src%') != pktIP.dst:
                        pass
                    elif len(response[TCP].payload) > 3:
                        print(response.sprintf(
                            '%IP.dst% \033[1m\033[91m<<<\033[0m    %TCP.flags%:    seq=\033[1m\033[35m%TCP.seq%\033[0m    ack=\033[1m\033[92m%TCP.ack%\033[0m'))
                        result = response
                        break
                    else:
                        print("!!! Unexpected response")
                        print(response.sprintf(
                            '\n%IP.dst% \033[1m\033[91m<<<\033[0m    %TCP.flags%:    seq=\033[1m\033[35m%TCP.seq%\033[0m    ack=\033[1m\033[92m%TCP.ack%\033[0m\n'))
                    i += 1
            else:
                result = None
        else:
            result = None
        return result

    def handshake(self, pktIP, srcPort, dstPort, orig_seq_num, http_payload):
        # Open with SYN
        syn_ack = self.initSYN(pktIP,srcPort,dstPort,orig_seq_num)
        # Respond to SYN-ACK with ACK
        ack = self.initACK(pktIP,srcPort,dstPort,syn_ack[TCP].seq,syn_ack[TCP].ack)
        # Send HTTP GET
        http_res = self.pshACK(pktIP,srcPort,dstPort,ack[TCP].seq,ack[TCP].ack,http_payload)

    def run(self, hosts, dport=80):

        for host in hosts:
            # Random source port
            sport = random.randint(1024, 65535)

            # Random starter TCP sequence number
            orig_seq_num = random.randint(0, (2 ** 32 - 1))

            # Constructing Scapy IP() used for all future packets
            pktIP = IP(dst=host)

            # HTTP GET payload with headers
            http_payload = """GET / HTTP/1.1\r
            Host: %s\r
            User-Agent: Python-Scapy\r
            Accept: */*\r
            Connection: keep-alive\r
            \r
            """ % host


            self.handshake(pktIP, sport, dport, orig_seq_num, http_payload)
