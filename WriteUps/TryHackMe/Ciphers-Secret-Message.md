# Cipher's Secret Message Walkthrough

## Intro
Welcome to the Cipher's Secret Message challenge, here is the link to the [room](https://tryhackme.com/room/hfb1cipherssecretmessage) on TryHackMe.
In this room we will have to apply our knowledge about cryptography to decrypt some cypher text and uncover the flag.

### Story
One of the Ciphers' secret messages was recovered from an old system alongside the encryption algorithm, but we are unable to decode it.

**Order:** Can you help void to decode the message?
**Message** : `a_up4qr_kaiaf0_bujktaz_qm_su4ux_cpbq_ETZ_rhrudm`

**Encryption algorithm** :
```python
from secret import FLAG

def enc(plaintext):
    return "".join(
        chr((ord(c) - (base := ord('A') if c.isupper() else ord('a')) + i) % 26 + base) 
        if c.isalpha() else c
        for i, c in enumerate(plaintext)
    )

with open("message.txt", "w") as f:
    f.write(enc(FLAG))
```

Let's begin!

<br/>
<br/>

## The Challenge
Since we are provided with the algorithm used for the encryption we need to build our own one to reverse that process.
Let's understand what exactly it does:
- iterate for each char of the plaintext and does some checks and actions:_
	- if the char is an uppercase letter it will replace it using the *Caesar Cipher* shift; and the  base is set to `ord('A')` (which is 65 ASCII value).
	- if the char is a lowercase letter; and the  base is set to `ord('a')` (which is 97 ASCII value).
	- if the char is not a letter it remains unchanged

So what we have to do is the opposite:
- check if each character is a letter, if yes we assign the ASCII value depending if is uppercase of lowercase (as explained previously), finally we calculate an index value depending on the character we are looking at and we subtract that to the base ASCII value, then we check which letter corresponds to that and save it in a list and move to the next one.
- otherwise we leave it unchanged
- we can save every char in a list and finally join all them in a string

```python
#!/usr/bin/python3
# Script to convert an encrypted text with the Caesar Cipher Shift 

ciphertext = "a_up4qr_kaiaf0_bujktaz_qm_su4ux_cpbq_ETZ_rhrudm"

# Function to decrypt the ciphertext
def decryptor(ciphertext):
    decrypted_text = []

    # Iterate through each character in the ciphertext
    for i, c in enumerate(ciphertext):
        # chek if the character is a letter
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            # Decrypt by shifting the character backwards by 'i'
            decrypted_char = chr((ord(c) - base - i) % 26 + base)
            decrypted_text.append(decrypted_char)
        else:
            # If the character is not an alphabet letter, keep it unchanged
            decrypted_text.append(c)

    # Join the decrypted characters into a single string
    return ''.join(decrypted_text)

decrypted_text = decryptor(ciphertext)

print(f"The original text is: {decrypted_text}")
```

--> REDACTED_FOR_THE_WRITEUP

<br/>
<br/>

Congratulations you have successfully reverted Caesar encryption and restored the original flag.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
