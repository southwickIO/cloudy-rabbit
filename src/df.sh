#!/bin/bash



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: df.sh                                                                 #
#                                                                             #
# VERSION: 20230403                                                           #
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
# INPUT: Runtime user input                                                   #
#                                                                             #
# OUTPUT: 1.) STDOUT                                                          #
#         2.) packets.cap (deleted at end)                                    #
#                                                                             #
# PRE-RUNTIME NOTES: This script sniffs packets. Consider local laws.         #
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

ifconfig -a | awk '/^[^ ]/ { iface=$1; } /mtu/ { print iface " MTU=" $NF }'



#request MTU size change
echo
echo
echo
read -p "Do you want to change MTU size for all interfaces with MTU not equal to 1500? (y/n): " answer



#change MTU to default if requested
if [ "$answer" == "y" ]; then

  for iface in $(ifconfig -a | grep -oP '^\S+')
  do

    mtu=$(ifconfig $iface | grep -oP 'mtu \K\d+')
    
    if [ "$mtu" != "1500" ]; then

      echo
      echo
      echo
      echo "Changing MTU size of $iface from $mtu to 1500"
      
      sudo ifconfig $iface mtu 1500

    fi
  
  done

fi



#get packet count
echo
echo
echo
read -p "How many packets would you like to sniff for fragmented packets: " count



#capture packets with MF flag set
echo
echo
echo
echo "Listening for fragmented packets for $count packets..."
echo
echo
echo
echo "Press CTRL+C to stop sniffing before $count packets."
echo "Run the following command in another terminal if you want to test:"
echo "ping -c 3 -s 3000 8.8.8.8"
echo
echo
echo
sudo tcpdump -v -i any -c $count 'ip[6] & 0x1 != 0' -w packets.cap



#change to proper ownership
sudo chown $(whoami) packets.cap


#check for hits
if [ -s packets.cap ]; then

  #list destination addresses of any hits
  echo
  echo
  echo
  echo "Any hits listed with source and destination address."
  sudo tcpdump -nn -r packets.cap 'ip[6] & 0x1 != 0' | awk '{print "Source address: " $3 " " "Destination address: " $5}' | sort -u

fi



#clean up
rm -f packets.cap