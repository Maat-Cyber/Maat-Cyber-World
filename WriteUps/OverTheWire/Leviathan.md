# Leviathan Walkthrough
Welcome to the Leviathan challenge from OverTheWire!
Here is the link to the official [page](https://overthewire.org/wargames/leviathan/)

Leviathan is a wargame that has been rescued from the demise of **intruded.net**, previously hosted on leviathan.intruded.net. **Big thanks to adc, morla and reth** for their help in resurrecting this game!

What follows below is the original description of leviathan, copied from intruded.net:
```
Summary:
Difficulty:     1/10
Levels:         8
Platform:   Linux/x86

Author:
Anders Tonfeldt

Special Thanks:
We would like to thank AstroMonk for coming up with a replacement idea for the last level,
deadfood for finding a leveljump and Coi for finding a non-planned vulnerability.

Description:
This wargame doesn't require any knowledge about programming - just a bit of common
sense and some knowledge about basic *nix commands. We had no idea that it'd be this
hard to make an interesting wargame that wouldn't require programming abilities from 
the players. Hopefully we made an interesting challenge for the new ones.
```

Leviathan’s levels are called **leviathan0, leviathan1, … etc.** and can be accessed on **leviathan.labs.overthewire.org** through SSH on port 2223.

To login to the first level use:
```
Username: leviathan0
Password: leviathan0
```

Data for the levels can be found in **the home directories**. You can look at **/etc/leviathan_pass** for the various level passwords.

<br/>
<br/>

### LEVEL 0 --> 1
Login into the machine via ssh
```zsh
ssh leviathan0@leviathan.labs.overthewire.org -p 2223
```
Insert the password "leviathan0" and we are in the first machine.

Now we are in the home directory of leviathan0, let's see what is inside using
```zsh
ls -la
```

We can see that some files and directory pops up, the one that intantly appears interesting is ".backup"  because it is also owned by leviathan1, the user we are trying to find the password of.

Navigate in that directory
```zsh
cd .backup
```

Let's see what's inside
```zsh
ls -la
```

There is a file: "bookmarks.html", maybe it contains the password?
Try to open it
```bash
cat bookmarks.html
```

Ok, there are too many lines, of code, maybe we can filter it with a keyword and see if anything useful appears.
To do so we can use the command `grep`, and as keyword i have chosen "password", run it
```bash
cat bookmarks.html | grep password
```

Much better now, and we can also see the password for leviathan1 : PPIfmI1qsA
<br/>
<br/>

### LEVEL 1 --> 2
Login into the machine via ssh
```bash
ssh leviathan1@leviathan.labs.overthewire.org -p 2223
```
Insert the password we have found in the previous level.

Let's see the content of the home directory
```bash
ls -la
```

Running the `ls` command with the `-l` flag gives us also the files permissions and tells information about the owner and group for the files.
We can see that "check" is owned by leviathan2 and we also have execute permissions, another interesting thing is that is has the SUID bit set.

If we try to execute it with
```bash
./check
```
It will ask us for a password that we don't yet know.

If we try to view the file with `cat` it will show us a lot of non readable characters, even using `strings` doesn't gives us more usefull infroamtions.
We can try another way, we can use a debugging utility like `ltreace`
```bash
ltrace ./check
```

Now we can analyze it and we come across word "sex", why is it in an executable? could it be the password that the executable want us to insert? let's try it.
I have ran again, as before, and provied the password, now we get a shell and if we check who we are with `whoami` we can see that now we are leviathan2.
We can retreive the password with
```bash
cat /etc/leviathan_pass/leviathan2
```

And there we have it : mEh5PNl10e
<br/>
<br/>

### LEVEL 2 --> 3
Login into the machine via ssh
```bash
ssh leviathan2@leviathan.labs.overthewire.org -p 2223
```
Insert the password we have found in the previous level.

Check the content of the home directory with
```bash
ls -la
```

We can see an executable called "printfile" that is owned by leviathan3 and the SUID bit is set.

The binary will print a file of choice, so we can try to print the one that contains the next level's password
```bash
./printfile /etc/leviathan_pass/leviathan3
```
Doing so we get an error saying that we can't have that file.

To better understeand it's behaviour we can create a file, use `ltrace` and compare the output of `ltrace` while we try to retrive the password file.

Create a directory and the text file 
```bash
mkdir /tmp/test
```
```bash
echo "text" > text.txt
```

Now we can trace the behaviour
```bash
ltrace ./printfile /tmp/test/text.txt
```
```bash
ltrace ./printfile /etc/leviathan_pass/leviathan3
```

The first thing we can notice comparing the 2 outputs is that the "access" function returned two different values: in the first case "0" and in the second "-1"; this is becose the function catches different file permissions for the file we want to read and in the second case it lack some and the program exits.

We need a way to bypass this problem...
Testing out the "printfile", we also understeand that if we  put 2 files only the first one get printed; another interesting behaviour is that if we create a file with a space in the middle of the filename, the access function looks at the whole filename, BUT /bin/cat only get the part before the space.

Knowing this we can create a new file that links the password file and gives leviathan3 user permissions to access the directory. Doing so the executable will be able to open the password file.

Ok many things all toghether, let's do it step by step:
Create the file with the space in the name
```bash
touch /tmp/test1/"test file.txt"
```

Creathe the link between the 2 files
```bash
ln -s /etc/leviathan_pass/leviathan3 /tmp/test1/test
```

Finally print the file to get the password
```bash
./printfile /tmp/test1/"test file.txt"
```

And the password will be displayed right before the error message : Q0G8j4sakn
<br/>
<br/>

### LEVEL 3 --> 4
Login into the machine via ssh
```bash
ssh leviathan3@leviathan.labs.overthewire.org -p 2223
```
Insert the password we have found in the previous level.

Check the content of the home directory with
```bash
ls -la
```

This time we can see a file, an executable, called "level3", it is owned by leviathan4 and has the SUID bit set.

If we try to execute it
```bash
./level3
```
it tells us to enter the password, but we don't know it, yet at least.

We can analyze the behavior with
```bash
ltrace ./level3
```
We can see a function called "strcmp" which is used to handle strings comparison, to be more specific it will compare the characters of the two strings in sequence until it finds a mismatch or until the end of the strings is reached.

Keep reading we can see that the string it look  for a match is "snlprintf", so we can simpy write that word when we are prompted for a password.

So run the executable, insert the password and we will be logged in a shell as leviathan3, now we can read the user password with
```bash
cat /etc/leviathan_pass/leviathan4
```

And here we have it : AgvropI4OA
<br/>
<br/>

### LEVEL 4 --> 5
Login into the machine via ssh
```bash
ssh leviathan4@leviathan.labs.overthewire.org -p 2223
```
Insert the password we have found in the previous level.

Check the content of the home directory with
```bash
ls -la
```

We can see there is ther trash directory, maybe something usefull to us was recently deleted, let's find out
```bash
cd .trash
```
```bash
ls -la
```

A file called "bin", is also an excutable, let's find out what it does by either using `ltrace` to understan his behavior or just by running it
```bash
ltrace ./bin
```

We can see that it prints out the leviathan5 password, but when we run the binary it gives us a binary encoded output, that's easy to solve, we can simply go online and find a converter from binary to text and once the message is decoded we have our password :  EKKlTF1Xqs
<br/>
<br/>

### LEVEL 5 --> 6
Login into the machine via ssh
```bash
ssh leviathan5@leviathan.labs.overthewire.org -p 2223
```
Insert the password we have found in the previous level.

Check the content of the home directory with
```bash
ls -la
```

This time we have an executable owned by leviathan6 with the SUID bit set;
We can analyze it with
```bash
ltrace ./leviathan5
```

The executable will try to open the file.log file, the "r" switch is for readingf mode; and if we run it it prints a message "cannot find /tmp/file.log" because that file doesn't really exist.

We can exploit that function by creating a link between the file with the passowrd and the log one :
```bash
ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log
```

Now when we run again the execitable we should have printed the password for the next level
```bash
./leviathan5
```

And yes here we have it : YZ55XPVk2l
<br/>
<br/>

### LEVEL 6 --> 7
Login into the machine via ssh
```bash
ssh leviathan6@leviathan.labs.overthewire.org -p 2223
```
Insert the password we have found in the previous level.

Check the content of the home directory with
```bash
ls -la
```

Another executable called "leviathan6", with the usual SUID bit set and owned by leviathan7.

If we analyze what it does
```bash
ltrace ./leviathan6
```
it will ask us to insert a 4 digit code.

From further analysis opening the executable with
```bash
string leviathan6
```
or even with cat, i was able to see `bin/bash` close to the end of the code, this means that once the 4 digit are checked the executable will give us a shell as leviathan7.

So... how can we find the right pin? 
Well... i kinda wanted to brute force something today.... so one way is to try to give the executable all the 4 digits combinations.

To do that i created a custom script than will print to a file the command + the digits, than we will transform that  file into an executable and run it to do the actual "brute forcing".
Here are all the steps

1. create a new folder, 
```bash
mkdir /tmp/newfolder
```

2. use this script to print the command + all the 4 digits combinations
```
for i in {0000..9999}; do echo ./leviathan6 $i" >> file; done
```

3. make the new file executable, it is the one that will do the brute-forcing for us
```bash
chamod +x file
```

4. Now from leviathan6 home directory run our brute force executable
```bash
/tmp/newfolder/file
```

Now it will try all the combinations and after all the "wrong" messages we will have a shell as leviathan7; you can check it by running
```bash
whoami
```

Now since we are leviathan7 we can read our own password with
```bash
cat /etc/leviathan_pass/leviathan7
```

And the password is : 8GpZ5f8Hze

**Extra Mile**
For the curious out there, by using this method we actually don't need to know the right pin, but what if after completing the level we want to know it?
One way is to copy all the "wrong" messages returned in the ssh session, check how many are them (7123), this means that the 7124th combination in the sheet was the right one, since the first one start with 0000, to find the right pin we can simply do 7124-1 which is 7123.

If you want to check it you can exit from the leviathan7 shell, re-run the executable and provide it the pin 7123 and you will instantly get the shell again !
<br/>
<br/>

### LEVEL 7 --> 8
Login into the machine via ssh
```bash
ssh leviathan7@leviathan.labs.overthewire.org -p 2223
```
Insert the password we have found in the previous level.

Welcome in the final level of the challenge!

Check the content of the home directory with
```bash
ls -la
```

There is a file called "CONGRATULATIONS", open it
```zsh
cat CON*
```

<br/>
<br/>
Congratulations, you have completed the leviathan challenge!
Thanks for following along, if you liked it you can check my others CTFs write ups 😃 
