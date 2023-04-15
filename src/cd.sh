#!/bin/bash



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: cd.sh                                                                 #
#                                                                             #
# VERSION: 20230415                                                           #
#                                                                             #
# SYNOPSIS: Syscall sniffer                                                   #
#                                                                             #
# DESCRIPTION: Must be run as sudo if you want to monitor a PID that isn't    #
#              yours or a PID that is owned by root. This script performs     #
#              syscall sniffing on the PID selected by the user.              #
#                                                                             #
#                                                                             #
# INPUT: Runtime user input                                                   #
#                                                                             #
# OUTPUT: None                                                                #
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



#print out all running PIDs and their associated program names
echo
echo
echo
echo "Running processes:"
ps -eo pid,comm | awk '{print $1,$2}'



#get PID to monitor
echo
echo
echo
read -p "Enter the PID you want to monitor: " PID



#strace the PID
sudo strace -p $PID -f -s 9999 -e trace=all 2>&1 | while read line



#extract relevant information and stdout
do

  echo "$line"

done