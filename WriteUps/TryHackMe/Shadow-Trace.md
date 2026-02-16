# Shadow Trace Walkthrough

## Intro
Welcome to the Shadow Trace challenge, here is the link to the [room](https://tryhackme.com/room/shadowtrace) on TryHackMe.
This challenge is divided into 2 parts, in the first one we will have to investigate a Windows executable and answer 6 questions, while in the second one we will have to analyze 2 alerts and answers to the related 3 questions.

Whenever you feel ready press on "Start Machine" and the system will spawn in split-view in your browser.

Let's begin!

<br/>
<br/>

## The Challenge

### File Analysis
We get this initial instructions:
```
Analyse the binary located C:\Users\DFIRUser\Desktop\windows-update.exe in the attached machine, answer the questions below. 

Start the lab by clicking the Start Machine button. It will take around 2 minutes to load properly. The VM will be accessible on the right side of the split screen.

You can find several tools installed in the machine that can help you with any kind of analysis under C:\Users\DFIRUser\DFIR Tools
```
<br>

1. **What is the architecture of the binary file windows-update.exe?**
	Import the executable in PeStudio, the info is in the first window.
	--> REDACTED
<br>

2. **What is the hash (sha-256) of the file windows-update.exe?**
	Still in the same window as the previous question.
	--> REDACTED
<br>

3. **Identify the URL within the file to use it as an IOC**
	This one can be quickly done via CLI, open PS and use `strings`:
```powershell
strings .\windows-update.exe | findstr http
```
--> REDACTED
<br>

4. **With the URL identified, can you spot a domain that can be used as an IOC?**
	Now that we know the domain name from the previous question we can filter for strings containing it:
```powershell
strings .\windows-update.exe | findstr tryhatme
```
--> REDACTED
<br>

5. **Input the decoded flag from the suspicious domain**
	The previous command gives also an encoded base64 string `VEhNe3lvdV9nMHRfc29tZV9JT0NzX..REDACTED` decoding it we get the flag.
--> REDACTED
<br>

6. **What library related to socket communication is loaded by the binary?**
	We can go back in PeStudio, click on `libraries` and spot the one related to Windows Socket.
--> REDACTED
<br>

And we are done with the first part of the investigation.
Now we can shut down the machine and move to the next section.

<br/>

### Alert Analysis
For this second part we need to click on "View Site" on the top right and again we will have this web-app in split-view in the browser to interact with and answer the 3 questions.

1. **Can you identify the malicious URL from the trigger by the process powershell.exe?**
	In the first alert we can see that a base64 strings gets decoded: `aHR0cHM6Ly90cnloYXRtZS5jb20vZGV2L21haW4uZXhl`, from that a file gets downloaded and executed, let's decode it ourselves.
--> REDACTED
<br>

2. **Can you identify the malicious URL from the alert triggered by chrome.exe?**
	Similarly in this second alert we see a `fetch` and an obfuscated strings with `charcode`. Let's copy that `104,116,116,112,115,58,47,47,114,101,97,108,108,121,115,101,99,117,114,101,117,112,100,97,116,101,46,116,114,121,104,97,116,109,101,46,99,111,109,47,117,112,100,97,116,101,46,101,120,101` and go to CyberChef to decode it.
	**Hint**: choose the receipe "from decimal"
--> REDACTED 
<br>

3. **What's the name of the file saved in the alert triggered by chrome.exe?**
	Well for this one simply read the filename in the alert.
	--> REDACTED

<br/>
<br/>

Congratulations you have successfully found all the relevant Window's artifacts and uncovered the attacker's actions.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
