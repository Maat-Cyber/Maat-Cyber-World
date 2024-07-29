# Friday Overtime
<br/>

## Intro
Welcome do the new Friday Overtime challenge from TryHackMe, here is the [link](https://tryhackme.com/r/room/fridayovertime) to it.
In this room we are analysts that have to solve a particular situation, we are also tasked to answer a set of 7 questions about it.

### Official Story
It's a Friday evening at PandaProbe Intelligence when a notification appears on your CTI platform. While most are already look
ing forward to the weekend, you realize you must pull overtime because SwiftSpend Finance has opened a new ticket, raising concerns about potential malware threats. The finance company, known for its meticulous security measures, stumbled upon something suspicious and wanted immediate expert analysis.

As the only remaining CTI Analyst on shift at PandaProbe Intelligence, you quickly took charge of the situation, realizing the gravity of a potential breach at a financial institution. The ticket contained multiple file attachments, presumed to be malware samples.

With a deep breath, a focused mind, and the longing desire to go home, you began the process of:

1. Downloading the malware samples provided in the ticket, ensuring they were contained in a secure environment.
2. Running the samples through preliminary automated malware analysis tools to get a quick overview.
3. Deep diving into a manual analysis, understanding the malware's behavior, and identifying its communication patterns.
4. Correlating findings with global threat intelligence databases to identify known signatures or behaviours.
5. Compiling a comprehensive report with mitigation and recovery steps, ensuring SwiftSpend Finance could swiftly address potential threats.
<br/>

Whenever you fell ready press "Start the Machine", it will open as a split view in your browser, give it some minutes to boot and fully set-up.
The credentials are `ericatracy:Intel321!`

<br/>
<br/>

## The Challenge
Before starting our analysis be conscious that artifacts used in this scenario were retrieved from a real-world cyber-attack, so pay attention and do NOT interact directly with them.

1. **Who shared the malware samples?**
   Read the message and at the top you will notice that it is sent by a guy called:
   --> REDACTED

<br/>

2. **What is the SHA1 hash of the file "pRsm.dll" inside samples.zip?**
   Click on the email title to fully open it, on the right side you can click to the attachment to download, then navigate to the file location. You can then use 
```bash
unzip -p Panda321! samples.zip
```
   Now with all the files extracted we can generate the hash:
```bash
sha1sum pRsm.dll
```
   --> REDACTED

<br/>

3. **Which malware framework utilizes these DLLs as add-on modules?**
   You can do a quick search online about the malicious dll and read articles, you will find the framework that has been used.
   --> REDACTED

<br/>

4. **Which MITRE ATT&CK Technique is linked to using pRsm.dll in this malware framework?**
   --> REDACTED

<br/>

5. **What is the CyberChef defanged URL of the malicious download location first seen on 2020-11-02?**
   You can find the URL in the [blog page](https://www.welivesecurity.com/2023/04/26/evasive-panda-apt-group-malware-updates-popular-chinese-software/)  as the other info above, copy it and defang with CyberChef.
   --> REDACTED

<br/>

6. **What is the CyberChef defanged IP address of the C&C server first detected on 2020-09-14 using these modules?**
   --> REDACTED

<br/>

7. **What is the SHA1 hash of the spyagent family spyware hosted on the same IP targeting Android devices on November 16, 2022?**
   To find this information i entered the previous found IP address on VirusTotal, located the point in time we are interested in, click on it, and we can see all the hashes of the spyware.
   --> REDACTED

<br/>
<br/>

Congratulations, you have completed the Friday Overtime challenge, succesfully identifiing and studing the new threat.

Catch you in the next CTF 😃
