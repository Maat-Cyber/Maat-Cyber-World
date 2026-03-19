# When Hearts Collide Walkthrough

## Intro
Welcome to the When Hearts Collide challenge, here is the link to the [room](https://tryhackme.com/room/lafb2026e1) on TryHackMe.
This is a medium level challenge about a web/crytpo vulnerability, part of the Valentine 2026 event.

### Scenario 
Matchmaker is a playful, hash-powered experience that pairs you with your ideal dog by comparing MD5 fingerprints. Upload a photo, let the hash chemistry do its thing, and watch the site reveal whether your vibe already matches one of our curated pups. The algorithm is completely transparent, making every match feel like a wink from fate instead of random swipes.

Come get your dog today!

You can access the web app here: `http://MACHINE_IP`

<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
Let's take a look at the website by navigating to `http://MACHINE_IP` in our web browser.
We can find an upload functionality, we can test with a random file and its says no match found.

What the app does is checking the MD5 hash of the uploaded picture and compare it with what it has in the database, if it is the same value we get the flag.

Basically we need to exploit an MD5 hashing algorithm vulnerability called *hash collision*, that is when 2 files even if different can have the same hash.
If you want to know more about it i found this GitHub project README file being nice: https://github.com/corkami/collisions

Download the dog pic of the website:
```bash
 wget http://10.81.174.72/view/00795a8b-fb58-47c0-91be-af068ddc71b4.jpg
```

We can use *Fastcoll* to generate an hash collision, you can either compile the official project or pull this third-party docker image
```bash
docker pull brimstone/fastcoll  
```
```bash
docker run --rm -v $PWD:/work -w /work brimstone/fastcoll --prefixfile 1.png - copy.jpg
```

Then submit the copy image and get the flag:
--> REDACTED

<br/>
<br/>

Congratulations, you have successfully performed an hash-collision attack and submitted the crafted image to get the flag.

Happy Valentine!

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
