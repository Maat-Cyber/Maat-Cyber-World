# Takeover Walkthrough
<br/>

## Intro
Welcome to the Takeover challenge Walkthrough from TryHackMe, here is the link to the [room](https://tryhackme.com/r/room/takeover).
This is an easy level room, created with the goal to practice subdomain enumeration.

To interact with the machine connect via OpenVPN or use the AttackBox

Whenever you feel ready press "Start Machine"

<br/>
<br/>

## The Story
The CEO of a futuristic space company called Futurevera asks us for help as some blackhat hackers are asking them a ransom, threatening them to takeover their infrastructure.
We have to find out which assets are vulnerable and are the probable targets of the hackers.
We also know that the company has a website at  https://futurevera.thm

Lets begin!

<br/>
<br/>

## The Challenge
As first thing we have to add the domain to our hosts file:
```bash
sudo -- sh -c "echo 'MACHINE-IP  futurevera.thm' >> /etc/hosts"
```

Now that we have set that up we can start enumerating.
Let's do a quick nmap scan 
```bash 
nmap -sV MACHINE-IP
```
It finds 3 open ports
```
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http     Apache httpd 2.4.41 ((Ubuntu))
443/tcp open  ssl/http Apache httpd 2.4.41 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Now we can look for subdomains:
```bash
gobuster vhost -u http://futurevera.thm -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 50 --append-domain --no-tls-validation
```

It finds "portal", "payroll" and "support", let's add this to the hosts file near the previous domain
```bash
nano /etc/hosts
```
now add them like this: `portal.futurevera.thm` in the same line. 

Exploring the first 2 subdomains nothing interesting happens, but looking at the third domain we can find an hidden gem.
In fact inspecting the certificate of the "support" subdomain we can notice there is another subdomain right there: `secrethelpdesk934752.support.futurevera.thm`.

We can add it to the hosts file as the other ones and navigate to it.

I have noticed that if we try to reach it using HTTPS it will just show the same website as the others, but if we go to it using HTTP we get the flag printed in the error screen.

<br/>
<br/>

Congratulations you have completed the Takeover room, hope you had fun and learned something new; in my case i wasted some time at the end as i was using a browser with enforced HTTPS settings on every request, this way i was never getting the flag.
After a bit i decided to change to a default setting browser and instantly got it, my takeaway from this experience is that when testing stuffs always remember to use the most neutral environment possible.

Thanks for following along; 

See you in the next CTF 😊
