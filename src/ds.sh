#!/bin/bash



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# NAME: ds.sh                                                                 #
#                                                                             #
# VERSION: 20230402                                                           #
#                                                                             #
# SYNOPSIS: Checks source routing toggle                                      # 
#                                                                             #
# DESCRIPTION: Checks if source routing is turned on (security risk), offers  # 
#              to toggle source routing for user, and displays the users      #
#              current routing table.                                         #
#                                                                             #
# INPUT: 1.) Runtime user input                                               #
#                                                                             #
# OUTPUT: 1.) STDOUT                                                          #
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



#check if source routing is enabled
if [[ $(sysctl -n net.ipv4.conf.all.accept_source_route) -eq 1 ]]; then
  
  echo
  echo
  echo
  echo "***SOURCE ROUTING IS CURRENTLY ENABLED***"
  echo
  echo
  echo


  #request toggle choice
  read -p "Do you want to keep source routing enabled? (y/n) " choice
  echo
  echo
  echo



  #toggle choice
  case "$choice" in

    y|Y )

      echo "Source routing will be kept enabled."
      echo
      echo
      echo

      ;;

    n|N )

      #disable source routing
      sudo sysctl -w net.ipv4.conf.all.accept_source_route=0

      echo "Source routing has been disabled."
      echo
      echo
      echo
      
      ;;

    * )

      echo "Invalid choice. Source routing will be kept enabled."
      echo
      echo
      echo

      ;;

  esac



else

  echo
  echo
  echo
  echo "***SOURCE ROUTING IS CURRENTLY DISABLED***"
  echo
  echo
  echo



  #request toggle choice
  read -p "Do you want to enable source routing? (y/n) " choice
  echo
  echo
  echo



  #toggle choice
  case "$choice" in

    y|Y )

      #enable source routing
      sudo sysctl -w net.ipv4.conf.all.accept_source_route=1

      echo "Source routing has been enabled."
      echo
      echo
      echo
      
      ;;

    n|N )
      
      echo "Source routing will be kept disabled."
      echo
      echo
      echo
      
      ;;
    * )

      
      echo "Invalid choice. Source routing will be kept disabled."
      echo
      echo
      echo
      
      ;;

  esac



fi

# Display the current routing table
echo "Here is the current routing table:"
ip route