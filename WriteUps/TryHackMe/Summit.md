# Summit Walkthrough
<br/>

## Intro
Welcome to the Summit challenge, part of the new update of the SOC 1 learning path, here is the link to the TryHackMe [room](https://tryhackme.com/r/room/summit).

In this situation we are working with an external penetration tester in an iterative purple-team scenario.
The tester will try to execute malware on a simulated workstation and we need to to configure PicoSecure's security tools to detect and prevent the malware from executing.

Additionally we are gonna be  "Following the **Pyramid of Pain's** ascending priority of indicators, your objective is to increase the simulated adversaries' cost of operations and chase them away for good. Each level of the pyramid allows you to detect and prevent various indicators of attack."

Whenever you feel ready press "start machine" and navigate to the URL `https://LAB_WEB_URL.p.thmlabs.com`

Let's begin!

<br/>
<br/>

## The Challenge
We have to sucesfully detect all 5 malware samples and block them before they execute on the sistem,

1. **What is the first flag you receive after successfully detecting sample1.exe?**
   In this first job we receive a mail with the malware sample, click on it and submit the scan, once the hashes are generated you can copy and add them into the blocklist situated on the left panel, after the submission you will receive an email containing the flag. <br/>
   --> ==REDACTED==

<br/>

2. **What is the second flag you receive after successfully detecting sample2.exe?**
   In the same email with the previous flag also comes the second malware sample, let's quickly scan it. This time, if you scroll down on the result, we can notice some network activity to a suspicious IP, we can copy it and create a firewall rule, type " egress" from any to `154.35.10.113` set to deny. Upon creation of the rule you will get the email with the flag. <br/>
   --> ==REDACTED==

<br/>

3. **What is the third flag you receive after successfully detecting sample3.exe?**
   We can now scan the third malware file, looking at the report we can notice that something is odd with the DNS requests, a domain `emudyn.bresonicz.info` is contacted. We can create a DNS filter and block this domain to get the flag. <br/>
   --> ==REDACTED==

<br/>

4. **What is the fourth flag you receive after successfully detecting sample4.exe?**
   Let's now analyze the sample number 4, the malicious software this time is attacking and changing some values in the registry to disable the AV and download files. In this scenario, as defenders, we can create a sigma rule, chose then "Sysmon event logs" -> "Registry modifications" and here put: 
   Registry key: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows Defender\Real-Time Protection`
   Reigistry Name: DisableRealTimeMonitoring
   Value: 1
   ATT&CK ID: Defence Evasion
   Create the rule and read the flag in the new email. <br/>
   --> ==REDACTED==

<br/>

5. **What is the fifth flag you receive after successfully detecting sample5.exe?**
   Click on the new malware attachment, the challenge is partially solved for us, read the email on the left side. We are provided the outgoing connections logs and we have to understand what to do.
   Analyzing the logs we can notice some packets being sent to the same IP that repeats every 30 minutes. Our option in this scenario is to create another Sigma rule, using Sysmon and finally choosing "network connections", here we can fill in:
   Remote IP:* any
   Remote Port:* any
   Size (bytes):* 97
   Frequency (seconds):* 1800
   ATT&CK ID:* command and control
   The final rule will look like this:
```
title: Alert on Suspicious Beacon Network Connections
id: network_connections_criteria_sysmon
description: |
  Detects network connections with specific criteria in Sysmon logs: remote IP, remote port, size, and frequency.

references:
  - https://attack.mitre.org/tactics/TA0011/

tags:
  - attack.ta0011
  - sysmon

detection:
  selection:
    EventID: 3
    RemoteIP: '*'
    RemotePort: '*'
    Size: 97
    Frequency: 1800 seconds

  condition: selection

falsepositives:
  - Legitimate network traffic may match this criteria.

level: high
```
   --> ==REDACTED==

<br/>

6. **What is the final flag you receive from Sphinx?**
   Finally in the new email we can open the commands log, looking at it we can see that a lots of data and info about the system and network are being collected and saved to `%temp%\exfiltr8.log`.
   Let's proceed with the creation of another sigma rule, using Sysmon to detect the creation or modification of files located in that directory, the MITRE tactic is obviously exfiltration.
   After the creation of the rule we get the final email from the pentester will give us the last flag.
   --> ==REDACTED==


<br/>
<br/>

Congratulations, you have completed the Summit challenge and practiced with the Pyramid of Pain!

Catch you in the next CTF 😃
