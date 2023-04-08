#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: da.py                                                                 #
#                                                                             #
# VERSION: 20230408                                                           #
#                                                                             #
# SYNOPSIS: Check for Apache ServerSignature/ServerTokens on remote server    #
#                                                                             #
# DESCRIPTION: This script checks the remote server to see if it is an Apache #
#              server. If it is, it checks for the "ServerSignature" and      #
#              "ServerTokens" headers/directives. The "ServerSignature"       #
#              directive controls whether the server includes a footer line   #
#              containing the server version number and other information in  #
#              error messages and directory listings. The "ServerTokens"      #
#              directive controls the level of detail in the server response  #
#              headers. A network defender can raise the sensitivity higher   #
#              than the default to reduce the attack surface. This script     #
#              checks if the network defender did that.                       #
#                                                                             #
# INPUT: Runtime user input                                                   #
#                                                                             #
# OUTPUT: STDOUT                                                              #
#                                                                             #
# PRE-RUNTIME NOTES: None.                                                    #
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



#get URL from user
url = input("\n\n\nEnter a URL (include http://): ")



#get response from remote server
res = requests.head(url)



#check if Apache server
if "Apache" in res.headers.get("Server"):

    print("\n\n\nThis is an Apache server. Checking for \"ServerSignature\" \
and \"ServerTokens\"")



    #check for Server-Tokens level
    servertokens = res.headers.get("Server-Tokens")

    if servertokens:

        print("\n\n\nServerTokens is set to: " + servertokens)



    else:

        print("\n\n\nServerTokens does not seem to be set")



else:

    print("\n\n\nThe server does not seem to be an Apache server")