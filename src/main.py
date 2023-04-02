#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: main.py	   															  #
#	 																		  #
# VERSION: 20230402	   														  #
#	 																	      #
# SYNOPSIS: Main menu for the cloudy-rabbit application	                      #
#	                                                                          #
# DESCRIPTION: Help youself navigate the application with this simple menu.   #
#	                                                                          #
# INPUT: 1.) Runtime user input	                                              #
#	                                                                          #
# OUTPUT: 1.) STDOUT	                                                      #
#	                                                                          #
# PRE-RUNTIME NOTES: 1.) Must be run as sudo to properly work	              #
#	                                                                          #
# AUTHORS: @southwickio	                                                      #
#	                                                                          #
# LICENSE: GPLv3	                                                          #
#	                                                                          #
# DISCLAIMER: All work produced by Authors is provided “AS IS”. Authors make  #
#	 no warranties, express or implied, and hereby disclaims any and          #
#	 all warranties, including, but not limited to, any warranty of           #
#	 fitness, application, et cetera, for any particular purpose,	          #
#	 use case, or application of this script.	                              #
#	                                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



#import dependencies
import subprocess



#splash
print('''   ________	__	 ____	__	__	_ __ 
  / ____/ /___  __  ______/ /_  __   / __ \\____ _/ /_  / /_  (_) /_
 / /   / / __ \\/ / / / __  / / / /  / /_/ / __ `/ __ \\/ __ \\/ / __/
/ /___/ / /_/ / /_/ / /_/ / /_/ /  / _, _/ /_/ / /_/ / /_/ / / /_  
\\____/_/\\____/\\__,_/\\__,_/\\__, /  /_/ |_|\\__,_/_.___/_.___/_/\\__/  
	 /____/	

author: @southwickio\n''')



#begin menu
while True:

	print("Select a script:")
	print("----------------\n")

	#list scripts
	print('''1. Fetch Comments (fc.py) - This script fetches all HTML comments 
		from a site specified by the user and outputs to STDOUT and 
		./comments.txt. This can be used from a cybersecurity standpoint as a 
		way to look for any developer comments that made it to production that
		shouldn't have; such as passwords, keys, or other proprietary 
		information.''')

	print('''2. Get Logs (gl.sh) - This script outputs all `.log` files on a 
		nix machine. Potential cybersecurity use cases include tracking down
		a specific log, what applications are running on the machine, and 
		modification dates for DFIR. Run as sudo for different results.''')
	
	print('''3. Track IP-IDs (tipid.py) - Must be run as sudo. Analyze the
		IP-IDs of an IP address to determine order of IDs. Different patterns
		can help determine exploits or corroborate any idle network scan (with
		a zombie) that only scans for sequential IP-IDs. This was based on the
		paper *A closer look at IP-ID behavior in the Wild* by Flavia Salutari,
		Danilo Cicalese, and Dario J. Rossi.''')
	
	print('''4. Count Host Command (ch.sh) - Must be run as sudo. Runs the host
		command N times and counts unique occurences across different
		geographical regions. This can assist an analyst in finding anomalous
		data and help further map an external network.''')



	#ingress choice
	choice = int(input("\nEnter your choice (1-4): "))



	#match choice
	match choice:

		case 1:
			subprocess.run(["python3", "./fc.py"])
			print("\n\n\n\n\n")
		
		case 2:
			subprocess.run(["bash", "./gl.sh"])
			print("\n\n\n\n\n")
		
		case 3:
			subprocess.run(["python3", "./tipid.py"])
			print("\n\n\n\n\n")
		
		case 4:
			subprocess.run(["bash", "./ch.sh"])
			print("\n\n\n\n\n")
		
		case _:
			print("\n\n\n\n\n")



	#offer another run
	updown = input("Would you like to run another script (y/n): ")

	if updown == 'y' or updown == 'Y':

		continue
	
	else:

		#end menu
		break