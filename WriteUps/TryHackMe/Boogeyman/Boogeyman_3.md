# Boogeyman 3 Walkthrough
<br/>

## Intro
Welcome to the last room of Bogeyman challenges, here is the link to the [room](https://tryhackme.com/r/room/boogeyman3) on TryHackMe.

This time we are gonna still be investigating a compromise that began with a phishing email, but here we will we analzying logs with Kibana.

Whenever you feel ready press "Start Machine" and connect via OpenVPN or use the AttackBox
Let's begin!

<br/>

### The Story
Due to the previous attacks of Boogeyman, Quick Logistics LLC hired a managed security service provider to handle its Security Operations Center. Little did they know, the Boogeyman was still lurking and waiting for the right moment to return.

Without tripping any security defences of Quick Logistics LLC, the Boogeyman was able to compromise one of the employees and stayed in the dark, waiting for the right moment to continue the attack. Using this initial email access, the threat actors attempted to expand the impact by targeting the CEO, Evan Hutchinson.

The email appeared questionable, but Evan still opened the attachment despite the scepticism. After opening the attached document and seeing that nothing happened, Evan reported the phishing email to the security team.

Upon receiving the phishing email report, the security team investigated the workstation of the CEO. During this activity, the team discovered the email attachment in the downloads folder of the victim.
In addition, the security team also observed a file inside the ISO payload.
Lastly, it was presumed by the security team that the incident occurred between **August 29 and August 30, 2023**.

Given the initial findings, you are tasked to analyse and assess the impact of the compromise.

<br/>
<br/>

## The Challenge
For this challenge we have to access the Kibana console at: `http://MACHINE_IP`, with the credentials: `elastic:elastic`.
Once logged in we can click on "Discover" in the menu on the left, here we have our workplace.

The first thing we have to to is to change the timeframe on the top right side, we chose "absolute" and set the period between **August 29 and August 30, 2023**, finally press "Refresh".
A number of events will appear, those are the ones we will be investigating today.

Looking at the attached screenshots in the task we can see that the email contained an attachment file with the name `ProjextFinancialSummary_Q3.pdf`.
This file probably contains the first stage payload, let's see if the file was opened, we can insert the file name in the search query on the top, and 4 events gets displayed.

Already in the first recorded event we can see that a process opened the file with the following command:
```powershell
C:\Windows\SysWOW64\mshta.exe" "D:\ProjectFinancialSummary_Q3.pdf.hta
```
A couple of lines above we can also see the process PID -> REDACTED

Upon execution the payload implanted another file, we can see this still with the same filter, just going down a couple of events we can notice this command:
```powershell
C:\Windows\System32\xcopy.exe" /s /i /e /h D:\review.dat C:\Users\EVAN~1.HUT\AppData\Local\Temp\review.dat
```

Let's focus now on this file, let's put it in the search query: `review.dat`.
We quickly find out in the first result/event that the file has been executed by `runddll32.exe`:
```powershell
C:\Windows\System32\rundll32.exe" D:\review.dat,DllRegisterServer
```
<br/>

### Persistence Established
Moving on, we know that the stage 1 payload established persistence on the victim system via a scheduled task, we know that in Windows to achieve that we have to use the `schtasks.exe` utility, we can filter for this keyword.
Unfortunately that gave me only 1 result with the name of another scheduled task, so i searched for the keyword `ScheduledTask` and sure enough i found a powershell script creating a new task wit the name REDACTED
```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe $A = New-ScheduledTaskAction -Execute 'rundll32.exe' -Argument 'C:\Users\EVAN~1.HUT\AppData\Local\Temp\review.dat,DllRegisterServer'; $T = New-ScheduledTaskTrigger -Daily -At 06:00; $S = New-ScheduledTaskSettingsSet; $P = New-ScheduledTaskPrincipal $env:username; $D = New-ScheduledTask -Action $A -Trigger $T -Principal $P -Settings $S; Register-ScheduledTask Review -InputObject $D -Force;
```

The execution of the implanted file inside the machine has initiated a potential C2 connection. We need to find out the IP:PORT of the C2 server.
For this information i have chosen to check the destination.ip filed values, sorting the values we can see that a huge chunk is occupied by this IP REDACTED, finally to find the port we can search for events containing this IP with the query:
```
destination.ip: 165.232.170.151
```
And we can see the communication happens via port REDACTED.
<br/>

**The attacker has discovered that the current access is a local administrator. What is the name of the process used by the attacker to execute a UAC bypass?** <br/>
Here i was struggling a bit, my idea was to search for for "process creation" events, but this gave me too many result, filtering for executables `*.exe` took the number down of to little.
Another option was to search also for file creations or new registry entries but was not the best here. So i searched online for approaches to find UAC bypass having sysmon logs and stumbled over this [paper](https://tcm-sec.com/bypassing-defender-the-easy-way-fodhelper/) by TCM about how the famous Trickbot malware was achieving UAC bypass.

Using REDACTED it is quite trivial to achieve the wanted result, i tought let's check if for any chances the actor used it as well, and searching for the keyword i got 3 hits, reading the logs confirmed my assumption.
<br/>

### Dumping Credentials
**Having a high privilege machine access, the attacker attempted to dump the credentials inside the machine. What is the GitHub link used by the attacker to download a tool for credential dumping?** <br/>
Let's try our luck again, one of the most commonly known tool to dump credentials in Windows is Mimikatz,  the question also talks about GitHub so we can search for a match containing that word: `*github*`, this gives us 149 events, still many, let's add a filter: `event.code: 1` now we get 7, much better.
--> REDACTED

Later the attacker use Mimikatz to dump credentials and used the username and hash to connect to another machine, let's find this credentials.
Searching for the tool's name gives us 40 results and already in the first ones we can find the command that has been run, containing the creds:
```powershell
C:\Users\allan.smith\Documents\mimi\x64\mimikatz.exe, sekurlsa::pth /user:itadmin /domain:QUICKLOGISTICS /ntlm:REDACTED /run:powershell.exe, exit
```

The attacker then decided to use this credentials to enumerate remote file shares and successfully accessed a file.
This has surely happened using a powershell command, we can simplify our life by selecting on the left side only the fileds: `process.command_line`, `process.parent.command_line`, `process.parent_pid`, `process.pid` and search for:
```
process.parent.pid: 6160
```
(which is the parent pid of the above mimikatz command)

With those filters we get 14 results and we can quickly identify the file that has been accessed:
```
cat FileSystem::\\WKSTN-1327.quicklogistics.org\ITFiles\REDACTED.ps1
```
--> REDACTED

Later on we can also see the attacker execute another remote file commonly used in pentests: `PowerView.ps1`.
<br/>

### Lateral Movement
Still in the same window we can also see the credentials used to move laterally:--> REDACTED on the host named: REDACTED
```powershell
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -c "$credential = (New-Object PSCredential -ArgumentList ('QUICKLOGISTICS\allan.smith', (ConvertTo-SecureString 'Tr!ckyP@ssw0rd987' -AsPlainText -Force))) ; Invoke-Command -Credential $credential -ComputerName REDACTED -ScriptBlock {whoami}"
```

Now let's check what the bad guy has done on this new machine, let's filter for the hostname we have just found and the name of the user that executed the command `user.name: allan.smith`:
```
host.hostname: REDACTED
```
There are a lots of results not containing any commands, let's filter them out: `process.command_line: exist`, much better now we have 37 results.
--> REDACTED

On this machine the attacker repeated the process and dumped credentials again
```
C:\Users\allan.smith\Documents\mimi\x64\mimikatz.exe" "sekurlsa::pth /user:administrator /domain:QUICKLOGISTICS /ntlm:REDACTED /run:powershell.exe" exit
```
--> REDACTED
<br/>

### Gaining Access to DC
**After gaining access to the domain controller, the attacker attempted to dump the hashes via a DCSync attack. Aside from the administrator account, what account did the attacker dump?** <br/>
This is quick and easy to find, we can remove the username filter and search for:
```
"lsadump::dcsync"
```

We get 3 results, 2 related to the administrator and the other one to:
```powershell
C:\Users\Administrator\Documents\mimi\x64\mimikatz.exe, lsadump::dcsync /domain:quicklogistics.org /user:REDACTED, exit
```
--> REDACTED

Finally the attacker downloaded a ransomware and ran it on the target system, i have noticed the executable while searching with `events.code: 1` which is `ransomboogey.exe`, we can use this as a search filter and look for an URL:
--> REDACTED

<br/>
<br/>

Congratulations you have completed the Boogeyman series and put in practice your detective skills to uncover the IOC on different Windows machines using a variety of tools.

I hope you had fun completing this challenges and following along.

Catch you again in the next challege 😊
