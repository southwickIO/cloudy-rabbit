#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: main.py                                                               #
#                                                                             #
# VERSION: 20230401                                                           #
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


print('''   ________                __         ____        __    __    _ __ 
  / ____/ /___  __  ______/ /_  __   / __ \____ _/ /_  / /_  (_) /_
 / /   / / __ \/ / / / __  / / / /  / /_/ / __ `/ __ \/ __ \/ / __/
/ /___/ / /_/ / /_/ / /_/ / /_/ /  / _, _/ /_/ / /_/ / /_/ / / /_  
\____/_/\____/\__,_/\__,_/\__, /  /_/ |_|\__,_/_.___/_.___/_/\__/  
                         /____/                                    

author: @southwickio\n''')



while True:
    print("Select an option:")
    print("1. Option 1")
    print("2. Option 2")
    print("3. Option 3")
    choice = input("Enter your choice (1-3): ")

    try:
        choice = int(choice)
        result = menu(choice)
        print(result)
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
match subject:
    case <pattern_1>:
        <action_1>
    case <pattern_2>:
        <action_2>
    case <pattern_3>:
        <action_3>
    case _:
        <action_wildcard>