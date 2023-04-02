#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: tipid.py                                                              #
#                                                                             #
# VERSION: 20230321                                                           #
#                                                                             #
# SYNOPSIS: Track IP-IDs for patterns and exploit analysis                    #
#                                                                             #
# DESCRIPTION: Analyze the IP-IDs of an IP address to determine order of IDs. #
# Different patterns can help determine exploits or corroborate any idle      #
# network scan that only scans for sequential IP-IDs. This was based on the   #
# paper *A closer look at IP-ID behavior in the Wild* by Flavia Salutari,     #
# Danilo Cicalese, and Dario J. Rossi.                                        #
#                                                                             #
# INPUT: 1.) Runtime user input                                               #
#                                                                             #
# OUTPUT: 1.) STDOUT                                                          #
#         2.) ./sample.pcap                                                   #
#         3.) ./ipids.txt                                                     #
#                                                                             #
# PRE-RUNTIME NOTES: 1.) You will need to open another terminal and ping your #
#                        target when prompted.                                #
#                    2.) At the time of writing, 68.173.202.37, was an        #
#                        example of sequential incremental IP-IDs. I do not   #
#                        own this IP address. Ping at your own risk.          #
#                    3.) The dir tree needs to be kept intact for this script #
#                        to work correctly. Otherwise you will need to set    #
#                        TARGETDIR yourself.                                  #
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
import scapy.all as scapy #sudo pip3 install scapy
import os
import shutil


#set constants
TARGETDIR = os.path.join(os.path.dirname(__file__), "..", "res", "output")

if not os.path.exists(TARGETDIR):
    os.makedirs(TARGETDIR)


#delete the target files if they exists
if os.path.exists(f"{TARGETDIR}/sample.pcap"):

    os.remove(f"{TARGETDIR}/sample.pcap")

if os.path.exists(f"{TARGETDIR}/ipids.txt"):

    os.remove(f"{TARGETDIR}/ipids.txt")


#get IP address
ip = input("\nEnter the IP address to capture packets from: ")
packetcount = int(input("Enter the number of packets to capture: "))



#STDOUT instructions and parameters
print("\n\n\nNow, open another terminal and enter the following command:")
print(f"\nping -c {int(packetcount * 1.1)} {ip}")
print("\nRepeat the command if there is a packet loss of more than 10%")
print("Find another IP address in the event of 100% packet loss.\n\n\n")
print(f"Sniffing for {packetcount} packets from {ip}...")



#sniff packets and provide status
packets = []

for i in range(packetcount):

    packet = scapy.sniff(filter=f"src host {ip}", count=1)[0]

    packets.append(packet)

    print(packet)

    if (i + 1) % 5 == 0:

        print(f"\n{i+1} packets captured.\n")



#extract IP-IDs
ipids = []

for packet in packets:

    if packet.haslayer('IP'):

        ipids.append(packet['IP'].id)



#determine patterned behavior
if all(x == ipids[0] for x in ipids):

    print("\nIP-ID values are constant.")

elif all(x == ipids[0]+i for i, x in enumerate(ipids)):

    print("\nIP-ID values are incremented sequentially.")

else:

    print("\nIP-ID values are random.")



#check for duplicates
if len(ipids) == len(set(ipids)):

    print("\nNo duplicate IP-ID values found.")

else:

    print("\nDuplicate IP-ID values found.")



#print IP-IDs
#print("\nIP-ID values:")
#
#for ipid in ipids:
#    print(ipid)



#output to sample.pcap file and ipids.txt for further analysis
scapy.wrpcap(f"{TARGETDIR}/sample.pcap", packets)

with open(f"{TARGETDIR}/ipids.txt", 'w') as file:

    for ip_id in ipids:

        file.write(str(ip_id) + '\n')

print("\nCaptured packets saved in ../res/output/sample.pcap file.")
print("\nIP-ID values saved in ../res/output/ipids.txt file.")
print("\nExiting...\n")