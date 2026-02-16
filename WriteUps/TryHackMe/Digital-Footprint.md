# Digital Footprint Walkthrough

## Intro
Welcome to the Digital Footprint challenge, here is the link to the [room](https://tryhackme.com/room/osintchallengeiv) on TryHackMe.
This is and OSINT challenge divided into 4 parts, for each one of them we will have to investigate the file/website to uncover the hidden flags.

Whenever you feel ready download the task's files.

Let's begin!

<br/>
<br/>

## The Challenge 

### The Leaked Photo
We can see 1 image gets downloaded, called `edited-house.jpg`, and guess what... its an image of an house.
Jokes aside, we can view the image metadata:
```bash
exiftool edited-house.jpg
```

In the exif data we can spot the GPS Position coordinates:
```
 26 deg 12' 14.76", 28 deg 2' 50.28"
```

We can go on Google Maps and paste that to find out the city and country name.
But google does not like that format so we can fix it as such:
```
26°12'14.8"S 28°02'50.3"E
```

--> REDACTED

<br/>

### Archived Company Website
For this section we find this scenario:
```
ACME Jet Solutions (warc-acme.com/jef/), is all over social meda claiming they were founded in 2025 and that they're the fastest-growing data company in Africa.
But something doesn't add up, one of their ex-employees ensures you that the company existed long before that.

Your job as an OSINT investigator is to verify their founding date using only public information.
```

You should start with a search on your favourite search engine, if you do not find anyting useful maybe the website existed in the past... give a look at `archive.org` and its wayback machine

--> REDACTED

<br/>

### Mysterious Landmark
Now we need to download another image:
```
Research reveals that to the right of the iconic landmark is a building that played a big role in the fight for independence of a particular country. Signs on the external wall provides the name of the building. 

Submit the name of building translated into English as the flag.
```

We can do a reverse image search with the given image and we find out that it is the `Spire of Dublin` monument.
Now that we know the location we can use "street-view" in google maps to find out about the name of the building.

You should find a text written in Gaelic `Ard Oifis an puisc`, we can translate that online and we get `the head office of the post office`.

With this new info we can research for that related precise name online and we get the answer.

--> REDACTED

<br/>

### Internal Documents
For the last part we need to download another file, this time is a `.odt` document.
```
After uncovering ACME Jet Solutions origins and tracing their online presence through archived websites and international landmarks, investigators believe that an internal document was accidentally leaked by one of the company's developers. 

The document may contain crucial information about the individual responsible for maintaining their systems. 
```

Here exiftool will help again:
```
exiftool internal-docs.odt 
```

We find a use called: REDACTED
We can also notice that the file contains a zip archive inside, we can extract it:
```bash
unzip internal-docs.odt
```

We get a series of files:
```
Archive:  internal-docs.odt
 extracting: mimetype
   creating: Configurations2/
  inflating: styles.xml
  inflating: manifest.rdf
  inflating: content.xml
  inflating: meta.xml
  inflating: settings.xml
 extracting: Thumbnails/thumbnail.png
  inflating: META-INF/manifest.xml
```

Nothing more interesting there.
Probably just the file structure.

Anyway in the original document we see this sentence:
```
I will be releasing a video very soon, I implore everyone to watch it!
```

Since we have the username let's search on YT if he has uploaded any video.

We see no videos but there if a channel: `https://www.youtube.com/@markwilliams7243` with a comment inside, if we expand that we can see the final flag.

--> REDACTED

<br/>
<br/>

Congratulations, thanks to your OSINT skill you were able to uncover all the hidden flags of this CTF.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
