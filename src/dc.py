#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: dc.py                                                                 #
#                                                                             #
# VERSION: 20230415                                                           #
#                                                                             #
# SYNOPSIS: Sniff out potential ICMP tunneling                                #
#                                                                             #
# DESCRIPTION: This script looks for potential indicators of ICMP tunelling.  #
#              ICMP tunneling is a technique used to encapsulate arbitrary    #
#              network traffic inside ICMP (Internet Control Message          #
#              Protocol) packets, in order to bypass network security         #
#              measures or to enable communication between networks where     #
#              normal traffic is blocked. The idea behind ICMP tunneling is   #
#              to use the ICMP protocol, which is typically used for error    #
#              reporting and diagnostic purposes, to carry data packets       #
#              between two endpoints. By encapsulating the data inside ICMP   #
#              packets, the data can traverse networks that might otherwise   #
#              block the type of traffic being carried.                       #
#              ICMP tunneling is often used by hackers to exfiltrate data or  #
#              to establish covert communication channels. It can also be     #
#              used by legitimate users to bypass network restrictions or to  #
#              enable communication in situations where normal network        #
#              traffic is blocked. Top 5 indicators of ICMP tunelling:        #
#              Top 5 indicators:                                              #
#              1.) Unusual ICMP traffic patterns: ICMP tunneling can be       #
#                  identified by monitoring network traffic for unusual       #
#                  patterns of ICMP packets, such as a high volume of ICMP    #
#                  traffic or ICMP packets that are unusually large.          #
#              2.) Presence of covert channels: ICMP tunneling can be used to #
#                  establish covert channels between two endpoints. The       #
#                  presence of such channels can be an indicator of ICMP      #
#                  tunneling.                                                 #
#              3.) Suspicious payload content: ICMP packets that contain      #
#                  suspicious payload content, such as encoded or encrypted   #
#                  data, can be an indicator of ICMP tunneling.               #
#              4.) Timing anomalies: ICMP tunneling can be identified by      #
#                  monitoring network traffic for timing anomalies, such as   #
#                  large delays between ICMP packets or patterns of ICMP      #
#                  traffic that do not match expected patterns.               #
#              5.) Abnormal network behavior: ICMP tunneling can cause        #
#                  abnormal network behavior, such as unexpected drops in     #
#                  network performance or network outages.                    #
#                                                                             #
# INPUT: None                                                                 #
#                                                                             #
# OUTPUT: STDOUT                                                              #
#                                                                             #
# PRE-RUNTIME NOTES: Make sure iface is set to the list of interfaces you     #
#                    want monitored                                           #
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
import psutil



#declare variables
lasticmppackettime = 0
icmppacketcounts = {}



#define functions
def icmpTunnelingDetector(pkt):

    if isUnusualIcmpTraffic(pkt):

        print(f"Unusual ICMP traffic pattern detected from {pkt[IP].src} to \
{pkt[IP].dst}")



    if isCoverChannel(pkt):

        print(f"Covert channel detected in ICMP packet from {pkt[IP].src} to \
{pkt[IP].dst}")



    if isSuspiciousPayload(pkt):

        print(f"Suspicious payload content detected in ICMP packet from \
{pkt[IP].src} to {pkt[IP].dst}")



    if isTimingAnomaly(pkt):

        print(f"Timing anomaly detected in ICMP packet from {pkt[IP].src} to \
{pkt[IP].dst}")



    if isAbnormalNetworkBehavior(pkt):

        print(f"Abnormal network behavior detected in ICMP packet from \
{pkt[IP].src} to {pkt[IP].dst}")



def isUnusualIcmpTraffic(pkt):

    global lasticmppackettime

    #check for unusually large or small ICMP packets
    if len(pkt[ICMP]) < 8 or len(pkt[ICMP]) > 1500:
      
        return True



    #check for high volume of ICMP packets
    if pkt[IP].src in icmppacketcounts:

        icmppacketcounts[pkt[IP].src] += 1



    else:

        icmppacketcounts[pkt[IP].src] = 1



    if icmppacketcounts[pkt[IP].src] > 100:

        return True



    #check for ICMP packets with unusual source or destination addresses
    if pkt[IP].src.startswith("10.") and not pkt[IP].dst.startswith("10."):

        return True



    #check for ICMP packets with unusual timing or delay
    if pkt.time - lasticmppackettime < 0.01:

        return True



    #update the last ICMP packet time
    lasticmppackettime = pkt.time



    #no unusual traffic patterns detected
    return False



def isCoverChannel(pkt):
    '''
    This function is a demo only and should be taken with a grain of salt
    '''

    # check if packet has a Raw layer
    if not pkt.haslayer(Raw):
        return False

    #check for covert channels in ICMP packet payload
    payload = str(pkt[Raw].load)
    
    if len(payload) < 8:
    
        return False



    #sloppy check for hidden messages using steganography
    if "steg" in payload.lower():
        
        return True



    #check for encoding of data in packet payload
    if "b64" in payload.lower():
        
        try:
        
            decodedpayload = base64.b64decode(payload)



            if "secret message" in decodedpayload:
        
                return True



        except:

            pass



    #no covert channels detected
    return False



def isSuspiciousPayload(pkt):

    # check if packet has a Raw layer
    if not pkt.haslayer(Raw):
        return False

    #check for payloads that are not valid ASCII
    try:
        payload = pkt[Raw].load.decode("ascii")
    except UnicodeDecodeError:
        return True

    #check for payloads that are not valid base64
    try:
        decodedpayload = base64.b64decode(payload)
    except:
        return True

    #check for payloads that are not valid JSON
    try:
        json.loads(payload)
    except:
        return True

    #check for payloads that contain shell commands
    if any(command in payload.lower() for command in ["sh", "bash", "cmd", "powershell"]):
        return True

    #no suspicious payloads detected
    return False



def isTimingAnomaly(pkt):

    #declare global because we need the previous packet time
    global lasticmppackettime



    #check for ICMP packets that are sent too quickly
    if pkt.time - lasticmppackettime < 0.01:
      
        return True



    #check for ICMP packets that are sent at unusual times
    if abs(pkt.time - int(pkt.time)) < 0.001:
    
        return True



    #update the last ICMP packet time
    lasticmppackettime = pkt.time



    #no timing anomalies detected
    return False



def isAbnormalNetworkBehavior(pkt):
    
    #check for unusually high network traffic volume
    if len(pkt) > 1500:
    
        return True



    #check for excessive use of network resources
    if psutil.net_io_counters().bytes_sent > 1e9:
      
        return True



    #check for unusual network latency or packet loss
    rtt = ping(pkt[IP].dst)

    if rtt is not None and rtt > 100:
 
        return True



    #no abnormal network behavior detected
    return False



def ping(host):
    '''
    Returns True if host (str) responds to a ping request.
    '''

    #ping parameter
    pingstr = "-c 1"



    #ping
    response = os.system(f"ping {pingstr} {host} > /dev/null 2>&1")



    #teturn True if the response code is zero
    return response == 0



#print to user
print("\n\n\nSniffing for ICMP tunneling...\n\n\n")



#set up packet capture on network interfaces
sniff(prn=icmpTunnelingDetector, filter="icmp", iface=["wlp1s0"])