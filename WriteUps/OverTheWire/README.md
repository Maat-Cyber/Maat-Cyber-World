<div align="center">

# 🔌 OverTheWire Writeups

## Wargame walkthroughs for 3 progressive series

[![Wargames](https://img.shields.io/badge/Wargames-3-F5A623?style=for-the-badge)](#-wargame-index) [![Levels](https://img.shields.io/badge/Levels_Covered-67-F5A623?style=for-the-badge)](#-wargame-index)
[![Platform](https://img.shields.io/badge/Platform-OverTheWire-F5A623?style=for-the-badge&logo=overthewire&logoColor=white)](https://overthewire.org) [![Access](https://img.shields.io/badge/Access-SSH%20%2B%20Browser-333333?style=for-the-badge)](#-how-to-use-these-writeups)

</div>

---

## 📑 Table of Contents

- [� OverTheWire Writeups](#-overthewire-writeups)
  - [Wargame walkthroughs for 3 progressive series](#wargame-walkthroughs-for-3-progressive-series)
  - [📑 Table of Contents](#-table-of-contents)
  - [🎯 Philosophy](#-philosophy)
  - [📖 How to Use These Writeups](#-how-to-use-these-writeups)
  - [📋 Wargame Index](#-wargame-index)
  - [🔬 Detailed Breakdown](#-detailed-breakdown)
    - [Overview](#overview)
    - [Connection](#connection)
    - [Level Coverage](#level-coverage)
    - [Key Takeaways](#key-takeaways)
    - [Overview](#overview-1)
    - [Connection](#connection-1)
    - [Level Coverage](#level-coverage-1)
    - [Key Takeaways](#key-takeaways-1)
    - [Overview](#overview-2)
    - [Access](#access)
    - [Level Coverage](#level-coverage-2)
    - [Key Takeaways](#key-takeaways-2)
  - [🗺️ Technique Coverage Map](#️-technique-coverage-map)
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
| **Guide, don't spoil** | You get the methodology, the commands, the reasoning. You never get the password handed to you on a silver platter. |
| **Explain the *why*** | Every command is accompanied by an explanation of what it does and why it was chosen. |
| **Reproducible** | Another person following the same steps on the same level should arrive at the same place. |

> 💡 **Note:** OverTheWire wargames are **always available** (no VPN, no subscription, no retired machines). You can follow along at any time, at your own pace, for free.

<br/>
<br/>

---

## 📖 How to Use These Writeups

OverTheWire wargames work differently from traditional CTF platforms. There are no machines to deploy or instances to spin up. You connect directly via SSH (or a browser, for Natas) and progress level by level.

1. **Open a terminal** on your Linux machine (or use any SSH client)
2. **Connect to the first level** using the SSH command provided at the top of each writeup
3. **Open the corresponding `.md` file** from the index below
4. **Follow along level by level**, typing each command yourself and reading the explanation before executing
5. **Use the password you find** at the end of each level to SSH into the next one
6. **Try to solve the next level on your own** before reading ahead

> ⚠️ **Important:** Each level's password is the key to the next. If you skip ahead in the writeup, you will not be able to log in. Progress sequentially.

> 💡 **Tip:** After completing each level, type `exit` to close the SSH session before connecting to the next one. This keeps your terminal clean and avoids confusion between sessions.

<br/>
<br/>

---

## 📋 Wargame Index

| # | Wargame | Levels | Difficulty | Focus | Access | Writeup |
|---|---------|--------|-----------|-------|--------|---------|
| 1 | **Bandit** | 34 (0 → 33) | 🟢 Beginner | Linux CLI fundamentals | SSH (port 2220) | [→](Bandit.md) |
| 2 | **Leviathan** | 8 (0 → 7) | 🟢 Beginner (1/10) | Linux privilege escalation, binary analysis | SSH (port 2223) | [→](Leviathan.md) |
| 3 | **Natas** | 26 (0 → 25)* | 🟡 Beginner → Intermediate | Server-side web security | Browser | [→](Natas.md) |

*\*Natas levels 26+ are marked "To Be Continued" in the writeup. Coverage will be expanded as those levels are completed.*

<br/>
<br/>

---

## 🔬 Detailed Breakdown

<details>
<summary><strong>1. Bandit</strong> (34 levels · Linux CLI · SSH port 2220)</summary>

### Overview

Bandit is the **starting point** for anyone new to OverTheWire and to Linux in general. It teaches essential command-line skills through progressively harder challenges, each requiring you to find a password hidden somewhere on the system.

### Connection

```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
# Password: bandit0
```

### Level Coverage

| Levels | Techniques Introduced |
|--------|----------------------|
| 0 → 5 | `ls`, `cat`, handling special filenames (`-`, spaces), `find`, `file`, `xargs` |
| 5 → 10 | `grep`, `sort`, `uniq`, `wc`, `tar`, `gzip`, `bzip2`, `strings`, `hexdump` |
| 10 → 15 | `base64`, `rot13` (tr), `netcat` (nc), port communication |
| 15 → 20 | `nmap` (port scanning), `openssl` (SSL/TLS), SSH private keys, `chmod`, `diff` |
| 20 → 25 | SUID binaries, `setuid`, cron jobs (`/etc/cron.d/`), `crontab` analysis |
| 25 → 30 | `git` (clone, log, show, diff), SSH key authentication, `git stash` |
| 30 → 33 | Shell escape (`$0`), uppercase shell bypass, reading `/etc/bandit_pass/` |

### Key Takeaways

- Bandit builds the **muscle memory** every security practitioner needs: file navigation, text processing, encoding/decoding, networking basics
- The difficulty curve is gentle but steady. By level 20 you will be using nmap, SSH keys, and cron job analysis confidently
- The final levels introduce version control (git) and shell escape techniques that appear constantly in real CTFs

</details>

<details>
<summary><strong>2. Leviathan</strong> (8 levels · Privilege Escalation · SSH port 2223)</summary>

### Overview

Leviathan is a short, focused wargame about **Linux privilege escalation** through SUID binary exploitation. No programming knowledge is required, just common sense and basic Linux commands. Originally hosted on intruded.net, it was rescued and re-hosted on OverTheWire.

### Connection

```bash
ssh leviathan0@leviathan.labs.overthewire.org -p 2223
# Password: leviathan0
```

### Level Coverage

| Levels | Techniques Introduced |
|--------|----------------------|
| 0 → 1 | Hidden directories (`.backup`), `grep` for filtering large files |
| 1 → 2 | SUID binaries, `ltrace` for dynamic analysis, `strcmp` password extraction |
| 2 → 3 | `access()` function bypass, symlink attacks, filename space exploitation |
| 3 → 4 | `ltrace` analysis, `strcmp` string comparison, hardcoded credentials |
| 4 → 5 | Hidden directories (`.trash`), binary-to-text decoding |
| 5 → 6 | Symlink attacks on file paths, `fopen()` exploitation |
| 6 → 7 | 4-digit PIN brute-force, bash scripting for automation, `/bin/bash` shell escalation |
| 7 → 8 | Completion (CONGRATULATIONS file) |

### Key Takeaways

- Leviathan is the perfect **bridge** between Bandit's CLI basics and real-world privilege escalation
- `ltrace` is the star tool here: it reveals function calls, hardcoded strings, and comparison logic inside binaries
- Symlink attacks and SUID exploitation patterns learned here transfer directly to TryHackMe and HackTheBox privesc challenges
- The brute-force level (6 → 7) introduces bash scripting for automation, a skill used extensively in CTF tooling

</details>

<details>
<summary><strong>3. Natas</strong> (26 levels · Web Security · Browser)</summary>

### Overview

Natas teaches **server-side web security** through a series of progressively harder challenges accessed entirely through a web browser. Each level is a small PHP application with a vulnerability that, when exploited, reveals the password for the next level.

### Access

```
http://natas0.natas.labs.overthewire.org
# Username: natas0
# Password: natas0
```

> Change the number after `natas` in the URL to navigate between levels.

### Level Coverage

| Levels | Techniques Introduced |
|--------|----------------------|
| 0 → 3 | View page source, HTML comments, browser developer tools, JavaScript blocking, `robots.txt`, hidden directories |
| 3 → 6 | HTTP `Referer` header manipulation (Burp Suite), cookie inspection and editing, session cookies, PHP `include` file access |
| 6 → 9 | PHP source code analysis, encoding chains (hex → reverse → base64), `grep` command injection, input filter bypass |
| 9 → 12 | Filtered command injection, XOR encryption/decryption, CyberChef, cookie forgery, PHP session manipulation |
| 12 → 14 | File upload bypass (extension swap, magic number / hex editing with `hexedit`), PHP webshells, JPEG header spoofing |
| 14 → 17 | SQL injection (authentication bypass, blind, time-based), `sqlmap`, Python scripting for automated brute-force |
| 17 → 20 | Session ID brute-force (`PHPSESSID`), hexadecimal encoding, PHP session file injection (`\n` injection), co-located site exploitation |
| 20 → 23 | PHP `$_SESSION` manipulation, `revelio` parameter abuse, `strstr()` type juggling, `strcmp()` null bypass (array injection) |
| 23 → 25 | Directory traversal bypass (`....//`), log poisoning via `User-Agent` header, PHP `shell_exec()` in logs, session-based log file access |
| 25 → 26 | PHP object serialization / deserialization *(marked "To Be Continued")* |

### Key Takeaways

- Natas is a **complete web security curriculum** in wargame form: from "view page source" to SQL injection, file upload bypass, and log poisoning
- Burp Suite becomes essential around level 4 and remains the primary tool through the end
- The writeup includes **full Python scripts** for the brute-force levels (15, 16, 17, 18, 19), making it a practical introduction to security scripting
- Multiple solution methods are documented for several levels (e.g., Burp Suite vs. browser dev tools, sqlmap vs. custom Python), encouraging you to find your own approach

</details>

---

## 🗺️ Technique Coverage Map

| Technique | Wargame(s) |
|-----------|-----------|
| File navigation & text processing (`ls`, `cat`, `grep`, `find`, `sort`, `uniq`, `diff`) | Bandit, Leviathan |
| Encoding & decoding (base64, rot13, hex, binary) | Bandit, Natas |
| SSH & key-based authentication | Bandit |
| Port scanning (`nmap`) | Bandit |
| Network communication (`netcat`, `openssl`) | Bandit |
| SUID binary exploitation | Leviathan |
| Dynamic binary analysis (`ltrace`, `strings`) | Leviathan |
| Symlink attacks | Leviathan |
| Brute-force automation (bash / Python) | Bandit, Leviathan, Natas |
| Cron job analysis | Bandit |
| Git version control | Bandit |
| Shell escape (`$0`) | Bandit |
| HTTP header manipulation (`Referer`, `User-Agent`) | Natas |
| Cookie & session manipulation | Natas |
| PHP source code analysis | Natas |
| SQL injection (classic, blind, time-based) | Natas |
| Command injection (`grep`, command substitution) | Natas |
| File upload bypass (extension, magic numbers) | Natas |
| Directory traversal & filter bypass | Natas |
| Log poisoning | Natas |
| XOR encryption / decryption | Natas |
| PHP type juggling (`strcmp`, `strstr`) | Natas |
| PHP session file injection | Natas |

<br/>
<br/>

---

## 🧰 Tools Referenced Across Writeups

| Tool | Category | Appears In |
|------|----------|-----------|
| **SSH** | Remote access | Bandit, Leviathan |
| **nmap** | Port scanning | Bandit |
| **netcat (nc)** | Network communication | Bandit |
| **openssl** | SSL/TLS communication | Bandit |
| **ltrace** | Dynamic binary analysis | Leviathan |
| **strings** | Binary string extraction | Leviathan |
| **Burp Suite** | Web proxy / interception | Natas |
| **sqlmap** | SQL injection automation | Natas |
| **CyberChef** | Encoding / decoding / XOR | Natas |
| **hexedit** | Binary file editing (magic numbers) | Natas |
| **Python 3** | Scripting / automation | Natas |
| **Browser Dev Tools** | Cookie inspection, DOM editing | Natas |
| **git** | Version control | Bandit |
| **grep / find / sort / uniq / diff** | Text processing | Bandit, Leviathan |

> 💡 For reusable automation scripts, check the [`Bash-Scripts/`](../../Bash-Scripts/) and [`Python-Scripts/`](../../Python-Scripts/) directories in the repository root.

<br/>
<br/>

---

## ✅ Prerequisites

| Requirement | Details |
|-------------|---------|
| **Linux machine** (or WSL) | Any distribution works. Kali, Parrot, Arch, Debian, Ubuntu all fine |
| **SSH client** | Pre-installed on all Linux distros (`openssh-client`). Windows users can use PuTTY or WSL |
| **Web browser** | Any modern browser for Natas. Firefox or Chromium recommended for dev tools |
| **Burp Suite Community** | Required for Natas levels 4+. [Download](https://portswigger.net/burp) |
| **Python 3** | Required for Natas brute-force scripts. Pre-installed on most distros |
| **sqlmap** | Optional but recommended for Natas SQLi levels. `apt install sqlmap` |
| **Basic Linux CLI knowledge** | Bandit will teach you from scratch, but knowing how to open a terminal helps |

> 💡 **Tip:** No VPN, no account, no subscription needed. OverTheWire is completely free and always online. Just open a terminal and SSH in.

<br/>
<br/>

---

## 🤝 Contributing & Corrections

Found an error, outdated step, or broken link in a writeup?

- **Open an issue** on the [main repository](https://github.com/Maat-Cyber/Maat-Cyber-World/issues) with the file name and level number
- **Email:** `maatghithub.phobia875@passinbox.com`
- **Pull requests** are welcome. Keep the "guide, don't spoil" philosophy intact

> 📝 **Note:** The Natas writeup currently covers levels 0 through 25. Level 26+ is marked "To Be Continued" and will be added as those levels are completed.

---

<div align="center">

**Now open a terminal, SSH in, and start climbing. The passwords are waiting.** 🏴‍☠️

[← Back to Repository Root](../../README.md) · [TryHackMe Writeups →](../TryHackMe/) · [HackTheBox Writeups →](../HackTheBox/)

</div>
