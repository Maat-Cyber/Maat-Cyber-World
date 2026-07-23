<div align="center">

# 🟢 TryHackMe Writeups

## Step-by-step walkthroughs for ~100 rooms, challenges, and events

[![Total Writeups](https://img.shields.io/badge/Writeups-97-2ea44f?style=for-the-badge)](#-index) [![Multi-Part Series](https://img.shields.io/badge/Series-4-blue?style=for-the-badge)](#-multi-part-series--events) [![Platform](https://img.shields.io/badge/Platform-TryHackMe-88cc14?style=for-the-badge&logo=tryhackme&logoColor=white)](https://tryhackme.com)
[![Philosophy](https://img.shields.io/badge/Philosophy-Guide%2C_Not%20Spoil-orange?style=for-the-badge)](#-philosophy)

</div>

---

## 📑 Table of Contents

- [🟢 TryHackMe Writeups](#-tryhackme-writeups)
  - [Step-by-step walkthroughs for ~100 rooms, challenges, and events](#step-by-step-walkthroughs-for-100-rooms-challenges-and-events)
  - [📑 Table of Contents](#-table-of-contents)
  - [🎯 Philosophy](#-philosophy)
  - [📖 How to Use These Writeups](#-how-to-use-these-writeups)
  - [🏆 Multi-Part Series \& Events](#-multi-part-series--events)
  - [📋 Index by Category](#-index-by-category)
    - [🌐 Web Exploitation](#-web-exploitation)
    - [🔐 Cryptography](#-cryptography)
    - [🔍 Forensics \& Steganography](#-forensics--steganography)
    - [🛡️ Network \& Blue Team](#️-network--blue-team)
    - [⚙️ Reverse Engineering \& Binary](#️-reverse-engineering--binary)
    - [🪟 Windows \& Privilege Escalation](#-windows--privilege-escalation)
    - [🕵️ OSINT \& Phishing](#️-osint--phishing)
    - [🎲 Mixed \& CTF Collections](#-mixed--ctf-collections)
  - [🧰 Tools Referenced Across Writeups](#-tools-referenced-across-writeups)
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
| **Reproducible** | Another person following the same steps on the same room should arrive at the same place. |

<br/>
<br/>

---

## 📖 How to Use These Writeups

1. **Open the room on TryHackMe** and start the target machine (or use the AttackBox)
2. **Open the corresponding `.md` file** from the list below
3. **Follow along step by step**, typing commands yourself rather than copy-pasting blindly
4. **Read the explanations** before running each command. Understanding the *why* is the whole point
5. **Try to solve the next step on your own** before reading ahead

> 💡 **Tip:** If you get stuck, re-read the last explanation. The writeup is designed so that each step logically leads to the next. The answer is usually one command away.

<br/>
<br/>

---

## 🏆 Multi-Part Series & Events

These are curated challenge sets that span multiple rooms or were part of platform-wide events. They are best experienced in order.

| Series | Challenges | Focus | Directory |
|--------|-----------|-------|-----------|
| 🎉 **3-Million-Special** | Bricks Heist · Sch3Ma D3Mon · TryHack3M Subscribe | THM 3M subscriber celebration | [`3-million-special/`](3-million-special/) |
| 👻 **Boogeyman** | Part 1 · Part 2 · Part 3 | Progressive forensics & incident response | [`Boogeyman/`](Boogeyman/) |
| 🎮 **The Game** | v1 · v2 | Web exploitation (two versions of the same challenge) | [`The-Game/`](The-Game/) |
| 💘 **Valentine-2026** | Corp-Website · Cupid's Matchmaker · Cupid-Bot · Love-Letter-Locker · TryHeartMe · Valenfind · When Hearts Collide | Seasonal event (7 challenges) | [`Valentine-2026/`](Valentine-2026/) |

<br/>
<br/>

---

## 📋 Index by Category

### 🌐 Web Exploitation

The largest category. Covers injection flaws, LFI/RFI, SSRF, SSTI, IDOR, authentication bypass, CMS exploitation, subdomain takeover, and more.

| Writeup | Key Techniques |
|---------|---------------|
| [Archangel](Archangel.md) | LFI, log poisoning, RCE |
| [Benign](Benign.md) | SSRF, SSTI, command injection |
| [Break-it](Break-it.md) | SQLi, LFI, command injection |
| [b3dr0ck](b3dr0ck.md) | Web enumeration, exploitation |
| [Cat-Pictures-2](Cat-Pictures-2.md) | SSRF, SSTI, command injection |
| [Chill-Hack](Chill-Hack.md) | Command injection, file upload bypass |
| [Convert-my-Video](Convert-my-Video.md) | Command injection |
| [Corridor](Corridor.md) | IDOR (Insecure Direct Object Reference) |
| [Creative](Creative.md) | SSRF, command injection |
| [Critical](Critical.md) | SQLi, SSTI, command injection |
| [CyberHeroes](CyberHeroes.md) | Client-side authentication bypass |
| [D2PDF](D2PDF.md) | RCE via file processing |
| [EasyPeasy](EasyPeasy.md) | Web enumeration, hidden directories, vhosts |
| [ElBandito](ElBandito.md) | LFI, command injection |
| [Evil-GPT](Evil-GPT.md) | JWT manipulation, token forgery |
| [Friday-Overtime](Friday-Overtime.md) | Web exploitation |
| [Game-Zone](Game-Zone.md) | SQLi, JWT abuse |
| [Glitch](Glitch.md) | Prototype pollution |
| [Hammer](Hammer.md) | Command injection |
| [hackerNote](hackerNote.md) | Web exploitation |
| [Ide](Ide.md) | CMS exploitation |
| [Include](Include.md) | LFI (Local File Inclusion) |
| [Infinity-Shell](Infinity-Shell.md) | Web shell upload |
| [Injectics](Injectics.md) | Injection attacks |
| [Invite-Only](Invite-Only.md) | Web exploitation |
| [IronShade](IronShade.md) | Web exploitation |
| [Light](Light.md) | Web exploitation |
| [Lo-Fi](Lo-Fi.md) | Web exploitation |
| [Lookup](Lookup.md) | User enumeration, brute-force |
| [Masterminds](Masterminds.md) | Web exploitation |
| [mKingdom](mKingdom.md) | Web exploitation |
| [Operation-Slither](Operation-Slither.md) | Web exploitation |
| [Order](Order.md) | Web exploitation |
| [Pickle-Rick](Pickle-Rick.md) | Command injection, source code analysis |
| [Poster](Poster.md) | Web exploitation |
| [Publisher](Publisher.md) | Web exploitation, privilege escalation |
| [Rabbit-Store](Rabbit-Store.md) | Web exploitation |
| [Simple-CTF](Simple-CTF.md) | CMS exploitation (CVE) |
| [Smol](Smol.md) | Web exploitation |
| [Speed-Chatting](Speed-Chatting.md) | Web exploitation |
| [Startup](Startup.md) | Web exploitation, privilege escalation |
| [Summit](Summit.md) | Web exploitation |
| [Surfer](Surfer.md) | Web exploitation |
| [Takeover](Takeover.md) | Subdomain takeover |
| [Team](Team.md) | Web exploitation, privilege escalation |
| [The-Cod-Caper](The-Cod-Caper.md) | Web exploitation |
| [The-Sticker-Shop](The-Sticker-Shop.md) | Web exploitation |
| [Traverse](Traverse.md) | Path traversal |
| [Trooper](Trooper.md) | Web exploitation |
| [U.A.-High-School](U.A.-High-School.md) | Web exploitation |
| [UltraTech](UltraTech.md) | Web exploitation, privilege escalation |
| [Whiterose](Whiterose.md) | Web exploitation |

<br/>

---

### 🔐 Cryptography

| Writeup | Key Techniques |
|---------|---------------|
| [Ciphers-Secret-Message](Ciphers-Secret-Message.md) | Classical ciphers, encoding schemes |
| [Cryptosystem](Cryptosystem.md) | RSA, key analysis |
| [W1seGuy](W1seGuy.md) | Cryptographic challenges |

<br/>

---

### 🔍 Forensics & Steganography

| Writeup | Key Techniques |
|---------|---------------|
| [Brains](Brains.md) | Digital forensics |
| [Cyborg](Cyborg.md) | Forensics, archive analysis, privilege escalation |
| [Disgruntled](Disgruntled.md) | Log analysis, forensics |
| [Extracted](Extracted.md) | File carving, forensics |
| [Grep_CTF](Grep_CTF.md) | CLI forensics, grep, file analysis |
| [Hidden-Deep-Into-My-Heart](Hidden-Deep-Into-My-Heart.md) | Steganography |
| [JPGchat](JPGchat.md) | Steganography, image analysis |
| [Mother's-Secret](Mother's-Secret.md) | Forensics, file analysis |
| [Retracted](Retracted.md) | Forensics |
| [Secret-Recipe](Secret-Recipe.md) | Forensics, file analysis |
| [Shadow-Trace](Shadow-Trace.md) | Forensics, OSINT |
| [Sneaky-Patch](Sneaky-Patch.md) | Binary patching, forensics |
| [Unattended](Unattended.md) | Forensics, disk analysis |

<br/>

---

### 🛡️ Network & Blue Team

| Writeup | Key Techniques |
|---------|---------------|
| [Exfilnode](Exfilnode.md) | Network traffic analysis, exfiltration detection |
| [Investigating_with_Splunk](Investigating_with_Splunk.md) | SIEM, Splunk queries, log analysis |
| [ItsyBitsy](ItsyBitsy.md) | Network forensics, Elastic/Kibana |
| [Monday-Monitor](Monday-Monitor.md) | Network monitoring, traffic analysis |
| [PownSniff](PownSniff.md) | Telnet sniffing, network capture |
| [Tempest](Tempest.md) | Blue team, Sysmon, EVTX analysis, incident response |
| [Tshark-Challenges-1-2](Tshark-Challenges-1-2_Teamwork-and-Directory.md) | Tshark, packet analysis, protocol dissection |

<br/>

---

### ⚙️ Reverse Engineering & Binary

| Writeup | Key Techniques |
|---------|---------------|
| [Compiled](Compiled.md) | Reverse engineering, binary analysis |
| [Sneaky-Patch](Sneaky-Patch.md) | Binary patching, disassembly |

<br/>

---

### 🪟 Windows & Privilege Escalation

| Writeup | Key Techniques |
|---------|---------------|
| [Alfred](Alfred.md) | Windows, Jenkins exploitation |
| [HackPark](HackPark.md) | Windows, CMS exploitation, privesc |
| [PrintNightmare-Thrice!](PrintNightmare-Thrice!.md) | Windows, CVE exploitation (PrintNightmare) |
| [Mac-Hunt](Mac-Hunt.md) | macOS exploitation |

<br/>

---

### 🕵️ OSINT & Phishing

| Writeup | Key Techniques |
|---------|---------------|
| [Digital-Footprint](Digital-Footprint.md) | OSINT, information gathering |
| [MrPhisher](MrPhisher.md) | Phishing analysis, OSINT |

<br/>

---

### 🎲 Mixed & CTF Collections

| Writeup | Key Techniques |
|---------|---------------|
| [CTF-Collection-Vol-1](CTF-Collection-Vol-1.md) | Multi-discipline (web, crypto, forensics, misc) |


<br/>
<br/>

---

## 🧰 Tools Referenced Across Writeups

These are the tools that appear most frequently throughout the writeups in this directory. Familiarity with them will make following along much smoother.

| Tool | Category | Appears In |
|------|----------|-----------|
| **nmap** | Reconnaissance | Nearly all writeups |
| **gobuster / ffuf / dirsearch** | Directory brute-force | Web exploitation rooms |
| **Burp Suite** | Web proxy / interception | Web exploitation rooms |
| **sqlmap** | SQL injection | Game-Zone, Break-it, Critical |
| **Wireshark / Tshark** | Packet analysis | Network & Blue Team rooms |
| **Splunk** | SIEM / log analysis | Investigating_with_Splunk |
| **Volatility** | Memory forensics | Boogeyman series |
| **John the Ripper / hashcat** | Password cracking | Cyborg, EasyPeasy |
| **radare2 / Ghidra** | Reverse engineering | Compiled, Sneaky-Patch |
| **exiftool** | Metadata extraction | Forensics rooms |
| **CyberChef** | Encoding / decoding | Crypto, steganography rooms |
| **linpeas** | Privilege escalation enumeration | Linux privesc rooms |
| **Metasploit** | Exploitation framework | Various |
| **netcat / socat** | Networking / shells | Various |
| **Autopsy / EvtxECmd** | Disk & log forensics | Tempest, Boogeyman |

> 💡 For a deeper dive into any of these tools, check the [`Tips-&-Resources/`](../../Tips-&-Resources/) directory or the [`Bash-Scripts/`](../../Bash-Scripts/) and [`Python-Scripts/`](../../Python-Scripts/) directories in the repository root.

---

## 🤝 Contributing & Corrections

Found an error, outdated step, or broken link in a writeup?

- **Open an issue** on the [main repository](https://github.com/Maat-Cyber/Maat-Cyber-World/issues) with the file name and section
- **Email:** `maatghithub.phobia875@passinbox.com`
- **Pull requests** are welcome. Keep the "guide, don't spoil" philosophy intact

<br/>
<br/>

---

<div align="center">

**Now go deploy a machine and start hacking. The writeups will be here when you need them.** 🏴‍☠️

[← Back to Repository Root](../../README.md) · [HackTheBox Writeups →](../HackTheBox/) · [OverTheWire Writeups →](../OverTheWire/)

</div>
