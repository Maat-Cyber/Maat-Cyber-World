<div align=center>

# 📝 CTF WriteUps

**111 detailed walkthroughs** across TryHackMe, HackTheBox, and OverTheWire.

Covering web exploitation, privilege escalation, forensics, cryptography, OSINT, blue team, and more. 

Every writeup documents the full attack chain: recon → enumeration → exploitation → root/system → lessons learned.

</div>

---

## 📑 Table of Contents

- [📝 CTF WriteUps](#-ctf-writeups)
  - [📑 Table of Contents](#-table-of-contents)
  - [📊 Stats at a Glance](#-stats-at-a-glance)
  - [📂 Directory Structure](#-directory-structure)
  - [🟩 HackTheBox (7)](#-hackthebox-7)
  - [🟨 OverTheWire (3)](#-overthewire-3)
  - [🔴 TryHackMe (101)](#-tryhackme-101)
    - [📦 Collections / Multi-Part Series](#-collections--multi-part-series)
      - [🎂 3-Million-Special (3 writeups)](#-3-million-special-3-writeups)
      - [👻 Boogeyman (3 writeups)](#-boogeyman-3-writeups)
      - [🎮 The Game (2 writeups)](#-the-game-2-writeups)
      - [💘 Valentine 2026 (7 writeups)](#-valentine-2026-7-writeups)
    - [📋 All Rooms (A–Z)](#-all-rooms-az)
  - [🧭 How to Read a WriteUp](#-how-to-read-a-writeup)
  - [🚀 Start Here (Beginner Path)](#-start-here-beginner-path)
  - [🤝 Contributing](#-contributing)
  - [🔗 Related Resources](#-related-resources)
  - [⚠️ Disclaimer](#️-disclaimer)

<br/>
<br/>

---

## 📊 Stats at a Glance

| Metric | Count |
|--------|-------|
| 📝 Total WriteUps | **111** |
| 🔴 TryHackMe | 101 (86 rooms + 4 collections) |
| 🟩 HackTheBox | 7 |
| 🟨 OverTheWire | 3 |
| 📦 Multi-part series | 4 (Boogeyman, The Game, 3-Million-Special, Valentine-2026) |
| 🐧 Linux targets | majority |
| 🪟 Windows targets | ~15+ |
| 🔵 Blue Team / DFIR | ~10+ |

<br/>
<br/>

---

## 📂 Directory Structure

```
WriteUps/
│
├── HackTheBox/                    ← 7 machines + index + usage guide
│   ├── README.md                  ← HTB index
│   ├── Usage.md                   ← How to approach HTB machines
│   ├── Bizness.md
│   ├── Cap.md
│   ├── Devvortex.md
│   ├── Headless.md
│   ├── Perfection.md
│   ├── PermX.md
│   └── WifineticTwo.md
│
├── OverTheWire/                   ← 3 wargames + index
│   ├── README.md                  ← OTW index
│   ├── Bandit.md
│   ├── Leviathan.md
│   └── Natas.md
│
└── TryHackMe/                     ← 101 writeups + index
    ├── README.md                  ← THM index
    │
    ├── 3-million-special/         ← 📦 Collection (3)
    │   ├── Bricks_Heist.md
    │   ├── Sch3Ma_D3Mon.md
    │   └── TryHack3M-Subscribe.md
    │
    ├── Boogeyman/                 ← 📦 Collection (3)
    │   ├── Boogeyman_1.md
    │   ├── Boogeyman_2.md
    │   └── Boogeyman_3.md
    │
    ├── The-Game/                  ← 📦 Collection (2)
    │   ├── The-Game.md
    │   └── The-Game-v2.md
    │
    ├── Valentine-2026/            ← 📦 Collection (7)
    │   ├── Corp-Website.md
    │   ├── Cupid's-Matchmaker.md
    │   ├── Cupid-Bot.md
    │   ├── Love-Letter-Locker.md
    │   ├── TryHeartMe.md
    │   ├── Valenfind.md
    │   └── When-Hearts-Collide.md
    │
    ├── Alfred.md                  ← 86 individual rooms
    ├── Archangel.md
    ├── ... (see full index below)
    └── Whiterose.md
```

<br/>
<br/>

---

## 🟩 HackTheBox (7)

> 📖 Full index & methodology: [`HackTheBox/README.md`](HackTheBox/README.md) · Approach guide: [`HackTheBox/Usage.md`](HackTheBox/Usage.md)

| # | Machine | Link |
|---|---------|------|
| 1 | **Bizness** | [→ WriteUp](HackTheBox/Bizness.md) |
| 2 | **Cap** | [→ WriteUp](HackTheBox/Cap.md) |
| 3 | **Devvortex** | [→ WriteUp](HackTheBox/Devvortex.md) |
| 4 | **Headless** | [→ WriteUp](HackTheBox/Headless.md) |
| 5 | **Perfection** | [→ WriteUp](HackTheBox/Perfection.md) |
| 6 | **PermX** | [→ WriteUp](HackTheBox/PermX.md) |
| 7 | **WifineticTwo** | [→ WriteUp](HackTheBox/WifineticTwo.md) |

<br/>
<br/>

---

## 🟨 OverTheWire (3)

> 📖 Full index: [`OverTheWire/README.md`](OverTheWire/README.md)

| # | Wargame | Levels | Focus | Link |
|---|---------|--------|-------|------|
| 1 | **Bandit** | 0–34 | Linux CLI, SSH, file permissions, piping | [→ WriteUp](OverTheWire/Bandit.md) |
| 2 | **Leviathan** | 0–7 | Linux privilege escalation, SUID, logic flaws | [→ WriteUp](OverTheWire/Leviathan.md) |
| 3 | **Natas** | 0–34 | Web security, HTTP, injection, auth bypass | [→ WriteUp](OverTheWire/Natas.md) |

<br/>
<br/>

---

## 🔴 TryHackMe (101)

> 📖 Full index: [`TryHackMe/README.md`](TryHackMe/README.md)

### 📦 Collections / Multi-Part Series

#### 🎂 3-Million-Special (3 writeups)

| # | Challenge | Link |
|---|-----------|------|
| 1 | **Bricks Heist** | [→ WriteUp](TryHackMe/3-million-special/Bricks_Heist.md) |
| 2 | **Sch3Ma D3Mon** | [→ WriteUp](TryHackMe/3-million-special/Sch3Ma_D3Mon.md) |
| 3 | **TryHack3M Subscribe** | [→ WriteUp](TryHackMe/3-million-special/TryHack3M-Subscribe.md) |

#### 👻 Boogeyman (3 writeups)

| # | Challenge | Link |
|---|-----------|------|
| 1 | **Boogeyman 1** | [→ WriteUp](TryHackMe/Boogeyman/Boogeyman_1.md) |
| 2 | **Boogeyman 2** | [→ WriteUp](TryHackMe/Boogeyman/Boogeyman_2.md) |
| 3 | **Boogeyman 3** | [→ WriteUp](TryHackMe/Boogeyman/Boogeyman_3.md) |

#### 🎮 The Game (2 writeups)

| # | Challenge | Link |
|---|-----------|------|
| 1 | **The Game** | [→ WriteUp](TryHackMe/The-Game/The-Game.md) |
| 2 | **The Game v2** | [→ WriteUp](TryHackMe/The-Game/The-Game-v2.md) |

#### 💘 Valentine 2026 (7 writeups)

| # | Challenge | Link |
|---|-----------|------|
| 1 | **Corp Website** | [→ WriteUp](TryHackMe/Valentine-2026/Corp-Website.md) |
| 2 | **Cupid's Matchmaker** | [→ WriteUp](TryHackMe/Valentine-2026/Cupid's-Matchmaker.md) |
| 3 | **Cupid Bot** | [→ WriteUp](TryHackMe/Valentine-2026/Cupid-Bot.md) |
| 4 | **Love Letter Locker** | [→ WriteUp](TryHackMe/Valentine-2026/Love-Letter-Locker.md) |
| 5 | **TryHeartMe** | [→ WriteUp](TryHackMe/Valentine-2026/TryHeartMe.md) |
| 6 | **Valenfind** | [→ WriteUp](TryHackMe/Valentine-2026/Valenfind.md) |
| 7 | **When Hearts Collide** | [→ WriteUp](TryHackMe/Valentine-2026/When-Hearts-Collide.md) |

<br/>

---

### 📋 All Rooms (A–Z)

> 86 individual room writeups, sorted alphabetically.

| # | Room | Link |
|---|------|------|
| 1 | **Alfred** | [→ WriteUp](TryHackMe/Alfred.md) |
| 2 | **Archangel** | [→ WriteUp](TryHackMe/Archangel.md) |
| 3 | **b3dr0ck** | [→ WriteUp](TryHackMe/b3dr0ck.md) |
| 4 | **Benign** | [→ WriteUp](TryHackMe/Benign.md) |
| 5 | **Brains** | [→ WriteUp](TryHackMe/Brains.md) |
| 6 | **Break-it** | [→ WriteUp](TryHackMe/Break-it.md) |
| 7 | **Carnage** | [→ WriteUp](TryHackMe/Carnage.md) |
| 8 | **Cat Pictures 2** | [→ WriteUp](TryHackMe/Cat-Pictures-2.md) |
| 9 | **CheckMate** | [→ WriteUp](TryHackMe/CheckMate.md) |
| 10 | **Chill Hack** | [→ WriteUp](TryHackMe/Chill-Hack.md) |
| 11 | **Ciphers Secret Message** | [→ WriteUp](TryHackMe/Ciphers-Secret-Message.md) |
| 12 | **Compiled** | [→ WriteUp](TryHackMe/Compiled.md) |
| 13 | **Convert my Video** | [→ WriteUp](TryHackMe/Convert-my-Video.md) |
| 14 | **Corridor** | [→ WriteUp](TryHackMe/Corridor.md) |
| 15 | **Creative** | [→ WriteUp](TryHackMe/Creative.md) |
| 16 | **Critical** | [→ WriteUp](TryHackMe/Critical.md) |
| 17 | **Cryptosystem** | [→ WriteUp](TryHackMe/Cryptosystem.md) |
| 18 | **CTF Collection Vol. 1** | [→ WriteUp](TryHackMe/CTF-Collection-Vol-1.md) |
| 19 | **CyberHeroes** | [→ WriteUp](TryHackMe/CyberHeroes.md) |
| 20 | **Cyborg** | [→ WriteUp](TryHackMe/Cyborg.md) |
| 21 | **D2PDF** | [→ WriteUp](TryHackMe/D2PDF.md) |
| 22 | **Digital Footprint** | [→ WriteUp](TryHackMe/Digital-Footprint.md) |
| 23 | **Disgruntled** | [→ WriteUp](TryHackMe/Disgruntled.md) |
| 24 | **EasyPeasy** | [→ WriteUp](TryHackMe/EasyPeasy.md) |
| 25 | **ElBandito** | [→ WriteUp](TryHackMe/ElBandito.md) |
| 26 | **Evil GPT** | [→ WriteUp](TryHackMe/Evil-GPT.md) |
| 27 | **Exfilnode** | [→ WriteUp](TryHackMe/Exfilnode.md) |
| 28 | **Extracted** | [→ WriteUp](TryHackMe/Extracted.md) |
| 29 | **Friday Overtime** | [→ WriteUp](TryHackMe/Friday-Overtime.md) |
| 30 | **Game Zone** | [→ WriteUp](TryHackMe/Game-Zone.md) |
| 31 | **Glitch** | [→ WriteUp](TryHackMe/Glitch.md) |
| 32 | **Grep CTF** | [→ WriteUp](TryHackMe/Grep_CTF.md) |
| 33 | **hackerNote** | [→ WriteUp](TryHackMe/hackerNote.md) |
| 34 | **HackPark** | [→ WriteUp](TryHackMe/HackPark.md) |
| 35 | **Hammer** | [→ WriteUp](TryHackMe/Hammer.md) |
| 36 | **Hidden Deep Into My Heart** | [→ WriteUp](TryHackMe/Hidden-Deep-Into-My-Heart.md) |
| 37 | **Ide** | [→ WriteUp](TryHackMe/Ide.md) |
| 38 | **Include** | [→ WriteUp](TryHackMe/Include.md) |
| 39 | **Infinity Shell** | [→ WriteUp](TryHackMe/Infinity-Shell.md) |
| 40 | **Injectics** | [→ WriteUp](TryHackMe/Injectics.md) |
| 41 | **Investigating with Splunk** | [→ WriteUp](TryHackMe/Investigating_with_Splunk.md) |
| 42 | **Invite Only** | [→ WriteUp](TryHackMe/Invite-Only.md) |
| 43 | **IronShade** | [→ WriteUp](TryHackMe/IronShade.md) |
| 44 | **ItsyBitsy** | [→ WriteUp](TryHackMe/ItsyBitsy.md) |
| 45 | **JPGchat** | [→ WriteUp](TryHackMe/JPGchat.md) |
| 46 | **Light** | [→ WriteUp](TryHackMe/Light.md) |
| 47 | **Lo-Fi** | [→ WriteUp](TryHackMe/Lo-Fi.md) |
| 48 | **Lookup** | [→ WriteUp](TryHackMe/Lookup.md) |
| 49 | **Mac Hunt** | [→ WriteUp](TryHackMe/Mac-Hunt.md) |
| 50 | **Masterminds** | [→ WriteUp](TryHackMe/Masterminds.md) |
| 51 | **mKingdom** | [→ WriteUp](TryHackMe/mKingdom.md) |
| 52 | **Monday Monitor** | [→ WriteUp](TryHackMe/Monday-Monitor.md) |
| 53 | **Mother's Secret** | [→ WriteUp](TryHackMe/Mother's-Secret.md) |
| 54 | **MrPhisher** | [→ WriteUp](TryHackMe/MrPhisher.md) |
| 55 | **New Hire Old Artifacts** | [→ WriteUp](TryHackMe/New-Hire-Old-Artifacts.md) |
| 56 | **Operation Slither** | [→ WriteUp](TryHackMe/Operation-Slither.md) |
| 57 | **Order** | [→ WriteUp](TryHackMe/Order.md) |
| 58 | **Pickle Rick** | [→ WriteUp](TryHackMe/Pickle-Rick.md) |
| 59 | **Poster** | [→ WriteUp](TryHackMe/Poster.md) |
| 60 | **PownSniff** | [→ WriteUp](TryHackMe/PownSniff.md) |
| 61 | **PrintNightmare Thrice!** | [→ WriteUp](TryHackMe/PrintNightmare-Thrice!.md) |
| 62 | **Publisher** | [→ WriteUp](TryHackMe/Publisher.md) |
| 63 | **Rabbit Store** | [→ WriteUp](TryHackMe/Rabbit-Store.md) |
| 64 | **Retracted** | [→ WriteUp](TryHackMe/Retracted.md) |
| 65 | **Secret Recipe** | [→ WriteUp](TryHackMe/Secret-Recipe.md) |
| 66 | **Shadow Trace** | [→ WriteUp](TryHackMe/Shadow-Trace.md) |
| 67 | **Simple CTF** | [→ WriteUp](TryHackMe/Simple-CTF.md) |
| 68 | **Smol** | [→ WriteUp](TryHackMe/Smol.md) |
| 69 | **Sneaky Patch** | [→ WriteUp](TryHackMe/Sneaky-Patch.md) |
| 70 | **Speed Chatting** | [→ WriteUp](TryHackMe/Speed-Chatting.md) |
| 71 | **Startup** | [→ WriteUp](TryHackMe/Startup.md) |
| 72 | **Summit** | [→ WriteUp](TryHackMe/Summit.md) |
| 73 | **Surfer** | [→ WriteUp](TryHackMe/Surfer.md) |
| 74 | **Takeover** | [→ WriteUp](TryHackMe/Takeover.md) |
| 75 | **Team** | [→ WriteUp](TryHackMe/Team.md) |
| 76 | **Tempest** | [→ WriteUp](TryHackMe/Tempest.md) |
| 77 | **The Cod Caper** | [→ WriteUp](TryHackMe/The-Cod-Caper.md) |
| 78 | **The Sticker Shop** | [→ WriteUp](TryHackMe/The-Sticker-Shop.md) |
| 79 | **Traverse** | [→ WriteUp](TryHackMe/Traverse.md) |
| 80 | **Trooper** | [→ WriteUp](TryHackMe/Trooper.md) |
| 81 | **Tshark Challenges 1-2** | [→ WriteUp](TryHackMe/Tshark-Challenges-1-2_Teamwork-and-Directory.md) |
| 82 | **U.A. High School** | [→ WriteUp](TryHackMe/U.A.-High-School.md) |
| 83 | **UltraTech** | [→ WriteUp](TryHackMe/UltraTech.md) |
| 84 | **Unattended** | [→ WriteUp](TryHackMe/Unattended.md) |
| 85 | **W1seGuy** | [→ WriteUp](TryHackMe/W1seGuy.md) |
| 86 | **Whiterose** | [→ WriteUp](TryHackMe/Whiterose.md) |

<br/>
<br/>

---

## 🧭 How to Read a WriteUp

Every writeup in this repository follows a **consistent attack-chain structure**:

| Phase | Section | What You'll Find |
|-------|---------|-----------------|
| 1️⃣ | **Reconnaissance** | `nmap` scans, port discovery, service identification |
| 2️⃣ | **Enumeration** | Directory brute-forcing (`gobuster`, `ffuf`), service-specific enum (SMB, SNMP, web) |
| 3️⃣ | **Exploitation** | Vulnerability identification, CVE research, exploit execution |
| 4️⃣ | **Initial Foothold** | First shell - how we got in and stabilized it |
| 5️⃣ | **Privilege Escalation** | `linpeas` / `winpeas`, SUID, kernel exploits, misconfigs |
| 6️⃣ | **Post-Exploitation** | Flag capture, data exfiltration, persistence |
| 7️⃣ | **Lessons Learned** | Key takeaways for future engagements |
| 8️⃣ | **Tools Used** | Full tool list with links |
| 9️⃣ | **References** | CVEs, articles, documentation consulted |

> 💡 **Tip:** Jump to **Lessons Learned** if you just want the key takeaways without re-reading the full walkthrough.

---

<br/>
<br/>

## 🚀 Start Here (Beginner Path)

New to CTFs? Follow this recommended order to build skills progressively:

```
 ① OverTheWire: Bandit        → Linux CLI fundamentals (0–34 levels)
 ② Pickle Rick                → Web basics, source code inspection
 ③ Corridor                   → IDOR, web logic flaws
 ④ Simple CTF                 → CMS enumeration, basic privesc
 ⑤ Game Zone                  → SQL injection, SSH tunneling
 ⑥ Archangel                  → LFI, SUID exploitation
 ⑦ Chill Hack                 → Command injection, multiple privesc paths
 ⑧ UltraTech                  → Docker, API enumeration
 ⑨ HackPark                   → Windows, service exploitation
 ⑩ Alfred                     → Jenkins RCE, Windows token impersonation
```

> After these 10, explore the **collections** (Boogeyman, Valentine-2026) and then try **HackTheBox** machines for a harder challenge.

<br/>
<br/>

---

## 🤝 Contributing
All writeups are written by myself by hand, but if you want to contribute follow this steps:

1. **Fork** the repository
2. **Create** your writeup `.md` file in the correct platform directory
3. **Follow** the template structure above - no skipping sections
4. **Add** screenshots where they clarify a step
5. **Update** the relevant index table in this README
6. **Open** a Pull Request with a short description

**Style guidelines:**

- Wrap all commands in ` ```bash ` code blocks
- Redact personal IPs with `10.10.x.x` placeholders
- Link every CVE to its NVD / Exploit-DB page
- Keep the tone educational - explain **why**, not just **what**
- Name files in `PascalCase.md` or `kebab-case.md` (match existing convention)

---

## 🔗 Related Resources

| Resource | Link |
|----------|------|
| 🏠 Main Repository | [Maat-Cyber-World](https://github.com/Maat-Cyber/Maat-Cyber-World) |
| 🐚 Bash Scripts | [`Bash-Scripts/`](https://github.com/Maat-Cyber/Maat-Cyber-World/tree/main/Bash-Scripts) |
| 🐍 Python Scripts | [`Python-Scripts/`](https://github.com/Maat-Cyber/Maat-Cyber-World/tree/main/Python-Scripts) |
| 📖 Tips & Resources | [`Tips-&-Resources/`](https://github.com/Maat-Cyber/Maat-Cyber-World/tree/main/Tips-%26-Resources) |
| 🔄 Reverse Shell Upgrade Guide | [`Reverse_Shell-Upgrade.md`](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) |
| 🌐 TryHackMe | [tryhackme.com](https://tryhackme.com/) |
| 🌐 HackTheBox | [hackthebox.com](https://www.hackthebox.com/) |
| 🌐 OverTheWire | [overthewire.org](https://overthewire.org/) |

<br/>
<br/>

---

## ⚠️ Disclaimer

> **These writeups are for educational purposes only.**
>
> They document solutions to **intentionally vulnerable** CTF challenges and lab environments. Do **not** use any techniques described here against systems you do not own or have explicit written permission to test.
>
> Always practice ethically and within the rules of the platform you're using.

<br/>

---

**Happy Hacking! 💻🏴‍☠️**

_Built with love by [Maat](https://github.com/Maat-Cyber)_
