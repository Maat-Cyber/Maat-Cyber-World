# OverHeard at Breakfast Walkthrough
<br/>

## Intro
Welcome to the OverHeard at Breakfast challenge, here is the link to the [room](https://tryhackme.com/room/hh-overheardatbreakfast-6f01793c) on TryHackMe.

This is a very easy level challege about a little bit of OSINT .

"*The breakfast terrace is loud this morning, clinking cutlery, espresso machines, the usual chatter. One guest couldn't help but linger at a nearby table, seeing more of a conversation than they were meant to.
When the table's occupant stepped away for a refill, they seized the moment and grabbed a screenshot before it could disappear. Somewhere in that conversation is enough to track down an account nobody was supposed to find.*"

Let's begin!

<br/>
<br/>

## The Challenge
Download the zip file and unpack it:
```bash
unzip overheard-at-breakfast.zip
```

Inside there is only one image containing a chat between 2 people.

Close to the end we find this email address `lambobytelotushotel@gmail.com` plus an hit that the user was on a site starting with a `G` that allows to upload a profile image and links to other social media.

First thing we need to find out what that site is, a quick search tells us that this site could be **Gravatar**.

Inserting the email in that website lands us to `https://gravatar.com/cheerfullysongf28e3c3716` where we find a base64 encoded string:
```bash
 echo "VEhNe1MzY3JlVF9QcjBmaWwzX0g0c19iMzNuX0lkZW50MWZpM2R9" |base64 -d
```

And here we have our flag:
--> REDACTED


<br/>
<br/>

Congratulations, you have successfully found the `G` website, located the user profile and decoded the flag!

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
