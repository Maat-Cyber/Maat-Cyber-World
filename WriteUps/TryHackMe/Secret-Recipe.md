# Secret Recipe Walkthrough
<br/>

## Intro
Welcome in the Secret Recipe challenge from TryHackMe, here is the link to the [room](https://tryhackme.com/r/room/registry4n6) on their website.

**The story:** <br>
"Jasmine owns a famous New York coffee shop **Coffely** which is famous city-wide for its unique taste. Only Jasmine keeps the original copy of the recipe, and she only keeps it on her work laptop. Last week, James from the IT department was consulted to fix Jasmine's laptop. But it is suspected he may have copied the secret recipes from Jasmine's machine and is keeping them on his machine.

His machine has been confiscated and examined, but no traces could be found. The security department has pulled some important **registry artifacts** from his device and has tasked you to examine these artifacts and determine the presence of secret files on his machine."

Whenever you feel ready press the "start machine" button, wait a couple of minutes and you should have the system available in split-view in your browser.

Let's begin!

<br/>
<br/>

## The Challenge
In the user desktop we have 2 folders we will be using during this challenge:
- Artifacts: containing 6 Registry Hives to investigate
- EZ Tools: containing the forensics tools we might need to perform our analysis

Let's start by loading the **SOFTWARE** hive inside *Registry Explorer*, then navigate to:
```
Microsoft\Windows NT\CurrentVesrsion
```

Here we can check that the system is running a "Windows Server 2019 Datacenter" .
To find out the computer name we have to load the **SYSTEM** hive and navigate to:
```
CurrentControlsSet\Control\ComputerName\ComputerName
```

On the challenge system the "CurrentControlSet" is defined as "ControlSet001", here we see that the name assigned is REDACTED.

Now would be nice to know the user's accounts that were active, their names, privileges and date of creation, we can do that loading the **SAM** hive and navigating to:
```
SAM\Domains\Accounts\Users
```

Here we can see "NUMBER_REDACTED" accounts, the date of creation of the Administrator one which is REDACTED and it's RID, in this case is written as a 3 digit decimal number  REDACTED and it correspond to `DOMAIN_USER_RID_ADMIN`.

Still in this section we can spot a suspicious user named REDACTED and with RID 1013.

Enough information from here for now, let's move back to the **SOFTWARE** hive and navigate to:
```
Microsoft\Windows NT\CurrentVersion\NetworkList
```

We can see that the system was connected to a VPN service called REDACTED_VPN and the first time of connection was REDACTED.

Now we know that some shared folder have been mounted on the system and we need to find the name of the third one, we can find it in the **SYSTEM** hive and navigating to:
```
ControlSet001\Services\LanmanServer\Shares
```
--> REDACTED

Next we have to check the last DHCP IP that was assigned to the machine, let's go to the **SYSTEM**  hive and reach:
```
ControlSet001\Services\Tcpip\Parameters\Interfaces
```
--> REDACTED

To find the answer of question number 10 about the file containing the secret coffee recipe we can take a look at recently opened files in the **NTUSER** hive:
```
\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
```

It is a PDF file called REDACTED
In this section we can also locate another recently opened file that we will need later, called: REDACTED

The suspect then ran commands to enumerate the network, let's check them in the **SOFTWARE** and go to:
```
Microsoft\Windows\CurrentVersion\RunMRU
```
--> REDACTED

Now we have to find which tool was the person trying to find in order to transfer files, since we know that its name has been searched in the file explorer we can find those queries in the **NTUSER** hive:
```
\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery
```
--> REDACTED

We can see the number of times that PowerShell has been executed by looking inside the **NTUSER.DAT** hive at:
```
Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}\Count
```
The tool was run REDACTED times.

Let's locate now which network monitoring tool has the user executed, still in the same hive reach:
```
Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags
```

Here we can see a list of programs, but only REDACTED has the capabilities to perform those actions.

We are now close to the end of the challenge and we need to find out how many seconds was the ProtonVPN process in focus.
This information is stored as well in the **NTUSER.DAT** hive at:
```
Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}\Count
```

Here we can find the value of 5 minutes and 43 seconds which are a total of REDACTED seconds.

As last search we have to find the location of the `Everything.exe` tool in the system, we can use the find tool in Registry Explorer and insert the application name, you will be provided with the right entry inside the **NTUSER.DAT** hive, showing the path: REDACTED

<br/>
<br/>

Congratulations you have successfully completed the investigation of a Windows Host.
I hope you had fun following along.

Catch you in the next CTF 😃 
