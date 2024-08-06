# --------------------- TShark Challenges 1 and 2 Walktroughs -----------------------
- [Challenge 1 Teamwork](#tshark-challenge-i-teamwork)
- [Challenge 2 Directory](#tshark-challenge-2-directory)

<br/>
<br/>

# TShark Challenge I: Teamwork
<br/>

## Intro
Welcome to the Teamwork challenge, here is the TryHackMe [webpage](https://tryhackme.com/r/room/tsharkchallengesone).
In this room we are gonna put at work what we have learned in the previous rooms about the CLI tool *TShark*.

The situation is:
An alert has been triggered: "The threat research team discovered a suspicious domain that could be a potential threat to the organisation."
The case was assigned to you. Inspect the provided **teamwork.pcap** located in `~/Desktop/exercise-files` and create artifacts for detection tooling.

Whenever you feel ready press "start machine" and wait for the split view to load.

<br/>
<br/>

## The Challenge
We have to analyze the network capture file to answer the 5 questions, let's begin!

1. **Investigate the contacted domains.  Investigate the domains by using VirusTotal. According to VirusTotal, there is a domain marked as malicious/suspicious.**  
   **What is the full URL of the malicious/suspicious domain address?**
   **Enter your answer in defanged format.**
   We can run this command to filter for unique dns names, the result will give us 4, it is pretty easy to guess the bad one, but just for confirmation copy it in Virus Total to see that it is a phishing website.
```bash
tshark -r teamwork.pcap -T fields -e dns.qry.name | awk NF | sort -r | uniq -c | sort -r
```

<br/>


2. **When was the URL of the malicious/suspicious domain address first submitted to VirusTotal?**
   In the details section In Virus Total we can see the field "First Submission".

<br/>

3. **Which known service was the domain trying to impersonate?**
   We can see the service name in the URL.

<br/>

4. **What is the IP address of the malicious domain? Enter your answer in defanged format.**
   In VirusTotal we can go to the relations section and see the resolved IP.

<br/>

5. **What is the email address that was used?Enter your answer in defanged format. (format: aaa[at]bbb[.]ccc)**
   Now we can go back to analyzing the pcap file, 
```bash
tshark -r teamwork.pcap -Y 'http.request.method matches "(GET|POST)"'  -T fields -e "text"  -q | grep @
```

<br/>
Nice we have now completed the first challenge and we can move to the second one.

<br/>
<br/>

---
# TShark Challenge 2: Directory
<br/>

## Intro
Welcome to the second part of the TShark challenge called: Directory, here is the TryHackMe [webpage](https://tryhackme.com/r/room/tsharkchallengestwo).
In this room we are gonna put at work what we have learned in the previous rooms about the CLI tool *TShark* and complete the TShark Challenge.

The situation is:
**An alert has been triggered:** "A user came across a poor file index, and their curiosity led to problems".
The case was assigned to you. Inspect the provided **directory-curiosity.pcap** located in `~/Desktop/exercise-files` and retrieve the artefacts to confirm that this alert is a true positive.

Whenever you feel ready press "start machine" and wait for the split view to load.

<br/>
<br/>

## The Challenge
Since it is a continuation of the previous TShark challenge it is structured the same, and we will still need VirusTotal and TShark tools.

1. **Investigate the DNS queries. Investigate the domains by using VirusTotal. According to VirusTotal, there is a domain marked as malicious/suspicious.**
   **What is the name of the malicious/suspicious domain? Enter your answer in a defanged format.**
```bash
tshark -r directory-curiosity.pcap -T fields -e dns.qry.name | awk NF | sort -r | uniq -c | sort -r
```
   We can see 7 unique domains, a quick search on VT will show us that one of them contains malware.

<br/>

2. **What is the total number of HTTP requests sent to the malicious domain?**
   We can use TShark to filter for only those interesting packets:
```bash
shark -r directory-curiosity.pcap -Y 'http.request.full_uri contains "jx2"' | awk NF | sort -r | uniq -c | sort -r | wc -l
```
<br/>

3. **What is the IP address associated with the malicious domain? Enter your answer in a defanged format.**
   We can find this answer by checking the network traffic capture and searching for the domain, we will see packets going to it:
```bash
shark -r directory-curiosity.pcap -Y 'http.request.full_uri contains "jx2"' | awk NF | sort -r | uniq -c | sort -r 
```
<br/>

4. **What is the server info of the suspicious domain?**
   Still with our TShark  tool we can search for a keyword like "server" in TCP packets and extract the field containing that information
```bash
tshark -r directory-curiosity.pcap -Y 'tcp contains "server"' -T fields -e http.server | awk NF | sort -r | uniq -c | sort -r 
```

<br/>

5. **Follow the "first TCP stream" in "ASCII". Investigate the output carefully.**
   **What is the number of listed files?**
   We can run this command to follow that TCP stream
```bash
shark -r directory-curiosity.pcap -z follow,tcp,ascii,0 -q
```

<br/>

6. **What is the filename of the first file? Enter your answer in a defanged format.**
   We can go through the previous command's output and locate the first one.

<br/>


7. **Export all HTTP traffic objects.  What is the name of the downloaded executable file? Enter your answer in a defanged format.**
   There was only one "executable" file from the ones we have found in question 5, anyway here is the command to export the HTTP traffic objects:
```bash
tshark -r directory-curiosity.pcap --export-objects http,. -q
```

<br/>

8. **What is the SHA256 value of the malicious file?**
   Let's calculate the file's hash.
```bash
sha256sum vlauto.exe
```

<br/>

9. **Search the SHA256 value of the file on VirtusTotal.  What is the "PEiD packer" value?**
   This is pretty straigth, go on VT, submit the hash and at the end of the first paragraph in the details tab there is the answer.

<br/>

10.  **Search the SHA256 value of the file on VirtusTotal. What does the "Lastline Sandbox" flag this as?**
    Still there we ca go in the "behavior" section, scroll down a bit to find that one Sandobox and read what it flag the malicious file as.

<br/>
<br/>

Congratulations, by completing this two challenges and the theory modules you have earned the "Packet Master" badge!

Catch you in the next CTF 😃 
