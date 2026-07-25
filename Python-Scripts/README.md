<div align=center>

# 🐍 Python Scripts

Custom Python utilities built for CTF challenges, forensics tasks, and quick automation during security assessments. Every script in this directory is **standalone**, **dependency-light**, and ready to drop into your CTF toolkit.

</div>

---

## 📑 Table of Contents

- [🐍 Python Scripts](#-python-scripts)
  - [📑 Table of Contents](#-table-of-contents)
  - [📂 Scripts Index](#-scripts-index)
  - [🔍 EnumerateUsers (Lookup)](#-enumerateusers-lookup)
    - [What It Does](#what-it-does)
    - [Requirements](#requirements)
    - [Usage](#usage)
    - [How It Works](#how-it-works)
    - [⚠️ Notes](#️-notes)
  - [🖼️ Base64 to Image](#️-base64-to-image)
    - [What It Does](#what-it-does-1)
    - [Requirements](#requirements-1)
    - [Usage](#usage-1)
    - [How It Works](#how-it-works-1)
    - [⚠️ Notes](#️-notes-1)
  - [🚀 Quick Setup (All Scripts)](#-quick-setup-all-scripts)
  - [🧩 Script Template](#-script-template)
  - [⚠️ Disclaimer](#️-disclaimer)
  - [🔗 Related](#-related)

<br/>
<br/>

---

## 📂 Scripts Index

| # | Script | Category | Use Case | Dependencies |
|---|--------|----------|----------|--------------|
| 1 | [`EnumerateUsers_lookup.py`](#-enumerateusers-lookup) | Web / Auth | Username enumeration + password brute-force | `requests` |
| 2 | [`base64_to_img.py`](#️-base64-to-image) | Forensics / Stego | Decode base64 text into a PNG image | `pybase64` |

> 📌 **This directory is growing.** New scripts are added as CTF challenges demand them. Check back often or ⭐ the repo to stay updated.

<br/>
<br/>

---

## 🔍 EnumerateUsers (Lookup)

**File:** [`EnumerateUsers_lookup.py`](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Python-Scripts/EnumerateUsers_lookup.py)
**Built for:** [TryHackMe — Lookup](https://tryhackme.com/room/lookup)

### What It Does

A two-stage authentication attack script:

| Stage | Action | Technique |
|-------|--------|-----------|
| **1 — Enumeration** | Sends login requests with a dummy password against a list of usernames | Detects valid users by comparing error messages (`"Wrong password"` vs. generic failure) |
| **2 — Brute-Force** | Asks for confirmation, then iterates a password list against the discovered username | Stops on first successful login |

<br/>

### Requirements

| Requirement | Details | Install |
|-------------|---------|---------|
| **Python 3** | Runtime | Pre-installed on most distros |
| **requests** | HTTP library | `pip install requests` |
| **names.txt** | Username wordlist | `/usr/share/seclists/Usernames/Names/names.txt` |
| **rockyou.txt** | Password wordlist | `/home/blackarch/Documents/rockyou.txt` *(edit path in script)* |

<br/>

### Usage

```bash
python3 EnumerateUsers_lookup.py
```

**Interactive flow:**

```
found a valid username jsmith
...
do you now want to brute-force it? yes/no
> yes
found a valid password s3cur3P@ss!
jsmith : s3cur3P@ss!
```

<br/>

### How It Works

```
┌─────────────────────────────────────────────────┐
│  1. Load usernames from names.txt (first 5000)  │
│  2. POST each username + dummy password          │
│  3. If response contains "Wrong password"        │
│     → username is VALID → stop enumeration       │
│  4. Prompt: brute-force? (yes/no)                │
│  5. Load passwords from rockyou.txt (first 5000) │
│  6. POST valid username + each password          │
│  7. If error message disappears                  │
│     → password FOUND → print credentials         │
└─────────────────────────────────────────────────┘
```

<br/>

### ⚠️ Notes

- **Wordlist paths are hardcoded.** Edit the two `open()` paths at the top of the script to match your system:
  ```python
  # Change these to your paths:
  '/usr/share/seclists/Usernames/Names/names.txt'
  '/home/blackarch/Documents/rockyou.txt'
  ```
- **Target URL is hardcoded** to `http://lookup.thm/login.php`. Modify the `url` variable for other targets.
- Reads only the **first 5,000 entries** from each wordlist to keep runtime manageable. Adjust the `range()` value if needed.
- The `admin` username is **excluded** from valid results (common default account).

<br/>
<br/>

---

## 🖼️ Base64 to Image

**File:** [`base64_to_img.py`](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Python-Scripts/base64_to_img.py)
**Built for:** Steganography & forensics CTF challenges

### What It Does

Reads a text file containing a **base64-encoded string**, decodes it, and writes the result as **`image.png`** in the current working directory.

| Input | Output |
|-------|--------|
| Text file with base64 data | `image.png` in CWD |

### Requirements

| Requirement | Details | Install |
|-------------|---------|---------|
| **Python 3** | Runtime | Pre-installed on most distros |
| **pybase64** | Fast base64 codec | `pip install pybase64` |

<br/>

### Usage

```bash
pip install pybase64
python3 base64_to_img.py
```

**Interactive flow:**

```
insert the name of the file with the base64 encoded data,
the image will be saved in the CWD as image.png
> encoded_data.txt
✅ image.png created successfully
```

<br/>

### How It Works

```
┌──────────────────────────────────────────┐
│  1. Prompt for input filename            │
│  2. Read the entire file as text         │
│  3. Decode base64 → raw bytes            │
│  4. Write bytes to image.png (wb mode)   │
│  5. Done — open image.png to view        │
└──────────────────────────────────────────┘
```

<br/>


### ⚠️ Notes

- Output is **always `image.png`**. If the decoded data is actually a JPEG, GIF, or BMP, rename the extension manually:
  ```bash
  mv image.png image.jpg   # if the source was a JPEG
  ```
- The script uses `pybase64` for speed. You can swap it with the stdlib `base64` module if you prefer zero dependencies:
  ```python
  import base64
  decoded_data = base64.b64decode(encoded_data)
  ```
- If the base64 string contains **data-URI headers** (e.g., `data:image/png;base64,iVBOR...`), strip the prefix before feeding it to the script.

<br/>
<br/>

---

## 🚀 Quick Setup (All Scripts)

```bash
# Clone the repo
git clone https://github.com/Maat-Cyber/Maat-Cyber-World.git
cd Maat-Cyber-World/Python-Scripts

# Install all Python dependencies at once
pip install requests pybase64

# Run a script
python3 base64_to_img.py
python3 EnumerateUsers_lookup.py
```

<br/>
<br/>

---

## 🧩 Script Template

Want to add your own script to this directory? Follow this structure to keep things consistent:

```python
#!/usr/bin/env python3
"""
Script Name : your_script.py
Author      : Maat
Category    : Web / Forensics / Crypto / Recon / ...
Use Case    : One-line description
Dependencies: list any pip packages needed
"""

# --- imports ---

# --- config / constants ---

# --- main logic ---

# --- entry point ---
if __name__ == "__main__":
    main()
```

**Checklist before committing:**

- [ ] Shebang line (`#!/usr/bin/env python3`)
- [ ] Docstring with name, category, use case, dependencies
- [ ] No hardcoded secrets or personal paths (use variables at the top)
- [ ] Tested on at least one CTF challenge
- [ ] Added to the [Scripts Index](#-scripts-index) table above

<br/>
<br/>

---

## ⚠️ Disclaimer

> **These scripts are for authorized security testing, CTF competitions, and educational purposes only.**
>
> Running enumeration or brute-force tools against systems you do **not** own or have **explicit written permission** to test is **illegal**. The author assumes no liability for misuse.
>
> Always operate within the rules of engagement of your CTF platform (TryHackMe, HackTheBox, OverTheWire, etc.) or your authorized pentest scope.

<br/>
<br/>

---

## 🔗 Related

| Resource | Link |
|----------|------|
| 🏠 Main Repository | [Maat-Cyber-World](https://github.com/Maat-Cyber/Maat-Cyber-World) |
| 🐚 Bash Scripts | [`Bash-Scripts/`](https://github.com/Maat-Cyber/Maat-Cyber-World/tree/main/Bash-Scripts) |
| 📖 Tips & Resources | [`Tips-&-Resources/`](https://github.com/Maat-Cyber/Maat-Cyber-World/tree/main/Tips-%26-Resources) |
| 📝 CTF Writeups | [`WriteUps/`](https://github.com/Maat-Cyber/Maat-Cyber-World/tree/main/WriteUps) |
| 🔄 Reverse Shell Upgrade Guide | [`Reverse_Shell-Upgrade.md`](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) |

<br/>

---

**Happy Hacking! 💻🏴‍☠️**

_Built with love by [Maat](https://github.com/Maat-Cyber)_
