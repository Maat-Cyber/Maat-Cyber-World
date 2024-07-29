# Monday Monitor Walkthrough
<br/>

## Intro
Welcome to the Monday Monitor challenge from TryHackMe, here is the link to the [page](https://tryhackme.com/r/room/mondaymonitor).
In this room we are gonna practice with some investigation in Windows using Wazu to check the logs; we also have to answer to 7 questions in order to complete the task.

### The Story
Here is the provided story about the challenge:
"Swiftspend Finance, the coolest fintech company in town, is on a mission to level up its cyber security game to keep those digital adversaries at bay and ensure their customers stay safe and sound.

Led by the tech-savvy Senior Security Engineer John Sterling, Swiftspend's latest project is about beefing up their endpoint monitoring using Wazuh and Sysmon. They've been running some tests to see how well their cyber guardians can sniff out trouble. And guess what? You're the cyber sleuth they've called in to crack the code!

The tests were run on Apr 29, 2024, between 12:00:00 and 20:00:00. As you dive into the logs, you'll look for any suspicious process shenanigans or weird network connections, you name it! Your mission? Unravel the mysteries within the logs and dish out some epic insights to fine-tune Swiftspend's defences."
<br/>

Whenever you feel ready press "Start Machine" and connect via OpenVPN or AttackBox.

<br/>
<br/>

## The Challenge
The first thing we have to do is to navigate to the provided link in our browser (`https://10-10-241-141.p.thmlabs.com/`) and login with the credentials `admin:Mond*yM0nit0r7`.
Once inside Wazu navigate to the security module and use the query `Monday_Monitor` to access the logs we need to work on.

Everything is ready, we can start our investigation!

1. **Initial access was established using a downloaded file. What is the file name saved on the host?**
   We are looking for a downloaded file so we can search for a keyword like `http` and looking at the logs we can see the use of the *curl* tool to download a phishing attachment on the machine and then rename it to look less suspicious.
   
<br/>

2. **What is the full command run to create a scheduled task?**
   In Windows the binary that is taking care of scheduling tasks is `schtasks.exe` so we can insert this keyword in the search bar and look for events.
   
<br/>

3. **What time is the scheduled task meant to run?**
   we can notice the task is meant to run daily at a specific time, which is specified at the end of the previous found command.
   
<br/>

4. **What was encoded?**
   Still looking at the command we can see there is a string block of encoded data in base64, we can use an online decoder or a linux binary to find out the original message.
   
<br/>

5. **What password was set for the new user account?**
   To answer this i know that to change the password for a user we would use the command `net user`, so i searched up for `net.exe` and after looking at some logs i found the new psw.
   Another option was to search for the command `net user`, but we would get a long list, so after checking a couple we can understand that we are inside `net1`, we can now change our search term to `net1 user` and quickly find the answer.
   
<br/>

6. **What is the name of the .exe that was used to dump credentials?**
   A commonly used utility for this type of job in Windows is `mimikatz`, so i searched for that and found this .exe :
   
<br/>

7. **Data was exfiltrated from the host. What was the flag that was part of the data?**
   Well this one is pretty easy, all flgs on this platform start with `THM`, search for that, there is only 1 entry

<br/>
<br/>

Congratulations you have successfully found all the information and explored Wazu's capabilities.

Catch you in the next CTF 😃
