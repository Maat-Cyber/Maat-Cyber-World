# IronShade Walkthrough
<br/>

## Intro
Welcome to the IronShade room, [here](https://tryhackme.com/room/ironshade) is the link to it on TryHackMe.
In this challenge we are tasked to perform a compromise assessment on a Linux host and identify the attack footprints, once we have gathered all the information we will have to answer a set of 12 questions about the incident.
### Story
Based on the threat intel report received, an infamous hacking group, **IronShade**, has been observed targeting Linux servers across the region. Our team had set up a honeypot and exposed weak SSH and ports to get attacked by the APT group and understand their attack patterns. 

You are provided with one of the compromised Linux servers. Your task as a Security Analyst is to perform a thorough compromise assessment on the Linux server and identify the attack footprints. Some threat reports indicate that one indicator of their attack is creating a backdoor account for persistence.


Whenever you feel ready start the lab by clicking the `Start Machine`, the VM will be accessible on the right side of the split screen.
Let's begin!

<br/>
<br/>

## The Challenge
To solve this challenge my approach will be to use tools such as *osquery*, `ps`, `systemctl`, `apt` for some questions, since i found them installed. 
For the rest Linux is based on files so we will mostly `cat` some relevant ones and use `grep` to filter the results to help us locate the relevant info.

It appears that the compromised system is the same one as we are doing our investigation with, pretty much a live analysis.

### Questions
1. What is the Machine ID of the machine we are investigating?
```bash
cat /etc/machine-id
```
--> REDACTED

2. What backdoor user account was created on the server?
```bash
cat /etc/passwd |grep bash
```
--> REDACTED

3. What is the cronjob that was set up by the attacker for persistence?
```bash
sudo crontab -e
```
--> REDACTED

4. Examine the running processes on the machine. Can you identify the suspicious-looking hidden process from the backdoor account?
```bash
sudo ps aux | grep mirco
```
--> REDACTED

5. How many processes are found to be running from the backdoor account’s directory?
```bash
sudo ps aux | grep mirco
```
--> REDACTED

6. What is the name of the hidden file in memory from the root directory?
	Open `Osquery` as root:
```sql
SELECT * FROM file WHERE path = '/.hidden' OR path LIKE '/.%';
```
--> REDACTED

7. What suspicious services were installed on the server? Format is service a, service b in alphabetical order.
```bash
systemctl list-units --type=service
```
--> REDACTED

8. Examine the logs; when was the backdoor account created on this infected system?
```bash
sudo cat  /var/log/auth.log | grep -a -C 30  "microservice" | grep "add"
```
--> REDACTED

9. From which IP address were multiple SSH connections observed against the suspicious backdoor account?
```bash
sudo cat  /var/log/auth.log | grep -a -C 30  "microservice" | grep "Failed"
```
--> REDACTED

10. How many failed SSH login attempts were observed on the backdoor account?
```bash
sudo cat  /var/log/auth.log |  grep -aE 'PAM|pam' | grep -a "sshd" | grep "mir
```
--> REDACTED

11. Which malicious package was installed on the host?
```bash
sudo apt-mark showmanual
```
--> REDACTED

12. What is the secret code found in the metadata of the suspicious package?
```bash
sudo apt show pscanner
```
--> REDACTED

<br/>
<br/>

Congratulations you have successfully uncovered the artifacts left behind by the hackers and did a little practice with some basic Linux commands.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
