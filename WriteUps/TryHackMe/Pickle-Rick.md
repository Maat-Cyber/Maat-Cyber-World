# Pickle Rick Walkthrough

## Intro
Welcome to another CTF walktrought, here is the link to the TryHackMe room https://tryhackme.com/room/picklerick.

In order to solve this challenge we will need some tools:
- nmap
- Nikto
- Burp Suite

If you have never heard of this tools i suggest you to study them first or complete the THM rooms, so you will have a better understeanding of what we are going to do.

Whenever you fell ready you can begin pressing START MACHINE;

To be able to interact with the machine, as THM explains you can either use their attack box or use your own kali linux machine by connecyting it via openVPN.

The walktrought won't contain the answers, to not take away the fun, but a step by step tutorial to reach them, by following it you will just have to read the flag or he answers on your own machine.

​
Now that everything has been set let's start with the CTF.
​
<br/>
<br/>

## HOW TO START
A good way to approach all the CTFs is to always start by launching an nmap scan, you can use de -a- flag to scan all ports or avoid it to scan only the most common ports.

Let's run it
```bash
nmap -sV [MACHINE IP] 
```

The result shows us that ports 22 and 80 are open, respectively running ssh and Apache http server.

<br>

Now we know that there is a website running on port 80, let's visit it 
```
http://[MACHINE IP]
```
​
Here we find an image with a little dialogue that gives us a big hint, it says he need him to BURP, wich remind us a very usefull tool, the BURP SUITE.

Open burp suite, go on PROXY and cpture the request of the website;

To do so you have to turn on the intercept and than you can chose to use their own browser or an extension like foxyproxy for firefox that will route the traffic trought burp suite.

Go on the repeater page, press SEND and than inspect carefully the response, you will find an username: R1ckRul3s.

<br>
​
We can now use NIKTO to check for hidden pages, the syntax is
```bash
nikto -h [MACHINE IP] 
```

We will see an interesting page: login.php

Let's go to visit it: 
```
http://MACHINE IP/login.php
```

It asks us an username, the one we have already found before and a password.

​<br>

We can run GOBUSTER that is quite fast to chck for other pages.
```bash
gobuster dir -u http://[YOUR MACHINE IP]  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
``` 

We get a page called /robots.txt

Let's visit it and we find this: Wubbalubbadubdub;
Maybe it is the password.

​<br>

Go on the login page again, insert the credentials and yes we have access now.

Here we find an empty page with a line that says Command panel, let's try to see which commands can we run.

I started with `ls` to see what's inside and i got a list of files, the interesting one is the first
--> Sup3rS3cretPickl3Ingred.txt

Looks like inside we will find the **FIRST INGREDIENT** to answer the first question.

Open the file
```bash
cat Sup3rS3cretPickl3Ingred.txt 
```

But it does not work, so i have tried again with another command: LESS and this time the files open and shows us the ingredient.

​

At this point i thought to inspect the page source to see if there were any hints or useful information, and at the end of the page we can see a comment with a long hash.
```
<!--Vm1wR1UxTnRWa2RUV0d4VFlrZFNjRlV3V2t0alJsWnlWbXQwVkUxV1duaFZNakExVkcxS1NHVkliRmhoTVhCb1ZsWmFWMVpWTVVWaGVqQT0== -->
```


Back again to the insert command spot, doing `ls` again we find another interesting file: clue.txt, once open it suggests us to look around in the file system.

At this point looks like we wont get any more information from here, we have to check in other directories, to do so we can use a technique called DIRECTORY TRAVERSAL.

let's start testing and after a bit doing it i found the second ingredient in rick's home directory, you can see it too with this command:
```
ls ../../../home/rick 
```

Now is time to open it and see what it is
```
less ../../../home/rick/'second ingredients' 
```
And here it is the **SECOND INGREDIENT**.

​<br>

Time to get our THIRD INGREDIENT

Considering that the previous one was in rick's home directory and since every machine has a root's one i tried to check there
```bash
ls /root 
```

Nothing happens, let's try again adding sudo, may we need higher privileges to do it, and yes we can see tha inside that there is a file called 3rd.txt

Open it
```bash
sudo less /root/3rd.txt 
```

Here we have our LAST INGREDIENT!

<br/>
<br/>

Congratulations, the room is finished, hope you had fun like i did.

If you want to see more CTFs Writeups explore the directory.

See you in the next challenge. 😊
