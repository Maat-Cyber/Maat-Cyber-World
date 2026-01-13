# Mac Hunt Walkthrough
<br/>

## Intro
Welcome to the Mac Hunt room, [here](https://tryhackme.com/room/machunt) is the link to it on TryHackMe.
In this challenge we are tasked to perform a compromise assessment on a MacOS host and identify the attack footprints, once we have gathered all the information we will have to answer a set of 9 questions about the incident.

### Scenario
Jake had gained some good knowledge and skills in the game development field. So, he decided to enter the industry through a decent job and upgrade his finances. Little did he know that there were many fake recruiters in search of people looking for jobs. These fake recruiters lure the victim through attractive jobs to achieve their objectives, often to compromise the victim's machines and use them for malicious purposes. Having conventionally overlooked cyber security, Jake fell prey to such an attack. A well-crafted phishing attack with a promising job offer compromised his Mac machine.


**Note:** Before you begin analyzing the case, mount the image present at `/home/ubuntu/Jack_Mac.img` to `/home/ubuntu/mac`. To mount the image, you can use the command: 
```zsh
sudo apfs-fuse -v 4 /home/ubuntu/Jack_Mac.img /home/ubuntu/mac
```
Then, switch to the root user with `sudo su` to analyze the mounted image.

<br/>

Whenever you feel ready start the lab by clicking the `Start Machine`, the VM will be accessible on the right side of the split screen.
Let's begin!

<br/>
<br/>

## The Challenge
This time we are investigating a MacOS system from it's image file from a Linux system. This means we will need to mount the image to access the File-System structure (you should have already done it with the command above), which mean that the Mac's relative root is mapped at our system `/home/ubuntu/mac/root`.

To investigate the artifacts we will use the Linux's version of *plutil* -> `plistutil`, which is already installed, to view some `.plist` files, additionally we will need *sqlitebrowser* for databases files + `cat` for some text human-readable files.

### Questions
1. What is the name of the most recently accessed folder by the user?
```zsh
cd /home/ubuntu/mac/root/Users/jake/Library/Preferences
plistutil -p com.apple.finder.plist
```
--> REDACTED

2. Which social platform did the attacker use to deliver the document?
	Checking `/home/ubuntu/mac/root/Applications` we can see Safari, let's check its history
```zsh
cd /home/ubuntu/mac/root/Users/jake/Library/Safari
sqlitebrowser History.db
```
Now view the `history_items` table and find the answer:
--> REDACTED

3. What link did the attacker craft for the victim to download the MeetMeLive application?
```zsh
cd /home/ubuntu/mac/root/Users/jake/Library/Safari/
plistutil -p Downloads.plist
```
--> REDACTED

4. Which network did Jake connect to after reading the instructions in the PDF?
	First let's view inside the downloaded PDF, we can open it, is in the user downloads direcotry, we can see it suggests to use it's hotspot. 
	Now let's check WiFi connections:
```zsh
cd /home/ubuntu/mac/root
plistutil -p  Library/Preferences/com.apple.wifi.known-networks.plist
```
--> REDACTED

5. What was the  IP address assigned to Jake’s system?
```zsh
cd /home/ubuntu/mac/root
cat private/var/db/dhcpclient/leases/en0.plist
```
--> REDACTED

6. When did the application get installed into the system? (YYYY-MM-DD HH:MM:SS)
```zsh
cd /home/ubuntu/mac/root
plistutil -p Library/Receipts/InstallHistory.plist
```
--> REDACTED

7. What is the human-friendly name for the permission the user explicitly granted for the application?
```zsh
cd /home/ubuntu/mac/root/Library/Application Support/com.apple.TCC
sqlitebrowser TCC.db
```
Here we see "kTCCServiceSystemPolicyAllFiles" which translates to:
--> REDACTED

8. Which feature of the OS did the attacker use to run their application at startup persistently?
	We can search for applications setted-up to auto-start:
```zsh
cd /home/ubuntu/mac/root/Users/jake/Library/LaunchAgents
ls -la
```
Here we find the culprit, this means that our guess was right:
--> REDACTED


9. What was the URL to which the application was exfiltrating data?
	Let's now view the content of the script we found in the previous question:
```zsh
cat MeetMeLive.sh
```
--> REDACTED

<br/>
<br/>

Congratulations you have successfully completed the investigation on this MacOS system and found all the activities of the user by practicing with 'plistutils' and 'cat'.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
