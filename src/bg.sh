#!/bin/bash



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: bg.sh                                                                 #
#                                                                             #
# VERSION: 20230403                                                           #
#                                                                             #
# SYNOPSIS: Simple nmap wrapped banner grabber to be included with the suite  #
#                                                                             #
# DESCRIPTION: This script collects banners using nmap for some of the more   #
#              popular ports.                                                 #
#                                                                             #
# INPUT: Runtime user input                                                   #
#                                                                             #
# OUTPUT: STDOUT                                                              #
#                                                                             #
# PRE-RUNTIME NOTES: This script scans domains. Consider local laws.          # 
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



# Ask user for IP or URL input
echo
echo
echo
read -p "Enter IP or URL: " target



# Run nmap with -sV flag and ports 20-8080
echo
echo
echo
nmap -sV -p20-9000 $target