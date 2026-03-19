# Invite Only Walkthrough

## Intro
Welcome to the Invite Only challenge, here is the link to the [room](https://tryhackme.com/room/exfilnode) on TryHackMe.
In this challenge we will have to analyze artifacts to answer a set of 10 questions.

### Story
You are an SOC analyst on the SOC team at Managed Server Provider TrySecureMe. Today, you are supporting an L3 analyst in investigating flagged IPs, hashes, URLs, or domains as part of IR activities. One of the L1 analysts flagged two suspicious findings early in the morning and escalated them. Your task is to analyse these findings further and distil the information into usable threat intelligence.

```
Flagged IP: **101[.]99[.]76[.]120**  
Flagged SHA256 hash: **5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f**
```

We recently purchased a new threat intelligence search application called TryDetectThis2.0. You can use this application to gather information on the indicators above.

<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge

1. **What is the name of the file identified with the flagged SHA256 hash?** <br>
	Start the "TryDetectThis2.0" executable on the desktop and paste inside the provided hash. <br>
	--> REDACTED
<br>

2. **What is the file type associated with the flagged SHA256 hash?** <br>
	Still on the same result page of the previous question we can see this info. <br>
	--> REDACTED
<br>

3. **What are the execution parents of the flagged hash? List the names chronologically, using a comma as a separator. Note down the hashes for later use.** <br>
	So i was curious to see if that was a special tool for the challenge that gives custom answers for this. But trying to copy the hash to VT i got the same info, so anyway we can find this 2 in the "Relations" tab, there is a specific section called "Execution Parents" <br>
--> REDACTED
<br>

4. **What is the name of the file being dropped? Note down the hash value for later use.** <br>
	Now simply go in the section called "Dropped Files", there is only 1 entry. <br>
--> REDACTED
<br>

5. **Research the second hash in question 3 and list the four malicious dropped files in the order they appear (from up to down), separated by commas.** <br>
	In Q3 we have found 2 things, the second one is an executable, get its hash and submit it to VT or i guess also the Desktop executable. Then go in the "Relations" tab, under the "Dropped Files" section, select the relevant (malicious) ones. <br>
--> REDACTED
<br>

6. **Analyse the files related to the flagged IP. What is the malware family that links these files?** <br>
	In the intro of the room we have seen an IP, let's send this guy to VT as well, the answer can be found in the "comments" section. <br>
--> REDACTED
<br>

8. **What is the title of the original report where these flagged indicators are mentioned? Use Google to find the report.** <br>
	To be fair we do not need to Google it, the guy in the comment section on VT already included this report but you are free to.<br> 
--> REDACTED
<br>

9. **Which tool did the attackers use to steal cookies from the Google Chrome browser?** <br>
	For this question we need to open and read the report, luckily is well structured, with key points on the top, this way you do not need to read it all if you do not want to, you can still answer the question.<br> 
--> REDACTED
<br>

10. **Which phishing technique did the attackers use? Use the report to answer the question.** <br>
	Same as previous question hint. <br>
--> REDACTED
<br>

11. **What is the name of the platform that was used to redirect a user to malicious servers?** <br>
	Again, still in the key points of the report. <br>
--> REDACTED

<br/>
<br/>

Congratulations you have successfully found all the relevant info about the hash and the IP address that triggered and alert.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
