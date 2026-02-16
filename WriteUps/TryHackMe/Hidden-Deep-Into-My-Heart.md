# Hidden Deep Into my Heart

## Intro
Welcome to the Hidden Deep Into my Heart challenge, here is the link to the [room](https://tryhackme.com/room/lafb2026e9) on TryHackMe.
This is an easy challenge about web enumeration and it is part of the 2026 Valentine event.

### Scenario 
Cupid's Vault was designed to protect secrets meant to stay hidden forever. Unfortunately, Cupid underestimated how determined attackers can be.

Intelligence indicates that Cupid may have unintentionally left vulnerabilities in the system. With the holiday deadline approaching, you've been tasked with uncovering what's hidden inside the vault before it's too late.

You can find the web application here: `http://10.82.186.180:5000`


<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's open our browser and navigate to the web application URL we have found tin the scenario.
The main page shows nothing interesting, we can check if the `robots.txt` file exists and have some hints for us:

```
http://10.82.186.180:5000/robots.txt
```

We find:
```
User-agent: *
Disallow: /cupids_secret_vault/*

# cupid_arrow_2026!!!
```

Navigating to that directory we find the message:
```
Cupid's Secret Vault
You've found the secret vault, but there's more to discover...
```

We can proceed with some directory scan using a tool such as *gobuster* to find hidden ones:
```bash
gobuster dir -u http://10.82.186.180:5000/cupids_s..REDACTED/  -w /usr/share/SecLists/Discovery/Web-Content/common.txt
```

We find `/administrator`, let's navigate to it at `http://10.82.186.180:5000/cupids_s..REDACTED/administrator`.
Here we can see a login page.

Since we have found a string in the `robots.txt` that looks like it could be the password, for the username, since it is in the `/administrator` we can either try that value or `admin`.
And it works, with REDACTED we log-in and we see the flag:

--> REDACTED

We also see the message:
```
Congratulations! You've discovered Cupid's secret vault and found the hidden treasure of love!
```

<br/>
<br/>

Congratulations, you have successfully fond the hidden flag.
Happy Valentine! 

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
