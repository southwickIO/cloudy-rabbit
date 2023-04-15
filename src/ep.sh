#!/bin/bash



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: ep.sh                                                                 #
#                                                                             #
# VERSION: 20230415                                                           #
#                                                                             #
# SYNOPSIS: Enumeration for ports 53, 445, 161-162, 389, 135, 137-139         #
#                                                                             #
# DESCRIPTION: This script checks if ports 53, 445, 161-162, 389, 135,        #
#              137-139 are open with nmap and then enum4linux performs simple #
#              enumeration. This is meant to have Microsoft targets.          #
#                                                                             #
#                                                                             #
# INPUT: Runtime user input                                                   #
#                                                                             #
# OUTPUT: 1.) STDOUT                                                          #
#         2.) directory                                                       #
#         3.) text file                                                       #
#                                                                             #
# PRE-RUNTIME NOTES: enum4linux.pl filepath must be correct for this script   # 
#                    to work                                                  #
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



#get target
echo
echo
echo
read -p "Enter the IP address or domain of the target host: " target



#create a temp directory to store results
mkdir -p ../res/output



echo
echo
echo
echo "Running preliminary nmap scan"
#scan ports and save results
nmap -Pn -p 53,445,161-162,389,135,137-139 -oN ../res/output/nmap.txt $target > /dev/null



echo
echo
echo
echo "Done. Running enum4linux.pl"
#run enum4linux and save results
perl ../res/enum4linux.pl -a -l -A $target > ../res/output/enum4linux.txt



#stdout
echo
echo
echo
echo "Done. Enumeration complete. Results saved to ../res/output/nmap.txt and \
../res/output/enum4linux.txt"