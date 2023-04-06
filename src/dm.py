#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: dm.py                                                                 #
#                                                                             #
# VERSION: 20230406                                                           #
#                                                                             #
# SYNOPSIS: Check for mod_headers on remote Apache Server                     #
#                                                                             #
# DESCRIPTION: This script checks a remote server to see if it is an Apache   # 
#              Server. If so, a check is done for mod_headers. Apache         #
#              mod_headers is a module for the Apache web server that allows  #
#              you to modify HTTP request and response headers. This allows a #
#              network defender to obfuscate banners if wanted.               #
#              If a server is running Apache, the Apache custom X-Mod-Modules #
#              header is checked if present. The X-Mod-Modules header is      #
#              added by the mod_ssl module in Apache, and it lists all the    #
#              loaded modules that were compiled with the                     #
#              AP_MODULE_DECLARE_DATA macro. Since mod_headers is one of the  #
#              Apache modules that uses this macro, it should be included in  #
#              the X-Mod-Modules header when it's loaded. The X-Mod-Modules   #
#              header lists all loaded modules that were compiled with the    #
#              AP_MODULE_DECLARE_DATA macro, regardless of whether they were  #
#              actually used to handle a request. This header is intended for #
#              use by external processes that need to know what modules are   #
#              loaded in the server.                                          #
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



#request IP address
address = input("\n\n\nEnter the URL to check (don't include http://): ")



#check if Apache server
res = requests.get(f"http://{address}")

if res.status_code != 200 or "Apache" not in res.headers.get("Server", ""):

    print("\n\n\nApache is not running on the remote server")

else:

    print("\n\n\nApache is running on the remote server")



    #debug
    #print('\n\n\n')
    #print(res.headers)
    #print('\n\n\n')



    #set up request for mod_headers
    headers = {"Host": "example.com", "User-Agent": "Mozilla/5.0"}

    res = requests.get(f"http://{address}/", headers=headers)
    


    #check for mod_headers
    if "headers_module" not in res.headers.get("X-Mod-Modules", ""):
    
        print("\n\n\nIt doesn't seem that mod_headers is enabled on the remote \
server")
    
    else:
    
        print("\n\n\nmod_headers is enabled on the remote server")
