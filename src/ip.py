#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: ip.py                                                                 #
#                                                                             #
# VERSION: 20230411                                                           #
#                                                                             #
# SYNOPSIS: Check for potential IP spoofing through a window size test        #
#                                                                             #
# DESCRIPTION: This script looks for potential IP spoofing by crafting, and   #
#              sending, a SYN/ACK packet that advertizes a window size of 0.  #
#              No communications are possible with a window size of 0, so if  #
#              a suspicious IP responds to that SYN/ACK, it is a good         #
#              indication that the IP is being spoofed. The window size on    #
#              packets from A to B indicate how much buffer space is          #
#              available on A for receiving packets. So when B receives a     #
#              packet with window size 1, it would tell B how many bytes it   #
#              is allowed to send to A before getting a response.             #
#                                                                             #
# INPUT: None                                                                 #
#                                                                             #
# OUTPUT: STDOUT                                                              #
#                                                                             #
# PRE-RUNTIME NOTES: None                                                     #
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
import time



#initialize members
spoofers = []
incomingips = []



#define workhorse
def processPacket(packet):



    #check if the packet has an ip layer
    if IP in packet:
        


        #store ip addresses
        ipsrc = packet[IP].src
        ipdst = packet[IP].dst



        #display incoming ip address
        print("Src IP address: " + ipsrc)



        #check if the packet is a SYN packet
        if 'TCP' in packet and packet[TCP].flags == "S":



            #let the user know
            print("\n\n\nA SYN packet was detected from", ipsrc)
            print("Testing response.")



            #craft a SYN/ACK packet with window size of 0
            '''
            / is the Scapy operator used to stack the ip and tcp layers 
            together
            '''
            synackpac = IP(dst=ipsrc, src=ipdst)/TCP(dport=packet[TCP].sport, \
                sport=packet[TCP].dport, \
                flags="SA", \
                window=0)



            #send the SYN/ACK packet to the source ip address
            send(synackpac, verbose=0)



            # Wait for a response
            response = sr1(synackpac, timeout=3)



            #if there is a response, try for another for redundancies
            if response and TCP in response and response[TCP].flags == "SA":



                #alert the user
                print("\n\n\nThe crafted packet was accepted. Checking again...")



                #craft another SYN/ACK packet with window size of 0
                synackpac2 = IP(dst=ipsrc, src=ipdst)/TCP(dport=packet[TCP].sport, \
                    sport=packet[TCP].dport, \
                    flags="SA", \
                    window=0)



                #send the second SYN/ACK packet to the incoming ip address
                send(synackpac2, verbose=0)



                #wait for a second response
                response2 = sr1(synackpac2, timeout=3)



                #check if there is a second response
                if response2 and TCP in response2 and response2[TCP].flags == "SA":



                    #alert the user
                    print("\n\n\nThe crafted packet was accepted again.")
                    print("Adding to potential spoofer list.")



                    #add the ip to the potential spoofers list
                    if ipsrc not in spoofers:
                        spoofers.append(ipsrc)



        #add the incoming ip to the list
        if ipsrc not in incomingips:
            incomingips.append(ipsrc)



#sniff on all interfaces
print("\n\n\nSrc IPs and potentially spoofed IPs will be printed for each \
packet. If you want a record outside of STDOUT, restart this script and \
output to your file.")
print("[ctrl+c to exit sniffing]")

time.sleep(5)

print("\n\n\nChecking for potential IP spoofing...\n\n\n")

#store=0 keeps the memory clear
sniff(prn=processPacket, store=0)


#print all src ips
print("\n\n\nAll Source IPs:")
print("---------------")

for address in incomingips:

    print(address)



#print the potentially spoofed IPs
print("\n\n\nPotentially Spoofed IPs:")
print("------------------------")

for address in spoofers:

    print(address)