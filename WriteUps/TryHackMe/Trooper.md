# Trooper
<br/>

## Intro
Welcome do the  Trooper challenge from TryHackMe, here is the [link](https://tryhackme.com/r/room/trooper) to it.
To solve this room we have to study the provided thread advisory report to identify TTPs and help our company that has been the victim of several cyber attacks.
Ultimately, with the collected information, we have to answer 10 questions to complete the challenge.

The credentials are:<br/>
**Username** info@tryhack.io <br/>
**Password** TryHackMe1234 <br/>
**OpenCTI IP** http://MACHINE_IP:8080**ATT&CK  <br/>
**Navigator IP** http://MACHINE_IP:4200 <br/>

Whenever you feel ready press "Start Machine" and connect via OpenVPN or AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
We can start the challenge by reading the provided PDF containing the report.

1. **What kind of phishing campaign does APT X use as part of their TTPs?**
   This information can be easily found in the first paragraph of the report.
   --> REDACTED

<br/>

2. **What is the name of the malware used by APT X?**
   The answer is located in the second paragraph.
   --> REDACTED

<br/>

3. **What is the malware's STIX ID?**
   To get this information open up the OpenCTI application navigating to the provided link, you can then login and search for the malware we identified in the previous question, by clicking on it you will see some information and the STIX ID.
   --> REDACTED

<br/>

4. **With the use of a USB, what technique did APT X use for initial access?**
   --> REDACTED

<br/>

5. **What is the identity of APT X?**
   To find this answer you can do a search inside the MITRE ATT&CK framework [site](https://attack.mitre.org/software/S0452/) with the info collected until now.
   --> REDACTED

<br/>

6. **On OpenCTI, how many Attack Pattern techniques are associated with the APT?**
   Inside OpenCTI search for the APT found in question 5, in the overview you can find the count of the attack patterns, the link is [this](http://MACHINE-IP:8080/dashboard/threats/intrusion_sets/d339751b-accf-4967-95c8-9e6bcf5b7315/knowledge/overview)
   --> REDACTED

<br/>

7. **What is the name of the tool linked to the APT?**
   --> REDACTED

<br/>

8. **Load up the Navigator. What is the sub-technique used by the APT under Valid Accounts?**
   In the MITRE ATT&CK you can find close to the entry "valid accounts" the sub-technique.
   --> REDACTED

<br/>

9. **Under what Tactics does the technique above fall?**
   Search up the technique of question 8 in the MITRE [website](https://attack.mitre.org/techniques/T1078/) and on the right you will notice a square with the Tactics
   --> REDACTED

<br/>

10.  **What technique is the group known for using under the tactic Collection?**
    Back exploring the MITRE ATT&CK navigator, under Collection you can notice a red entry.
    --> REDACTED

<br/>
<br/>

Congratulations, you have completed the Trooper challenge and practiced with the MITRE and OpenCTI frameworks to conduct an investigation.

Catch you in the next CTF 😃
