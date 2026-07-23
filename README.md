<div align="center">

# 🏴‍☠️ Maat-Cyber-World

### CTF Writeups · Custom Scripts · Cybersecurity Guides

*A growing collection of hands-on Capture The Flag walkthroughs, purpose-built automation scripts, and practical guides for aspiring security practitioners.*

[![Platforms](https://img.shields.io/badge/Platforms-TryHackMe%20%7C%20HackTheBox%20%7C%20OverTheWire-2ea44f?style=for-the-badge)](#-writeups)
[![Writeups](https://img.shields.io/badge/Writeups-100%2B-blue?style=for-the-badge)](#-writeups)
[![Scripts](https://img.shields.io/badge/Scripts-Bash%20%2B%20Python-orange?style=for-the-badge)](#-scripts--tools)
[![Language](https://img.shields.io/badge/Language-Shell%2079.7%25%20%7C%20Python%2020.3%25-yellow?style=for-the-badge)](#-repository-structure)
[![Commits](https://img.shields.io/badge/Commits-145-success?style=for-the-badge)](https://github.com/Maat-Cyber/Maat-Cyber-World/commits/main)
[![License](https://img.shields.io/badge/License-See%20Repo-lightgrey?style=for-the-badge)](https://github.com/Maat-Cyber/Maat-Cyber-World)

[**Website**](https://maat-feather.wixsite.com/maat-cyber-world) · [**TryHackMe Profile**](https://tryhackme.com) · [**Contact**](mailto:maatghithub.phobia875@passinbox.com)

</div>

<br/>
<br/>

---

## 📑 Table of Contents

- [🏴‍☠️ Maat-Cyber-World](#️-maat-cyber-world)
    - [CTF Writeups · Custom Scripts · Cybersecurity Guides](#ctf-writeups--custom-scripts--cybersecurity-guides)
  - [📑 Table of Contents](#-table-of-contents)
  - [🎯 About](#-about)
  - [👥 Who Is This For?](#-who-is-this-for)
  - [📂 Repository Structure](#-repository-structure)
  - [📝 Writeups](#-writeups)
    - [TryHackMe](#tryhackme)
      - [Individual Rooms](#individual-rooms)
      - [Multi-Part Series \& Events](#multi-part-series--events)
    - [HackTheBox](#hackthebox)
    - [OverTheWire](#overthewire)
  - [🛠️ Scripts \& Tools](#️-scripts--tools)
    - [EasyScan.sh](#easyscansh)
    - [Pin Codes Generator](#pin-codes-generator)
    - [EnumerateUsers (Lookup)](#enumerateusers-lookup)
    - [Base64 to Image](#base64-to-image)
  - [📚 Tips \& Resources](#-tips--resources)
    - [Reverse Shell Upgrade](#reverse-shell-upgrade)
  - [🚀 Getting Started](#-getting-started)
    - [Browsing Writeups](#browsing-writeups)
    - [Using the Scripts](#using-the-scripts)
  - [✅ Prerequisites](#-prerequisites)
  - [🤝 Contributing](#-contributing)
  - [❓ FAQ](#-faq)
  - [🔗 Connect](#-connect)

<br/>
<br/>


---

## 🎯 About

**Maat-Cyber-World** is a personal knowledge base and community resource built by [Maat](https://github.com/Maat-Cyber), a cybersecurity enthusiast who documents the journey of solving CTF challenges across multiple platforms.

This repository contains:

| Category | Description |
|----------|-------------|
| 📝 **Writeups** | Step-by-step walkthroughs for 100+ CTF rooms and challenges |
| 🛠️ **Scripts** | Hand-crafted Bash and Python tools to automate common CTF tasks |
| 📚 **Guides** | Practical reference material for techniques like reverse shell upgrades |

Every writeup follows a consistent philosophy: **guide you to the solution without handing you the flag**. You will learn the methodology, the tools, and the reasoning, but the final answer is yours to discover on your own machine.

> *"The walkthrough won't contain the answers, to not take away the fun, but a step-by-step tutorial to reach them."*

<br/>
<br/>

---

## 👥 Who Is This For?

| Audience | How This Repo Helps |
|----------|-------------------|
| **CTF Beginners** | Structured, jargon-light walkthroughs that explain *why* each step is taken, not just *what* to type |
| **Intermediate Players** | Multi-part challenge series (Boogeyman, The Game, Valentine-2026) that build progressively harder skills |
| **Script Collectors** | Ready-to-use recon and utility scripts you can drop into your own CTF toolkit |
| **Self-Learners** | Tips & Resources section with technique references you can revisit anytime |

<br/>
<br/>

---

## 📂 Repository Structure

```
Maat-Cyber-World/
├── Bash-Scripts/
│   ├── EasyScan.sh              # Automated multi-tool recon scanner
│   └── Pin_Codes_Generator.sh   # PIN code wordlist generator
├── Python-Scripts/
│   ├── EnumerateUsers_lookup.py # User enumeration + brute-force (THM Lookup)
│   └── base64_to_img.py         # Base64 string to image file converter
├── Tips-&-Resources/
│   └── Reverse_Shell-Upgrade.md # Guide: upgrading reverse shells to full TTY
├── WriteUps/
│   ├── TryHackMe/               # 80+ individual walkthroughs + multi-part series
│   │   ├── 3-million-special/   # THM 3M subscriber event (3 challenges)
│   │   ├── Boogeyman/           # 3-part series
│   │   ├── The-Game/            # 2 versions
│   │   ├── Valentine-2026/      # 7-challenge event
│   │   └── *.md                 # Individual room walkthroughs
│   ├── HackTheBox/              # 8 machine walkthroughs
│   └── OverTheWire/             # 3 wargame walkthroughs (Bandit, Leviathan, Natas)
└── README.md

```
**Language breakdown:** Shell 79.7% · Python 20.3%

<br/>
<br/>

---

## 📝 Writeups

All writeups are organized by platform. Each guide walks you through the methodology from initial reconnaissance to flag capture, explaining the reasoning behind every command.

### TryHackMe

The largest section, covering **80+ rooms** ranging from beginner-friendly to advanced. Walkthroughs span web exploitation, privilege escalation, cryptography, forensics, network analysis, and more.

<details>
<summary><strong>📋 Full TryHackMe Writeup Index (click to expand)</strong></summary>

<br/>

#### Individual Rooms

| Writeup | Category Hint |
|---------|--------------|
| [Alfred](WriteUps/TryHackMe/Alfred.md) | Windows / Jenkins |
| [Archangel](WriteUps/TryHackMe/Archangel.md) | Web / LFI |
| [Benign](WriteUps/TryHackMe/Benign.md) | Web |
| [Brains](WriteUps/TryHackMe/Brains.md) | Forensics |
| [Break-it](WriteUps/TryHackMe/Break-it.md) | Web |
| [b3dr0ck](WriteUps/TryHackMe/b3dr0ck.md) | Web |
| [Cat-Pictures-2](WriteUps/TryHackMe/Cat-Pictures-2.md) | Web |
| [Chill-Hack](WriteUps/TryHackMe/Chill-Hack.md) | Web / Privesc |
| [Ciphers-Secret-Message](WriteUps/TryHackMe/Ciphers-Secret-Message.md) | Cryptography |
| [Compiled](WriteUps/TryHackMe/Compiled.md) | Reverse Engineering |
| [Convert-my-Video](WriteUps/TryHackMe/Convert-my-Video.md) | Web / Command Injection |
| [Corridor](WriteUps/TryHackMe/Corridor.md) | Web |
| [Creative](WriteUps/TryHackMe/Creative.md) | Web |
| [Critical](WriteUps/TryHackMe/Critical.md) | Web |
| [Cryptosystem](WriteUps/TryHackMe/Cryptosystem.md) | Cryptography |
| [CTF-Collection-Vol-1](WriteUps/TryHackMe/CTF-Collection-Vol-1.md) | Mixed |
| [CyberHeroes](WriteUps/TryHackMe/CyberHeroes.md) | Web |
| [Cyborg](WriteUps/TryHackMe/Cyborg.md) | Forensics / Privesc |
| [D2PDF](WriteUps/TryHackMe/D2PDF.md) | Web |
| [Digital-Footprint](WriteUps/TryHackMe/Digital-Footprint.md) | OSINT |
| [Disgruntled](WriteUps/TryHackMe/Disgruntled.md) | Forensics |
| [EasyPeasy](WriteUps/TryHackMe/EasyPeasy.md) | Web / Crypto |
| [ElBandito](WriteUps/TryHackMe/ElBandito.md) | Web |
| [Evil-GPT](WriteUps/TryHackMe/Evil-GPT.md) | AI / Web |
| [Exfilnode](WriteUps/TryHackMe/Exfilnode.md) | Network |
| [Extracted](WriteUps/TryHackMe/Extracted.md) | Forensics |
| [Friday-Overtime](WriteUps/TryHackMe/Friday-Overtime.md) | Web |
| [Game-Zone](WriteUps/TryHackMe/Game-Zone.md) | Web / SQLi |
| [Glitch](WriteUps/TryHackMe/Glitch.md) | Web |
| [Grep_CTF](WriteUps/TryHackMe/Grep_CTF.md) | Forensics / CLI |
| [HackPark](WriteUps/TryHackMe/HackPark.md) | Windows / Web |
| [Hammer](WriteUps/TryHackMe/Hammer.md) | Web |
| [hackerNote](WriteUps/TryHackMe/hackerNote.md) | Web |
| [Hidden-Deep-Into-My-Heart](WriteUps/TryHackMe/Hidden-Deep-Into-My-Heart.md) | Steganography |
| [Ide](WriteUps/TryHackMe/Ide.md) | Web |
| [Include](WriteUps/TryHackMe/Include.md) | Web / LFI |
| [Infinity-Shell](WriteUps/TryHackMe/Infinity-Shell.md) | Web |
| [Injectics](WriteUps/TryHackMe/Injectics.md) | Web / Injection |
| [Investigating_with_Splunk](WriteUps/TryHackMe/Investigating_with_Splunk.md) | Blue Team / SIEM |
| [Invite-Only](WriteUps/TryHackMe/Invite-Only.md) | Web |
| [IronShade](WriteUps/TryHackMe/IronShade.md) | Web |
| [ItsyBitsy](WriteUps/TryHackMe/ItsyBitsy.md) | Network / Forensics |
| [JPGchat](WriteUps/TryHackMe/JPGchat.md) | Steganography |
| [Light](WriteUps/TryHackMe/Light.md) | Web |
| [Lo-Fi](WriteUps/TryHackMe/Lo-Fi.md) | Web |
| [Lookup](WriteUps/TryHackMe/Lookup.md) | Web / Privesc |
| [Mac-Hunt](WriteUps/TryHackMe/Mac-Hunt.md) | macOS |
| [Masterminds](WriteUps/TryHackMe/Masterminds.md) | Web |
| [mKingdom](WriteUps/TryHackMe/mKingdom.md) | Web |
| [Monday-Monitor](WriteUps/TryHackMe/Monday-Monitor.md) | Network |
| [Mother's-Secret](WriteUps/TryHackMe/Mother's-Secret.md) | Forensics |
| [MrPhisher](WriteUps/TryHackMe/MrPhisher.md) | Phishing / OSINT |
| [Operation-Slither](WriteUps/TryHackMe/Operation-Slither.md) | Web |
| [Order](WriteUps/TryHackMe/Order.md) | Web |
| [Pickle-Rick](WriteUps/TryHackMe/Pickle-Rick.md) | Web / Command Injection |
| [Poster](WriteUps/TryHackMe/Poster.md) | Web |
| [PownSniff](WriteUps/TryHackMe/PownSniff.md) | Network / Telnet |
| [PrintNightmare-Thrice!](WriteUps/TryHackMe/PrintNightmare-Thrice!.md) | Windows / CVE |
| [Publisher](WriteUps/TryHackMe/Publisher.md) | Web / Privesc |
| [Rabbit-Store](WriteUps/TryHackMe/Rabbit-Store.md) | Web |
| [Retracted](WriteUps/TryHackMe/Retracted.md) | Forensics |
| [Secret-Recipe](WriteUps/TryHackMe/Secret-Recipe.md) | Forensics |
| [Shadow-Trace](WriteUps/TryHackMe/Shadow-Trace.md) | Forensics / OSINT |
| [Simple-CTF](WriteUps/TryHackMe/Simple-CTF.md) | Web / CMS |
| [Smol](WriteUps/TryHackMe/Smol.md) | Web |
| [Sneaky-Patch](WriteUps/TryHackMe/Sneaky-Patch.md) | Binary / Patching |
| [Speed-Chatting](WriteUps/TryHackMe/Speed-Chatting.md) | Web |
| [Startup](WriteUps/TryHackMe/Startup.md) | Web / Privesc |
| [Summit](WriteUps/TryHackMe/Summit.md) | Web |
| [Surfer](WriteUps/TryHackMe/Surfer.md) | Web |
| [Takeover](WriteUps/TryHackMe/Takeover.md) | Subdomain Takeover |
| [Team](WriteUps/TryHackMe/Team.md) | Web / Privesc |
| [Tempest](WriteUps/TryHackMe/Tempest.md) | Blue Team / Forensics |
| [The-Cod-Caper](WriteUps/TryHackMe/The-Cod-Caper.md) | Web |
| [The-Sticker-Shop](WriteUps/TryHackMe/The-Sticker-Shop.md) | Web |
| [Traverse](WriteUps/TryHackMe/Traverse.md) | Web / Path Traversal |
| [Trooper](WriteUps/TryHackMe/Trooper.md) | Web |
| [Tshark-Challenges-1-2](WriteUps/TryHackMe/Tshark-Challenges-1-2_Teamwork-and-Directory.md) | Network / Wireshark |
| [U.A.-High-School](WriteUps/TryHackMe/U.A.-High-School.md) | Web |
| [UltraTech](WriteUps/TryHackMe/UltraTech.md) | Web / Privesc |
| [Unattended](WriteUps/TryHackMe/Unattended.md) | Forensics |
| [W1seGuy](WriteUps/TryHackMe/W1seGuy.md) | Cryptography |
| [Whiterose](WriteUps/TryHackMe/Whiterose.md) | Web |


#### Multi-Part Series & Events

| Series | Files | Description |
|--------|-------|-------------|
| [3-Million-Special](WriteUps/TryHackMe/3-million-special/) | Bricks Heist, Sch3Ma D3Mon, TryHack3M Subscribe | THM 3M subscriber celebration event |
| [Boogeyman](WriteUps/TryHackMe/Boogeyman/) | Parts 1, 2, 3 | Progressive forensics & incident response series |
| [The Game](WriteUps/TryHackMe/The-Game/) | v1, v2 | Web exploitation challenge (two versions) |
| [Valentine-2026](WriteUps/TryHackMe/Valentine-2026/) | 7 challenges | Seasonal event: Corp-Website, Cupid's Matchmaker, Cupid-Bot, Love-Letter-Locker, TryHeartMe, Valenfind, When Hearts Collide |

</details>

<br/>

### HackTheBox

| Writeup | Difficulty |
|---------|-----------|
| [Bizness](WriteUps/HackTheBox/Bizness.md) | Easy |
| [Cap](WriteUps/HackTheBox/Cap.md) | Easy |
| [Devvortex](WriteUps/HackTheBox/Devvortex.md) | Easy |
| [Headless](WriteUps/HackTheBox/Headless.md) | Easy |
| [Perfection](WriteUps/HackTheBox/Perfection.md) | Easy |
| [PermX](WriteUps/HackTheBox/PermX.md) | Easy |
| [Usage](WriteUps/HackTheBox/Usage.md) | Easy |
| [WifineticTwo](WriteUps/HackTheBox/WifineticTwo.md) | Medium |

> ⚠️ *Difficulty ratings are approximate and based on HTB's own classification at time of writing. Verify on the platform.*

<br/>

### OverTheWire

| Writeup | Wargame |
|---------|---------|
| [Bandit](WriteUps/OverTheWire/Bandit.md) | Linux CLI fundamentals |
| [Leviathan](WriteUps/OverTheWire/Leviathan.md) | Linux privilege escalation |
| [Natas](WriteUps/OverTheWire/Natas.md) | Web security |

<br/>
<br/>

---

## 🛠️ Scripts & Tools

Custom-built automation scripts designed to speed up common CTF workflows. All scripts are tested on **Kali Linux** and **BlackArch**.

### EasyScan.sh

**Path:** `Bash-Scripts/EasyScan.sh`

An all-in-one reconnaissance scanner that chains together the most common CTF recon tools into a single interactive workflow.

| Feature | Details |
|---------|---------|
| **Tools integrated** | nmap, gobuster, nikto, ffuf, dirsearch, wpscan |
| **Workflow** | Port scan → Directory brute-force → DNS/VHost enumeration → Vulnerability scan → Recursive fuzzing |
| **Output** | Organized report file at `/home/kali/Documents/Scans/Reports/` |
| **Dependency check** | Auto-detects missing tools and offers to install them |
| **Modes** | Basic scan (common ports) or full scan (all 65535 ports) |

**Quick start:**

```bash
chmod +x Bash-Scripts/EasyScan.sh
./Bash-Scripts/EasyScan.sh
 ```

> ⚠️ **Note:** Paths default to `/home/kali/`. If you use a different username or distribution, edit the paths at the top of the script. Wordlist paths assume standard Kali/SecLists locations.

<br/>

---

### Pin Codes Generator

**Path:** `Bash-Scripts/Pin_Codes_Generator.sh`

Generates PIN code wordlists for brute-force challenges involving numeric authentication.

```bash
chmod +x Bash-Scripts/Pin_Codes_Generator.sh
./Bash-Scripts/Pin_Codes_Generator.sh
 ```

<br/>

---

### EnumerateUsers (Lookup)

**Path:** `Python-Scripts/EnumerateUsers_lookup.py`

A purpose-built script for the [TryHackMe Lookup room](WriteUps/TryHackMe/Lookup.md). It performs:

1. **Username enumeration** via login error message differentiation
2. **Password brute-force** against the discovered valid username

| Requirement | Details |
|-------------|---------|
| Python 3 | `#!/bin/python3` |
| Dependencies | `requests` (`pip install requests`) |
| Wordlists | `/usr/share/seclists/Usernames/Names/names.txt` and `rockyou.txt` |

```bash
python3 Python-Scripts/EnumerateUsers_lookup.py
 ```

> ⚠️ **Note:** Wordlist paths are hardcoded. Adjust them to match your system before running.

---

<br/>

### Base64 to Image

**Path:** `Python-Scripts/base64_to_img.py`

Converts a file containing base64-encoded data into a PNG image. Useful for steganography and forensics challenges where image data is encoded as text.

| Requirement | Details |
|-------------|---------|
| Python 3 | Standard |
| Dependencies | `pybase64` (`pip install pybase64`) |
| Output | `image.png` in the current working directory |

```bash
pip install pybase64
python3 Python-Scripts/base64_to_img.py
# Enter the filename containing base64 data when prompted
 ```

<br/>
<br/>


---

## 📚 Tips & Resources

Practical technique references you can bookmark and revisit during any CTF session.

### Reverse Shell Upgrade

**Path:** `Tips-&-Resources/Reverse_Shell-Upgrade.md`

A comprehensive guide covering four methods to upgrade a basic reverse shell into a fully interactive TTY:

| Method | When to Use |
|--------|-------------|
| Python PTY (`pty.spawn`) | Python is available on target |
| Full TTY (`stty raw -echo` + env vars) | Best interactive experience; requires Python |
| `/usr/bin/script` | Python unavailable; Linux targets |
| Socat | Socat installed on target (rare) |

Includes troubleshooting tips for zsh users and `rlwrap` alternatives.

[**→ Read the full guide**](Tips-&-Resources/Reverse_Shell-Upgrade.md)

<br/>
<br/>

---

## 🚀 Getting Started

### Browsing Writeups

1. Navigate to the [`WriteUps/`](WriteUps/) directory
2. Choose your platform: `TryHackMe/`, `HackTheBox/`, or `OverTheWire/`
3. Open any `.md` file to read the walkthrough
4. Follow along on your own machine (or the platform's AttackBox)

### Using the Scripts

```bash
# Clone the repository
git clone https://github.com/Maat-Cyber/Maat-Cyber-World.git
cd Maat-Cyber-World

# Make scripts executable
chmod +x Bash-Scripts/*.sh

# Run EasyScan (interactive)
./Bash-Scripts/EasyScan.sh

# Run Python utilities
pip install pybase64 requests
python3 Python-Scripts/base64_to_img.py
python3 Python-Scripts/EnumerateUsers_lookup.py
 ```

<br/>
<br/>


---

## ✅ Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| **nmap** | Port scanning | Pre-installed on Kali; `apt install nmap` |
| **gobuster** | Directory/DNS brute-force | `apt install gobuster` |
| **nikto** | Web vulnerability scanner | `apt install nikto` |
| **ffuf** | Fast web fuzzer | `apt install ffuf` |
| **dirsearch** | Directory enumeration | `apt install dirsearch` |
| **wpscan** | WordPress scanner | `apt install wpscan` |
| **Python 3** | Script runtime | Pre-installed on most distros |
| **SecLists** | Wordlists | `apt install seclists` |
| **Burp Suite** | Web proxy (for writeups) | [Download](https://portswigger.net/burp) |

> 💡 **Tip:** If you are on Kali Linux, most tools are pre-installed. The `EasyScan.sh` script will detect and offer to install any missing dependencies automatically.

<br/>
<br/>


---

## 🤝 Contributing

This is a personal project, but suggestions and collaboration are welcome.

**Ways to contribute:**

- 🐛 **Report errors** in writeups (outdated steps, broken links, typos)
- 💡 **Suggest rooms** you would like to see covered
- 🔧 **Improve scripts** (bug fixes, new features, better portability)
- 🤝 **Group up** to solve challenges together

**To get in touch:**

- 📧 Email: `maatghithub.phobia875@passinbox.com`
- 🌐 Website: [maat-feather.wixsite.com/maat-cyber-world](https://maat-feather.wixsite.com/maat-cyber-world)

If you would like to submit a pull request:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-improvement`)
3. Commit your changes with clear messages
4. Open a pull request describing what you changed and why

<br/>
<br/>

---

## ❓ FAQ

<details>
<summary><strong>Do the writeups contain the actual flags/answers?</strong></summary>

No. By design, walkthroughs provide the methodology and steps to reach the answer, but never the flag itself. This respects platform guidelines and preserves the learning experience.

</details>

<details>
<summary><strong>What OS do I need to follow along?</strong></summary>

The writeups can be followed on any Linux distribution with the appropriate tools installed. Some challenges also work with the platform's built-in AttackBox.

</details>

<details>
<summary><strong>Are the scripts safe to run?</strong></summary>

The scripts are designed for use in CTF lab environments and authorized testing only. `EasyScan.sh` performs active network scanning and should only be run against machines you have explicit permission to test (e.g., TryHackMe/HackTheBox targets). Never run these against systems you do not own or have authorization to test.

</details>

<details>
<summary><strong>How often is the repository updated?</strong></summary>

The repository has been actively maintained from April 2024 through March 2026, with 145 commits. New writeups are added as challenges are completed. Check the [commit history](https://github.com/Maat-Cyber/Maat-Cyber-World/commits/main) for the latest activity.

</details>

<details>
<summary><strong>Can I use these writeups for teaching or study groups?</strong></summary>

Yes. The content is educational in nature. Credit the repository when sharing. Do not redistribute the writeups as your own work.

</details>

<details>
<summary><strong>I found a mistake in a writeup. What do I do?</strong></summary>

Open an issue on GitHub or send an email to the contact address above. Include the file name, the section with the error, and what the correct information should be.

</details>


<br/>
<br/>

---

## 🔗 Connect

| Platform | Link |
|----------|------|
| 🌐 Website | [maat-feather.wixsite.com/maat-cyber-world](https://maat-feather.wixsite.com/maat-cyber-world) |
| 🎮 TryHackMe | [Profile](https://tryhackme.com) *(linked in repo)* |
| 📧 Email | `maatghithub.phobia875@passinbox.com` |
| 🐙 GitHub | [github.com/Maat-Cyber](https://github.com/Maat-Cyber) |

---

<div align="center">

**Happy Hacking! 💻🏴‍☠️**

*Built with love by Maat*

</div>
