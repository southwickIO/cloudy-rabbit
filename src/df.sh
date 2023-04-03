#!/bin/bash



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# NAME: df.sh                                                                 #
#                                                                             #
# VERSION: 20230402                                                           #
#                                                                             #
# SYNOPSIS: Checks endpoint network packet fragmentation                      # 
#                                                                             #
# DESCRIPTION: This script does the following:                                #
#              1.) Check MTU size and asks user if they want a reset to 1500  #
#              2.) Listen to all interfaces for network packet fragmentation. #
#                  Fragmentation is a lowish level indicator on it's own, but #
#                  can help detect IDS evasion. The following listening       #
#                  features are implemented:                                  #
#                  a.) -nn to disable DNS resolution and display IP addresses #
#                      instead of hostnames                                   #
#                  b.) The filter expression 'ip[6] & 0x1 != 0' to capture IP #
#                      packets with the "fragmentation needed" bit set in the #
#                      IP header.                                             #
#              3.) Lists indicators of fragmentation                          #
#              4.) Perform script related cleanup duties                      #
#                                                                             #
# INPUT: 1.) Runtime user input                                               #
#                                                                             #
# OUTPUT: 1.) STDOUT                                                          #
#         2.) packets.cap (deleted at end)                                    #
#                                                                             #
# PRE-RUNTIME NOTES: 1.) None                                                 #
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



#list all interfaces and their MTU size
echo
echo
echo
echo "List of network interfaces and their MTU size:"

ifconfig -a | grep -oP '^\S+: .*mtu \K\d+'



#request MTU size change
echo
echo
echo
read -p "Do you want to change MTU size for all interfaces with MTU not equal to 1500? (y/n): " answer



#change MTU to default if requested
if [ "$answer" == "y" ]; then
  # Change MTU size for all interfaces with MTU not equal to 1500
  for iface in $(ifconfig -a | grep -oP '^\S+')
  do
    mtu=$(ifconfig $iface | grep -oP 'mtu \K\d+')
    if [ "$mtu" != "1500" ]; then
      echo "Changing MTU size of $iface from $mtu to 1500"
      sudo ifconfig $iface mtu 1500
    fi
  done
fi

# Get duration of tcpdump capture
read -p "How many seconds would you like to listen for fragmented packets?: " duration

# Capture packets with MF flag set
echo "Listening for fragmented packets for $duration seconds..."
sudo tcpdump -v -i any 'ip[6] & 0x1 != 0' -G $duration -W 1 -w packets.cap

# Check if there were any hits
if [ -s packets.cap ]; then
  # List destination addresses of captured packets
  echo "Fragmented packets detected. Destination addresses:"
  sudo tcpdump -nn -r packets.cap 'ip[6] & 0x1 != 0' | awk '{print $3}' | sort -u
else
  echo "No fragmented packets detected."
fi

# Clean up
rm -f packets.cap







test with ping -c 1 -s 3000 8.8.8.8