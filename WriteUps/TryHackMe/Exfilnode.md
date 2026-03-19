# ExfilNode Walkthrough

## Intro
Welcome to the ExfilNode challenge, here is the link to the [room](https://tryhackme.com/room/exfilnode) on TryHackMe.
In this challenge we will have to analyze files from Linux disk image to answer a set of 14 questions.

### Scenario
The analysis of Liam's company-provided Windows workstation in the DiskFiltration room revealed major evidence of his involvement in the TECH THM's data exfiltration. However, he could argue that he was framed as he did not own the workstation. So, to uncover the whole truth and gather all the possible undeniable evidence, the investigators turned their attention to Liam's personal workstation (Linux machine), which was suspected to have played a key role in handling the exfiltrated data.

As this was Liam's personal workstation, he had full control over covering his tracks more effectively. But was he careful enough? It seems like the investigators not only revealed more about the external entity Liam worked with but also exposed a betrayal: Liam was double-crossed.

Liam's personal workstation's disk is mounted at `/mnt/liam_disk`, and the disk image is available at `/home/ubuntu`.
**Note:** If you get the error `grep: /mnt/liam_disk/var/log/auth.log: binary file matches` with any log file, use `grep -a` which will treat the file as text. An example is given below:
```bash
grep -i -a "string-pattern" /mnt/liam_disk/var/log/auth.log
```

Additionally, you can utilize the Autopsy tool to assist with the analysis. However, Autopsy is optional. All the questions in this room can be answered by running commands on the mounted disk.

To use Autopsy, open a terminal and navigate to `/home/ubuntu/autopsy/autopsy-4.21.0/bin` and execute the command `./autopsy --nosplash` to execute it. The GUI of the tool will open. Now, select `Open Recent Case` from here and open the recent case named `Liam_Personal_Workstation` in which we have already imported the disk image.

<br/>

Whenever you feel ready press on "Start Machine" and the machine will appear in your browser in "split-view".
Let's begin!

<br/>
<br/>

## The Challenge
Let's navigate to the directory with the disk image:
```bash
cd /mnt/liam_disk
```


1. **When did Liam last logged into the system? (Format: YYYY-MM-DD HH:MM:SS)** <br>
	We can find the timestamp in the auth.log, we can search for a keyword such as "session opened" 
```bash
grep -i -a "session opened" /mnt/liam_disk/var/log/auth.log | grep liam
```
--> REDACTED
<br>

2. **What was the timezone of Liam’s device?**
	On Linux systems there is a file whose role is to store this info only.
```bash
cat /mnt/liam_disk/etc/timezone 
```
--> REDACTED
<br>

3. **What is the serial number of the USB that was inserted by Liam?** <br>
	We can find this information registered in Syslog, with some grepping you should find it quickly.
```
grep -i -a "serial" /mnt/liam_disk/var/log/syslog
```
--> REDACTED
<br>

4. **When was the USB connected to the system? (Format: YYYY-MM-DD HH:MM:SS)** <br>
	We have this info already in the result from the previous command, simply read the beginning of the line of the serial number log.
	--> REDACTED
 <br>
 
5. **What command was executed when Liam ran 'transferfiles'?** <br>
	We can navigate in the user home directory and check for aliases in the `.bashrc` file.
```bash
cat /mnt/liam_disk/home/liam/.bashrc
```
--> REDACTED
<br>

6. **What command did Liam execute to transfer the exfiltrated files to an external server?** <br>
	Since we have found the user was using Bash as shell, we can find the history of the commands ran by the user in the `~/.bash_history` file.
```bash
cat /mnt/liam_disk/home/liam/.bash_history
```
--> REDACTED
<br>

7. **What is the IP address of the domain to which Liam transferred the files to?** <br>
	In the previous uncovered command the user transferred the data to a domain, since it ends with `.thm` we know is probably not a real one resolved by a normal DNS server. In those scenarios usually we manually add the IP address and the domain in the hosts file, as on Linux is the first thing that gets checked to resolve the name.
```bash
cat /mnt/liam_disk/etc/hosts
```
--> REDACTED
<br>

8. **Which directory was the user in when they created the file 'mth'?** <br>
	Again we can see the commands ran in the Bash history file and get some context.
	--> REDACTED
<br>

9. **Remember Henry, the external entity helping Liam during the exfiltration? What was the amount in USD that Henry had to give Liam for this exfiltration task?** <br>
	We have just seen the "mth" file being mentioned, it is worth reading its content.
	--> REDACTED
<br>

10. **When was the USB disconnected by Liam? (Format: YYYY-MM-DD HH:MM:SS)** <br>
	This is another of the information that gets stored in the system log file, grepping for a keyword such as "usb" or "disconnect" will help finding it faster.
```bash
grep -i -a "usb" /mnt/liam_disk/var/log/syslog | grep disconnect
```
--> REDACTED
<br>

11. **There is a .hidden/ folder that Liam listed the contents of in his commands. What is the full path of this directory?** <br>
	We have found this directory when navigating the user's bash history, let's navigate to his home and run `find` from there.
```bash
find ./ -type d -name ".hidden"
```
--> REDACTED
<br>

12. **Which files are likely timstomped in this .hidden/ directory (answer in alphabetical order, ascending, separated by a comma. e.g example1.txt,example2.txt)** <br>
	Now we can navigate to the directory we were searching in the previous question and use the `stat` command to get more info, we run it for every file and interpret the results (2 of them really stand out).
	We can run all in one go with this simple one liner:
```bash
for file in *; do stat "$file"; done
```
--> REDACTED
<br>

13. **Liam thought the work was done, but the external entity had other plans. Which IP address was connected via SSH to Liam's machine a few hours after the exfiltration?** <br>
	Back to our log files, in the auths one we can search for "ssh" and quickly spot the address
```bash
grep -i -a "ssh" /mnt/liam_disk/var/log/auth.log
```
--> REDACTED
<br>

14. **Which cronjob did the external entity set up inside Liam’s machine?** <br>
	We can check some common locations such as `/etc/crontab`, `/etc/cron.d/*`, `/etc/cron.*` and `/var/spool/cron/crontabs`. In one of those you will find a file named  "liam" with the aswer.
--> REDACTED

<br/>
<br/>

Congratulations, you have successfully uncovered the artifacts left behind by Liam by analyzing the relevant files in the mounted Linux filesystem.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
