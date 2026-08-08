# After Hours Walkthrough
<br/>

## Intro
Welcome to the *After Hours* challenge, here is the link to the [room](https://tryhackme.com/room/hh-afterhours-b090d1f0) on TryHackMe.

This is a medium level challenge about forensics investigation of some Windows related artifacts to uncover an hidden flag.

*"Long after the front desk closes and the pool lights dim, the resort's back-office machines keep humming. Someone, or something, has been logging in during the small hours, well after the night-shift technician has gone home.
Nothing obvious shows up in Startup, Scheduled Tasks, or the registry Run keys. Whatever's keeping itself alive is hiding somewhere quieter, tucked away in a corner of the system most tools don't think to check."*

Whenever you feel ready download the task's files or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
With the archive on our machine we can now extrct the files within:
```bash
 unzip attachments.zip
```
- Might need this pass for the extraction `Aft3rH0ursAtt4chm3ntP4ss`.

5 files gets extracted:
```
 inflating: INDEX.BTR
  inflating: MAPPING1.MAP
  inflating: MAPPING2.MAP
  inflating: MAPPING3.MAP
  inflating: OBJECTS.DATA
```

Looking at them we can see they are **Windows WMI repository files**. 

WMI Event Subscriptions are used for fileless persistence because it hides in this database rather than in standard Autoruns, Registry Run keys, or Scheduled Tasks.

We can check the file type with:
```bash
file FILENAME
```

And notice that they are all of this format: `MAPPING1.MAP: data`.

Because of that reading them with `cat` is not suggested, it would be a nigthmare, if you want to look for text use `strings`.

We can check for quick wins, if somehow the flag was left in plain text there with:
```bash
for f in INDEX.BTR MAPPING1.MAP MAPPING2.MAP MAPPING3.MAP OBJECTS.DATA; do
    echo " $f "
    strings -a -n 6 -e l "$f" | rg -i "THM|flag"
done
```
- `-e l` flag stands for 16-bit little-endian (UTF-16LE). Because this is a Windows artifact, many strings (such as registry-like or PS artifacts) are stored in UTF-16LE.

As we could image that was too easy to be the solution.

All this strings are from the "OBJECTS.DATA" file and they are: 
```
=== OBJECTS.DATA ===
LUAInstall: error 0x00000005 setting flags [{93AAD2A0-036A-4B11-A078-DA8776B38139}]
LUAInstall: error 0x00000005 setting flags [{93AC9CB8-27D5-4482-BFDF-68F21C7454A3}]
LUAInstall: error 0x00000005 setting flags [{93C063B0-68CB-4DE7-B032-8F56C1D2E99D}]
```

We need a better way to investigate this files.
Since we did not find the flag with strings, probably it is either multiple time encoded or encrypted.

Let's start easy and find if there are any base64 blobs:
```bash
strings -a -n 20 OBJECTS.DATA | rg -o "[A-Za-z0-9+/]{60,}={0,2}" > output
```
- or with *grep*: `grep -Eo "[A-Za-z0-9+/]{60,}={0,2}`

Yep, we can find many of them, but decoding them we find again binary data:
```bash
cat output | base64 -d > output_decoded; file output_decoded
```

We get again `output_decoded: data`.
This is not the best way, and if we try to read strings again and find the flag it fails to parse some lines.

<br/>

### PE Extraction
We can build a short python script to get the base64 data, recover the Windows PE executable and write it to an `.exe` file, than we will read directly from it.
We isolate the single longest base64 blob, decode it, and force Python to decompress it without expecting an header.
```python
import base64
import zlib
import re

# 1. Read the raw binary file
with open('OBJECTS.DATA', 'rb') as f:
    data = f.read()

# 2. Find all large ASCII base64 blobs
blobs = re.findall(rb'[A-Za-z0-9+/]{100,}={0,2}', data)

# malicious payload is probably the longest base64 string in the file
longest_blob = max(blobs, key=len)
print(f"[*] Found base64 blob of length: {len(longest_blob)}")

# 3. Decode Base64
binary_data = base64.b64decode(longest_blob)

# 4. Decompress Raw DEFLATE
# wbits=-15 tells zlib to expect RAW DEFLATE (no headers)
try:
    payload = zlib.decompress(binary_data, -15)
    print(f"[+] Successfully decompressed! First two bytes: {payload[:2]}")
    
    with open('extracted_payload.exe', 'wb') as out:
        out.write(payload)
    print("[+] Saved to extracted_payload.exe")
except zlib.error as e:
    print(f"[-] Decompression failed: {e}")
```

Now read strings in the binary:
```bash
strings -e l extracted_payload.exe
```

We find cmd.exe call and a command:
```cmd
/c net user patch VEhNe1A0dGNoX29wM25lZF9....REDACTED /add
```

Looking at the first chars "VEhN.." it is probably base64 encoding of the THM word.

Let's decode it:
```bash
echo "VEhNe1A0dGNoX29wM...REDACTED...." | base64 -d
```

--> REDACTED

<br/>
<br/>

Congratulations, you have successfully practiced wiht a bit of decompression and decoding and found the hidden flag in a Windows Portable Executable.


Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
