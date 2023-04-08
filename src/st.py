#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: st.py                                                                 #
#                                                                             #
# VERSION: 20230408                                                           #
#                                                                             #
# SYNOPSIS: Check for potential HTTP tunneling on a local host                #
#                                                                             #
# DESCRIPTION: This script looks for over a dozen different indicators of     #
#              potential HTTP tunelling by running a function on each packet. #
#              The analyzePacket function checks for the following indicators #
#              and HTTP protocol violations around ports 80 and 443 that      #
#              could indicate HTTP tunneling.                                 #
#                                                                             #
#              Indicators:                                                    #
#              1.) Unusual HTTP traffic patterns such as repeated connections #
#                  to the same IP address or multiple requests for the same   #
#                  resource                                                   #
#              2.) Large and unexpected HTTP request or response sizes        #
#              3.) Use of anomalous HTTP ports                                #
#              4.) Use of unusual or non-standard HTTP methods such as        #
#                  CONNECT                                                    #
#              5.) Use of HTTP compression to hide the data being transmitted #
#              6.) Unexpected user agents                                     #
#              7.) HTTP traffic over non-HTTP protocols such as ICMP or DNS   #
#              8.) Unusual traffic from known good sources such as traffic    #
#                  from a printer or IoT device that is sending HTTP traffic  #
#              9.) Large amount of traffic in a short amount of time          #
#                                                                             #
#              Protocol Violations. Sending a request or response with:       #
#             10.) Invalid syntax or incomplete headers                       #
#             11.) Missing or incorrect HTTP version                          #
#             12.) Invalid or missing HTTP headers                            #
#             13.) Unsupported HTTP methods                                   #
#             14.) Invalid or unsupported HTTP URL                            #
#             15.) Incorrect or invalid status code such as a 404 status code #
#                  for a request that was successful                          #
#             16.) Invalid or unsupported HTTP cookies                        #
#                                                                             #
# INPUT: None                                                                 #
#                                                                             #
# OUTPUT: STDOUT                                                              #
#                                                                             #
# PRE-RUNTIME NOTES: 1.) packet[Raw] is a layer in the Scapy packet capture   #
#                        library that represents the raw data payload of a    #
#                        packet. In the context of HTTP traffic, the Raw      #
#                        layer contains the HTTP request or response body as  #
#                        a string of bytes.                                   #
#                    2.) I used regex101.com as a source for regex checking   #
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
import re
from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse
import time



#create functions
def analyzePacket(packet):
    
    '''
    packet analysis function to detect indicators of HTTP tunelling
    '''
    


    #extract packet fields
    srcip = packet[IP].src
    dstip = packet[IP].dst
    srcport = packet[TCP].sport
    dstport = packet[TCP].dport
    httpmethod = packet[Raw].load.split()[0] if Raw in packet else ""
    useragent = packet[HTTPRequest].User_Agent if HTTPRequest in packet else ""
    requestsize = len(packet[Raw].load) if Raw in packet else 0 #bytes
    responsesize = len(packet[Raw].load) if Raw in packet else 0 #bytes
    httpport = 80 if dstport == 80 else 443 if dstport == 443 else None



    #print packet src and dst
    print(srcip + " -> " + dstip)



    #check for potential indicators
    #0x018 = TCP flag for repeat connection attempt
    if packet[TCP].flags == 0x018:

        print("Indicator 1: Repeated connections to the same IP address \
detected (src={}, dst={}, sport={}, dport={})".format(srcip, \
                                                      dstip, \
                                                      srcport, \
                                                      dstport))

    if requestsize > 1000000 or responsesize > 1000000:

        print("Indicator 2: Large HTTP request or response size detected.")

        if requestsize >= responsesize:

            print("              Request size (bytes):", requestsize)

        else:

            print("              Response size (bytes):", responsesize)

    if httpport not in [80, 443]:

        print("Indicator 3: Anomalous HTTP port detected (port {})"\
            .format(dstport))

    if httpmethod == "CONNECT":

        print("Indicator 4: Unusual HTTP method detected (CONNECT)")
    
    if "Content-Encoding" in str(packet) and "gzip" in str(packet):

        print("Indicator 5: HTTP compression detected (gzip)")
    
    if useragent == "":

        print("Indicator 6: Empty or missing user agent detected")
    
    #6 = TCP, 17 = UDP
    if packet[IP].proto not in [6, 17]:

        print("Indicator 7: HTTP traffic over non-HTTP protocol detected \
(protocol {})".format(packet[IP].proto))
    
    if srcport > 1024 and srcport not in [80, 443] and httpport == None:

        print("Indicator 8: Non-standard port detected (port {})"\
            .format(srcport))

    if requestsize > 100000 and httpmethod != "POST":

        print("Indicator 9: Large amount of data transferred in a short amount \
of time ({} bytes)".format(requestsize))



    #resource saving if
    if Raw in packet:
        
        #serialize packet[Raw]
        raw = str(packet[Raw].load)



        #check for potential violations
        #match the first line of an HTTP request or response message
        if not re.search(r"^([A-Z]+) /(\S+) HTTP/(\d\.\d)$", raw):

            print("Violation 10: Invalid request syntax detected: " + raw)
        
        #match the first line and captures the version and status code
        if not re.search(r"^HTTP/(\d\.\d) (\d{3}) .*$", raw):

            print("Violation 11: Invalid response syntax detected: " + raw)
        
        if HTTPRequest in packet and "Host" not in packet[HTTPRequest].fields:

            print("Violation 12: Missing Host header in HTTP request")
        
        if HTTPRequest in packet and packet[HTTPRequest].fields["Host"] == "":

            print("Violation 12: Empty Host header in HTTP request")
        
        if HTTPRequest in packet and httpmethod not in ["GET", \
                                                        "HEAD", \
                                                        "POST", \
                                                        "PUT", \
                                                        "DELETE", \
                                                        "CONNECT", \
                                                        "OPTIONS", \
                                                        "TRACE"]:

            print("Violation 13: Unsupported HTTP method: " + httpmethod)

        #match a URL
        if HTTPRequest in packet and not \
        re.search(r"^[a-zA-Z0-9\-\._~:/\?#\[\]@!\$&'\(\)\*\+,;=]*$",\
                  packet[HTTPRequest].Path):

            print("Violation 14: Invalid characters in HTTP request URL \
detected: " + packet[HTTPRequest].Path)

        if HTTPRequest in packet and packet[HTTPRequest].Path == "":
            
            print("Violation 14: Empty HTTP request URL detected")
        
        if HTTPResponse in packet and packet[HTTPResponse].Status_Code == "":
         
            print("Violation 15: Empty HTTP response status code detected")
        
        #match the first line of an HTTP response
        if HTTPResponse in packet and not \
        re.search(r"^HTTP/(\d\.\d) \d{3} .*$", str(packet[HTTPResponse])):
            
            print("Violation 15: Invalid HTTP response status line detected: "\
                  + str(packet[HTTPResponse]))
        
        #match a string that represents an HTTP cookie
        if HTTPRequest in packet and "Cookie" in packet[HTTPRequest].fields \
        and not re.search(r"^[a-zA-Z0-9\-\._~:\+%/]*=\S*$", \
                          packet[HTTPRequest].fields["Cookie"]):

            print("Violation 16: Potential invalid HTTP cookie format detected: "\
                  + packet[HTTPRequest].fields["Cookie"])



    #onto the next packet
    print("\n\n\n")



#sniff on all interfaces
print("\n\n\nIndicators will be printed for each packet. If you want a record outside of STDOUT, restart this script and output to your file.")
print("[ctrl+c to exit sniffing]")

time.sleep(5)

print("\n\n\nChecking for HTTP Tunelling indicators and HTTP Violations...\n\n\n")

sniff(filter="tcp port 80 or tcp port 443", prn=analyzePacket)