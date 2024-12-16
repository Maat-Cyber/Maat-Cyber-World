# Unattended Walkthrough
<br/>

## Intro
Welcome in another TryHackMe challenge, here is the [link to the room](https://tryhackme.com/r/room/unattended)


**The scenario:** <br>
"*Our client has a newly hired employee who saw a suspicious-looking janitor exiting his office as he was about to return from lunch.*  
*I want you to investigate if there was user activity while the user was away **between** **12:05 PM to 12:45 PM on the 19th of November 2022**. If there are, figure out what files were accessed and exfiltrated externally.*"

We are also reminded that we have signed an NDA and we have not avoid looking into classified files.

Initial investigations reveal that someone accessed the user's computer during the previously specified time-frame.

Whenever you feel ready press "start the machine" and access the system via split-view in your browser.

Let's begin!

<br/>
<br/>

## The Challenge
Once the system is fully load we can open the PDF file on the desktop, containing a welcome letter from the TryHatMe company.

The image of the machine we have to investigate is located in the `kape-results\C` directory on the user's desktop, while all the tools we need are in the `tools` folder.

The first thing we have to find out is the file type that was searched using the search bar in Windows Explorer.

We can achieve it by opening with *RegistryExplorer* the NTUSER.dat file located at `C:\Users\THM-RFedora\Desktop\kape-results\C\Users\THM-RFedora`, you' ll need to load it twice creating a "clean" version by pressing `SHIFT` while selecting the file, this will export a clean copy where you prefer and then load that one.

Once the registry is loaded navigate from root to: 
```
Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery
```

Here you will find 3 entries, you can click on each of them and view below in the "Type Viewer" the text data, this way we can notice that the file being searched was a .REDACTED and the keyword was REDACTED.

Next we are suggested to use autopsy to find out more information about a downloaded file.
Let's start the tool from the taskbar and set it up, decide a name for your case, select the data source (the one in the `C:\Users\THM-RFedora\Desktop\kape-results\C` as files) and ingest **only** the "Recent Activity" to speed tings up.

Give it a minute or two to load all the data, then we can see a directory from the data artifact tree called " Web Downloads", looking the files we can spot one of interest called REDACTED downloaded in the date: REDACTED.

Thanks to this file the user was able to open a PNG file called continental.PNG which was extracted from the archive file continental.7z thanks to the downloaded tool.
The PNG file was accessed at the date/time REDACTED, we can see this in the *Web History*, one entry in fact contains this file call:
```
file:///C:/Program%20Files%20(x86)/Windows%20Media%20Player/Skins/tophatsecret/continental.png
```

Moving on we know that they have hit some kind of *Jackpot* and they were trying to exfiltrate data, but since that was not possible via USB the found another way.

We also know that a text file was created in the Desktop folder.

{ cant make it work for the part of finding date
Now let's heck out the machine's Jump Lists using *JLECmd*, run the Windows Command Prompt as an Administrator:
```
JLECmd.exe -d C:\Users\THM-RFedora\Desktop | findstr .txt
```
}

Let's go again in the "Web History" section, scrolling down a bit we can find a file called "launchcode.txt" located in the user's Desktop, we can also locate the timestamp for the last modification, which is REDACTED

We could find the date also using the registry explorer to look at:
```
Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs\.txt
```
We can see that it was opened 2 times.

The contents of the file were exfiltrated to pastebin.com, we can find the URLs containing that domain and view the URL that has been used: `https://pastebin.com/1FQASAav`, looking in the text section in the tabs below we can also find the string copied as the title `ne7AIRhi3PdESy9RnOrN`.

<br/>

We have now completed all the tasks and found out that *the malicious threat actor was able to successfully find and exfiltrate data. While we could not determine who this person is, it is clear that they knew what they wanted and how to get it.*

<br/>
<br/>

Congratulations you have successfully completed the investigation and uncovered the tracks of the malicious actor.

Catch you in the next CTF 😃 
