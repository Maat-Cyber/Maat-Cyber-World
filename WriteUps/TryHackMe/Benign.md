# Benign CTF Walkthrough

Welcome in another challenge, in this CTF we have to investigate an infected host. <br/>
The original link to the room on TryHackMe is: https://tryhackme.com/r/room/benign <br/>

Before starting the challenge it is suggested to have some knowledge about Splunk and logs investigation, as it will be the key to solve it. <br/>
In order to complete the challenge we have to analyze and find clues to submit 10 answers to the related questions. <br/>

As always in the THM challenges i will not post the answers but a step by step guide to get them. Find out more in the README.md file.

Here are the provided information about our investigation:

<br/>

## The Situation
One of the client’s IDS indicated a potentially suspicious process execution indicating one of the hosts from the HR department was compromised. Some tools related to network information gathering / scheduled tasks were executed which confirmed the suspicion. Due to limited resources, we could only pull the process execution logs with Event ID: 4688 and ingested them into Splunk with the index **win_eventlogs** for further investigation.  

### About the Network Information
The network is divided into three logical segments. It will help in the investigation.  

**IT Department**
- James
- Moin
- Katrina

**HR department**
- Haroon
- Chris
- Diana

**Marketing department**
- Bell
- Amelia
- Deepak

Now that we have all the information, whenever you feel ready start the machine, give it about 5 minutes, than connect to the machine IP via the provided attack-box or your Linux machine connected via OpenVPN. <br/>
Let's begin <br/>

<br/>

## The Investigation
The instructions tell us that the logs are ingested in the index `win_eventlogs`.

Once inside Splunk, click on the left side **Search and Reporting**, here is the ground for our investigations.

Firstly click on the data on the top right and select "All Time", this way we will see all the collected logs.
We know that the logs we want to check are saved in the index main, to tell Splunk to show them we have to write in the search bar `index="win_eventlogs"`

Now is time to hunt for anomalies in the logs and find out what exactly has happened.

**1. How many logs are ingested from the month of March, 2022?** <br/>
	To answer this question go on the right side, near the search bar and change the date time range from the 1st to the 31st march 2022. than apply it and the number of logs will appear. 

<br/>

**2. Imposter Alert: There seems to be an imposter account observed in the logs, what is the name of that user?** <br/>
	An username looks suspicious, if we go on the left side, find the field called "UserName", click on it and select "Rare Values", here we see the full list of 11 usernames, but one seems a copycat, it is the same as the original one but it has a "1" at the place of an "i".

<br/>

**3. Which user from the HR department was observed to be running scheduled tasks?** <br/>
	Now clear the last question filter; we know the names of the HR department users. We also know that the program `schtasks.exe` is used to manage tasks in windows. Combining all together we can create this query
```
	index="win_eventlogs" schtasks.exe  UserName IN ("Haroon*", "Chris*", "Diana*")
```

<br/>

**4. Which user from the HR department executed a system process (LOLBIN) to download a payload from a file-sharing host.** <br/>
	Here the hint tells us to search online  lolbas-project.github.io/ and understand which binary is used to download payloads. So let's open the website, write in the search bar `/Download`, now we have a list of all the binaries that can be used to download.
	Back in Splunk we can search on the left the Command Line field, than click on RARE, and we can see the first one uses a binary called `certutil.exe`, looking in the other website it is in the list, now let's view the event to find out the user.
```
index="win_eventlogs" certutil.exe   UserName IN ("Haroon", "Chris*", "Diana*")
```

<br/>

**5. To bypass the security controls, which system process (lolbin) was used to download a payload from the internet?** <br/>
	We already know this answer from the previous question investigation. It is also the exe file we shave searched in the list.

<br/>

**6. What was the date that this binary was executed by the infected host? format (YYYY-MM-DD),** <br/>
	Investigate the event of question 4, and we can find the answer. Just check the EventTime filed.

<br/>

**7. Which third-party site was accessed to download the malicious payload?** <br/>
	Investigate the event of question 4, and we can find the answer. It is the domain in the only URL.

<br/>

**8. What is the name of the file that was saved on the host machine from the C2 server during the post-exploitation phase?** <br/>
	Investigate the event of question 4, and we can find the answer. You can notice the file name in the URL, also it has something to do with the title of the challenge.

<br/>
	
**9. The suspicious file downloaded from the C2 server contained malicious content with the pattern THM{..........}; what is that pattern?** <br/>
	Controlc.com is a platform that let people drop some code so others can copy it, let's navigate to the URL found in the Splunk log and read the flag.txt file content that has been left for us.

<br/>
	
**10. What is the URL that the infected host connected to?** <br/>
	Investigate the event of question 4, is the only value that starts with https, it is also the one we have just used to find the THM flag

<br/>

Congratulations you have completed the investigation, hope you had fun as well. <br/>
See you in the next CTF WriteUp 🤗 <br/>

