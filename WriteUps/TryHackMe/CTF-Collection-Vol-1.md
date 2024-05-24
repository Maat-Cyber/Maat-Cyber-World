# CTF Collection Vol. 1 Writeup

## Intro
This room is a collection of 20 Tryhackme beginner's friendly challenges, purposely made to show different CTF's topics and strategies that will be usefull in others rooms.

To solve the challenge i suggest to log into your kali linux pc, VM or use the tryhackme attack box, so you will be able to take advantage of all the inbuilt tools when necessary.

Link to the [TryHackMe room](https://tryhackme.com/r/room/ctfcollectionvol1)

The flags in this room will have the format THM{SOMETHINGHERE}

<br/>
<br/>

## The Challenges​
Let's begin, (yes it starts from number 2 🤷‍♂️)

**2. What does the base said?** <br/>
We see a  string: 
```
VEhNe2p1NTdfZDNjMGQzXzdoM19iNDUzfQ==
```

The purpose of this question is to teach us that in many challenges a text can be hide insite random words, this is simply done by converting the text to a different format and to decode it we have to know wich one.

To decode the message we can simply search online for a string decoder, paste it and check wich one gives us a readable flag. In this case is a string encoded in base64

<br/>

**3. Meta meta** <br/>
To start this task we have to download the file, if we open it we will simply see an image that wont show us the flag we need.

Taking advantage of the title we can quickly understeand that we have to search inside the file metadata to find what we need.

To do so we can use a very usefull program called *EXIFTOOL*, wich is a command line tool to check metadata;

To get our flag we can run: 
```bash
exiftool [IMAGE _NAME]
``` 

Scrolling down a bit we can see under the owner name title our flag.

<br/>​

**4. Mon, are we going to be ok?** <br/>
Again we can see there is a file to download, and image and if we open it we see a little conversation but no flags.

The hint suggest us to use STEGHIDE, a tool that will help us file files inside other files and much more.

To verify our hypotesis of a hidden file we can run this command:
```bash
steghide --info Extinction.jpg
```

And..... yes there is another file inside the photo called  "Final_message.txt"

So now we have to extract it, we can use again SETGHIDE but we have to change the syntax a little bit
```bash
steghide extract -sf Extinction.jpg     
```  

The program will ask for a passphrase but since we dont have one we can simply press enter and see if it work.... it does!

So now we will have another file in our folder: the "Final_message.txt" , lets open it 
```bash
cat Final_message.txt
```

And the flag appears.

<br/>​​

**5. Erm....Magic** <br/>
Here we dont have any file to download, to find our flag we can simply select  with the mose after the give sentence, by doing so we will highlight the hidden message that is our flag

​<br/>

**6. QRrrrr** <br/>
In this task we have another file to download and by opening it we can see that is a QR code.

To see what it is hiding we can upload the image on a website like scnqr.org that will scan our QR code and will show us the flag.

​<br/>​

**7. Reverse it or read it?** <br/>
Afer downloading the file we find out that by clicking on it we can't open it, but lets try if it doesn't open even via command like, let's run:
```bash
cat hello.hello
```

And yes the file will show on the screen some random strings but also our flag.
​
<br/>

**8. Another decoding task** <br/>
We are given again a string like in the first exercise but we can see that the format isn't the same, but is also not much different.

We can still copy `3agrSy1CewF9v8ukcSkPSYm3oKUoByUpKG4L` in an online string decoder and we find out that this time it is in base58 and by decoding it we can read the flag.

​<br/>

**9. Left or Right** <br/>
This time we can see a text `MAF{atbe_max_vtxltk}` that remeinds us of the flag's stile but with different letters, we can think that a letter rotation algorithm was used and the task tells us that is not ROT13.

We can either throw it in the same string decoder or read the hint that tells us is a ROT CHIPER text, we can look for a specific decoder online if the one you have first choosen doesn't support it and get our flag.

<br/>

**10. Make a comment** <br/>
One more time we don't have any strings, number or file to download, using the strategy of highlighting with our mouse gives no results this time.

In CTFs there are many scenarios like this were apparently there is nothing to see or do, a good practice in this cases is to always check the page source or inspect certaint parts by right clicking with the mouse and selecting one of those options.

Many times developers can forget something or hardcode things that should not be visible to everyone; in this particular case we can see that there is a comment and it is exactly what we need, the task's flag!

<br/>​

**11. Can you fix it?** <br/>
A file to download again..... ok, but as we could imagine we can't open it, the title tell us that we have to fix it meaning that there is something we have to change probably.

Just by looking at the file we can't see anything usefull beside his extension that is JPG, remember this, will be usefull later.

One way to check what's going on with the file is to see its hexadecimal value, to do so we can use a tool like hexedit; run
```bash
hexedit [FILENAME] 
```
​
Now you will see a lot's of numbers and letters, what is interesting for our task is to look at the first 8 bit, every file extension has a "magic number" that are those 8 bit that are used to identify it, by looking on the internet we can find that JPG's magic number is 89 50 4e 47 0d 0a 1a 0a,  this digits are differents from the ones we see in hexedit, so we can simply overwrite the wrong one with the correct ones and save the file before exiting.

Now if we try to open the file again it works and in the image there is our flag.

<br/>

**12. Read it** <br/>
The exercise tells us that the flag is in the tryhackme social account, by doing a quick research we find a reddit tryhackme profile but if we open it there are a lots of posts now and will be hard to find what we need.

A faster way is to practice the use of Search Dorks that will do the job for us.

In the browser's search bar we can write:
```
inurl:"reddit.com" & intext:"THM" & intitle:"tryhackme"
```

Press search and the firs result will show the flag! 

​<br/>

**13. Spin my head** <br/>
This time we are given this thing: 
```
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++++++++++++++.------------.+++++.>+++++++++++++++++++++++.<<++++++++++++++++++.>>-------------------.---------.++++++++++++++.++++++++++++.<++++++++++++++++++.+++++++++.<+++.+.>----.>++++.

```
 
A lots of signs that gives us an headache, we can copy that on the search bar or read the hint that says "brainfuck" wich is a programming language.

Now that we know what it is we can search for an online decoder to text and see the flag.

<br/> 

**14. An exclusive!** <br/>
Here we can see two different strings:
```
S1: 44585d6b2368737c65252166234f20626d

S2: 1010101010101010101010101010101010
```

And if we try to decode them like we did in the previous taks we wont find anything usefull, but the hint tells us XOR.

XOR is a logical operator (exclusive or), i suggest you to read more online about this as you will find some other rooms that will require to use it.

For now just have to know that there are tools online that can do the XOR calculation for us, so search online for one of this tools, insert the 2 string and be sure to chose ASCII as a output format because, execute it and ther is the flag.

​<br/>

**15. Binary walk** <br/>
Let's download the provided file once again, this time reading the title we 
understeand that to get the flag we have to check into the file binaries.

To do so we use a tool called  BINWALK, the syntax is:
```bash
binwalk -e hell.jpg 
```

if an error occur we might need to force the command: 
```bash
binwalk --run-as=root -e hell.jpg
```

A new file will appear in our direcorty, now we can open it and read the flag.

​<br/>​

**16. Darkness** <br/>
Another file to download, this time is apparently a black image, but we know that the flag must be inside that balck wall.

The hint tells us to use STEGOSOLVE that will help us reading what is hiding there.

To install that tool:
```bash
wget http://www.caesum.com/handbook/Stegsolve.jar -O stegsolve.jar
```

Once the download is complete we need to make it executable:​
```bash
chmod +x stegsolve.jar
```

Now we can launch it with this command:
```bash
java -jar stegsolve.jar
```

The program will starts, go to open and chose the task file, than keep pressing the right or left botton until we find the correct mode and the text containing the flag will appear.
​
<br/>
​
**17. A sounding QR** <br/>
After downloading the file we can see it is another QR code, let's upload it like we did on task6 on scnqr.org, it will give us a link: 
```
https://soundcloud.com/user-86667759/thm-ctf-vol1.
```

By clicking on it we will be prompted to a new web-page with a sound track, listen it carefully and u will hear the flag.

​<br/>

**18. Dig up the past.** <br/>
The purpose of this task is to show us that there is a website wich inside has snapshots of many many websites during time, in this way we can visit a "website of the past" like a time travel.

WE have to give the time machine the correct instructions:

Targetted website: https://www.embeddedhacker.com/
Targetted time: 2 January 2020

Than click on the correct calendar date and the old website version will appear, look around the page and you will find the flag.

<br/>​

**19. Uncrackable!** <br/>
This task tells us 2 things: 
```
MYKAHODTQ{RVG_YVGGK_FAL_WXF}
```
Flag format: TRYHACKME{FLAG IN ALL CAP}

The hint says vingenere cipher.

Let's find the proper decoder online and put the first phrase, but to proceede we need a KEY, by re looking at the 2 things provided in the task we can notice that this time the flag doesn't starts with THM....... hmmm... maybe is an hint that this 3 letters are the key, insert them as the key, press enter and YES we have the flag.

<br/> 

**20. Small bases** <br/>
There is a long series  of numbers, if we put it in an online decoder at first gives us no text.

Reading the hint we now know that we have to do multiple decodings: dec -> hex -> ascii --> from decimal to hexadecimal and finally to text.

Let's search for a tool online, i've used this website: https://www.rapidtables.com/convert/number, do the double decoding and get the flag.

<br/>

**21. Read th packet** <br/>
For the last task we have to download another file, looking at it we see is a PCAP file, this mean is a WIRESHARK capture, so let's open it.

Ok now we see a very long list of packets, we know that we have to check if in one of this captures there is the flag.

If it is yor first time i suggest you to go and take a look at TryHackMe Wireshark's room to understeand how it works and how to read and filter packets as this tool will be very usefull in the future.

So now we can chose to apply all the right filters or destroy our head by scrolling and manually inspecting all the packets until we find something usefull.

The things of our interest appear on packets 1825 and 1827, infact we can see a certaing flag.txt file, the one we want to investgate more is the 1827, open it and check in the data part to see the flag.
 
<br/>
<br/>

And with this the room is finished, i hope you had fun and learnt something new completing it like i did.

I hope to see you again in another challege 😊
