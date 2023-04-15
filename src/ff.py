#!/usr/bin/env python3



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NAME: db.py                                                                 #
#                                                                             #
# VERSION: 20230415                                                           #
#                                                                             #
# SYNOPSIS: Check for hidden fields in forms and extracts their values        #
#                                                                             #
# DESCRIPTION: This script looks for hidden fields in forms from a user       #
#              specified domain. Hidden form fields are used in HTML          #
#              web forms to store data that should not be visible or edited   #
#              by users, but is needed by the server to process the form      #
#              submission. For example, a hidden form field may contain a     #
#              session token, a user ID, or other data that the server uses   #
#              to validate the user's identity or perform some other          #
#              function. A network defender may want to keep track of hidden  #
#              form fields to detect and prevent attacks that use these       #
#              fields to manipulate or bypass the intended form submission    #
#              process. Attackers may use hidden form fields to inject        #
#              malicious code, change the value of a field, or bypass         #
#              validation checks, among other things. By monitoring hidden    #
#              form fields, defenders can detect these attacks and take       #
#              appropriate actions to protect the system.                     #
#                                                                             #
# INPUT: User input                                                           #
#                                                                             #
# OUTPUT: STDOUT                                                              #
#                                                                             #
# PRE-RUNTIME NOTES: None                                                     #
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
from bs4 import BeautifulSoup



#get domain
target = input("\n\n\nEnter a domain: ")



#get forms
response = requests.get(f"http://{target}")
soup = BeautifulSoup(response.text, "html.parser")
forms = soup.find_all("form")



#print hidden fields
for form in forms:

    hiddenfields = form.find_all("input", type="hidden")



    if hiddenfields:

        if 'id' in form.attrs:

            print(f"\n\n\nHidden fields found in form {form['id']}:")



        else:

            print("\n\n\nHidden fields found in form without ID:")



        for field in hiddenfields:

            if 'name' in field.attrs:

                name = field['name']



            else:

                name = '<no name>'



            if 'value' in field.attrs:

                value = field['value']



            else:

                value = '<no value>'



            print(f"{name}: {value}")