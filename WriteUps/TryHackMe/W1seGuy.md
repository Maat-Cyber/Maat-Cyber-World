# W1seGuy Walkthrough
<br/>

## Intro
Welcome into the W1SeGuy challenge from TryHackMe, here is the link to the [room](https://tryhackme.com/r/room/w1seguy).
This time we are gonna get our hands dirty with encryption, we will have to download a python script, understand what it does to successfully find our way to the flags.

Whenever you feel ready download the attachment and press on "start machine".

Let's begin!

<br/>
<br/>

## The Challenge
Before starting here is a tip: do not worry if you do not understand how this all works at the first try, take some time and research online about encryption, it is a great opportunity to learn more about the topic!
<br>

Once you have downloaded the .py file, open and read trough it.

The Python script is:
```python
import random
import socketserver 
import socket, os
import string

flag = open('flag.txt','r').read().strip()

def send_message(server, message):
    enc = message.encode()
    server.send(enc)

def setup(server, key):
    flag = 'THM{thisisafakeflag}' 
    xored = ""

    for i in range(0,len(flag)):
        xored += chr(ord(flag[i]) ^ ord(key[i%len(key)]))

    hex_encoded = xored.encode().hex()
    return hex_encoded

def start(server):
    res = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    key = str(res)
    hex_encoded = setup(server, key)
    send_message(server, "This XOR encoded text has flag 1: " + hex_encoded + "\n")
    
    send_message(server,"What is the encryption key? ")
    key_answer = server.recv(4096).decode().strip()

    try:
        if key_answer == key:
            send_message(server, "Congrats! That is the correct key! Here is flag 2: " + flag + "\n")
            server.close()
        else:
            send_message(server, 'Close but no cigar' + "\n")
            server.close()
    except:
        send_message(server, "Something went wrong. Please try again. :)\n")
        server.close()

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        start(self.request)

if __name__ == '__main__':
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 1337), RequestHandler)
    server.serve_forever()
```

Reading the code we can understand that when we connect to the specified port we get a string that is the encoded flag.
The encoding happens via a method called XOR, using a 5 character key that gets randomly generated every time we try to connect, finally after that the result is also encoded again in hex.
If we submit the right key value we will get the flag 2, otherwise the connection will drop and we will have to try again. To get the flag 1 we have to revert the XOR encryption and hex encoding with the key.

Let's see what we get:

We can connect to the machine open's port using *netcat*
```bash
nc MACHINE_IP  1337  
```

By doing that we receive and hex - XOR encoded text and we have now to provide the encryption key.

In my situation the string was:
```
161e750d447337541840072e4c374036625b1d5703384a45552e1a411e613022414641302e770449
```

Now to find out what was the key we have to keep in mind that, the string above has to be hes-decoded first, then we can use the XOR but we need the key and the flag which is usually something like `THM{....}`.

All this sounds fine but we need some formulas to actually do the math operations, looking online i found this as the general operation rules for XOR:
$$A⊕0 = A$$ <br/>
$$A⊕A = 0$$ <br/>
$$A⊕B =B⊕A$$ <br/>
$$(A⊕B)⊕C = A⊕(B⊕C)$$ <br/>
$$(B⊕A)⊕A = B⊕0 = B$$ <br/>

So we know that the XOR encryption is *symmetrical*: $$reverse XOR = XOR$$ <br/>
A bit of more theory, the XOR has a *Truth Table* which basically re-write the formulas we have seen above but with zeroes and ones:

| A   | B   | A xor B |
| --- | --- | ------- |
| 0   | 0   | 0       |
| 0   | 1   | 1       |
| 1   | 0   | 1       |
| 1   | 1   | 0       |

Knowing all this info and part of the plain-text flag + the final encoded string we can start the process to find the key.

Resuming what we know:
- the encoded string which is 40 chars 
- the first 4 chars of the flag (`THM{`)
- how XOR is symmetrical

So with first char of the encoded-string and the first one of the flag we can find the first char of the key like this:
$$0x16⊕T = B$$
(since the string is hex encoded `16` is the first couple, and `T` is the first letter of the flag).
This means that `B` is the first letter of the 5 chars key, we can now find the other ones. 

But calculating manually is a bit time consuming, so we can create a script in python to automate it:
```python
#!/bin/python3

from pwn import xor

encoded_flag = bytes.fromhex('161e750d447337541840072e4c374036625b1d5703384a45552e1a411e613022414641302e770449')
firs_part = xor(encoded_flag[:4], b"THM{")

last_digit = xor(encoded_flag[-1], b"}")

full_key = first_part + last_digit
key = full_key.decode('utf-8').strip("'b") 

print("The key is:", key)
```

The result in my case was: BV8v4
(You can reuse my simple script if you like, but you have to change the hex encoded string, as you will probably have another value)

Now we have all the elements to reconstruct the flag:
$$DecodedHexString = key⊕Flag$$

In my situation i created a python script to do it:
```python
#!/bin/python3

import itertools
from pwn import xor


hex_string = '161e750d447337541840072e4c374036625b1d5703384a45552e1a411e613022414641302e770449'
key = b'BV8v4' 

xored_result = bytes.fromhex(hex_string)

key_repeated = itertools.cycle(key)
plain_text_bytes = bytes([x ^ y for x, y in zip(xored_result, key_repeated)])
plain_text = plain_text_bytes.decode('utf-8')

print("The flag is:", plain_text)

```

Flag1 --> REDACTED

Finally we can get the second flag by submitting the key in our terminal, where we left the connection with *netcat* open.

Flag 2 --> REDACTED
<br/>

Now let's go a step forward, after completing the room we have some more insight and we can actually create a single script that will find the solution for us:

(please do not use the script to just get the flags without trying to solve it yourself :))

```python
import itertools
from pwn import xor

# First part to find the key
encoded_flag = bytes.fromhex('161e750d447337541840072e4c374036625b1d5703384a45552e1a411e613022414641302e770449')
firs_part = xor(encoded_flag[:4], b"THM{")

last_digit = xor(encoded_flag[-1], b"}")

full_key = first_part + last_digit
key = full_key.decode('utf-8').strip("'b") 

print("The key is:", key)


# Second part to find the first flag 
xored_result = bytes.fromhex(encoded_flag)

key_repeated = itertools.cycle(key)
plain_text_bytes = bytes([x ^ y for x, y in zip(xored_result, key_repeated)])
plain_text = plain_text_bytes.decode('utf-8')

print("The flag is:", plain_text)


# Third part (homework (lol))

```

There is one more thing we can do to fully automate the process, we can even retrieve the first encoded string and the submit the key to get the flag 2 all by automation.
We can use the python requests library to..... if you wanna practice with your python skills, give it a try!

<br/>
<br/>

Congratulations you have successfully reverted the encryption and managed to restore the flag!
I personally had fun trying to solve the challenge and learning better how the XOR encryption works, as well as practicing creating some little Python scripts; hope you enjoyed as well.

Catch you in the next CTF 😃 
