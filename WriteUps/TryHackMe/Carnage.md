# Carnage Walkthrough   
## Intro
Welcome to the Carnage challenge, here is the link to the [room](https://tryhackme.com/room/c2carnage) on TryHackMe.
In this challenge we will investigate a network capture using WireShark to spot signs of malicious activity.

### Scenario
Eric Fischer from the Purchasing Department at Bartell Ltd has received an email from a known contact with a Word document attachment.  Upon opening the document, he accidentally clicked on "Enable Content."  The SOC Department immediately received an alert from the endpoint agent that Eric's workstation was making suspicious connections outbound. The pcap was retrieved from the network sensor and handed to you for analysis.

Whenever you feel ready click on "Start Machine" and connect using OpenVPN or via the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
Since the AttackBox is super slow because of my internet and it also has few resources i decided to start the the machine and transfer the `carnage.pcap` file we need to analyze on my own VM. 

> [!NOTE] Warning
> Note that interacting directly with IP, URIs and files related to this incident can be risky, if you plan to transfer it on your machine you should set up a sandboxed environment in an isolated VM.

On the AttackBox:
```bash
cd ~/Desktop/Analysis
python3 -m http.server
```

Now on my VM:
```bash
 wget http://10.82.175.86:8000/carnage.pcap
```

Now that we have the file we can open it in *WireShark*.

1. **What was the date and time for the first HTTP connection to the malicious IP?** (**answer format**: yyyy-mm-dd hh:mm:ss) <br>
	Filter for `http`, click on the first packet and expand the "frame" there you can see the timestamp.
--> REDACTED
<br>

2. **What is the name of the zip file that was downloaded?** <br>
```
http contains "zip"
```
--> REDACTED

<br>

3. **What was the domain hosting the malicious zip file?** <br>
	From the previous query result we can follow the HTTP stream and view the domain in the request's headers.
--> REDACTED
   
<br>

5. **Without downloading the file, what is the name of the file in the zip file?** <br>
	Still in the HTTP stream we can see the name in the request's body.
--> REDACTED
   
<br>

6. **What is the name of the webserver of the malicious IP from which the zip file was downloaded?** <br>
	Still in the same request we can check the `Server` header to find the answer.
--> REDACTED
   
<br>

7. **What is the version of the webserver from the previous question?** <br>
	Again, still there but this time check the `x-powered-by` header.
--> REDACTED
   
<br>

9. **Malicious files were downloaded to the victim host from multiple domains. What were the three domains involved with this activity?** <br>
	For this one i decided to exclude all the domains i know are from Microsoft and one that kept appearing. We are left with not too many to check and some looks more sus that others.
```
tls.handshake.type == 1 && !(tls.handshake.extensions_server_name contains "microsoft.com") && !(tls.handshake.extensions_server_name contains "skype.com") && !(tls.handshake.extensions_server_name contains "windows.com") && !(tls.handshake.extensions_server_name contains "azureedge.net") && !(tls.handshake.extensions_server_name contains "msn.com") && !(tls.handshake.extensions_server_name contains "live.com") && !(tls.handshake.extensions_server_name contains "outlook.com") && !(tls.handshake.extensions_server_name contains "bing.com") && !(tls.handshake.extensions_server_name contains "ipify.org")
```
--> REDACTED

<br>

8. **Which certificate authority issued the SSL certificate to the first domain from the previous question?**  <br>
	We can take the first domain and do a `whois`.
--> REDACTED
   
<br>

10. **What are the two IP addresses of the Cobalt Strike servers? Use VirusTotal (the Community tab) to confirm if IPs are identified as Cobalt Strike C2 servers. (answer format: enter the IP addresses in sequential order)** <br>
	While answering Q7 i found another suspicious domain `securitybusinpuff.com`, checking it on VT confirmed that and in the Community tab we can find the 2 IPs
--> REDACTED
    
<br>

12. **What is the Host header for the first Cobalt Strike IP address from the previous question?** <br>
	We can filter for the first IP, then follow the HTTP stream, finally check the host header.
```
ipp.addr == 185.106.96.158
```
--> REDACTED

<br>

11. **What is the domain name for the first IP address of the Cobalt Strike server? You may use VirusTotal to confirm if it's the Cobalt Strike server (check the Community tab).** <br>
	We simply copy and paste the IP to VirusTotal and check the relations tab, only one domain is flagged ad malicious.
--> REDACTED
    
<br>

13. **What is the domain name of the second Cobalt Strike server IP?  You may use VirusTotal to confirm if it's the Cobalt Strike server (check the Community tab).** <br>
	Same process as the previous question.
--> REDACTED
    
<br>

14. **What is the domain name of the post-infection traffic?** <br>
	Since we are talking about post infection the direction of the traffic is probably from infected machine to C2, maybe sending some data via and HTTP POST request:
```
http.request.method == POST
```
We can start to follow the HTTP stream from the third packet and we see a clear culprit in the host header.
--> REDACTED

<br>

14. **What are the first eleven characters that the victim host sends out to the malicious domain involved in the post-infection traffic?** <br>
	Still in the same stream we can see this in the `POST /....` in the request, grab only the first 11 chars.
--> REDACTED
    

16. **What was the length for the first packet sent out to the C2 server?** <br>
--> REDACTED
    
<br>

17. **What was the Server header for the malicious domain from the previous question?** <br>
	Still in the same request we look at the `Server` header.
--> REDACTED
    
<br>

18. **The malware used an API to check for the IP address of the victim’s machine. What was the date and time when the DNS query for the IP check domain occurred? (answer format: yyyy-mm-dd hh:mm:ss UTC)**  <br>
	The answer of this question and the next one was already spotted when we were trying to find the malicious domains, if you see my previous query the domain was excluded cause there were many requests and was not relevant to that question. But clearly any high amount of requests on a specific domain is worth checking. 
--> REDACTED
    
<br>

19. **What was the domain in the DNS query from the previous question?** <br>
--> REDACTED
    
<br>

20. **Looks like there was some malicious spam (malspam) activity going on. What was the first MAIL FROM address observed in the traffic?** <br>
	Viewing the protocols of the captured file we see SMTP with an easy filter we can get this:
```
smtp contains "MAIL FROM"
```
--> REDACTED

<br>

20. **How many packets were observed for the SMTP traffic?** <br>
	Simply filter for `smtp` and read at the bottom the total number.
--> REDACTED

<br/>
<br/>

Congratulations, you have successfully investigated the WireShark logs and uncovered all the artifacts of the malicious activity and found all the answers.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
