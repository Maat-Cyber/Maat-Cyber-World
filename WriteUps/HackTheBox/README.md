<div align="center">

# 🧊 HackTheBox Writeups

### CTFs walkthroughs for ~10 retired boxes

[![Machines](https://img.shields.io/badge/Machines-8-9FEF00?style=for-the-badge)](#-machine-index) [![Difficulty](https://img.shields.io/badge/Difficulty-Easy%20%7C%20Medium-FFB800?style=for-the-badge)](#-machine-index)
[![Platform](https://img.shields.io/badge/Platform-HackTheBox-9FEF00?style=for-the-badge&logo=hackthebox&logoColor=white)](https://hackthebox.com) [![OS](https://img.shields.io/badge/OS-Linux%20(8%2F8)-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#-machine-index)

</div>

---

## 📑 Table of Contents

- [🧊 HackTheBox Writeups](#-hackthebox-writeups)
    - [CTFs walkthroughs for ~10 retired boxes](#ctfs-walkthroughs-for-10-retired-boxes)
  - [📑 Table of Contents](#-table-of-contents)
  - [🎯 Philosophy](#-philosophy)
  - [📖 How to Use These Writeups](#-how-to-use-these-writeups)
  - [📋 Machine Index](#-machine-index)
  - [🗂️ By Technique](#️-by-technique)
    - [🌐 Web Exploitation](#-web-exploitation)
    - [🔓 Privilege Escalation](#-privilege-escalation)
  - [🧰 Tools Referenced Across Writeups](#-tools-referenced-across-writeups)
  - [✅ Prerequisites](#-prerequisites)
  - [🤝 Contributing \& Corrections](#-contributing--corrections)

<br/>
<br/>

---

## 🎯 Philosophy

> *"The walkthrough won't contain the answers, to not take away the fun, but a step-by-step tutorial to reach them."*

Every writeup in this directory follows three rules:

| Rule | What It Means |
|------|---------------|
| **Guide, don't spoil** | You get the methodology, the commands, the reasoning. You never get the flag handed to you. |
| **Explain the *why*** | Every command is accompanied by an explanation of what it does and why it was chosen. |
| **Reproducible** | Another person following the same steps on the same machine should arrive at the same place. |

> ⚠️ **Note:** All machines covered here are **retired**. A HackTheBox VIP subscription is required to access retired boxes. Do not apply these techniques against active machines or any system you do not have explicit authorization to test.

<br/>
<br/>

---

## 📖 How to Use These Writeups

1. **Retire the machine** on [HackTheBox](https://hackthebox.com) and start the instance
2. **Note the target IP** assigned to your session
3. **Open the corresponding `.md` file** from the index below
4. **Follow along step by step**, typing commands yourself rather than copy-pasting blindly
5. **Read the explanations** before running each command. Understanding the *why* is the whole point
6. **Try to solve the next step on your own** before reading ahead

> 💡 **Tip:** Each writeup is structured so that every finding leads logically to the next action. If you get stuck, re-read the last explanation. The answer is usually one command away.

<br/>
<br/>

---

## 📋 Machine Index

| # | Machine | Difficulty | OS | Initial Access Vector | PrivEsc Vector | Writeup |
|---|---------|-----------|-----|----------------------|----------------|---------|
| 1 | **Bizness** | 🟢 Easy | Linux | ColdFusion deserialization (CVE-2023-26360) | H2 database JDBC manipulation | [→](Bizness.md) |
| 2 | **Cap** | 🟢 Easy | Linux | IDOR in Flask web app | Packet capture analysis (FTP creds) | [→](Cap.md) |
| 3 | **Devvortex** | 🟢 Easy | Linux | Joomla RCE (CVE-2023-23752) | Ubuntu kernel exploit (CVE-2023-2640 + CVE-2023-32629) | [→](Devvortex.md) |
| 4 | **Headless** | 🟢 Easy | Linux | XSS + command injection (Flask) | Sudo script abuse (`init.sh`) | [→](Headless.md) |
| 5 | **Perfection** | 🟢 Easy | Linux | ERB template injection (SSTI) | Sudo Ruby YAML deserialization | [→](Perfection.md) |
| 6 | **PermX** | 🟢 Easy | Linux | Chamilo file upload (CVE-2023-4220) | PATH hijacking (`acl_set_file`) | [→](PermX.md) |
| 7 | **Usage** | 🟢 Easy | Linux | SQLi + file upload bypass (Laravel) | Wildcard injection in `7z` (sudo) | [→](Usage.md) |
| 8 | **WifineticTwo** | 🟡 Medium | Linux | OpenPLC RCE (CVE-2021-31630) | WPS PIN attack via Reaver (hostapd) | [→](WifineticTwo.md) |

<br/>
<br/>

---

## 🗂️ By Technique

### 🌐 Web Exploitation

Every machine in this collection begins with a web-facing service. The initial access vectors span a wide range of web vulnerability classes.

| Technique | Machines |
|-----------|----------|
| Deserialization (Java / ColdFusion) | Bizness |
| Insecure Direct Object Reference (IDOR) | Cap |
| SQL Injection | Usage |
| Server-Side Template Injection (SSTI / ERB) | Perfection |
| Cross-Site Scripting (XSS) → session hijack | Headless |
| Command Injection | Headless |
| Arbitrary File Upload / Upload Bypass | PermX, Usage |
| CVE-based RCE (CMS / PLC) | Devvortex (Joomla), WifineticTwo (OpenPLC) |

<br/>

### 🔓 Privilege Escalation

| Technique | Machines |
|-----------|----------|
| Sudo misconfiguration / script abuse | Headless, Perfection, PermX, Usage |
| PATH hijacking | PermX |
| Wildcard injection (archive commands) | Usage |
| YAML deserialization | Perfection |
| Kernel exploit (OverlayFS) | Devvortex |
| Database abuse (H2 JDBC) | Bizness |
| Credential reuse / capture analysis | Cap |
| Wireless attack (WPS / Reaver) | WifineticTwo |

<br/>
<br/>

---

## 🧰 Tools Referenced Across Writeups

These are the tools that appear most frequently throughout the writeups in this directory. Familiarity with them will make following along much smoother.

| Tool | Category | Appears In |
|------|----------|-----------|
| **nmap** | Reconnaissance / port scanning | All 8 machines |
| **gobuster / ffuf / dirsearch** | Directory & subdomain enumeration | Bizness, Devvortex, PermX, Usage |
| **Burp Suite** | Web proxy / request interception | Headless, Perfection, Usage |
| **sqlmap** | SQL injection automation | Usage |
| **Wireshark / Tshark** | Packet capture analysis | Cap |
| **Metasploit** | Exploitation framework | Bizness, Devvortex |
| **John the Ripper / hashcat** | Password / hash cracking | Perfection, Usage |
| **Reaver** | WPS PIN brute-force | WifineticTwo |
| **netcat / socat** | Reverse shells / networking | All machines |
| **linpeas** | Linux privilege escalation enumeration | All machines |
| **curl / wget** | File transfer / HTTP requests | All machines |
| **Python 3** | Custom exploit scripts | Bizness, Devvortex, PermX |

> 💡 For reusable automation scripts, check the [`Bash-Scripts/`](../../Bash-Scripts/) and [`Python-Scripts/`](../../Python-Scripts/) directories in the repository root.

<br/>
<br/>

---

## ✅ Prerequisites

| Requirement | Details |
|-------------|---------|
| **HackTheBox account** | Free tier works for active machines; **VIP required** for retired boxes |
| **Kali Linux** (or equivalent) | Primary attack environment; all commands assume Kali paths |
| **OpenVPN connection** | Connect to HTB's EU or US VPN server before starting a machine |
| **SecLists** | Wordlists for enumeration (`apt install seclists`) |
| **Burp Suite Community** | Web proxy for intercepting and modifying requests |
| **Basic Linux CLI knowledge** | File navigation, permissions, piping, text processing |

> 💡 **Tip:** If you prefer not to set up a local environment, HackTheBox's **AttackBox** (available with VIP) provides a browser-based Kali instance with most tools pre-installed.

<br/>
<br/>

---

## 🤝 Contributing & Corrections

Found an error, outdated step, or broken link in a writeup?

- **Open an issue** on the [main repository](https://github.com/Maat-Cyber/Maat-Cyber-World/issues) with the file name and section
- **Email:** `maatghithub.phobia875@passinbox.com`
- **Pull requests** are welcome. Keep the "guide, don't spoil" philosophy intact

---

<div align="center">

**Now go spin up a machine and start hacking. The writeups will be here when you need them.** 🏴‍☠️

[← Back to Repository Root](../../README.md) · [TryHackMe Writeups →](../TryHackMe/) · [OverTheWire Writeups →](../OverTheWire/)

</div>
