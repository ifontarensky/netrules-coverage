************
Test Netbook
************


Envrionnement de test
======================

.. graphviz::
   :align:   center

    digraph G {

         rankdir=LR
         node [
            shape=box,
            fontname="arial",
            fontsize=8,
            style=filled,
            color="#d3edea"
         ];
         splines="compound"

         ids [shape=none, label="IDS", labelloc="b", image="_static/zoom-3.png"]

         subgraph internal {
            node [style=filled,color=white];
            style=filled;
            color=red;
            graph[style=dotted];

            sw_int [ label="192.168.1.101" shape=none image="_static/network-switch.png" labelloc=b color="#ffffff"];
            cmp_1   [shape=none, label="192.168.1.x",  labelloc="b", image="_static/computer-2.png"]
            cmp_2   [shape=none, label="192.168.1.x",  labelloc="b", image="_static/computer-2.png"]
            victim   [shape=none, label="192.168.1.10",  labelloc="b", image="_static/computer-2.png"]

            cmp_1 -> sw_int [color=grey arrowhead=none]
            cmp_2 -> sw_int [color=grey arrowhead=none]
            victim -> sw_int [color=grey arrowhead=none]
            label = "192.168.0.0/16";
         }

         subgraph external {
            node [style=filled,color=white];
            style=filled;
            color=lightgrey;
            label = "172.16.0.0/16";

            sw_ext [ label="172.16.1.100" shape=none image="_static/network-switch.png" labelloc=b color="#ffffff"];
            cmp_3   [shape=none, label="172.16.1.x",  labelloc="b", image="_static/computer-2.png"]
            attacker [shape=none, label="172.16.1.11", labelloc="b", image="_static/computer-2.png"]
            sw_ext -> attacker [color=grey arrowhead=none];
            sw_ext -> cmp_3 [color=grey arrowhead=none];

         }

         sw_int -> ids -> sw_ext [color=grey arrowhead=none]

    }



TCP Port Range Scanner
=======================

This is a fairly basic attack to test whether a host has specific TCP ports open and listening.
We start to use a random TCP source port to help obfuscate the attack (although most firewalls are smarter than this
nowadays), we send a TCP SYN packet to each destination TCP port specified.
If we get no response or a TCP RST in return, we know that the host is filtering or not listening on that port. If we
get an ICMP unreachable or error response, we also know the host is not willing to take requests on that port. But, if
we get an expected TCP SYN/ACK response, we will send a RST so the host doesn’t keep listening for our ACK since
we already know the host is listening on that port.


ICMP Ping Scanner
=================
This attack is simply an extension of the ICMP ping utility from the sending and receiving example. The idea is to use
a network with a CIDR mask to specify the hosts on which to ping. Then, using a Python for loop, we go through each
address and try to ping. If the response times out or returns an ICMP error (such as inaccessible or refused by the
administrator), we know that the host is not active or is blocking ICMP. Otherwise, if we receive an answer, we know
that the host is online.