# Love Letter Locker Walkthrough

## Intro
Welcome to the Love Letter Locker challenge, here is the link to the [room](https://tryhackme.com/room/lafb2026e2) on TryHackMe.
This is a quick and easy level challenge about a specific common vulnerability in a web application, part of the Valentine 2026 event.

### Scenario 
Welcome to Lover Letter Locker, where you can safely write and store your Valentine's letters. For your eyes only?

You can access the web app here: `http://MACHINE_IP:5000`

<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
Let's go and take a look at the website at `http://10.82.160.233:5000`.
We find Cupid's new storage service, let's create a new account and log-in.

In the home page we find some interesting info, there are a total of 2 letters in the archive but we cant see them, we also that "love letter gets a unique number in the archive."
This makes me think about an IDOR hidden somewhere, let's see if this is the case.

We can try to create a test letter to see what happens, once created we see the counter going from 2->3  and since we have created this letter we can click on it in the `/letters` page.
Upon clicking on the letter we reach the page `http://10.81.173.88:5000/letter/3` and we can see the letter's content.

And as imagined my was the third letter and got the ID 3 in the URL, if the IDOR i was thinking about previously exist we should be able to change the ID at the end of the URL to 1 or 2 and see the content of this 2 letters.

Yes, `http://10.81.173.88:5000/letter/1` we can see the letter containing the flag:
-->  REDACTED 

For those that are interested IDOR stands for **Insecure Direct Object Reference** and is a vulnerability that arises when attackers can access or modify objects by manipulating identifiers used in a web application's URLs or parameters. 

This happens because the proper controls are either not well implemented or completely missing, failinfg to verify if the user should be allowed to access specific resources.

In our situation in fact there were no checks at all and our test user was able to read someone else's letter, which obviously should not be possible.

<br/>
<br/>

Congratulations, you have successfully exploited  the Indirect Object Reference Vulnerability in the web-application and retrieved the the letter containing the flag.

Happy Valentine!

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
