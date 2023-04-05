#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: di.py                                                                 #
#                                                                             #
# VERSION: 20230405                                                           #
#                                                                             #
# SYNOPSIS: Check for IIS Lockdown Tool on remote server.                     #
#                                                                             #
# DESCRIPTION: This script checks a remote server to see if it is an IIS      #
#              server. If so, a check is done for the IIS Lockdown Tool. The  #
#              IIS Lockdown Tool is a security tool developed by Microsoft to #
#              help secure IIS web servers by reducing the attack surface.    #
#              Examples of what IIS can do include:                           #
#              1.) disabling unnecessary services,                            #
#              2.) removing unnecessary features,                             #
#              3.) banner obfuscation,                                        #
#              4.) URLScan,                                                   #
#              5.) configure SSL/TLS                                          #
#                                                                             #
# INPUT: Runtime user input                                                   #
#                                                                             #
# OUTPUT: STDOUT                                                              #
#                                                                             #
# PRE-RUNTIME NOTES: None.                                                    #
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
import http.client



#set parameters
rserver = input("\n\n\nEnter IP address: ")
PORT = 80



#connect to rserver and send the request
conn = http.client.HTTPConnection(rserver, PORT)

conn.request("HEAD", "/")



#fetch the response
res = conn.getresponse()
print("\n\n\nServer:", res.getheader("Server"))


#check for IIS Server and IIS Lockdown Tool
if "Microsoft-IIS" in res.getheader("Server"):

    print("\n\n\nThe remote server is running IIS web server.")



    #check for IIS Lockdown Tool
    conn.request("GET", "/iisadmpwd/aexp2b.aspx")

    res = conn.getresponse()

    if res.status == 404:

        print("\n\n\nThe IIS Lockdown Tool is not installed on the remote \
server.")

    else:

        print("\n\n\nThe IIS Lockdown Tool is installed on the remote server.")



else:

    print("\n\n\nThe remote server is not running IIS web server.")