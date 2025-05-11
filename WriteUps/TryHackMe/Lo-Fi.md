# Lo-Fi Walktorugh
<br/>

## Intro
Welcome to the Lo-Fi challenge, here is the link to the [room](https://tryhackme.com/room/lofi) on TryHackMe.

This is a "very easy" challenge, once we spot the vulnearble point it is trivial to exploit it.

Navigate to the following URL using the AttackBox: `http://MACHINE_IP` and find the flag in the root of the filesystem.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's visit the challenge website: `http://MACHINE_IP`

Looking on the side panel we can see a search function, also checking the source code we can see pages located at `http://MACHINE_IP/?page=relax.php`.

Thje `page` parameter get's passed in the URL.
In php this is usually used to redirect or fetch another page, it is archived by specifying the path to the "next page".

But this function if not properly handled can be vulnrable to manipulation by an user to reach restricted pages.

We can try to manipulate it to exploit a possible Path Traversal Vulnerability like:
```
http://MACHINE_IP/?page=../../../../../../flag.txt
```

This worked and we got the flag:
-->  REDACTED

<br/>
<br/>

## Conclusion
Congratulations you have successfully found and exploited the LFI vulnearability to read the flag file!

As per the intro, this was a quick POC on how LFI works and can be found on web applications.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
