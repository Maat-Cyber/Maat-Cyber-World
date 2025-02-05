# Boogeyman 2 Walkthrough
<br/>

## Intro
Welcome to the second of the 3 series of Bogeyman challenges, here is the link to the [room](https://tryhackme.com/r/room/boogeyman1) on TryHackMe.
This time we are gonna start again from a phishing email and then move to the anlaysis of a Windows memory dump to uncover the tracks left behind by the malicous actor,

To solve this challenge we will use:
- *Volatility*
- *Olevba*

Whenever you feel ready press "Start Machine" and in a couple of minute the Ubuntu machine should be available in split-view.

Let's begin!

### The Story
Maxine, a Human Resource Specialist working for Quick Logistics LLC, received an application from one of the open positions in the company. Unbeknownst to her, the attached resume was malicious and compromised her workstation.

The security team was able to flag some suspicious commands executed on the workstation of Maxine, which prompted the investigation. Given this, you are tasked to analyse and assess the impact of the compromise.

<br/>
<br/>

## The Challenge
For the investigation, we will be analyzing with the following artefacts:
- Copy of the phishing email.
- Memory dump of the victim's workstation.

Both located at `/home/ubuntu/Desktop/Artefacts`.

### Email Analysis
We can start by reading the phishing email and analyzing headers file on the previous challenge:
**NOTE**: if you are using the provided machine i suggest to set "unlimited scrolls" in the terminal settings, as the email content is quite long.
```bash
cat Resume\ -\ Application\ for\ Junior\ IT\ Analyst\ Role.eml 
```

We can find the sender:
```bash
cat Resume\ -\ Application\ for\ Junior\ IT\ Analyst\ Role.eml | grep "From:"
```
--> REDACTED

The victim:
```bash
cat Resume\ -\ Application\ for\ Junior\ IT\ Analyst\ Role.eml | grep "To:"
```
--> REDACTED

As we could image by the consistent output containing base 64 data, the phishing email contains an attachment, we can quikly get the name:
```bash
cat Resume\ -\ Application\ for\ Junior\ IT\ Analyst\ Role.eml | grep "attachment"
```
--> REDACTED

Since we have the base 64 data we can extract that encoded data and reconstruct the original attachment file:
```bash
grep -A 1125 "base64" 'Resume - Application for Junior IT Analyst Role.eml' | tail -n +2 | base64 -di >  Resume_WesleyTaylor.doc
```
(you can find the block size in line by running the `nl` command which will put a number for each line, then a simple subtraction give you this)

Now we can get the attachment file md5 hash, can be handy if we want to check on VirusTotal or just for identify the file in a report:
```bash
md5sum Resume_WesleyTaylor.doc
```
--> REDACTED

Next, we know that this file contains a macro, when executed it downloads the second stage, we can find the contacted  URL:
```
strings  Resume_WesleyTaylor.doc | grep -A http
```
--> REDACTED

From here we can also see that the REDACTED then executed the `C:\ProgramData\update.js` file.

Well, looks like we got enough info from the email for now, let's now move on investigating the memory dump.

<br/>

### Memory Analysis
For this job we will use *Volatility* with the file `WKSTN-2961.raw`.
We can get some system info:
```bash
vol -f WKSTN-2961.raw windows.info
```

As we could imagine the dump is of a Windows 10 system.

Now let's get some more information about the process that started the payload:
```bash
vol -f WKSTN-2961.raw windows.pslist | grep -A 1 -B 1 "wscript.exe"
```

We can see the process PID is: REDACTED, now we can check the parent PID: REDACTED.

A connection with a C2 server was established, let's find the process used by checking again with `pstree` if there are any intersting relationships with the process used to execute the payload before:
```bash
vol -f WKSTN-2961.raw windows.pstree | grep -A 2 -B 2 "wscript.exe"
```
The process is `updater.exe` with PID: REDACTED.

We can see the file location by checking at the cmd history and filtering for it:
```bash
vol -f WKSTN-2961.raw windows.cmdline | grep "updater.exe"
```
--> REDACTED

Another thing to investigate is the  C2 server IP address, this can be useful to add it in the firewall blocklist:
```bash
vol -f WKSTN-2961.raw windows.netscan | grep "updater.exe"
```
--> REDACTED

Coming to the end we are now asked the full path of the phishing email attachment, i have tried with the `filescan` plugin but got no results, so i went back using the `cmdline` one:
```bash
vol -f WKSTN-2961.raw windows.cmdline | grep "Resume_WesleyTaylor"
```
--> REDACTED

Finally the attacker implanted a backdoor in the system to grant himself later access, to achieve persistence on the target he exploited a scheduled task, let's check that out:
```bash
strings WKSTN-2961.raw | grep "schtasks"
```
--> REDACTED

Running that command the attacker successfully established persistence using listener http stored in HKCU:\Software\Microsoft\Windows\CurrentVersion\debug with Updater daily trigger at 09:00.

<br/>
<br/>

Congratulations you have successfully investigated the phishing message and the uncovered the track of the actor on the victim system, i hope you had fun completing the machine and following along.

Catch you again in the next challege 😊
