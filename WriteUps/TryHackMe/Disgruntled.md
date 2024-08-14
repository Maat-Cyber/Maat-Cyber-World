# Disgruntled
<br/>

## Intro
Welcome to the Disgruntled challenge, here is the link of the [room]() on TryHackMe.
In this CTF we are gonna be investigate a Linux system, to find the information we need about the event the logs will come in our help.

Whenever you feel ready press "start machine", it will open the target system in split-view, but if you prefer you can connect first with OpenVPN and then SSH into the machine:
```bash
ssh root@MACHINE_iP 
```
and insert "password" when prompted.

<br/>
<br/>

## The Challenge
Before starting we can download the attachment that contains a cheatsheet of the Linux Forensic room, this might be useful later.
Following the hint we can start investigate the privileged commands that were run. 

1. **The user installed a package on the machine using elevated privileges. According to the logs, what is the full COMMAND?**
```bash
cat /var/log/auth.log | grep install
```

<br/>


2. **What was the present working directory (PWD) when the previous command was run?**
   We can look at the previous command output and notice the current working directory at the time of the command execution.

<br/>

*"Keep going. Our disgruntled IT was supposed to only install a service on this computer, so look for commands that are unrelated to that."*

<br/>

3. **Which user was created after the package from the previous task was installed?**
   From that user home directory check the log of the runned commands:
```bash
cat .bash_history | grep user
```

<br/>

4. **A user was then later given sudo priveleges. When was the sudoers file updated? (Format: Month Day HH:MM:SS)**
```bash
cat /var/log/auth.log | grep visudo
```

<br/>

5. **A script file was opened using the "vi" text editor. What is the name of this file?**
   Same process as question 4

<br/>

*"That `bomb.sh` file is a huge red flag! While a file is already incriminating in itself, we still need to find out where it came from and what it contains. The problem is that the file does not exist anymore."*

<br/>

6. **What is the command used that created the file bomb.sh?**
   Go in the it-admin home directory and check the bash history file
```bash
cat /home/it-admin/.bash_history | grep bomb.sh
```

<br/>

7. **The file was renamed and moved to a different directory. What is the full path of this file now?**
   From the bash history file we can see the next command was /etc/crontab and then the bob file was removed, suspiciously there there is a new script added.
```bash
cat /etc/crontab
```

<br/>

8. **When was the file from the previous question last modified? (Format: Month Day HH:MM)**
```bash
stat /bin/os-update.sh
```

<br/>

9. **What is the name of the file that will get created when the file from the first question executes?**
We can read the content of the script file and locate the name of the output file.
```bash
cat /bin/os-update.sh 
```


<br/>

*"So we have a file and a motive. The question we now have is: how will this file be executed?*
*Surely, he wants it to execute at some point?"*

<br/>

10. **At what time will the malicious file trigger? (Format: HH:MM AM/PM)**
    Check the crontab file, from left to right the time is composed by: minutes, hours, day of month, months, day of week. 

<br/>

*"Thanks to you, we now have a good idea of what our disgruntled IT person was planning.
We know that he had downloaded a previously prepared script into the machine, which will delete all the files of the installed service if the user has not logged in to this machine in the last 30 days. It’s a textbook example of a  “logic bomb”, that’s for sure.
Look at you, second day on the job, and you’ve already solved 2 cases for me. Tell Sophie I told you to give you a raise."*

<br/>
<br/>

Congratulations you have successfully completed the investigation and uncovered the tracks of the malicious actor.

Catch you in the next CTF 😃 
