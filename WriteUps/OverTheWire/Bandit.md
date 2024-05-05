# Bandit
Welcome to the first CTF of the WarGames from OverTheWire.

This CTF series is created for beginners, it will leads us trough many useful linux commands and tools.

The challenge is constructed in 34 levels, in each level we need to find a password or a way to access the next one.
To access the Bandit challenge you will need a linux machine and we will use SSH to remotely connect to the target machine.


Here is the link to the original OverTheWire page with the rules and a quick explaination https://overthewire.org/wargames/bandit

Once you are ready let's start by connecting to the level 0 machine with the following command
```
ssh bandit0@bandit.labs.overthewire.org -p 2220
```
The password is bandit0

To access every level you will need to change the number of it and then proceed to insert the password.
After the end of every level remember to use the command exit to close the ssh session so you can start the next one.

The Passwords provided may vary in the future, so use this guide to reach the solution on your own and get your code.

<br/>
<br/>

---
### LEVEL 0 --> 1
Login with 
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```
After logging into any machine the first thing to do is to check what's inside it, like when you get a pack; to do so we can use the command ls.

After typing ls and pressing enter we will see a file called "readme", to open a file the most common command is cat, so let' use it.
```bash
cat readme 
```
​
And we will be given a code that will be the password to ssh login into level1.
--> NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL

​<br/>
---

### LEVEL 1 --> 2
Login with 
```bash
ssh bandit1@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

​Let's do ls again and we find a file called "-"

​To open it we use:
```bash
cat ./- 
```

​And we have the password: rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi

​<br/>
---

### LEVEL 2 --> 3
Login with 
```bash
ssh bandit2@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

​We begin as always with the ls command and we find a file called: spaces in this filename.

​This level was created to teach us how to open or select a file that has spaces in the name, they correct way to do it is by using " " (double quote) at the start and at end of the name.
​Than to open is we use the cat command.

​The final command will look like this:
--> cat "spaces in this filename" 
​
And we will see the password: aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG

​<br/>
---

### LEVEL 3 --> 4
Login with 
```bash
ssh bandit3@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

​We begin as always with the ls command;
This time we see not a file but a folder, to go inside the folder we use the command cd with the folder name.
​
The final command will be:
--> cd inhere 

Once there we try to use ls to see what's inside but nothing seems to appear, in this situation we have to use it with the flag -la that means list all.
--> ls -la
​
And now we can see there is a file called  .hidden

To open it we can simply use the cat command with this file name.
--> cat .hidden 

​And now we have found the password: 2EW7BBsr6aMMoJ2HjW067dm8EgX26xNe

​<br/>
---

### LEVEL 4 --> 5
Login with 
```bash
ssh bandit4@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

​We begin as always with the ls command;
As the previous level we see a folder, cd inside it.

​
Now we find 9 different  files and the hint says that the password is in the only human-readable file.
There are various options: open every file, open all files or look for the only one with text inside it.

​I will show the option3 as i think the purpose here is to learn how to use the find command.

To do so we will write:
--> find . -type f | xargs file 

​We will get something like this:  
  
​Looking at it we can see that file number 7 is the only one with text inside.
​
We open it with cat as we did in level1
--> cat ./file07
​
And we get the password: lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR

​<br/>
---
​
### LEVEL 5 --> 6
Login with 
```bash
ssh bandit5@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

​We begin as always with the ls command;
As the previous level we see a folder, cd inside it.

​
This time we are presented with many different folders and the password is in the one that has this properties:
- human-readable
- 1033 bytes in size
- not executable
    
To avoid checking in every folder we can use the find command and specify some more info about the file we want to see.
--> find . -type f -size 1033c |xargs file 

​This way we looked for: a file, a size of 1033 bytes and that is a text file.
Quickly we get:  ./maybehere07/.file2: ASCII text, with very long lines (1000)

​Now is time to open it:
--> cat maybehere07/.file2 

​And here we have the password: P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU  
  
​<br/>
---

### LEVEL 6 --> 7
Login with 
```bash
ssh bandit6@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

​We begin as always with the ls command but we can't see anything useful even adding the -la tag.

We have a nice hint that tells us where is the password located, in a file:
- owned by user bandit7
- owned by group bandit6
- 33 bytes in size

Well, guess what we can use find again and put all this inside of it
--> find / -user bandit7 -group bandit6 -type f -size 33c  

Now a long list may appear with a lot's of "permission denied" but looking closely we will find what we need is here: /var/lib/dpkg/info/bandit7.password
Bingo! now we just need to open it with cat command
--> cat /var/lib/dpkg/info/bandit7.password 

And the password is : z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S  

​<br/>
---
 
### LEVEL 7 --> 8
Login with 
```bash
ssh bandit7@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

​We begin as always with the ls command;
We see a file called data.txt but if we open it with cat as usual we get a huge amount on words and numbers.

The hint tells us that what we need is near the word "millionth", to quickly get the password without reading the whole list we can use the command grep together with cat to show only the line we need.
--> cat data.txt |grep millionth  

And yep we got the word "millionth" underlined and near it the password TESKZC0XvTetK0S9xNwm25STk5iWrBvP  

​<br/>
---
​
### LEVEL 8 --> 9
Login with 
```bash
ssh bandit8@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

​We begin as always with the ls command;
We find a file called data.txt, if we open it with cat we can see a very long lis of passwords but only one is the correct one and, as the hint says, is the one that recurr only once.

To achieve this we have to use 2 new commands, sort and uniq:
--> sort data.txt | uniq -u | cat

sort, as we can immagine will sort all entries and uniq -u will delete all the duplicate lines that occurs consecutively, in this way we will be left with the only line that's unique.

EN632PlfYiZbn3PhVK3XOGSlNInNE00t

​<br/>
---

### LEVEL 9 --> 10
Login with 
```bash
ssh bandit9@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

We begin as always with the ls command;
Ok, a very long list of non readable characters and this time the password is ne of the few human-readable strings, preceded by several ‘=’ characters.

This time we can't use cat because if we try to use it we will see something we aren't able to read, so we will use the command strings together with grep to call out the line with the "=" at the start.

```bash
strings data.txt | grep "="
```

Doing so we get some different lines here but we can quickly see which one is similar to the previous levels' password: G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s

​<br/>
---

### LEVEL 10 --> 11
Login with 
```bash
ssh bandit10@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

We begin as always with the ls command;
This time the data.txt file is encoded in base 64, so to decode it we can either open the file, copy the content and paste it in an online decoder or we can use a linux command: base64 that will do the same thing locally.

```bash
base64 -d data.txt
```

And here we have the password: 6zPeziLdR2RKNdNYFNb6nVCKzphlXHBM

​<br/>
---

### LEVEL 11 --> 12
Login with
```bash
ssh bandit11@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

We begin as always with the ls command;
This time the data.txt file is a text file, but the password has been changed from the original, all letters have been rotated by 13 positions. To see the old password we can open the file, copy the text WIAOOSFzMjXXBC0KoSKBbJ8puQm5lIEi, search online for a ROT13 decoder, paste it and here we have the right password:
JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv

​<br/>
---

### LEVEL 12 --> 13
Login with 
```bash
ssh bandit12@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

We begin as always with the ls command;
This time the data.txt file is a file full of hex digits that we can't read, the file is an hexdump.

Ok this one is a bit long to solve, read the hint and follow closely: 

1-make a new directory
```bash
mkdir /tmp/new
```

2-copy the file in the new directory
```bash
cp data.txt /tmp/new
```

3-go in the new directory
```bash
xd /tmp/new
```

4-rename the file
```bash
mv data.txt newname.txt
```

5-do a reverse hashdump of the file with xxd
```bash
xxd -r newname.txt > pass.txt
```

6-control that the new file has been created
```bash
ls
```


FROM NOW ON WE WILL KEEP REPEATING THE CYCLE OF LOOKING AT THE FILE TIPE, CHANGE TO THE CORRECT EXTENSION AND  UNZIPPING THE FILE IN THE DIFFERENT FORMATS TILL WE GET A TEXT FILE WE CAN READ

7-check the new file format
```bash
file pass.txt
```

8- rename the file with the correct extension for gzip
```bash
mv pass.txt pass.gz
```

9- unzip the file
```bash
gunzip pass.gz
```

10- check the files
```bash
ls
```

11- check the new file format
```bash
file pass
```

12- change name with the correct extension for bzip2
```bash
mv pass pass.bz2
```

13 - unzip
```bash
bzip2 -d pass.bz2
```

```bash
ls
mv pass pass.gz
gunzip pass.gz
```

```bash
ls
file pass 
mv pass pass.tar
tar xvf pass.tar data5.bin
```
data5.bin


```bash
ls
file data5.bin
mv data5.bin data5.tar
tar xvf data5.tar data6.bin
```

```bash
ls
file data6.bin
mv data6.bin data6.bz2
bzip2 -d data6.bz2
```

```bash
ls
file data6
mv data6 data6.tar
tar xvf data6.tar data7.bin
```

```bash
ls
file data7.bin
mv data7.bin data7.gz
gzip -d data7.gz
```

```bash
ls 
```

now if we check the last file with the "file" command is finally an ASCII text, open it with cat and get the deserved password: wbWdlBxEir4CaE8LaPhauuOo6pwRmrDw

​<br/>
---

### LEVEL 13 --> 14
Login with 
```bash
ssh bandit13@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

We begin as always with the ls command;
we see a file called *sshkey.private*; it contains the RSA private key to connect via ssh as bandit14.

So we can use this command
```bash
ssh -i sshkey.private bandit14@localhost -p2220
```

now we are logged as bandit14 and we can get the password 
```bash
cat /etc/bandit_pass/bandit14
```

And here we have it: fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq

​<br/>
---

### LEVEL 14 --> 15
Login with 
```bash
ssh bandit14@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.
Or we can either keep the connection as we were already in as bandit14 from the previous task.

Now for this level the password can be retrieved by submitting the password of the current level to port 30000 on localhost.

We can do it using netcat
```bash
echo PASSWORD |nc localhost 30000 
```

And the password will be displayed on the screen: jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt

​<br/>
---

### LEVEL 15 --> 16
Login with 
```bash
ssh bandit15@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

Here we have to submit the password of the current level to port 30001 on localhost using SSL encryption.

To do so we can use 2 new commands: openssl and s_client, i suggest to check them to learn more about.
The final command will be:
```bash
echo PASSWORD |openssl s_client -connect localhost:30001 -ign_eof
```

At the end of the new screen we will have the new password: JQttfApK4SeyHwDlI9SXGR50qclOAil1

​<br/>
---

### LEVEL 16 --> 17
Login with 
```bash
ssh bandit16@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

In order to find the password we have to submit the current one to a specific open port on the local host and the hit tells us that an ssl service is running on it and the port is in the range 31000-32000.

To discover the right port we will be using one of the most famous tools in CTFs, i suggest you to take some time, read the manual page and look online as you will be using it in almost every CTF as first step.
The tool i am talking about is nmap, it will help us at scanning ports and finding the one we need.

The command we run is:
```bash
nmap -sV -p 31000-32000 localhost
```

Quick explaination: with that command we are telling namp to show us the service and the version of it (-sV), the port range (-p) and filally the ip to scan that in our case is the localhost.

Wait a couple of minutes and nmap will show you this screen
PICTURE
Looking at it we can see that only 2 ports are running an ssl server and only one will send us the needed response, the 31790.

Now we have to procede like in the previous challenge with this command
```bash
echo PASSWORD | openssl s_client -connect localhost:31790 -ign_eof
```

ok now save the rsa private key as we will need it to connect to the next level.

​<br/>
---

### LEVEL 17 --> 18
This time the login to level 17 will be different from the previeus ones.
Do you remember that in level 16 we didn't receive a password at the end but an rsa key, now we will need it to accees.

Create a new file and name it rsa.key 
```bash
nano rsa.key
```

Now paste inside the private key we found, save and exit the editor.
Before moving to the ssh login we still have to set the right permissions to the key file, otherwise it will return us an error:
```bash
chmod 400 rsa.key
```
 
Ok, time to login, now we will use the same old ssh command but with the -i switch that is used to specify the private key file
```bash
ssh -i rsa.key bandit17@bandit.labs.overthewire.org -p 2220
```

Once logged we can procede with ls to see what's inside the home directory.
We can see there are 2 passwords files, old and new and the hint says the password is the only different line between the files.

To help us in this task we can use the diff command they will check for us the differences between the 2 files
```bash
diff passwords.new passwords.old
```

And the first response line will be our password: hga5tuuCLF6fFzUpnagiMN8ssu9LFrdg

​<br/>
---

### LEVEL 18 --> 19
Login with 
```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220  
```
After inserting the password we see a sceen telling us ByeBye and it will logs us out.

A problem arises, if we can't login how can we complete the next level?
Reading the level description it says that the someone has modified the .bashrc, so now we know what is the reason why we can't login normally; time to find a solution!

The ssh command offers us an option to run directly a typical command we whould use once logged, we just need the correct username an passowrd to do so.
At first let's run ls to check what is inside the home directory
```bash
ssh  bandit18@bandit.labs.overthewire.org -p 2220 ls
```

Ok we can confirm there is a file called readme as the description told us, now we can do the same process but with the cat command to retrive the password.
```bash
ssh  bandit18@bandit.labs.overthewire.org -p 2220 cat readme
```

And the password will be displayed: awhqfNnAbc1naukrpqDYcF95h7HoMTrC

​<br/>
---

### LEVEL 19 --> 20
Login with 
```bash
ssh bandit19@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

Let's run ls as usual to check what is inside the directory;
We can see there is a file called bandit20-do.

The hint suggests us that we have to use the setuid binary and that the password is stored in /etc/bandit_pass .

In general you can check the permissions of a file using the ls -l that will show you r=read w=write and x=execute permission, it will also display tho is the owner and the group of the file.

If we try it in the home directory
```bash
ls -l
```
we can see that the file bandit20-do is owned by bandit 20, is in bandit 19 group and the user's in bandit19 group can execute the binary and more specifically it will be executed as bandit20 user.

Knowing this we can exploit it at our need and open the file containing the passowrd that we could not open as bandit19 with cat.

Another final thing to keep in mind is that /etc/bandit_pass direcorty conrains a list of passwords for different level, all the files have the name of the level.

So we can now run the executable
```bash
./bandit20-do
```
*-rwsr-x--- 1 bandit20 bandit19 14876 Apr 23 18:04 bandit20-do*

It says, as we have just learnt, that it run a command as another user (bandit20 in our case), so we chose cat to open the password file
```bash
./bandit20-do cat /etc/bandit_pass/bandit20
```

And the password is: VxCazJaVykI6W36BkBU0mJTCM8rR95XT

​<br/>
---

### LEVEL 20 --> 21
Login with 
```bash
ssh bandit20@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

Since the level talks about setuid again let's run `ls -l` to either see the files and their permissions/owners and groups.

We see a file called suconnect owned by bandit21 and part of bandit20 group, we also have execute permission.
*-rwsr-x--- 1 bandit21 bandit20 15600 Apr 23 18:04 suconnect*

This executable makes a connection to localhost on the port you specify as a commandline argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).

Before proceding we have to call back a few informations we have learnt before and add some other fast theory.

In order to connect to a port on the localhost we firstly need to set up a server, to do so we use Netcat, we will also need to specify the ip, in our case the local host with the -l switch and with the -p flag the port of our choice.

We also know that we have to submit the password found in the previous level, to do so we can unite the command echo that will input the password and netcat that will crate the connection.

To pass the password from the echo to the netcat comman we can use the pipe "|" that we have already found some levels before.

One last thing to do, since we are connected with only one terminal, is to background this process with "&" so we can later run the executable that will spit out the final password.

Putting all together the 1st command will be:
```bash
echo VxCazJaVykI6W36BkBU0mJTCM8rR95XT | nc -l -p 12345 &
```

Now let's run the executable file trough the port 12345 
```bash
./suconnect 12345
```

And now we can see the final password: NvEJF7oVjkddltPSrdKEFOllh9V1IBcq

​<br/>
---

### LEVEL 21 --> 22
Login with 
```bash
ssh bandit21@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

In this level cron jobs are introduced.
To make it simple cron is a tool that automate scripts and commands to run with a regular interval; cron jobs are all defined in a file called crontab.
You can read more online on how it function and how to exploit it.

Back to the level task we are directed to a directory, lets visit it
```bash
cd /etc/cron.d/
```

Once inside we can see different cronjobs for various users, we need to investigate the level 22 one
```bash
cat cronjob_bandit22
```

Looking inside the file we can see a file with the .sh extension, time to open and see what it does
```bash
cat /usr/bin/cronjob_bandit22.sh
```

Ok we can see that the script inside opens a shell, change a file permission and than saves the level 22 password in a file in temp directory.

Now we can catch the password opening the file in /temp
```bash
cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

And the password will be displayed on the screen: WdDozAdTM2z9DiFEQ2mGlwngMfj4EZff

​<br/>
---

### LEVEL 22 --> 23
Login with 
```bash
ssh bandit22@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

In this level we have again cron jobs; lets go to the same directory as last time:
```bash
cd /etc/cron.d
```

Now we chose to see the level 23 one
```bash
cat cronjob_bandit23
```

Once inside we can see the full path of the file, open it
```bash
cat /usr/bin/cronjob_bandit23.sh
```

- [ ] The script declares a variable called myname and its value is the result of the whoami command; whoami is used to know which user we are in inux, so is gonna be bandit 23.
Than declares another variable called mytarget, to know its value we have to execute ourselves the command between the parenthesis.

So open another terminal on your linux machine and write:
```bash
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
```

This will return the value: 8ca319486bfbbc3663ea0fbe81326349
Now save that value for later.

Keep reading the script we can see that it than copies the password of bandit 23 into /tmp/$mytarget but now we know the value of $mytarget is 8ca319486bfbbc3663ea0fbe81326349 so we can read the file
```bash
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

And here we have our password: QYw0Y2aiA672PsMmh9puTQuhoz8SyR2G

​<br/>
---

### LEVEL 23 --> 24
Login with 
```bash
ssh bandit23@bandit.labs.overthewire.org -p 2220  
```
Insert the password we have found in the previous level and let's start.

More cron jobs for this level.
Navigate to the directory with the cron jobs
```bash
cd /etc/cron.d/
```

Check what is inside 
```bash
ls
```

Open the level 24 one
```bash
cat cronjob_bandit24
```

Open the .sh file
 ```bash
cat usr/bin/cronjob_bandit24.sh
```

This script executes and delete every minute all the files located in the directory called /var/spool/bandit24/foo

What we need to do now is to create our own script to catch the password of bandit24 user.
It will look something like this
```bash
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/exercise/password
```

Now we have to create our environment to plant it and successfully get the result we want.

1. create the directory
```bash
mkdir /tmp/exercise
```

2. go in the new created directory
```bash
cd /tmp/exercise
```

3. create the file that will host the final password
```bash
touch password
```

4. set permissions on that file so anyone can write or read it
```bash
chmod 666 password
```

5. create the script file
```bash
nano script.sh
```
Once the editor opens copy the script we have just written than save and exit.

6. change the script file permissions to make it executable
```bash
chmod 777 script.sh
```

7. copy the script to the directory we found before
 ```bash
cp script.sh /var/spool/bandit24/
```

Ok now everything is set, since that cron job runs every 60 seconds, just wait one minute.

Now open the file containing the password
```bash
cat /tmp/exercise/password
```

And here you have it: VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar

​<br/>
---

### LEVEL 24 --> 25
Login with `ssh bandit24@bandit.labs.overthewire.org -p 2220`  
Insert the password we have found in the previous level and let's start.

In this level, to get the password we have to provide to the daemon listening to port 30002 the current level password and a pin code.

The problem is that we don't know the pincode, BUT we have an hint, we can perform a Brute Force attack that means trying all the combinations for a 4 digit pincode, that are 10000.

To do so we need a file with all those combinations, here we have 3 choices:
1. Find a numberlist online
2. Using an online tool to generate the combinations and than copy them on a file
3.  Create a simple script that will do the work

Here i will discuss option 3 as the first 2 don't really need any explaination.

So, we can create a bash script containing a loop that will print all the combinations and associate them to the level password, than will save the output to a file.
To conclude we can also add a command to open that file and send the combinations to the deamon, with netcat, and print in a new file the results, we can also add a line that will filter all the wrong combinations out and give us the right one.
it will look like this:
```bash
#!/bin/bash 

#now the loop
for n in {0000..9999}
do
	 echo VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar $n >> combinations.txt
done

#send the file to the daemon and strip the wrong results, finally open the file with the password for level 25

cat combinations.txt | nc localhost 30002 > results.txt
cat results.txt | grep bandit25 > final.txt
cat final.txt
```

Cool right? Now let's create the encironment to procede:

1. Create a new folder in /tmp
```bash
mkdir /tmp/newfolder
```

2. Go inside the folder
```bash
cd /tmp/new
```

3. Create the script file
```bash
nano script
```
Once the editor opens paste the script from above inside, save with `ctrl + s` and exit with `ctrl + x` .

4. Make the script file executable
```bash
chmod +x script
```

5. Run the script
```bash
./script
```

Don't worry if seems nothing is happening, be batient it will take a bit (up to 5 min, sometimes more) to try all the combinations, but after a while we will have displayed the passoword: p7TaowMYrmu23Ol8hiZh9UvD0O9hpx8d

​<br/>
---

### LEVEL 25 --> 26
Login with 
```bash
ssh bandit25@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

Use the `ls` command to check inside the home directory.
There is a fille called bandit26.sshkey that contains the rsa private key to connect to the next level.

Now we can connect to bandit26 with ssh
```bash
ssh -i bandit26.sshkey bandit26@localhost -p 2220
```

After trying it we ccan see that the connection gets immediately closed and we can't access bandit26 this way.

Let's try to look inside /etc/passwd because here are stored the info regrading the shell's for each user.
```bash
cat /etc/passwd
```

We see a different path than usual : /usr/bin/showtext

Now we check what is really inside that file
```bash
cat /usr/bin/showtext
```

Reading the script we can understeand that the reason why we are getting disconnected is because more is displaying the content of the file "text.txt", but it is very short, so it can print it without entering trhe interactive more.

The way to exploit 'more' is to make the command line very small so we will access the interactive more once we ssh into bandit26.
So resize you window and make it small, than login via ssh
```bash
ssh bandit26@localhost -i bandit26.sshkey -p 2220
```

Than press `v` and now we will have the vim editor running.
Now to retrive the bandit26 password we can simply load the file from the directory we know contains the passowrds for every level.
```bash
:e /etc/bandit_pass/bandit26
```

And here we have it c7GvcKlw9mC7aUQaPx7nwFstuAIBw1o1

Now don't close the editor yet as we need to connect to the next level from here, because if we use ssh we will get disconnected as before. 

So from the beginning we can remember that the shell was not in /bin/bash, so we can now set it /bin/bash via vim.

In the vim editor write
```bash
:set shell=/bin/bash
```

Than still from vim we can launch the shell
```bash
:shell
```

And yes now we are logged as bandit26

​<br/>
---

### LEVEL 26 --> 27
If we run the ls -l command we can see a file "bandit27-do wich has the SUID bit set"
We can exploit it to retrive tha bandit27 password 
```bash
./bandit27-do cat /etc/bandit_pass/bandit27
```

And here we have the password : YnQpBuifNMas1hcUFk70ZmqkhUU2EuaS

​<br/>
---

### LEVEL 27 --> 28
Login with 
```bash
ssh bandit27@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

This time the hint tells us that there is a git repository at `ssh://bandit27-git@localhost/home/bandit27-git/repo` via the port `2220`, and the password for the user bandit27-git is the same as for the user bandit27.

Let's begin by creating a folder to work in
```bash
mkdir /tmp/lv27
```

Now we can clone the repositorty inside the new folder
```bash
cd /tmp/lv27
```
```bash
git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
```
When prompted for the password insert the one used to log into this level.

Now we have the repository cloned in our directory, navigate inside of it
```bash
cd repo
```

To discover what there is inside of it use:
```bash
ls -la
```

Hmm a README file, i guess we can read it
```bash
cat README
```

And the passoword is here : AVanL161y9rsbcJIsFHuw35rjaOM19nR

​<br/>
---

### LEVEL 28 --> 29
Login with 
```bash
ssh bandit27@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

Ok looks like they want us to practice with `git`, for this and some of the next level we will have to procede as we did by cloning the repo.

NOTE : for all the next levels i will repeat all the steps, but if you are following along and doing more levels in a row, you can simply create a new directory and clone every repo without the need to re log in every bandit-level user via ssh.

Create a new folder
```bash
mkdir /tmp/lv28
```

Clone the repo
```bash
cd /tmp/lv28
```
```bash
git clone ssh://bandit28-git@localhost:2220/home/bandit28-git/repo
```
Insert the level password when asked.

Go into the repo directory
```bash
cd repo
```

Discover files
```bash
ls -la
```

We see README.md, which is a file in markdow, open it
```bash
cat README.md
```

The password is not here, maybe the file was edited and in an older version there was the full password.
We can do so with the `show` command
```bash
git show README.md
```

And yes, we can see that the password is : tQKvmcwNYcFS6vmPHIUSI3ShmsrQZK8S

​<br/>
---

### LEVEL 29 --> 30
Login with 
```bash
ssh bandit29@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

Git stuffs again, let's repeat the process to clone the repository.

Create a new folder
```bash
mkdir /tmp/lv29
```

Clone the repo
```bash
cd /tmp/lv29
```
```bash
git clone ssh://bandit29-git@localhost:2220/home/bandit29-git/repo
```
Insert the level password when asked.

Go into the repo directory
```bash
cd repo
```

Discover files
```bash
ls -la
```

There is again a file called README.md, but if we open it we can't find any password.

Using `git show` we can see that at the password place there is a sentence that says "<no passwords in production!>", it could be that there are multiple branches.
To check it run
```bash
git branch -a
```

Yes, our guess was right, infact there are 4 branches. Knowing the sentence we can guss thath if there is a password and is not in production maybe it is under development, let's check it going in the dev branch.
```bash
git checkout dev
```

Now let's see the content
```bash
ls -la
```

View the README.md file
```bash
cat README.md
```

And here we can see the password : xbhV3HpNGlTIdnjUrdAlPzc2L6y9EOnS

​<br/>
---

### LEVEL 30 --> 31
Login with 
```bash
ssh bandit30@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

Git stuffs again, let's repeat the process to clone the repository.

Create a new folder
```bash
mkdir /tmp/lv30
```

Clone the repo
```bash
cd /tmp/lv30
```
```bash
git clone ssh://bandit30-git@localhost:2220/home/bandit30-git/repo
```
Insert the level password when asked.

Go into the repo directory
```bash
cd repo
```

Discover files
```bash
ls -la
```

There is again a file called README.md, but if we open it it tells us that the file it empty.

So i have tried doing the same steps as before, viewing `git show`, `git log`, `git branch` and nothing usefull appears; BUT another thing we can try is to check if there are tagged any specific points in a repository’s history.

We can do so with
```bash
git tag
```

Luckly enought we see one called "secret"

Let's view it
```bash
git show secret
```

And we get the password for the next level : OoffzGDlzhAlerFJ2cAiz1D41JW1Mhmt

​<br/>
---

### LEVEL 31 --> 32
Login with 
```bash
ssh bandit31@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

Git stuffs again, let's repeat the process to clone the repository.

Create a new folder
```bash
mkdir /tmp/lv31
```

Clone the repo
```bash
cd /tmp/lv31
```
```bash
git clone ssh://bandit31-git@localhost:2220/home/bandit31-git/repo
```
Insert the level password when asked.

Go into the repo directory
```bash
cd repo
```

Discover files
```bash
ls -la
```

Let's see this time what there is inside the README.md file
```bash
cat README.md
```

Ok, cool ! this  time there is written that  for this task we have to push a file to the remote repo and it gives us some details.

Create the new file
```bash
echo 'May I come in?' > key.txt
```


If we try to `git push` we will fail, thats because in the .ignore file there is `*.txt`, which means all txt files will be ignored.

To be able to do it anyway
```bash
git add -f key.txt

```
```bash
git commit -a
```bash
This command will open the nano editor, write a word in the first line, than save and exit the editor.

Now we can push it into the master branch
```bash
git push -u origin master
```
It will ask us a password, use the one we got to log into this level.

Once the process is completed we will have the password printed on the screen : rmCBvG56y58BXzv98yZGdO7ATVL5dW8y 

​<br/>
---

### LEVEL 32 --> 33
Login with 
```bash
ssh bandit32@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

Welcome in the last Bandit challenge !

Once connected we can see a sentence that says we are in an uppercase shell, meaning that all our usuall commands wont work as linux is case sensitive.

One way around is to find those linux commands that are uppercase by default, and those are the variables, one in particular is usefull for us : `$0`, this one has the info about the shell, writing it is equal to running a shell, this way we can braek from the upppercase one.
```bash
$0
```

Now we have the "normal" shell and can operate as usual.

So now we can retrive the password for level 33 
```bash
cat /etc/bandit_pass/bandit33
```

And it is : odHo63fHiFqcWWJG9rLiLDtPm45KzUKy

Now we can login to the last level and check if there are any final messages.

​<br/>
---

### LEVEL 33
Login with 
```bash
ssh bandit33@bandit.labs.overthewire.org -p 2220
```
Insert the password we have found in the previous level and let's start.

We can list the home directory content with `ls` and open the file
```bash
cat README.txt
```

<br/>
​<br/>

---


Congratulations, you have completed the Bandit challenge; I hope you had fun and have learnt something new in this journey.

See you in the next challenge 😃

