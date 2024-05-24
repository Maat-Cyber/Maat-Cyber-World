# ItsyBitsy 
Welcome to another CTF walkthrough, here is the link to the TryHackMe room https://tryhackme.com/room/itsybitsy <br/>
In order to solve this challenge you will need to use the Elk's tools, so it is highly suggested to complete the introduction theory room before this challenges.

Whenever you fell ready you can begin pressing START MACHINE.

To be able to interact with the machine, as THM explains you can either use their attack box or use your own Kali Linux machine by connecting it via OpenVPN.
​
Now that everything has been set let's start with the CTF.

The walkthrough won't contain the answers, in order to not take away the fun, but a step by step tutorial to reach them, by following it you will just have to read the flag or the answers on your own machine.

<br/>
<br/>

## Access to the challenge
Once the room and your Linux machine are ready navigate to the assigned machine IP address and login using the provided credentials:
Username: Admin
Password: elastic123

I don’t know exactly why but in my case there was not a login page and simply navigating to the machine IP opened the elastic interface.
We can now open the menu on the top left and select Discover, here is where we will conduct ours investigations.

<br/>
<br/>

## The Investigation scenario
“During normal SOC monitoring, Analyst John observed an alert on an IDS solution indicating a potential C2 communication from a user Browne from the HR department. A suspicious file was accessed containing a malicious pattern THM:{ ________ }. A week-long HTTP connection logs have been pulled to investigate. Due to limited resources, only the connection logs could be pulled out and are ingested into the connection_logs index in Kibana.”

<br/>
<br/>

## Guide to the Answers
Our task is to investigate the logs and answer all the questions.
 

1. **How many events were returned for the month of March 2022?**
On the top right of the page we can see a form, choose “absolute” and than set the beginning date to the 1 of March and the ending one on 31 March 2022. Then press the blue button “UPDATE”, leave it a couple of seconds and we can read the number of events for this month.

<br/>

2. **What is the IP associated with the suspected user in the logs?** <br/>
On the left side of the page we can click on the filter “source IP” and notice that 99% of the traffic is coming from an IP, but there is a small percentage coming from another one, this looks suspicious.

<br/>

3. **The user’s machine used a legit windows binary to download a file from the C2 server. What is the name of the binary?** <br/>
It’s time to start investigating, where we found the suspected IP address, there was a tiny plus sign, click it to display the traffic.
On march 10 there is a log showing a connection to the IP that we are investigating, the user-agent field tells us which binary has been used.

<br/>

4. **The infected machine connected with a famous file-sharing site in this period, which also acts as a C2 server used by the malware authors to communicate. What is the name of the file-sharing site?** <br/>
Still inside the log we used for question 3, there is another filed of interest, the “host” which tells us the name of the website that acts as a C2 server.

<br/>

5. **What is the full URL of the C2 to which the infected host is connected?** <br/>
For this question we have to look for the “URI” which in this case is /yTg0Ah6a.
To create the full URL simply put the domain/URI, the domain is the one we have just found in question 4.

<br/>

6. **A file was accessed on the file-sharing site. What is the name of the file accessed?** <br/>
To find this answer i navigated to the full URL that has been accessed and luckily enough in this page there is the file name with it’s content.

<br/>

7. **The file contains a secret code with the format THM{_____}.** <br/>
In the file-sharing website, in the field under the file name there is the secret code!
 
<br/>
<br/>

Congratulations, you have reached the end of this Elk challenge, hope you had fun doing the investigation.

If you want to see more CTFs Writeups explore the directory.

See you in the next challenge. 😊
