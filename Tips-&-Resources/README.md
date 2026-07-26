<div align=center>

# 📚 Tips & Resources

Practical technique references, exploitation checklists, and tool documentation you can bookmark and revisit during any CTF session or pentest engagement.

Every file in this directory is designed to be a **quick-reference companion** - open it alongside your terminal and work through the phases in order.

</div>

<br/>
<br/>

---

## 📑 Table of Contents

- 📚 Tips & Resources
  - 📑 Table of Contents
  - 📂 Files Index
  - 🐧 Linux Privilege Escalation Checklist
  - 🪟 Windows Privilege Escalation Checklist
  - 🌐 Web Application Exploitation Checklist
  - 🔄 Reverse Shell Upgrade
  - 🔱 Reverse Shell Generator (CLI)
  - 🧭 How to Use These Guides
  - ⚠️ Disclaimer
  - 🔗 Related

<br/>
<br/>

---

## 📂 Files Index

| # | File | Category | Phases / Sections |
|---|------|----------|-------------------|
| 1 | `Linux-Privilege-Escalation-Checklist.md` | Privesc / Linux | 15 phases (0–14) |
| 2 | `Windows-Privilege-Escalation-Checklist.md` | Privesc / Windows | 18 phases (0–17) |
| 3 | `Web_Apps-Exploitation-Checklist.md` | Web Exploitation | 15 phases (0–14) |
| 4 | `Reverse_Shell-Upgrade.md` | Post-Exploitation | 4 upgrade methods |
| 5 | `Reverse_Shell-Generator-CLI.md` | Tool Documentation | 15 payload categories |

> 📌 **This directory is growing.** New checklists and guides are added as new techniques are encountered. Check back often or ⭐ the repo to stay updated.

<br/>
<br/>

---

## 🐧 Linux Privilege Escalation Checklist

**File:** `Linux-Privilege-Escalation-Checklist.md`

A phased checklist covering the full Linux privesc attack surface. Work phases in order - phases 2–7 cover 90% of CTF/real-world privesc.

| Phase | Focus |
|-------|-------|
| 0 | Stabilize Shell |
| 1 | Situational Awareness |
| 2 | SUID / SGID Binaries |
| 3 | Sudo Misconfigurations |
| 4 | Cron Jobs |
| 5 | PATH Hijacking |
| 6 | Writable Files & Directories |
| 7 | Linux Capabilities |
| 8 | Kernel Exploits (last resort) |
| 9 | Docker / Container Escape |
| 10 | NFS Shares |
| 11 | Sensitive Files & Credentials |
| 12 | Network & Pivoting |
| 13 | Wildcard & Symlink Attacks |
| 14 | Automated Tools (linpeas, LinEnum, lse, pspy) |

Includes a **Quick-Reference Command Table** at the end for fast lookups.

<br/>
<br/>

---

## 🪟 Windows Privilege Escalation Checklist

**File:** `Windows-Privilege-Escalation-Checklist.md`

A phased checklist for Windows privesc, from initial shell stabilization through lateral movement.

| Phase | Focus |
|-------|-------|
| 0 | Stabilize Shell |
| 1 | Situational Awareness |
| 2 | Privileges & Tokens |
| 3 | Unquoted Service Paths |
| 4 | Weak Service Permissions |
| 5 | Weak Registry Permissions |
| 6 | AlwaysInstallElevated |
| 7 | Scheduled Tasks |
| 8 | Stored Credentials |
| 9 | Sensitive Files |
| 10 | Kernel Exploits |
| 11 | Token Impersonation (PrintSpoofer, GodPotato) |
| 12 | UAC Bypass |
| 13 | Network Pivoting |
| 14 | Auto-Enum Tools (winPEAS, Seatbelt, PowerUp) |
| 15 | Mimikatz & Credential Dumping |
| 16 | SMB Enumeration & Lateral Movement |
| 17 | RDP Access & Abuse |

Includes a **Quick Command Table** with 28 essential commands.

<br/>
<br/>

---

## 🌐 Web Application Exploitation Checklist

**File:** `Web_Apps-Exploitation-Checklist.md`

A full-spectrum web app testing checklist, from recon through post-exploitation.

| Phase | Focus |
|-------|-------|
| 0 | Setup & Intercepting Proxy |
| 1 | Recon & Technology Fingerprinting |
| 2 | Content Discovery & Mapping |
| 3 | Input Point Identification |
| 4 | Injection Attacks (SQLi / CMDi / SSTI / XXE) |
| 5 | Client-Side Attacks (XSS / CSRF / Clickjacking) |
| 6 | File Inclusion & File Upload |
| 7 | SSRF & Request Forgery |
| 8 | Authentication & Session Attacks |
| 9 | IDOR & Broken Access Control |
| 10 | Insecure Deserialization |
| 11 | Business Logic & Race Conditions |
| 12 | WAF Bypass & Evasion |
| 13 | Post-Exploitation & Pivoting |
| 14 | Automated Scanners (nikto, nuclei, wpscan) |

Includes a **Quick Command Table** with 20 key commands.

<br/>
<br/>

---

## 🔄 Reverse Shell Upgrade

**File:** `Reverse_Shell-Upgrade.md`

A guide covering four methods to upgrade a basic reverse shell into a fully interactive TTY:

| Method | When to Use |
|--------|-------------|
| Python PTY (`pty.spawn`) | Python is available on target |
| Full TTY (`stty raw -echo` + env vars) | Best interactive experience; requires Python |
| `/usr/bin/script` | Python unavailable; Linux targets |
| Socat | Socat installed on target (rare) |

Includes troubleshooting tips for zsh users and `rlwrap` alternatives.

<br/>
<br/>

---

## 🔱 Reverse Shell Generator (CLI)

**File:** `Reverse_Shell-Generator-CLI.md`

Documentation for the `Reverse_Shell-Generator-CLI.sh` script (located in `Bash-Scripts/`). An interactive terminal tool that generates copy-paste-ready reverse shell payloads across **15 categories** and **100+ variants**, including:

Bash · Netcat · Python · Perl · PHP · Ruby · PowerShell · Node.js · Java/Groovy · Compiled (C, C#, Go, Rust) · Socat/OpenSSL/Lua · Encoded · MSFVenom · HoaxShell · Listeners

Each selection prints the payload with your LHOST/LPORT pre-filled, the matching listener command, and a link back to the Reverse Shell Upgrade guide.

<br/>
<br/>

---

## 🧭 How to Use These Guides

1. **During a CTF:** Open the relevant checklist in a split terminal or browser tab
2. **Work top-to-bottom:** Phases are ordered by likelihood and impact
3. **Don't skip Phase 0:** A stable shell saves hours of frustration
4. **Cross-reference:** After web exploitation → pivot to Linux/Windows privesc checklist
5. **Verify automated tools manually:** Scanners find low-hanging fruit; CTFs need manual testing

<br/>
<br/>

---

## ⚠️ Disclaimer

> **These guides are for authorized security testing, CTF competitions, and educational purposes only.**
>
> Do **not** use any techniques described here against systems you do not own or have explicit written permission to test. The author assumes no liability for misuse.
>
> Always operate within the rules of engagement of your CTF platform (TryHackMe, HackTheBox, OverTheWire, etc.) or your authorized pentest scope.

<br/>
<br/>

---

## 🔗 Related

| Resource | Link |
|----------|------|
| 🏠 Main Repository | [Maat-Cyber-World](https://github.com/Maat-Cyber/Maat-Cyber-World) |
| 🐚 Bash Scripts | `Bash-Scripts/` |
| 🐍 Python Scripts | `Python-Scripts/` |
| 📝 CTF Writeups | `WriteUps/` |
| 🔱 Reverse Shell Generator Script | `Bash-Scripts/Reverse_Shell-Generator-CLI.sh` |

---

**Happy Hacking! 💻🏴‍☠️**

_Built with love by Maat_
