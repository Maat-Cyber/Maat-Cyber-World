# Retracted Walkthrough
<br/>

## Intro
Welcome to another CTF, this time we are gonna solve the Retracted challenge from TryHackMe; here is the link to the [room](https://tryhackme.com/r/room/retracted).
In this challenge we are gonna be helping a co-worker having some problems after the installation of a program. From the few information we know it looks like the "program" was actually a ransomware and now we have all the data encrypted with the request to pay the ransom in bitcoin in order to have our data back.

We are gonna investigate the situation and try to see if we can remediate it, after every step we will also need to submit the answer to some questions about the new info we managed to gather about the matter.

Whenever you feel ready press "Start Machine" and connect via OpenVPN or use the AttackBox.

<br/>
<br/>

## The Challenge
Once the machine is ready we can connect via RDP, or either just use the split-view in our browser, it works OK.

| Field    | Value           |
| -------- | --------------- |
| Username | sophie          |
| Password | fluffy19601234! |
| IP       | 10.10.68.152    |

The challenge is composed by multiple sub-tasks, in each one we have to find some information and we will uncover step-by-step the full story of what happened.

<br/>

### The Message
"So, as soon as you finish logging in to the computer, you'll see a file on the desktop addressed to me."
"I have no idea why that message is there and what it means. Maybe you do?"

Let's give a look at the questions:

1. **What is the full path of the text file containing the "message"?** <br/>
   Once logged in we can see the user's desktop, on it there is a text file with the name Sophie

<br/>

2. **What program was used to create the text file?** <br/>
   This is easy guessable, considering we are investigating in windows, but let's open up the event viewer and search the date 8 jan 2024, this is the date of creation of the document, we can see it by opening the file's properties. Once in the Event Viewer let's check sysmon: Application and Service Logs > Microsoft > Windows > Sysmon > Operational. Here we can create a filter and insert the file name.
   --> ==REDACTED==

<br/>

3. **What is the time of execution of the process that created the text file? Timezone UTC (Format YYYY-MM-DD hh:mm:ss)** <br/>
   While in question 2 we found the program name we can also check the time of the process creation. (tip: you need the UTC time, cut out the values after the seconds)
   --> ==REDACTED==

<br/>

Nice now we know that in that date someone opened a text editor to leave Sophie the message "Check your Bitcoins."
Let's proceed 

<br/>
<br/>

### Something Wrong
"I swear something went wrong with my computer when I ran the installer. Suddenly, my files could not be opened, and the wallpaper changed, telling me to pay."
"Wait, are you telling me that the file I downloaded is a virus? But I downloaded it from Google!"

4. **What is the filename of this "installer"? (Including the file extension)** <br/>
   Still looking at the logs in Event Viewer we can look for "File Creation", looking inside the XML of the event we can see the name of the "installer" that has been downloaded.
   --> ==REDACTED==

<br/>

5. **What is the download location of this installer?** <br/>
   In the same event as the one above we can see the full path of the program, so we can just strip out the installer name and we have the location.
   --> ==REDACTED==

<br/>

6. **The installer encrypts files and then adds a file extension to the end of the file name. What is this file extension?** <br/>
   Still looking inside the event we can see a "new" extension appearing.
   --> ==REDACTED==

7. **The installer reached out to an IP. What is this IP?**  <br/>
   This time we are looking for a different event: "Network connection detected" aka ID: 3, we can also filter out for the date and for the installer name.
   --> ==REDACTED==

<br/>

Looks like the installer was not what it should have been and that it showed up to be a ransomware that contacted a malicious IP and encrypted files on the machine.
Moving on...

<br/>
<br/>

### Back to Normal
"So what happened to the virus? It does seem to be gone since all my files are back."

8. **The threat actor logged in via RDP right after the “installer” was downloaded. What is the source IP?** <br/> 
   Here we are still looking at network events, looking closely to the time of the download we can see a remote desktop session has been initiated by an IP.
   --> ==REDACTED==

<br/>

9. **This other person downloaded a file and ran it. When was this file run? Timezone UTC (Format YYYY-MM-DD hh:mm:ss)** <br/>
   A file to "revert" the current situation has been downloaded. We can look for a "process creation event" since the file was run, and search around the time we are investigating 
   --> ==REDACTED==

<br/>

A file decryptor has been downloaded on the machine.. why? has the ransom been payed?
Let's find out!

<br/>

### Doesn't Make Sense
"So you're telling me that someone accessed my computer and changed my files but later undid the changes?"  
"That doesn't make any sense. Why infect my machine and clean it afterwards?"
"Can you help me make sense of this?"
Arrange the following events in sequential order from 1 to 7, based on the timeline in which they occurred.

The right sequence is:
1. Sophie downloaded the malware and ran it.
2. The malware encrypted the files on the computer and showed a ransomware note.
3. Sophie ran out and reached out to you for help.
4. Someone else logged into Sophie's machine via RDP and started looking around.
5. The intruder downloaded a decryptor and decrypted all the files.
6. A note was created on the desktop telling Sophie to check her Bitcoin.
7. We arrive on the scene to investigate.

<br/>
<br/>

### Conclusion
"Adelle from Finance just called me. She says that someone just donated a huge amount of bitcoin to our charity's account!"
"Could this be our intruder? His malware accidentally infected our systems, found the mistake, and retracted all the changes?"
"Maybe he had a change of heart?"

<br/>
<br/>

You have correctly unfolded the situation and reconstructed the timeline of the incident.
Congratulations for the investigation!

Catch you in the next CTF 😃 
