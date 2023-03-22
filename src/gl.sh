#!/bin/bash



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# NAME: gl.sh                                                                 #
#                                                                             #
# VERSION: 20230321                                                           #
#                                                                             #
# SYNOPSIS: Fetch .log files from a *nix machine                              # 
#                                                                             #
# DESCRIPTION: This script outputs all `.log` files on a *nix machine.        #
#              Potential cybersecurity use cases include tracking down a      #
#              specific log, what applications are running on the machine,    #
#              and modification dates for DFIR. Run as sudo for different     #
#              results.                                                       #
#                                                                             #
# INPUT: 1.) Runtime user input                                               #
#                                                                             #
# OUTPUT: 1.) STDOUT                                                          #
#         2.) ./logs.csv                                                      #
#                                                                             #
# PRE-RUNTIME NOTES: 1.) None.                                                #
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



#define constants
TARGETDIR="../res/output"
TARGETFILE="logs.csv"



# Create output directory if it doesn't exist
if [ ! -d "$TARGETDIR" ]; then

  mkdir -p "$TARGETDIR"

fi



# Delete output file if it exists
if [ -f "$TARGETDIR/$TARGETFILE" ]; then

  rm "$TARGETDIR/$TARGETFILE"

fi



read -p "Do you want to output to a CSV file? (Y/N): " answer



if [ "$answer" == "Y" ] || [ "$answer" == "y" ]



then
  find / -type f -iname "*.log" -printf "%TY-%Tm-%Td %TH:%TM,%p\n" > "$TARGETDIR/$TARGETFILE" 2>/dev/null
  echo "Output saved to ../res/output/logs.csv"



else
  echo "Printing output to screen..."
  find / -type f -iname "*.log" -printf "%TY-%Tm-%Td %TH:%TM,%p\n" 2>/dev/null



fi