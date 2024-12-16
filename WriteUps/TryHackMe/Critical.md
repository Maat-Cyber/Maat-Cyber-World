# Critical Walkthrough
<br/>

## Intro
Welcome in another TryHackMe challenge, here is the [link to the room](https://tryhackme.com/r/room/critical).
Today we are gonna practice with some memory investigation of a windows machine using the famous tool called Volatility-

The scenario: <br>
"*Our user "Hattori" has reported strange behavior on his computer and realized that some PDF files have been encrypted, including a critical document to the company named `important_document.pdf`. He decided to report it; since it was suspected that some credentials might have been stolen, the `DFIR` team has been involved and has captured some evidence. Join the team to investigate and learn how to get information from a memory dump in a practical scenario.*"

Whenever you feel ready start the machine and wait a couple of minute for it to load in split  view inside your browser.

Let's begin!

<br/>
<br/>

## The Challenge
A memory dump named `memdump.mem` will be present at the home address at `/home/analyst`.
We will use *volatility* to analyze the memory dump. This tool use the following syntax:
```bash
vol OPTION MEMORY_DUMP_FILE PLUGIN_NAME
```

Here is a table with some useful volatility plugins that we will be using:

| Name                 | Description                                                                         |
| -------------------- | ----------------------------------------------------------------------------------- |
| Windows.cmdline      | Lists process command line arguments                                                |
| windows.drivermodule | Determines if any loaded drivers were hidden by a rootkit                           |
| Windows.filescan     | Scans for file objects present in a particular Windows memory image                 |
| Windows.getsids      | Print the SIDs owning each process                                                  |
| Windows.handles      | Lists process open handles                                                          |
| Windows.info         | Show OS & kernel details of the memory sample being analyzed                        |
| Windows.netscan      | Scans for network objects present in a particular Windows memory image              |
| Widnows.netstat      | Traverses network tracking structures present in a particular Windows memory image. |
| Windows.mftscan      | Scans for Alternate Data Stream                                                     |
| Windows.pslist       | Lists the processes present in a particular Windows memory image                    |
| Windows.pstree       | List processes in a tree based on their parent process ID                           |

Now we can start our investigation discovering some info about the system with this command:
```bash
vol -f memdump.mem windows.info
```

With the output of this command we can then proceed to further analysis, like checking the network activity of the system with the following command:
```bash
vol -f memdump.mem windows.netstat
```

We can observe a connection established on port `3389` from the IP `192.168.182.139` with timestamp `2024-02-24 22:47:52.00`; this could indicate an attacker's initial access.

We can then find out which processes were running at that time to find out what triggered that connection:
```bash
vol -f memdump.mem windows.pstree
```

Knowing the "normal" Windows processes we can quickly spot a dubious one called `critical_updat` with `updater.exe` as its parent process.

There is another plugin we can use to analyze the network:
```bash
vol -f memdump.mem windows.netscan
```

We can see that an IP address established a connection on port 80 -> ==192.168.182.128== and the program used, which was ==msedge.exe==.

Now that we have a little general overview of the system state we can focus on investigating the suspicious program `critical_updat`.

We can use the plugin *windows.filescan* to examine files accessed and saved in memory and redirect the output to a file with the command:
```bash
vol -f memdump.mem windows.filescan > filescan_out
```

Now we can retrieve the info related to the process:
```bash
cat filescan_out | grep updater
```

```
0xe50ed736e8a0\Users\user01\Documents\updater.exe216
0xe50ed846fc60\Program Files (x86)\Microsoft\EdgeUpdate\1.3.185.17\msedgeupdateres_en.dll2
16
0xe50ed8482d10\Program Files (x86)\Microsoft\EdgeUpdate\1.3.185.17\msedgeupdateres_en.dll2
16
```


Now that we know the executable file path we can target it to get more info with this command:
```bash
vol -f memdump.mem windows.mftscan.MFTScan > mftscan_out
```

Then run this to read the info from the file:
```bash
cat mftscan_out | grep updater
```

And here is the output:
```
* 0xd389c63ce528FILE1114172FileArchiveFILE_NAME2024-02-24 22:
51:50.000000 2024-02-24 22:51:50.000000 2024-02-24 22:51:50.000000 2024-02-24 22:
51:50.000000 updater[1].exe
```

Now we can dump the memory region that correspond to that executable file:
```bash
vol -f memdump.mem -o . windows.memmap --dump --pid 1612
```

This will generate ad `.dmp` file, we can read through it to find all we need:
```bash
strings pid.1612.dmp |less
```

Inside we can spot an URL which contains also a key file: `http://key.critical-update.com/encKEY.txt`, scrolling down we an also see that the executable interacted with another file called `important_document.pdf`.

Is time to look at the HTTP request, you can either have already done it just by viewing the file manually or get the targeted part like this:
```bash
strings pid.1612.dmp | grep -B 10 -A 10 "http://key.critical-update.com/encKEY.txt"
```

And we have a probable key "REDACTED" used to encrypt the PDF file.

Now we can apply the same process using `cat` and `grep` to find the answers of the task's questions:

```bash
cat filescan_out | grep critical_updat
```
--> REDACTED

```bash
cat mftscan_out | grep important_document.pdf
```
--> REDACTED

```bash
strings pid.1612.dmp | grep -B 10 -A 10 "http://key.critical-update.com/encKEY.txt" | grep Server
```
--> REDACTED

<br/>
<br/>

Congratulations you have successfully completed the investigation and uncovered the tracks of the malicious actor.

Catch you in the next CTF 😃 
