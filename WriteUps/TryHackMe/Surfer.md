# Surfer Walkthrough
<br/>

## Intro
Welcome into the surfer room, here is the link of the [challenge](https://tryhackme.com/r/room/surfer) on TryHackMe.
In this CTF we are gonna explore one of the many possible roads to exploit a vulnerable web-application.

"*Woah, check out this radical app! Isn't it narly dude? We've been surfing through some webpages and we want to get you on board too! They said this application has some functionality that is only available for internal usage -- but if you catch the right wave, you can probably find the sweet stuff!*"

Whenever you feel ready press "start machine" and connect via OpenVPN or use the AttackBox

<br/>
<br/>

## The Challenge
Let's add the IP to the hosts file for commodity:
```bash
echo "MACHINE-IP surfer.thm" | sudo tee -a /etc/hosts
```
(sobsitute with the actual machine IP address)

We already know that we are gonna deal with a web-app vulnerability so we can guess that it is accessible on the default port 80, but to be sure we can do a quick *nmap* scan:
```bash
nmap -sV surfer.thm
```

Yes we got the confirmation we needed, we can do some directory scan to locate any interesting accessible webpages:
```bash
dirseach -u http://surfer.thm
```

We have many pages but let's begin with "robots.txt" which contains a list of webpages that should not be indexed:
```
http://surfer.thm/robots.txt
```

We find one interesting file:
```
Disallow: /backup/chat.txt

```

Let's view the content by navigating to:
```
http://surfer.thm/backup/chat.txt
```

```
Admin: I have finished setting up the new export2pdf tool.
Kate: Thanks, we will require daily system reports in pdf format.
Admin: Yes, I am updated about that.
Kate: Have you finished adding the internal server.
Admin: Yes, it should be serving flag from now.
Kate: Also Don't forget to change the creds, plz stop using your username as password.
Kate: Hello.. ?
```

Looks like the admin is using some default credentials and have not changed the password yet, whith this information we can go to the login page and access the dashboard: `http://surfer.thm/login.php`.
Logi in with the credentials `admin:admin`

inside the dashboard, on the right side, we see a message:
*Internal pages hosted at `/internal/admin.php`. It contains the system flag.*

But if we try to go to that location we get access-nagated.

Another thing to look at is that at the bottom of the page there is a button which will print a pdf file containing some information.
Since there are not other elements we can interact with in the page, let's inspect that element or view the page source:

Inspect the "Export PDF" button, this line of code looks interesting
```html
<input type="hidden" id="url" name="url" value="http://127.0.0.1/server-info.php">

```

The `value` field contains a call to a and internal (127.0.0.1 which is localhost) php file.
Maybe we can change that value and get printed the flag rather than the server info:

In fact if we change it to:
```html
<input type="hidden" id="url" name="url" value="http://127.0.0.1/internal/.php">
```

And then click to the button it will print us the PDF file with inside the flag!
This was a quick and easy example of Server Side Request Forgery, in which we are manipulating request to apper like an internal server is contacting another internal resource, this way we can bypass the filter that did not allow us to view the page because we are not part of the internal network.

<br/>
<br/>

Congratulations, you have succesfully found the flag and practiced with the exploitation of SSRF in a web-application, hope you had fun doing it and following along.

Catch you in the next CTF 😃 
