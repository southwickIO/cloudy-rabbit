#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# NAME: fc.py                                                                 #
#                                                                             #
# VERSION: 20230321                                                           #
#                                                                             #
# SYNOPSIS: Fetch HTML comments from a user specified site.                   # 
#                                                                             #
#                                                                             #
# DESCRIPTION: This script fetches all HTML comments from a site specified by #
# the user and outputs to STDOUT and ./comments.txt.                          #
#                                                                             #
# INPUT: 1.) Runtime user input                                               #
#                                                                             #
# OUTPUT: 1.) STDOUT                                                          #
#         2.) ./comments.txt                                                  #
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



#import dependencies
import requests
from bs4 import BeautifulSoup, Comment



#program entry
while True:

    #get website URL
    url = input("Enter the website URL: ")

    #url condition check
    if "http://" in url:

        #fetch the website content using requests
        response = requests.get(url)

        #request condition check
        if response.status_code == 200:

            #parse the website content
            soup = BeautifulSoup(response.content, "html.parser")



            #grab all of the comments and add them in a list
            comments = soup.find_all(text=lambda text: isinstance(text, Comment))



            #output results to STDOUT and ./comments.txt
            with open("comments.txt", 'w') as f:

                #STDOUT headline
                print(f"\n{str.upper(url)} SOURCE COMMENTS")
                print(f"{'~' * len(url)}" + "~~~~~~~~~~~~~~~~\n")

                #write headline
                f.write(f"\n{str.upper(url)} SOURCE COMMENTS\n")
                f.write(f"{'~' * len(url)}" + "~~~~~~~~~~~~~~~~\n\n")

                #write comments
                for comment in comments:
                    
                    print(comment + '\n')

                    f.write(comment + "\n\n")



            #program exit
            break



        else:
            print(f"\nFailed to fetch the website content. Status code: {response.status_code}. Exiting.\n")
            break



    else:
        print("\nPlease use http:// when entering a site. Try again.\n")