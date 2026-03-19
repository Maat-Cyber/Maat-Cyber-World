# The Game v2 Walkthrough
## Intro
Welcome to the The Game v2 challenge, here is the link to the [room](https://tryhackme.com/room/hfb1thegamev2) on TryHackMe.

This is the second version of The Game challenge, i have made a write-up of it [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/3be7499aff35e6eeaa54d6435f1e5f825e01a133/WriteUps/TryHackMe/The-Game/The-Game.md).

In this one we are gonna deal again with the game executable but we'll have to dig a bit more.

"*Cipher’s trail led us to a new version of Tetris hiding encrypted information. As we cracked its code, a chilling message emerged: "The game is never over."*"

Whenever you feel ready click on "Download Task Files"
Let's begin!

<br/>
<br/>

## The Challenge
The downloaded file is called `TetrixFinal.exe.zip`, is an archive, we can extract the content with:
```bash
unzip TetrixFinal.exe.zip
```

We get the following files:
```
.
├── __MACOSX
│   └── ._TetrixFinal.exe
├── TetrixFinal.exe
└── TetrixFinal.exe.zip
```

If we try to get the flag like in the first challenge with:
```bash
 strings TetrixFinal.exe | grep THM
```

We see "THM{GAME_MASTER_HACKER}" which is not the right one and clearly mocking us.. lol.

Checking some other strings in general i found out the game is using *godot* engine:
```
godot
godot: ENABLING GL DEBUG
https://godotengine.org
[96m[options] [path to scene or "project.godot" file]
```

Having no clue about what that is i went on a search online and reached this reverse engineering project on GitHub, link [here](https://github.com/GDRETools/gdsdecomp).
```bash
wget https://github.com/GDRETools/gdsdecomp/releases/download/v2.4.0/GDRE_tools-v2.4.0-linux.zip
```

We can now unzip the archive:
```bash
 unzip GDRE_tools-v2.4.0-linux.zip
```

Launch the tool and import the game executable:
```bash
 ./gdre_tools.x86_64
```

Now again, since we are on a CTF and not on a real pentest i am looking for quick wins, i recovered the project with the tool, then navigating the new directory with all the files we can find a file called `sol.jpg` which contains a string.
Opening the image we find the flag that will be presented to the player if some conditions are met.

--> REDACTED

<br/>
<br/>

Congratulations, you have successfully found the flag in the game's assets.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
