# New Hire Old Artifacts Walkthrough
## Intro
Welcome to the New Hire Old Artifacts challenge, here is the link to the [room](https://tryhackme.com/room/newhireoldartifacts) on TryHackMe.
This is a log analysis challenge using Splunk, there are 10 questions we need to answer.

### Scenario
 You are a SOC Analyst for an MSSP (managed Security Service Provider) company called TryNotHackMe.

A newly acquired customer (Widget LLC) was recently onboarded with the managed Splunk service. The sensor is live, and all the endpoint events are now visible on TryNotHackMe's end. Widget LLC has some concerns with the endpoints in the Finance Dept, especially an endpoint for a recently hired Financial Analyst. The concern is that there was a period (December 2021) when the endpoint security product was turned off, but an official investigation was never conducted. 

Your manager has tasked you to sift through the events of Widget LLC's Splunk instance to see if there is anything that the customer needs to be alerted on.
<br/>

Whenever you feel ready click on "Start Machine" and connect using OpenVPN or via the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
Let's navigate to the Splunk interface using the browser `http://MACHINE_IP:8000`, wait a couple of minutes so that it will be fully loaded.
From the scenario we know the user is a guy in finance, probably 6'5.... anyway we can start with a generic load of the logs `index=*`, change the timespan to all time and check the user names.

There is one clearly related to finance called `DESKTOP-H1ATIJC\Finance01`

<br>

1. **A Web Browser Password Viewer executed on the infected machine. What is the name of the binary? Enter the full path.** <br>
	With the info we got so far + is a binary this means `*.exe` and is a password viewer, which we can safely assume the event contains at least the string `*view*`:
```
index=* User="DESKTOP-H1ATIJC\\Finance01" *.exe *view*
```
--> REDACTED

<br>

2. **What is listed as the company name?**  <br>
	We can open the previous event and look at the field `Company`.
--> REDACTED

<br>

3. **Another suspicious binary running from the same folder was executed on the workstation. What was the name of the binary? What is listed as its original filename? (format: file.xyz,file.xyz)** <br>
	We know know the user and the path to look for and also the field `Image`:
```
index=* User="DESKTOP-H1ATIJC\\Finance01" 
|  top Image
```
--> REDACTED

<br>

4. **The binary from the previous question made two outbound connections to a malicious IP address. What was the IP address? Enter the answer in a defang format.** <br>
```
index=* User="DESKTOP-H1ATIJC\\Finance01"   Image="C:\\Users\\Finance01\\AppData\\Local\\Temp\\IonicLarge.exe" 
|  top DestinationIp
```
The magiority of requests are on localhost, which we do not care here, the second one is the answer. <br>
--> REDACTED

<br>

5. **The same binary made some change to a registry key. What was the key path?** <br>
	We can filter for registry value set and the previous binary, only few events are left to check out, one stands out:
```
index=* User="DESKTOP-H1ATIJC\\Finance01"   Image="C:\\Users\\Finance01\\AppData\\Local\\Temp\\IonicLarge.exe" *reg* TaskCategory set
```
--> REDACTED

<br>

6. **Some processes were killed and the associated binaries were deleted. What were the names of the two binaries? (format: file.xyz,file.xyz)**  <br>
	We know they are 2 executables, we also know that they were either killed or deleted, but do not know if that happened via CLI or other method, we can filter for general keyword related to both and get only 3 events to check:
```
index=* User="DESKTOP-H1ATIJC\\Finance01"   *.exe *del* *kill*
```
--> REDACTED

<br>

7. **The attacker ran several commands within a PowerShell session to change the behaviour of Windows Defender. What was the last command executed in the series of similar commands?** <br>
	Now we can filter for PowerShell and Defender, finally output the `CommandLine` fileds:
```
index=* User="DESKTOP-H1ATIJC\\Finance01" *powershell* *defender* 
|  table CommandLine 
|  head
```
--> REDACTED

<br>

8. **Based on the previous answer, what were the four IDs set by the attacker? Enter the answer in order of execution. (format: 1st,2nd,3rd,4th)**  <br>
	Same search query as the previous question, simply go trough the commands and find them.
--> REDACTED

<br>

9. **Another malicious binary was executed on the infected workstation from another AppData location. What was the full path to the binary?**  <br>
	We can use the query from Q3 and check the other executables:
```
index=* User="DESKTOP-H1ATIJC\\Finance01" 
|  top Image
```
--> REDACTED

<br>

10.  **What were the DLLs that were loaded from the binary from the previous question? Enter the answers in alphabetical order. (format: file1.dll,file2.dll,file3.dll)** <br>
	Filter now for the new found executable and for `*.dll`:
```
index=* User="DESKTOP-H1ATIJC\\Finance01" EasyCalc.exe *.dll* 
|  table OriginalFileName 
|  uniq
```
--> REDACTED

<br/>
<br/>


Congratulations, you have successfully investigated the logs and gound all the signs of the malicious actibity.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
