# ☀️ Hacker Holidays 2026

Welcome to the **Hacker Holidays 2026** writeups directory! 🍹

This event takes us on a virtual vacation to the luxurious (and highly vulnerable) **Byte Lotus Hotel**. 

The challenges range from easy to hard, covering a mix of OSINT, web exploitation, forensics, and privilege escalation. Whether you're lounging by the pool or grabbing a drink at the beach bar, there's plenty of security misconfigurations to exploit!

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
| 🔑 **Crypto Cabana** | Medium | Source code disclosure (JavaScript), Azure Blob Storage SAS token enumeration, Azure Key Vault secret version analysis |
| 🚪 **Do Not Disturb** | Medium | NoSQL injection bypass, EJS Server-Side Template Injection (SSTI), Node.js V8 Inspector privesc |
| 🏊 **Infinity Pool** | Medium | Web command injection, SSH key injection, internal API enumeration, root privilege escalation via Gunicorn command injection |
| 🛏️ **Room 404** | Easy | Exposed `.git` directory, source code disclosure via `git-dumper`, ripgrep |
| 🤖 **The Guestbook** | Medium | LLM prompt injection (VERA AI), command execution (`override` directive), base64 encoding to bypass redaction filters |
| 🐚 **The Hollow Shell** | Medium | ZIP SLIP path traversal, arbitrary file overwrite, Python hook execution for RCE |
| 🏖️ **Towel on the Sunbed** | Medium | Race condition (TOCTOU) exploitation, Burp Suite parallel requests, Express.js logic flaw bypass |

<a id="osint--forensics"></a>
### 🕵️ OSINT & Forensics

Challenges focused on open-source intelligence gathering and network traffic analysis.

| Writeup | Difficulty | Key Techniques |
| :--- | :---: | :--- |
| 🌃 **After Hours** | Medium | Windows WMI repository forensics, fileless persistence analysis, UTF-16LE string extraction, Base64 payload decoding |
| 💻 **Management Wants a Word** | Hard | Windows memory dump analysis (SAM/SECURITY hives), `secretsdump.py` & `Hashcat` cracking, DPAPI master key decryption, Chrome login data extraction, VeraCrypt container mounting |
| 🥐 **OverHeard at Breakfast** | Easy | OSINT, Gravatar email lookup, Base64 decoding |
| 🧳 **Packed Light** | Easy | PCAP network forensics, Wireshark stream analysis, Custom Python C2, Base64 + XOR decryption |

---

<a id="event-overview"></a>
## 🏖️ Event Overview

The **Hacker Holidays 2026** series is centered around a single fictional narrative: a stay at the **Byte Lotus Hotel**. Every room tells a different story of poor operational security, rushed deployments, and leaked secrets.

*   **The Vibe:** Tropical, relaxed, and full of hidden vulnerabilities. 🌴
*   **The Goal:** Hack your way through the resort, from the beachside jukebox to the poolside cabana management portal. 🎯
*   **The Skills:** A well-rounded mix of cloud security (AWS & Azure), web application attacks, LLM exploitation, cryptography, and Windows/Linux forensics. 🛠️

---

> 💡 **Tip:** If you get stuck on the AWS challenges, ensure your `awscli` is properly configured with the temporary credentials extracted from Cognito! For the forensics challenges, don't be afraid to drop into Wireshark and follow those TCP streams. For the Azure challenge, use the Azure CLI (`az`) to easily inspect the Key Vault secrets!

Happy Hacking! 💻✈️🌴
