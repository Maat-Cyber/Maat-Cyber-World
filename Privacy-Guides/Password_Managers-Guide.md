# Password Managers: Your First Line of Defence

## Introduction

In this page we are going to talk about Password Managers as a tool to increase your cyber security and protect your data from third parties.
Every day you access tens of different services and websites and on each of them you carry a portion of your identity.

In order to protect it from criminals and data breaches you have to create a different password for every application, the password has also to be complex and secure.
All this work can easily scare people away from implementing the right protections, here is where password managers come in aid.

These tools are purposely made to store all the user's credentials, passwords and doing the authentication at our place. You have a single app with all your passwords, that will create secure ones, store and use them.
The days when you had to remember all the passphrases are ended, you will only need to remember **one**: the password manager's vault key.

---

## Table of Contents

- [Password Managers: Your First Line of Defence](#password-managers-your-first-line-of-defence)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Are They Safe to Use?](#are-they-safe-to-use)
  - [🔍 Things to Look For](#-things-to-look-for)
    - [➕ For Advanced Users](#-for-advanced-users)
    - [🎁 Bonus: Passkeys Support](#-bonus-passkeys-support)
  - [👍 My Recommendations](#-my-recommendations)
    - [🥇 Best Overall: Bitwarden](#-best-overall-bitwarden)
    - [🥈 Best On-Device: KeePassXC](#-best-on-device-keepassxc)
    - [🥈 Best Self-Hosted: Vaultwarden or KeepassXC + Synchthing](#-best-self-hosted-vaultwarden-or-keepassxc--synchthing)
    - [Great NON-Free Option: 1Password](#great-non-free-option-1password)
    - [Best Built-In Options](#best-built-in-options)
    - [🏅 Honourable Mentions](#-honourable-mentions)
  - [What To Do After](#what-to-do-after)
  - [Warning / Side Note](#warning--side-note)
  - [Comparison Table](#comparison-table)
  - [Conclusion](#conclusion)

<br/>
<br/>

---

## Are They Safe to Use?

Before reaching my suggestions section I want to take a moment to answer a common question: *but if I store all my passwords together isn't it riskier?*

The quick answer is **not really**, as soon as you follow some good practices and you carefully choose the right application.

The reason is also quite simple, a "well made" password manager has purposely been created and is maintained with security in mind:

- All the secrets in your vault are encrypted with a strong cipher (typically **AES-256-GCM** or **ChaCha20-Poly1305**), this means that even if the server gets hacked they won't be able to access your personal data;
- You can enable multi-factor authentication and combine it with a strong unique password to protect the access;
- The application undergoes constant scrutiny and external audits / penetration tests to guarantee its all-around safety;
- The app is correctly maintained, problems are fixed, new solutions and protections are constantly applied to protect the users and the data centres;
- There are even options that let you save your vault fully on your local machine, so you have 100% control of your data.

Think of it this way: a password manager is a **safe with a single key**, versus leaving your valuables scattered under doormats, in drawers, and taped under desks all over town. The safe concentrates the risk, yes, but it also concentrates the *protection* to a level you could never achieve with dozens of sticky notes.

<br/>
<br/>

---

## 🔍 Things to Look For

Now let's say I have convinced you to upgrade your digital security, how can you choose the right application without falling into some common traps?

Here is a list of things to pay attention to:

- **Don't choose unknown services.** Check the brand's reputation, are they known or is it a sketchy app? A quick search for `"<app name>" breach OR scandal OR review` will save you a lot of headaches.
<br>

- **Is it open source and audited?** This means that the code is public and everyone can check if the app is doing something in the shadows. Also, an external audit provides a kind of certified accountability (check *who* did the audit as well - a big-name firm like Cure53, NCC Group, or Trail of Bits carries more weight than an unknown contractor).
<br>

- **Check where the data is stored.** Is it on the cloud? In which nation are the servers? Or is it on your local device? Jurisdiction matters: data stored in the EU falls under GDPR, data in Switzerland under the FADP, and so on.
<br>

- **Read the privacy policy.** I know this is something that usually nobody does, but it is here that the company has to say which of your data are collected and how it handles them. Look specifically for: do they log your IP? Do they sell analytics? Can they decrypt your vault?
<br>

- **Does it support safe two-factor authentication?** Hardware keys (FIDO2 / WebAuthn), authenticator apps (TOTP), and solid recovery methods. The last thing you want is losing access to your vault. SMS-based 2FA is better than nothing but is vulnerable to SIM-swapping; prefer app-based or hardware-based options.
<br>

- **Portability and Functionalities.** Be sure to choose an application that lets you import/export credentials (CSV, JSON, encrypted backup) and that has all the functionalities you need for your workflow. Vendor lock-in is real.

<br/>

### ➕ For Advanced Users

There are other things you can give a look at:

- **Encryption at rest vs. in transit.** What algorithm protects your data on disk (AES-256-GCM, XChaCha20)? Which protocol handles transmission (TLS 1.3)? Are they using authenticated encryption or just plain AES-CBC?
<br>

- **Which fields are encrypted?** Sometimes not all of them are. Metadata like website URLs, folder names, or timestamps may be stored in plaintext on the server.
<br>

- **Master key derivation.** How is your master password being protected? Look for **Argon2id** (preferred), scrypt, or at minimum PBKDF2 with a high iteration count (≥ 600 000). Do they apply good practices such as salting? How is it implemented?
<br>

- **Types of secrets.** Is it possible to save only passwords or also other types of secrets (SSH keys, API tokens, TOTP seeds, certificates, encrypted notes)?
<br>

- **Zero-knowledge architecture.** Can the provider technically decrypt your data? In a true zero-knowledge design, the answer must be *no*.

<br/>

### 🎁 Bonus: Passkeys Support

Passkeys (FIDO2 / WebAuthn credentials) are still a technology on the rise, so keep a look at them if you are interested. Different services may have already implemented them or are going to in the future. The advantage of this functionality built into a password manager is the ability to make the passkey **portable** and to stay safe in the situation where you lose access to your main device.

As of 2025–2026, the [FIDO Alliance](https://fidoalliance.org/) and major OS vendors (Apple, Google, Microsoft) have pushed passkeys into the mainstream, and the [W3C WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/) specification is stabilising multi-device passkey sync. If your password manager already supports storing and autofilling passkeys, you are ahead of the curve.

<br/>
<br/>

---

## 👍 My Recommendations

With all the information above everyone should be able to vet the market's offers and choose what the best options are for their needs, but I have decided to share my top picks to simplify your work.

The following are some of my personal preferences, some I have personally tested and that in my opinion best comply with the guidelines I have shared.

---

### 🥇 Best Overall: Bitwarden

| | |
|---|---|
| **Website** | [bitwarden.com](https://bitwarden.com/) |
| **Source Code** | [github.com/bitwarden](https://github.com/bitwarden) |
| **License** | AGPL-3.0 (server), GPL-3.0 (clients) |
| **Platforms** | Windows, macOS, Linux, Android, iOS, all major browser extensions, CLI |
| **Price** | Free tier (unlimited passwords, 2 devices) · Premium **$10 / year** · Families $40 / year |

Bitwarden is one of the most known and downloaded password managers. The app is free and open source and available for every system and as a browser extension.
It is community-driven and has been audited multiple times (most recently by Cure53 and Insight Risk Consulting), supports high standards of encryption (AES-256-CBC for data at rest, TLS 1.3 in transit, PBKDF2-SHA256 with 600 000+ iterations for key derivation, with Argon2id available as an option).

It also offers multiple functionalities other than storing logins: encrypted notes, credit cards, identity data, the chance to create different folders, display image icons, generate passwords, built-in TOTP authenticator (premium), and more.

As it is a community-driven project most of the functionalities are available for free, but if you want to choose the premium plan at $10 a year (at the moment of writing) you will also be able to share data with other users, use it as an authenticator app, and get 1 GB of encrypted file storage.

Another key thing is that all the data is also available offline and will then get automatically uploaded and synced across your devices when you are connected to the internet.

**Bonus:** you have the chance to choose to save your vault either on **US or EU servers**, and if you are a power user you can self-host the entire stack via [Vaultwarden](https://github.com/dani-garcia/vaultwarden) (see below).

<br/>

---

### 🥈 Best On-Device: KeePassXC

| | |
|---|---|
| **Website** | [keepassxc.org](https://keepassxc.org/) |
| **Source Code** | [github.com/keepassxreboot/keepassxc](https://github.com/keepassxreboot/keepassxc) |
| **License** | GPL-2.0 / GPL-3.0 |
| **Platforms** | Windows, macOS, Linux (native); Android via [KeePassDX](https://www.keepassdx.com/); iOS via [Strongbox](https://strongboxsafe.com/) or [KeePassium](https://keepassium.com/) |
| **Price** | 100 % free |

KeePassXC is another free and open source application. The difference from the others is that it stores all the data directly on your device in an encrypted `.kdbx` database file, so **no data will be transmitted on the internet** unless you explicitly set it up.

There is also the possibility to access synchronisation by using a third-party cloud service (Nextcloud, Dropbox, Syncthing, etc.) after you have encrypted your vault - the cloud only ever sees ciphertext.

The app offers the main functionalities: storing passwords, creating folders and groups, choosing different icons, password generation, password health check, TOTP integration, SSH agent integration, and YubiKey / hardware-key support for unlocking the database.

The only downside here is that, since it is on your device, you will have to take care first-hand of the **backups and synchronisation**. Lose the file and the master password, and the data is gone - no support ticket will save you.

I also have to say that it does not have the most user-friendly interface; it is functional and clean, but it feels more "engineer-oriented" than the polished SaaS competitors.

> **Note on mobile:** KeePassXC itself does not ship an official mobile app. The community-maintained **KeePassDX** (Android, open source) and **Strongbox / KeePassium** (iOS) read and write the same `.kdbx` format, so the ecosystem works, but you are juggling multiple apps.

<br/>

---

### 🥈 Best Self-Hosted: Vaultwarden or KeepassXC + Synchthing

| | |
|---|---|
| **Website / Repo** | [github.com/dani-garcia/vaultwarden](https://github.com/dani-garcia/vaultwarden) |
| **License** | AGPL-3.0 |
| **Platforms** | Any server that runs Docker or a Rust binary; clients are the standard Bitwarden apps |
| **Price** | Free (you pay for your own hosting) |

If you liked the Bitwarden ecosystem but the idea of *anyone else* hosting your vault makes you uncomfortable, **Vaultwarden** is the answer. It is a lightweight, community-maintained reimplementation of the Bitwarden server API written in Rust. You spin it up in a Docker container on a Raspberry Pi, a VPS, or a home NAS, and then point the official Bitwarden clients at your own URL.

You get every Bitwarden client feature - browser extensions, mobile apps, CLI - but the encrypted blobs never leave your infrastructure. Updates are frequent, the community is active, and the resource footprint is tiny (it runs happily in < 50 MB of RAM).

The trade-off is obvious: **you are the sysadmin.** You handle TLS certificates, backups, updates, and uptime. If that sounds fun rather than frightening, this is a fantastic option.

<br/>

---

### Great NON-Free Option: 1Password

| | |
|---|---|
| **Website** | [1password.com](https://1password.com/) |
| **Source Code** | Proprietary (closed source) |
| **Platforms** | Windows, macOS, Linux, Android, iOS, all major browser extensions, CLI |
| **Price** | Individual **$2.99 / month** (billed annually) · Families $4.99 / month · Teams / Business tiers available |

Another commonly suggested password manager if you don't mind paying for it.
Unfortunately this app is only available with a subscription plan; there is no permanent free tier (they offer a 14-day trial).

It offers many functionalities similar to the apps listed above, plus some unique touches: **Travel Mode** (temporarily remove sensitive vaults when crossing borders), **Watchtower** (monitors for breached or weak passwords), and a very polished **Secret Key** mechanism that adds a second factor to the master password so that even 1Password's own servers cannot decrypt your data without it.

The main difference is that it has multiple versions ranging from personal to business use, and the UI is arguably the most refined in the category.

The code is **not open source**, but they run a public [bug bounty program on Bugcrowd](https://bugcrowd.com/1password) and have undergone independent audits (most notably by Cure53 and ISE). You are trusting the company's implementation, but the cryptographic design (SRP-based key exchange, Secret Key + master password) is well documented in their [security whitepaper](https://1password.com/security/).

<br/>

---

### Best Built-In Options

Before you install anything, it is worth mentioning what you already have:

- **Apple Keychain / iCloud Keychain** – deeply integrated into macOS and iOS, syncs via iCloud, supports passkeys natively since iOS 16 / macOS Ventura. Zero extra cost, but you are locked into the Apple ecosystem and the code is closed source.
<br>

- **Google Password Manager** – built into Chrome and Android, syncs with your Google account. Convenient, but you are handing your credential metadata to Google's advertising empire, which is a privacy trade-off many will not want to make.
<br>

- **Microsoft Edge / Windows Credential Manager** – similar story for the Microsoft ecosystem.

These are *fine* for casual users who want zero friction, but they lack the portability, auditability, and advanced features (encrypted notes, custom fields, self-hosting) of a dedicated manager.

<br/>

### 🏅 Honourable Mentions

**Proton Pass** – [proton.me/pass](https://proton.me/pass)
A password manager from the Proton company. The app is free and open source, but to access multiple features - creation of multiple vaults, built-in authenticator, offline access, and passkey management - you have to choose the Plus plan starting at **€1.99 / month** (at time of writing, billed annually).
One of the best things is the super easy and modern interface, and it is available on all systems.
Another key point is that **all fields are encrypted end-to-end** (including URLs and metadata, which many competitors leave in plaintext), and the company is based in **Switzerland**, which has a strong history of privacy regulations (FADP).
Even though the app is relatively new (launched mid-2023), it has already been audited (by Cure53) and employs high security standards.
The only "downside" is that it is a newer player in the market and some advanced functionalities are still being rolled out.
**Bonus:** it supports passkeys on Android 14+ and iOS 17+.
<br/>

**NordPass** – [nordpass.com](https://nordpass.com/)
Rising in popularity, from the NordVPN / Nord Security company.
They offer a free version with very limited functionalities (one device, no sharing) and then a Premium subscription starting from **$1.79 / month** (at time of writing, billed for a 2-year term).
The app has been audited (by Cure53), but unfortunately the code is **proprietary**, so we cannot actually see the source code and we have only to trust the company about the implementations and the different security measures being used.
It uses XChaCha20 encryption, which is a solid modern cipher, and the UI is clean. A reasonable choice if you are already in the Nord ecosystem, but the closed-source nature keeps it a step behind the options above for the privacy-conscious.

<br/>
<br/>

---

## What To Do After

Once you have decided the application to use as your companion you will need to:

1. **Enable autofill and password suggestion** if you want it to automatically complete and save new login credentials while you navigate.
2. **On mobile devices** you might need to allow the permission also in the accessibility settings (Android) or under *Settings → Passwords → AutoFill* (iOS), depending on which OS version you are using.
3. **Enable biometric unlock** (face / fingerprint) on mobile or on your desktop if you have a reader, so you can quickly access your vault without typing the master password every time.
4. **Run a password audit.** Most managers (Bitwarden, 1Password, KeePassXC, Proton Pass) have a built-in report that flags reused, weak, or breached passwords. Fix those first.
5. **Enable 2FA on the password manager itself.** This is the single most important step. A hardware key (YubiKey, Nitrokey) is ideal; a TOTP app is the minimum.
6. **Export an encrypted backup** and store it offline (USB drive, printed recovery key in a safe). Test that you can restore from it.
7. **Migrate gradually.** You don't have to move 300 logins in one evening. Change the most critical ones first (email, banking, primary social media), then let the manager capture the rest as you browse.

Now you can finally create and use unique, long, and complex passwords for every service you want to access, staying safe without the need to remember them all.

<br/>
<br/>

---

## ⚠️ Warning / Side Note

Another commonly downloaded password manager is **LastPass**. If you have it or you plan to use it, I highly suggest you review the following sources before taking the risk, considering the **multiple breaches** (most critically the August 2022 breach where encrypted vault backups were exfiltrated) and some questionable post-incident communications:

- [LastPass Security Incident – Official Disclosure (Dec 2022)](https://blog.lastpass.com/2022/12/notice-of-recent-security-incident/)
- [Ars Technica – LastPass breach analysis](https://arstechnica.com/information-technology/2022/12/password-manager-lastpass-says-hackers-stole-encrypted-vaults/)
- [Krebs on Security – LastPass: The Gift That Keeps on Giving](https://krebsonsecurity.com/2023/01/lastpass-the-gift-that-keeps-on-giving/)

If you are currently on LastPass, **export your vault and migrate** to one of the options above. The trust has been broken more than once, and the closed-source nature means we cannot independently verify their fixes.

<br/>
<br/>

---

## Comparison Table

| Feature | **Bitwarden** | **KeePassXC** | **Vaultwarden** | **1Password** | **Proton Pass** | **NordPass** | 
|---|---|---|---|---|---|---|
| **Price** | Free / $10 yr | Free | Free (self-host) | $2.99 mo | Free / €1.99 mo | Free / $1.79 mo | 
| **Open Source** | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ❌ No | 
| **Audited** | ✅ Multiple | ✅ Community | ⚠️ (inherits BW) | ✅ Cure53, ISE | ✅ Cure53 | ✅ Cure53 | 
| **Zero-Knowledge** | ✅ | ✅ (local) | ✅ | ✅ (Secret Key) | ✅ | ✅ | 
| **Data Location** | US / EU cloud | Local device | Your server | Cloud (US/CA) | Switzerland | Cloud | 
| **Encryption** | AES-256-CBC | AES-256 / ChaCha20 | AES-256-CBC | AES-256-GCM | AES-256 / XChaCha20 | XChaCha20 | 
| **Key Derivation** | PBKDF2 / Argon2id | AES-KDF / Argon2id | PBKDF2 / Argon2id | PBKDF2 + Secret Key | bcrypt / Argon2 | Argon2id | G
| **2FA / MFA** | TOTP, FIDO2, email | YubiKey, TOTP | TOTP, FIDO2 | TOTP, FIDO2 | TOTP | TOTP | 
| **Passkeys** | ✅ | ❌ On adroid with KeepassDx Yes ✅ | ✅ | ✅ | ✅ (Android 14+) | ⚠️ Limited | 
| **Offline Access** | ✅ | ✅ (native) | ✅ | ✅ | ✅ (premium) | ✅ | 
| **Mobile App** | ✅ Official | ⚠️ 3rd-party | ✅ (BW clients) | ✅ Official | ✅ Official | ✅ Official | 
| **Browser Extension** | ✅ All major | ✅ (via browser integration) | ✅ (BW ext.) | ✅ All major | ✅ All major | ✅ All major | 
| **Self-Hostable** | ✅ (official) | ✅ (local) | ✅ (purpose-built) | ❌ | ❌ | ❌ | 
| **Sharing / Teams** | ✅ (premium) | ❌ | ✅ | ✅ | ✅ (premium) | ✅ (premium) | 
| **Best For** | Most users | Privacy purists | Self-hosters | Polished UX | Proton ecosystem | Nord ecosystem | 

> *Prices and features are subject to changes. Always check the official sites for the latest information.*

<br/>
<br/>

---

## Conclusion

Thanks for following along. I hope you will take this little step to enhance your cyber security. A password manager is arguably the **single highest-impact, lowest-effort** change you can make to your digital hygiene - it takes an afternoon to set up and protects you every single day after.

I encourage everyone to not only follow online recommendations but also **do your own research** for every software you use. Read the audit reports. Skim the source code if you can. Ask questions in community forums. Trust, but verify.

Stay safe out there. 🔐

<br/>

---

*Last updated: July 2026. The privacy landscape moves fast. Always verify the current state of any tool before trusting it with your data.* 
