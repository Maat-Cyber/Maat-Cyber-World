# Operation Slither Walkthrough

## Intro
Welcome to the Operation Slither challenge, here is the link to the [room](https://tryhackme.com/room/operationslitherIU) on TryHackMe.
This OSINT challenge is divided into 3 parts, each with is own part of the story and 2 questions to answer.

To complete this CTF it is not required to start any machine or connect via OpenVPN.

Let's begin!

<br/>
<br/>

## The Challenge 
To solve this challenge we will user our web browser to search online for the related info.

### The leader
We got access to a hacker forum and found the info of our company on sale! All the info we have is in this post. Find any information related to the leader of the Sneaky Viper group.

```shell
Full user database TryTelecomMe on sale!!!

As part of Operation Slither, we've been hiding for weeks in their network and have now started to exfiltrate information. This is just the beginning. We'll be releasing more data soon. Stay tuned!

@v3n0mbyt3_

---
```

Reconnaissance Guide
- Begin with the provided username and perform a broad search across common social platforms.
- Correlate discovered profiles to confirm ownership and authenticity.
- Review interactions, posts, and replies for potential leads.
<br>

1. **Aside from Twitter / X, what other platform is used by v3n0mbyt3_? Answer in lowercase.** <br>
	Copy and paste the username in a search engine and you will find it. <br>
-->  REDACTED
<br>

2. **What is the value of the flag?** <br>
	On that platform we can find a comment with a base64 encoded string, we can decode it:
```bash
echo "VEhNe3NsMXRoM3J5X3R3MzN0el80bmRfbDM0a3lfcjNwbDEzcyF9" | base64 -d
```
-->  REDACTED

<br/>

### The Sidekick
A second message has been made public! Our accountt in their forum was deleted, so we couldn't get the operator's handle this time. Follow the crumbs from the first task and hunt any information related to the second operator of the group.

```shell
60GB of data owned by TryTelecomMe is now up for bidding!

Number of users: 64500000 Accepting all types of crypto
For takers, send your bid on Threads via this handle:

HIDDEN CONTENT 
----------------------------------------------------------------------------------------------------- 
You must register or log in to view this content
```

Reconnaissance Guide
- Use related usernames or connections identified in earlier steps to expand reconnaissance.
- Enumerate additional platforms for linked accounts and shared content.
- Follow media or resource references across platforms to trace information flow.
<br>

3. **What is the username of the second operator talking to v3n0mbyt3 from the previous platform?** <br>
	It is the name of the user that replied with that encoded string we saw previously. <br>
--> REDACTED
<br>

4. **What is the value of the flag?** <br>
	Exploring that user we can find an Instagram profile with 5 posts, in one of them there is a link `https://soundcloud.com/v1x3n-195859753`, under "prototype2" we find another encoded string
```bash
echo "VEhNe3MwY20xbnRfMDBwcz....REDACTED" | base64 -d
```
--> REDACTED

<br/>

### The Last Operator
A new post is up. Hunt the third operator using past discoveries and find any details related to the infrastructure used for the attack.
```shell
FOR SALE

Advanced automation scripts for phishing and initial access!

Inclusions:
- Terraform scripts for a resilient phishing infrastructure 
- Updated Google Phishlet (evilginx v3.0)
- GoPhish automation scripts
- Google MFA bypass script
- Google account enumerator
- Automated Google brute-forcing script
- Cobalt Strike aggressor scripts
- SentinelOne, CrowdStrike, Cortex XDR bypass payloads

PRICE: $1500
Accepting all types of crypto
Contact me on REDACTED@protonmail.com 

---
```

Reconnaissance Guide
- Identify secondary accounts through visible interactions (likes, follows, collaborations). 
- Extend reconnaissance into developer or technical platforms associated with the identity.
- Analyse activity history (such as repositories or commits) for embedded information.
<br>
 
5. **What is the handle of the third operator?** <br>
	Inside soundcloud we can see the user is followed by another particular username: <br>
--> REDACTED
<br>

6. **What other platform does the third operator use? Answer in lowercase.** <br>
	Searching for that we can see the user has an account on a commonly used app in the IT sector. <br>
--> REDACTED
<br>

7. **What is the value of the flag?** <br>
	Looking at the user repo we can find one that is not a known tool that already exist, we can view the files history and on the `terraform.tfstate` file we can find another encoded string. Let's decode it and get the last flag:
```bash
echo "VEhNe3NoNHJwX2Y0bmd6X2wzNGszZ...REDACTED" | base64 -d
```
--> REDACTED

<br/>
<br/>

Congratulations, you have successfully connected all the dots around the web putting into practice your OSINT skills.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
