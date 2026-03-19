# The Game Walkthrough
## Intro
Welcome to the The Game challenge, here is the link to the [room](https://tryhackme.com/room/hfb1thegame) on TryHackMe.
This is a very easy challenge about a windows executable game file.

"*Cipher has gone dark, but intel reveals he’s hiding critical secrets inside Tetris, a popular video game. Hack it and uncover the encrypted data buried in its code.*"

Whenever you feel ready click on "Download Task Files"
Let's begin!

<br/>
<br/>

## The Challenge
The downloaded file is called `Tetrix.exe.zip`, is an archive, we can extract the content with:
```bash
unzip Tetrix.exe.zip
```

This gives us the Tetrix executable + a `__MACOSX` directory:
```
├── __MACOSX
│   └── ._Tetrix.exe
├── Tetrix.exe
```

Before running the executable and thinking about disasembling it we can check for quick wins using `strings`.
We know that flags on TryHackMe are in the format of `THM{}`, let's check if it is there in plain-text:
```bash
strings Tetrix.exe | grep THM
```

Yep, we have already found the flag and concluded the challenge:
-->REDACTED

<br/>
<br/>

Congratulations, you have successfully found the hidden flag.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
