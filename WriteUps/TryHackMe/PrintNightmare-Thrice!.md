# PrintNightmare, thrice! Walkthrough

## Intro
Welcome to the "PrintNightmare, thrice!" challenge, here is the link to the [room](https://tryhackme.com/room/printnightmarec3kj) on TryHackMe.
In this challenge we will have to investigate the artifacts left behind to detect the PrintNightmare exploit used and answer a set of 10 questions.

**Scenario**: After discovering the PrintNightmare attack the security team pushed an emergency patch to all the endpoints. The PrintNightmare exploit used previously no longer works. All is well. Unfortunately, the same 2 employees discovered yet another exploit that can possibly work on a fully patched endpoint to elevate their privileges.

Whenever you feel ready press on "Start Machine" and a vm will appear in "split-view" in your browser.
Let's begin!

<br/>
<br/>

## The Challenge
On the desktop we can see 2 files: 
- a network capture called "traffic.pcap"
- a log file called "Logfile.PML"

Click on both of them and leave it some time to load.

Per the scenario we are investigating a known vulnerability dubbed PrintNightmare, i leave to you the study on how it precisely works, what is of interest for us here is that involves the use of SMB

1. **What remote address did the employee navigate to?**
	 We can find this in WireShark, filtering for `smb` we see the IP negotiating the protocol request
	--> REDACTED_FOR_THE_WRITEUP
<br>

2. **Per the PCAP, which user returns a STATUS_LOGON_FAILURE error?**
	Still in WireShark we can build a filter to match smb packets containing errors and the IP we just found:
```
ip.addr==20.188.56.147 && smb2.cmd==0x01
```
It is also possible to use another filter, to show different ways i will use it in the next question.
And packet 4456 contains that message, a couple of packets above (4453) we can see the user.
	--> REDACTED_FOR_THE_WRITEUP
<br>

3. **Which user successfully connects to an SMB share?**
	 Now let's filter for logon success:
```
smb2.nt_status==STATUS_SUCCESS
```
--> REDACTED_FOR_THE_WRITEUP
<br>

4. **What is the first remote SMB share the endpoint connected to? What was the first filename? What was the second?** (**format**: answer,answer,answer)
	We can look for accessed shares and files combining with the `or` operator this 2 filters:
```
smb2.cmd==3 || smb2.cmd==5
```
--> REDACTED_FOR_THE_WRITEUP
<br>

5. **From which remote SMB share was malicious DLL obtained? What was the path to the remote folder for the first DLL? How about the second?** (format: answer,answer,answer)
	We can simply scroll down from the previous output and read the following packets info in search of this. <br>
--> REDACTED_FOR_THE_WRITEUP
<br>

6. **What was the first location the malicious DLL was downloaded to on the endpoint? What was the second?**
	 We can now move to the *FullEventLogView* tool (on the taskbar). Once loaded we go on advanced options and select as timeframe "select events from all times". Now we can use the quick filter to search for the dll we have uncovered in the previous question. Finally check through the events to find the answer. <br>
--> REDACTED_FOR_THE_WRITEUP
<br>

7. **What is the folder that has the name of the remote printer server the user connected to? (provide the full folder path)**
	For this one we can simply open File Explorer and insert the name in the search box, it is painfully slow but we get the answer right. <br>
--> REDACTED_FOR_THE_WRITEUP
<br>

8. **What is the name of the printer the DLL added?**
	We can find this in the same filtered data in the event logs we previously used to find the DLL location. <br>
--> REDACTED_FOR_THE_WRITEUP
<br>

9. **What was the process ID for the elevated command prompt? What was its parent process?** (**format**: answer,answer)
	In the logs we have previously seen already `spoolsv.exe`, we can search for "cmd.exe" in the Logfile on the desktop to get the process ID. <br>
--> REDACTED_FOR_THE_WRITEUP
<br>

10.  **What command did the user perform to elevate privileges?**
	Still in the filter for the process name `cmd.exe` in the processes logfile we can look for "command line" and read it: <br>
--> REDACTED_FOR_THE_WRITEUP

<br/>
<br/>

Congratulations you have successfully put into practice your Linux forensics skills and uncovered all the relevant artifacts to answer the question and uncover the attacker steps.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
