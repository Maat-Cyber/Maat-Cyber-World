# ☀️ Hacker Holidays 2026

Welcome to the **Hacker Holidays 2026** writeups directory! 🍹

This event takes us on a virtual vacation to the luxurious (and highly vulnerable) **Byte Lotus Hotel**. 

The challenges range from easy to medium, covering a mix of OSINT, web exploitation, forensics, and privilege escalation. Whether you're lounging by the pool or grabbing a drink at the beach bar, there's plenty of security misconfigurations to exploit!

---

## 🧭 Quick Navigation

- 📋 Index by Category
  - 🌐 Web Exploitation & Cloud
  - 🕵️ OSINT & Forensics
- 🏖️ Event Overview

---

<a id="index-by-category"></a>
## 📋 Index by Category

<a id="web-exploitation--cloud"></a>
### 🌐 Web Exploitation & Cloud

The largest category in this event. Covers application logic flaws, cloud misconfigurations, injection attacks, and source code disclosure.

| Writeup | Difficulty | Key Techniques |
| :--- | :---: | :--- |
| 🍹 **Beach Bar** | Easy | Unsafe YAML deserialization, Python reverse shell, systemd plaintext credential leak |
| 🧖 **Complimentary** | Easy | AWS Cognito misconfiguration, overprivileged IAM roles, DynamoDB scan bypass |
| 🚪 **Do Not Disturb** | Medium | NoSQL injection bypass, EJS Server-Side Template Injection (SSTI), Node.js V8 Inspector privesc |
| 🐚 **The Hollow Shell** | Medium | ZIP SLIP path traversal, arbitrary file overwrite, Python hook execution for RCE |
| 🏊 **Infinity Pool** | Medium | Web command injection, SSH key injection, internal API enumeration, root privilege escalation via Gunicorn command injection |
| 🛏️ **Room 404** | Easy | Exposed `.git` directory, source code disclosure via `git-dumper`, ripgrep |
| 🏖️ **Towel on the Sunbed** | Medium | Race condition (TOCTOU) exploitation, Burp Suite parallel requests, Express.js logic flaw bypass |

<a id="osint--forensics"></a>
### 🕵️ OSINT & Forensics

Challenges focused on open-source intelligence gathering and network traffic analysis.

| Writeup | Difficulty | Key Techniques |
| :--- | :---: | :--- |
| 🌃 **After Hours** | Medium | Windows WMI repository forensics, fileless persistence analysis, UTF-16LE string extraction, Base64 payload decoding |
| 🥐 **OverHeard at Breakfast** | Easy | OSINT, Gravatar email lookup, Base64 decoding |
| 🧳 **Packed Light** | Easy | PCAP network forensics, Wireshark stream analysis, Custom Python C2, Base64 + XOR decryption |

---

<a id="event-overview"></a>
## 🏖️ Event Overview

The **Hacker Holidays 2026** series is centered around a single fictional narrative: a stay at the **Byte Lotus Hotel**. Every room tells a different story of poor operational security, rushed deployments, and leaked secrets.

*   **The Vibe:** Tropical, relaxed, and full of hidden vulnerabilities. 🌴
*   **The Goal:** Hack your way through the resort, from the beachside jukebox to the poolside cabana management portal. 🎯
*   **The Skills:** A well-rounded mix of cloud security (AWS), web application attacks, cryptography, and Linux privilege escalation. 🛠️

---

> 💡 **Tip:** If you get stuck on the AWS challenges, ensure your `awscli` is properly configured with the temporary credentials extracted from Cognito! For the forensics challenges, don't be afraid to drop into Wireshark and follow those TCP streams. 

Happy Hacking! 💻✈️🌴
