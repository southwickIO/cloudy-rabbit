#!/bin/bash



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# NAME: gl.sh                                                                 #
#                                                                             #
# VERSION: 20230321                                                           #
#                                                                             #
# SYNOPSIS: Host command iteration for further analysis                       # 
#                                                                             #
# DESCRIPTION: This script runs the host command N times and counts unique    #
#              occurences. This can assist an analyst in finding load         #
#              balancers and help further map an external network.            #
#                                                                             #
# INPUT: 1.) Runtime user input                                               #
#                                                                             #
# OUTPUT: 1.) STDOUT                                                          #
#         2.) ../res/output/hostcommand.csv"                                  #
#                                                                             #
# PRE-RUNTIME NOTES: 1.) This script has a 5 second delay between each        #
#                        iteration                                            #
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



#buildup check
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run as root. Exiting."
  exit 1
fi



#define variables and constants
dns=$(resolvectl status | grep "DNS Servers" | awk '{print $NF}')
linknumber=$(resolvectl dns | grep "\." | awk '{print $2}')
TARGETDIR="../res/output"
TARGETFILE="hostcommand.csv"
DELIMETER=","
DNSSERVERS=($dns 8.8.4.4 1.0.0.1 208.67.220.220)



#create output directory if it doesn't exist
if [ ! -d "$TARGETDIR" ]; then

  mkdir -p "$TARGETDIR"

fi



#delete output file if it exists
if [ -f "$TARGETDIR/$TARGETFILE" ]; then

  rm "$TARGETDIR/$TARGETFILE"

fi



#write header to output file
echo "Artifact" > "$TARGETDIR/$TARGETFILE"



#get user input
read -p "Enter URL: " url
read -p "Enter number of iterations: " iterations
read -p "Enter sleep time (sec): " sleeptime
echo


#iterate and append to output file
for server in "${DNSSERVERS[@]}"
do

  for (( i=1; i<=$iterations; i++ )); do

    #run host command and capture output
    output=$(host -t a "$url"; \
      host -t aaaa "$url"; \
      host -t cname "$url"; \
      host -t mx "$url"; \
      host -t ns "$url"; \
      host -t ptr "$url"; \
      host -t soa "$url"; \
      host -t srv "$url"; \
      host -t caa "$url"; \
      host -t spf "$url"; \
      host -t hinfo "$url"; \
      host -t naptr "$url"; \
      host -t rp "$url"; \
      host -t dname "$url"; \
      host -t txt "$url")



    #extract artifacts and message
    while read -r line; do
     
      #get artifact
      artifact=$(echo "$line" | awk '{ print substr($0, length($1)+2) }')
      


      #append artifact
      echo "$artifact" >> "$TARGETDIR/$TARGETFILE"

    

    done <<< "$output"



    #print status
    printf "Host command iteration %d complete. Sleeping..." "$i"
    echo



    #wait for sleeptime seconds
    sleep "$sleeptime"



  done


  #change DNS servers
  echo
  echo
  echo
  echo "Switching DNS servers..."

  resolvectl dns "$linknumber" "$server"

  resolvectl dns | grep "\."

  echo "DNS SERVER: $server" >> "$TARGETDIR/$TARGETFILE"
  echo
  echo
  echo



done



#count entries
count=$(cut -d "$DELIMETER" -f 1 "$TARGETDIR/$TARGETFILE" | sort | uniq -c)



#output entry count
echo
echo
echo
echo "$count" | sort -n



#teardown and restore
resolvectl dns "$linknumber" "$dns"
echo
echo
echo
echo "Switching to your original DNS server."
resolvectl dns | grep "\."



#exit instructions
echo
echo
echo
echo "Consider running this from a different IP address in the same country to compare results."
echo "Consider running this from a different IP address in a different country to find new, potentially relevant results."
echo
echo "Exiting."
echo