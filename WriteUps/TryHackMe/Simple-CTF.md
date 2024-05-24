# Simple CTF Walkthrough

## Intro
This is an easy level CTF provided by TryHackme, to check their room you can use this link https://tryhackme.com/room/easyctf <br>
To solve this challenge you will need some tools:
- nmap
- gobuster
- ssh

It is also required a basic knowledge about sql injections, linux commands and privilege escalation.​

Whenever you fell ready you can begin pressing START MACHINE;
To be able to interact with the machine, as THM explains you can either use their attack box or use your own kali linux machine by connecyting it via openVPN.

​The walktrought won't contain the answers, to not take away the fun, but a step by step tutorial to reach them, by following it you will just have to read the flag or he answers on your own machine.

Now that everything has been set let's start with the CTF.

<br/>
<br/>​

## The Challenge
we can start by following the questions as a path finding the answers to move on.

**How many services are running under port 1000?** <br/>​
To answer this question we will use probably the most common tool for this types of challenges that is NMAP.
Nmap will scan ports for us telling wich ones are open or closed, it can also gives us info about the services that are running on this ports and many more.

For this question we can use this command:
```bash
nmap -sV [YOUR ROOM IP] 
```

Press enter and wait that the scan is completed, we will find a bunch of open ports, write them down because they will be usefull later.

<br/>​​​

**What is running on the higher port?** <br/>​
Since we have run nmap with the -SV tag, the tool will provide us with the type and version of service running on the ports.
​
<br/>​

**WHAT TO DO NOW?** <br/>​
Now that we got a couple of information thanks to nmap we can start by visiting the machine website, since our port scan revealed that port 80 was open and an apache server is running.

To do so simply go on your browser, type: 
```
http://[YOUR MACHINE IP]
```

Once on the website we find the default Apache2 webpage that isn't very usefull for us, seems that there we can't find much more.

​<br/>​

It's time to use *GOBUSTER*, a special tool that will scan for hidden pages, directories and files for us.

You can run it with the following command:
```bash
gobuster dir -u http://[YOUR MACHINE IP]  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
``` 

After a minute or two it will give us this result:
/simple

This is an hidden page so lets visit it on our browser:
```
http://[YOUR MACHINE IP]/simple
```

We are now prompted to a new page with the title CMS MADE SIMPLE.

​<br/>​​

**What is the CVE you are using against the application?** <br/>​
Now that we have found our target, the CMS page, we can search in exploit db

Now there are many CVE we can chose from but only one is the correct answer, if we go again on out target website, at the end of the page we can find that it is version 2.2.8, so only one of this exploit will work, the SQL INJECTION, click on it and check the CVE number on the top to respond the question.

Those informations will also answer the next question about waht type of vulnerability is the application vulnerable.
​
<br/>​

### HOW TO EXPLOIT WITH THE SQL INJECTION
We have find out the vulnerability, now is time to exploit it.

Copy the code that you can found in the explotdb page and create a new python file with this command
```bash
nano exploit.py 
```
copy the code inside it, save and exit the file editor.

Now let's run the script:
```bash
python3 exploit.py -u http://[MACHINE IP]/simple -w [WORD LIST OF YOUR CHOICE]
``` 

Wait a little bit and on the screen we will see: username, password and an email.

We can now answer to the what is the password question.

<br/>​​

**Where can you login with the details obtained?** <br/>​
Now that we have the credentials we can use them, we can log into the website but wont be the correct answer and also once inside won't be very usefull to find the next flags.

But looking back at the nmap results we have found another interesting open port that can be used to remotely connect to the target machine, read the service name and answer the question.

<br/>​​

### User Flag
**What is the user flag?** <br/>​
To get our user flag first we need to be connected to the target machine, we can do so using this command
```bash
ssh USERNAME@[MACHINE IP] 
```

Press enter and when asked insert the password we have previously foud.

​
Once inside we can use the command:
```bash
ls
``` 
to list files and directories, we find one of interest --> user.txt

open it with:
```bash
cat user.txt 
```
read the flag inside it and answer the question

​<br/>​

**Is there any other user in the home directory? What’s its name?**
To find this answer we can simply go in the home directory, list the directories with LS and we see another name, that's the other user we have been asked about.

​<br/>​

​
### Privilege Escalation
**What can you leverage to spawn a privileged shell?**
It is time to do a bit of privilege escalation!

Run:
```bash
sudo -l 
```

with this command we will see what ptograms we can run, read the name and answer te question.

To take advantage of this binary go on the GTFObins webiste, insert it and we can see that a certain command will help us to get a privileged shell, so let's run:
```bash
-c ':!/bin/sh' 
```

once it open let's write
```
:!sh
``` 

​<br/>​

#### Root Flag
Well now we have a root shell, time to look around, let's go in the root home directory:
```bash
cd /root 
```

Now let's see what is inside:
```bash
ls 
```

We find a text file called root.txt, let's open it!
```bash
cat root.txt
```

And we have made it to the end, read the root flag and answe the last question.

​<br/>​
<br/>​

Hope you had fun doing and following this room.

If you want to see more CTFs Writeups explore the directory.

See you in the next challenge 😊
