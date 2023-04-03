#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: main.py                                                               #
#                                                                             #
# VERSION: 20230403                                                           #
#                                                                             #
# SYNOPSIS: Main menu for the cloudy-rabbit application                       #
#                                                                             #
# DESCRIPTION: Help youself navigate the application with this simple menu.   #
#                                                                             #
# INPUT: 1.) Runtime user input                                               #
#                                                                             #
# OUTPUT: 1.) STDOUT                                                          #
#                                                                             #
# PRE-RUNTIME NOTES: 1.) Must be run as sudo to properly work                 #
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
import subprocess



#splash
print('''
   ________                __         ____        __    __    _ __ 
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
	print("1. Fetch Comments (fc.py)")
	print("2. Get Logs (gl.sh)")
	print("3. Track IP-IDs (ti.py)")
	print("4. Count Host Command (ch.sh)")
	print("5. Detect Source Routing (ds.sh)")
	print("6. Detect Network Packet Fragmentation (df.sh)")



	#ingress choice
	choice = int(input("\nEnter your choice (1-6): "))



	#match choice
	if choice == 1:

		subprocess.run(["python3", "./fc.py"])
		print("\n\n\n\n\n")
		


	elif choice == 2:

		subprocess.run(["bash", "./gl.sh"])
		print("\n\n\n\n\n")
		


	elif choice == 3:
		subprocess.run(["python3", "./ti.py"])
		print("\n\n\n\n\n")
		


	elif choice == 4:
		subprocess.run(["bash", "./ch.sh"])
		print("\n\n\n\n\n")



	elif choice == 5:
		subprocess.run(["bash", "./ds.sh"])
		print("\n\n\n\n\n")



	elif choice == 6:

		#try clause for tcpdump quit
		try:

			subprocess.run(["bash", "./df.sh"])

		except KeyboardInterrupt:

			pass

		print("\n\n\n\n\n")		



	else:
		print("\n\n\n\n\n")



	#offer another run
	updown = input("Would you like to run another script (y/n): ")

	if updown == 'y' or updown == 'Y':

		continue
	
	else:

		#end menu
		break