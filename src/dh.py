#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: dh.py                                                                 #
#                                                                             #
# VERSION: 20230415                                                           #
#                                                                             #
# SYNOPSIS: Aggregate virtual hosting entities                                #
#                                                                             #
# DESCRIPTION: This script detects and list all virtual hosts from a remote   #
#              server. Virtual hosting or virtual routing is a technique used #
#              to host multiple websites on a single web server, where each   #
#              website has its own domain name and appears to have its own IP #
#              address. This is done by configuring the web server to         #
#              recognize different domain names and to serve different        #
#              content for each domain name.                                  #
#              Some  possible reasons why an attacker would want to know if a #
#              server is using virtual hosting:                               #
#              1.) Targeted attacks: An attacker may want to launch a         #
#                  targeted attack against a specific website hosted on the   #
#                  virtual host. By identifying the IP address and virtual    #
#                  host name of the target website, the attacker can focus    #
#                  their attack on that specific website rather than trying   #
#                  to attack the entire server.                               #
#              2.) Resource allocation: An attacker may want to know if a     #
#                  server is using virtual hosting in order to determine how  #
#                  the server's resources are allocated. If multiple websites #
#                  are hosted on the same server, the attacker may be able to #
#                  exploit vulnerabilities in one website to gain access to   #
#                  other websites hosted on the same server.                  #
#              3.) Information gathering: An attacker may want to gather      #
#                  information about the server's configuration and setup in  #
#                  order to plan future attacks. By identifying the virtual   #
#                  hosts and IP addresses associated with a server, the       #
#                  attacker can learn more about the server's architecture    #
#                  and potential vulnerabilities. This information can then   #
#                  be used to plan more effective attacks in the future.      #
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
import socket
import re

#get IP address
ip = input("\n\n\nEnter an IP address: ")



#get list of websites on that IP address
try:

    hostname = socket.gethostbyaddr(ip)[0]



except socket.herror:

    print("\n\n\nNo hostnames found for IP address:", ip)



    exit()



#filter out invalid domain names
hostname = re.sub(r'\.$', '', hostname) #remove trailing dot, if present



if re.match(r'^[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$', hostname):

    domainnames = [hostname]



else:

    domainnames = []



#list domain names
if domainnames:
    
    print("\n\n\nWebsites hosted on", ip + ":")
    


    for name in domainnames:
    
        print(name)



else:

    print("\n\n\nNo websites found on IP address:", ip)