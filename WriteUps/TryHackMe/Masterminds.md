# Masterminds Walkthrough
<br/>

## Intro
Welcome to the Masterminds challenge, here is the link to the [room](https://tryhackme.com/room/mastermindsxlq) on TryHackMe.

This is an investigation challenge with *Brim*.

The story:
"Three machines in the Finance department at Pfeffer PLC were compromised. We suspect the initial source of the compromise happened through a phishing attempt and by an infected USB drive. The Incident Response team managed to pull the network traffic logs from the endpoints. Use Brim to investigate the network traffic for any indicators of an attack and determine who stands behind the attacks."

**NOTE: DO NOT** directly interact with any domains and IP addresses in this challenge. 

Whenever you feel ready press on "start machine" and in a couple of minutes the system will appear in your browser as split-view.

Let's begin!

<br/>
<br/>

## The Challenge
(RISKY): But i hate the slowness of spawned VMs online, so i started it only to transfer the 3 infection files on my own Sandboxed environment in a VM.
Do not do it, unless you are in a safe environment, we will be interacting with malicious IPs and domains.

**How to work with Brim**
This tools allows us to call specific views and fileds + run commands like `sort` and `uniq` to get a new custom view of the desired target.

We will begin our query with the `__path` variable, then pipe the result and `cut` for specific fields we might be intereset in, finally as a good practice to get a clean result we will use sort the results and elminiate the duplicates.

In the following paragraphs i will show the commands i build to get the information needed to answer the questions, (obviously) without including the final flags/answers.

If you get stuck you will get the answer simply by pasting my command and analyzing the couple of results.

<br/>

### Infection 1
Start by loading the Infection1 packet capture in Brim to investigate the compromise event for the first machine. 
All the PCAPs can be found here: `/home/ubuntu/Desktop/PCAPs`

Provide the victim's IP address:
```
_path=="conn" | cut id.orig_h, id.resp_h| sort | uniq
```
--> REDACTED

The victim attempted to make HTTP connections to two suspicious domains with the status '404 Not Found'. Provide the hosts/domains requested.
```
_path=="http"|  status_code==404 | cut host |sort | uniq 
```
--> REDACTED

The victim made a successful HTTP connection to one of the domains and received the response_body_len of 1,309 (uncompressed content size of the data transferred from the server). Provide the domain and the destination IP address.
```
_path=="http" | cut id.resp_h, host, response_body_len|1309 
```
--> REDACTED

How many unique DNS requests were made to cab[.]myfkn[.]com domain (including the capitalized domain)?
```
_path=="dns" | cut query | CAB | count()
```
--> REDACTED

Provide the URI of the domain bhaktivrind[.]com that the victim reached out over HTTP.
```
_path=="http" | cut host, uri | bhak
```
--> REDACTED

Provide the IP address of the malicious server and the executable that the victim downloaded from the server.
```
_path=="http" | cut host, uri | sort | uniq
```
--> REDACTED

Based on the information gathered from the second question, provide the name of the malware using [VirusTotal](https://www.virustotal.com/gui/home/upload).
Search for 
```
cambiasuhistoria.growlab.es
```
--> REDACTED

<br/>

### Infection 2
Navigate to the Infection2 packet capture in Brim to investigate the compromise event for the second machine.
Note: For questions that require multiple answers, please separate the answers with a comma.

For each question we will build a query to filter the relevant results.

Provide the IP address of the victim machine.
```
_path=="conn" | cut id.orig_h, id.resp_h| sort | uniq
```
--> REDACTED

Provide the IP address the victim made the POST connections to.
```
_path=="http" |cut  host, id.orig_h, uri, method | 192.168.75.146 | POST |sort | uniq
```
--> REDACTED

How many POST connections were made to the IP address in the previous question?
```
_path=="http" |cut  host, id.orig_h, id.resp_h method  | 5.181.156.252 | POST | count()
```
--> REDACTED

Provide the domain where the binary was downloaded from.
```
_path=="http" |cut host, id.orig_h, id.resp_h, method, uri | GET
```
--> REDACTED

Provide the name of the binary including the full URI.
```
_path=="http" |cut host, id.orig_h, id.resp_h, method, uri | GET
```
-->==`/jollion/apines.exe`==

Provide the IP address of the domain that hosts the binary.
```
_path=="http" |cut host, id.orig_h, id.resp_h, method, uri | GET
```
--> REDACTED

There were 2 Suricata "A Network Trojan was detected" alerts. What were the source and destination IP addresses?
```
event_type=="alert" | cut src_ip, dest_ip, alert | Trojan
```
--> REDACTED

Taking a look at .top domain in HTTP requests, provide the name of the stealer (Trojan that gathers information from a system) involved in this packet capture using [URLhaus Database](https://urlhaus.abuse.ch/).
Search in the URLhaus database `hypercustom.top`.
--> REDACTED

<br/>

### Infection 3
Please, load the Infection3 packet capture in Brim to investigate the compromise event for the third machine.  
Note: For questions that require multiple answers, please separate the answers with a comma.

Provide the IP address of the victim machine.
```
_path=="conn" | cut id.orig_h, id.resp_h, orig_bytes |sort -r | uniq
```
--> REDACTED

Provide three C2 domains from which the binaries were downloaded (starting from the earliest to the latest in the timestamp)
```
_path=="http" | cut host, uri, ts | sort ts | uniq
```
--> REDACTED

Provide the IP addresses for all three domains in the previous question.
```
_path=="http" | cut host, uri, id.orig_h | uniq
```
--> REDACTED

How many unique DNS queries were made to the domain associated from the first IP address from the previous answer?
```
_path=="dns" | cut id.orig_h, id.resp_h, query | efhoahegue.ru | count()
```
--> REDACTED

How many binaries were downloaded from the above domain in total?
```
_path=="http" | cut host, uri, | efhoahegue.ru 
```
--> REDACTED

Provided the user-agent listed to download the binaries.
```
_path=="http" | cut host, uri, user_agent | efhoahegue.ru
```
--> REDACTED

Provide the amount of DNS connections made in total for this packet capture.
```
_path=="dns" | count()
```
--> REDACTED

With some OSINT skills, provide the name of the worm using the first domain you have managed to collect from Question 2. (Please use quotation marks for Google searches, don't use .ru in your search, and DO NOT interact with the domain directly).
--> REDACTED

<br/>
<br/>

## Conclusion
Congratulations you have successfully practiced with some log analysis skills and unconvered the power that logs give yuo as an analyst to understand whats happening or what has already happened in your systems.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
