# CyberHeroes Walkthrough

## Intro
Welcome to the CyberHeroes challenge, here is the link to the [room](https://tryhackme.com/room/cyberheroes) on TryHackMe.
In this challenge we will have to bypass an authentication form and capture the flag.

"*Want to be a part of the elite club of CyberHeroes? Prove your merit by finding a way to log in!*"

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
We can start with a port scan:
```bash
rustscan -a 10.80.153.90 -r 0-65535  --ulimit 5000 -- -sV -sC
```

It finds port 22 for SSH and and HTTP server on port 80, let's check it out `http://10.80.153.90`.
We can spot a login page at `http://10.80.153.90/login.html`.

Looking at the page source code we find some interesting JavaScript:
```js
  function authenticate() {
      a = document.getElementById('uname')
      b = document.getElementById('pass')
      const RevereString = str => [...str].reverse().join('');
      if (a.value=="h3ck3rBoi" & b.value==RevereString("54321@terceSrepuS")) { 
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            document.getElementById("flag").innerHTML = this.responseText ;
            document.getElementById("todel").innerHTML = "";
            document.getElementById("rm").remove() ;
          }
        };
        xhttp.open("GET", "RandomLo0o0o0o0o0o0o0o0o0o0gpath12345_Flag_"+a.value+"_"+b.value+".txt", true);
        xhttp.send();
      }
      else {
        alert("Incorrect Password, try again.. you got this hacker !")
      }
    }
```
- it check if the username matches the string `h3ck3rBoi` and the password is the reverse of `54321@terceSrepuS` which is `SuperSecret@12345`,

Well this is another level of easy challenge, lol, we basically have already the credentials there, simply insert them and get the flag.

--> REDACTED_FOR_THE_WRITEUP

<br/>
<br/>

Congratulations you have successfully found credentials that the dev left behind and logged into the app to get the flag.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
