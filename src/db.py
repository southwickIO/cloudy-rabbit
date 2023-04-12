#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: db.py                                                                 #
#                                                                             #
# VERSION: 20230411                                                           #
#                                                                             #
# SYNOPSIS: Check for potential IP spoofing through a window size test        #
#                                                                             #
# DESCRIPTION: This script looks for bogon traffic coming in from the         #
#              internet. This is a huge sign of spoofing or something         #
#              malicious. Bogon networks are IP addresses or ranges of IP     #
#              addresses that have not been allocated or assigned to any      #
#              organization or user, and thus are not supposed to be used in  #
#              the public internet. They are typically blocked by network     #
#              administrators to prevent traffic from those networks from     #
#              entering or leaving the network.                               #
#                                                                             #
# INPUT: None                                                                 #
#                                                                             #
# OUTPUT: STDOUT                                                              #
#                                                                             #
# PRE-RUNTIME NOTES: This script is not that good of a technique to detect    #
#                    bogon traffic, but it helps. This is because malicious   #
#                    actors can hide traffic in class A,B,C networks that     #
#                    your traffic is on. So if you see a class A address and  #
#                    your network is another class; that is the only real     #
#                    indicator of bogon traffic that this script can help you #
#                    with.                                                    #
#                                                                             #
# AUTHORS: @southwickio                                                       #
#                                                                             #
# LICENSE: GPLv3                                                              #
#                                                                             #
# DISCLAIMER: All work produced by Authors is provided “AS IS”. Authors make  #
#             no warranties, express or implied, and hereby disclaims any and #
#             all warranties, including, but not limited to, any warranty of  #
#             fitness, application, et cetera, for any particular purpose,    #
#             use case, or application of this script.                        #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



#import dependencies
from scapy.all import *
import ipaddress
import time



#initialize members
interface = "wlp1s0" #replace with the name of your external interface
private = []
loopback = []
reserved = []
multicast = []



#define bogon networks
private.append(ipaddress.ip_network("10.0.0.0/8"))
private.append(ipaddress.ip_network("172.16.0.0/12"))
private.append(ipaddress.ip_network("192.168.0.0/16"))
loopback.append(ipaddress.ip_network("127.0.0.0/8"))
reserved.append(ipaddress.ip_network("0.0.0.0/8"))
reserved.append(ipaddress.ip_network("169.254.0.0/16"))
multicast.append(ipaddress.ip_network("224.0.0.0/4"))



#define workhose
def capturePackets(packet):
    


    #check for bogon networks
    if IP in packet \
    and (any(packet[IP].src in net for net in private) \
    or any(packet[IP].src in net for net in loopback) \
    or any(packet[IP].src in net for net in reserved) \
    or any(packet[IP].src in net for net in multicast)):
        


        #print bogon traffic
        print("Packet from a private IP address:", packet.summary())



#sniff on simgle interfaces
print("\n\n\nPotential bogon src IPs will be printed. Over 99% will be false \
positives. If you want a record outside of STDOUT, restart this script and \
output to your file. Look for class networks that aren't in your internal \
network and investigate those.")
print("[ctrl+c to exit sniffing]")

time.sleep(5)

print("\n\n\nChecking for potential bogon traffic...\n\n\n")

#store=0 keeps the memory clear
sniff(prn=capturePackets, filter="", store=0, iface=interface)