# Room 404 Walkthrough

## Intro
Welcome to the Room 404 challenge, here is the link to the [room](https://tryhackme.com/room/hh-room404-804573bf) on TryHackMe.

This is an easy one, part of the Hacker Holidays 2026 CTF event.

*"He booked the quiet room. It's not on the floor plan, not in the brochure, not on any door. But port 8080 is wide open, and the rooms it never lists are the ones worth finding."*

Whenever you feel ready click on "Start Machine" and connect using OpenVPN or via the AttackBox.

Let's begin!

<br/>
<br/>


## The Challenge
In the room info we are told that `http://MACHINE_IP:8080` has been left accessible, we also get a hint about a repo.

Let's confirm that there is actually a git repo there, we do a quick directory enumeration with *gobuster*:
```bash
 gobuster dir -u http://10.82.135.121:8080  -w /usr/share/SecLists/Discovery/Web-Content/common.txt
```

We can instantly see a `.git` dir, we can pause the scan and move on.
```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.82.135.121:8080
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/SecLists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.git                 (Status: 200) [Size: 437]
/.git/HEAD            (Status: 200) [Size: 21]
/.git/config          (Status: 200) [Size: 92]
/.git/index           (Status: 200) [Size: 289]
/.git/logs/           (Status: 200) [Size: 165]
```

Now is time to download that repo, we will use *git-dumper*, if you do not have it here are the commands to install it:
```bash
python3 -m venv venv; source venv/bin/activate
pip3 install git-dumper
```

Now download the repo:
```
git-dumper http://10.82.135.121:8080/ ./
```

At this point we want to find the flag, we know all flags on TryHackMe  are of the format: "THM{}".

We can user *ripgrep*, a better and faster *grep* written in rust to recursively search for that:
```bash
rg THM
```

And in the output there is already the flag:
```
README.md
6:Staging flag (remove before launch): THM{REDACTED}
```

If you prefer using *grep* do:
```bash
grep -rn "THM"
```

-->  THM{REDACTED}

<br/>
<br/>

Congratulations, you have successfully found the flag in the git repo!

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
