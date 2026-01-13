# Order Walkthrough

## Intro
Welcome to the Order challenge, here is the link to the [room](https://tryhackme.com/room/hfb1order) on TryHackMe.
In this room we will have to apply our knowledge about cryptography to decrypt some cypher text and uncover the flag.

"*We intercepted one of Cipher's messages containing their next target. They encrypted their message using a repeating-key XOR cipher. However, they made a critical error—every message always starts with the header*"  `ORDER:`

Let's begin!

<br/>
<br/>

## The Challenge
This is the intercepted message:
```
1c1c01041963730f31352a3a386e24356b3d32392b6f6b0d323c22243f6373

1a0d0c302d3b2b1a292a3a38282c2f222d2a112d282c31202d2d2e24352e60
```

Using Python we can build a script to extract the XOR key, since we already know the header.
Once we have the key we will decrypt the message.

Note: we need to first clean and convert the hex strings given to us to bytes, then we will perform the decryption.

```python 
#!/usr/bin/python3
# Script to convert XOR ecnrypted data to playntaxt knoing the header.

conversation = """
	1c1c01041963730f31352a3a386e24356b3d32392b6f6b0d323c22243f6373
	1a0d0c302d3b2b1a292a3a38282c2f222d2a112d282c31202d2d2e24352e60
"""

header = "ORDER:"

# Convert to bytes
header_bytes = header.encode()

ciphertext = bytes.fromhex(conversation)

# Function to extract the key by XORing the header with the ciphertext
def extract_key_from_header(ciphertext, header_bytes):
    key = bytes([c ^ p for c, p in zip(ciphertext[:len(header_bytes)], header_bytes)])

    # Clean-up the output (only printable chars)
    final_key = ''.join(chr(k) if 32 <= k <= 126 else '.' for k in key)  

    print(f"Extracted XOR Key: {final_key}")  

    # Return the key as a string
    return final_key

# Decrypt the ciphertext using the repeating-key XOR
def decryptor(ciphertext, key):
    decrypted = bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(ciphertext)])

    # Convert the decrypted byte values to a string 
    return decrypted.decode(errors='replace')

key = extract_key_from_header(ciphertext, header_bytes)

decrypted_message = decryptor(ciphertext, key)

print("\nDecrypted Message:", decrypted_message)
```

<br/>
<br/>

Congratulations you have successfully put into practice your Python scripting and crypto skills to revert the decrypt the conversation and find the flag.

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
