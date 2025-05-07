# Mr Phisher Walkthrough
<br/>

## Intro
Welcome to the Injectics challenge, here is the link to the [room](https://tryhackme.com/room/mrphisher) on TryHackMe.

This time we will be dealing with a quick investigation of a phishing attempt.

When ever you feel ready start the machine, it will open a VM in split view.

Let's Begin!

<br/>
<br/>

## The Challenge
Let's open the terminal and navigate to the directory containing the files for the challenge:
```bash
cd /home/ubuntu/mrphisher
```

Here we find a file called `MrPhisher.docm` and an archive: `mr-phisher.zip`.

If we double click on the file it opens in Libre Office Writer and we can see it contains a meme image saying "not sure if link or malware"
We can get the md5 hash of the file or directly upload the file to get some initial information.

It gets flagged as a malicious word document using macro to achieve its objective.

I decided to transfer the malicious file to my vm, so i could do more testing and reach the internet as well.

I installed the *oletools* suite:
```bash
pip install oletools
```
```bash
olevba MrPhisher
```

The analysis gave me the following:
```
FILE: MrPhisher.docm
Type: OpenXML
WARNING  For now, VBA stomping cannot be detected for files in memory
-------------------------------------------------------------------------------
VBA MACRO ThisDocument.cls 
in file: word/vbaProject.bin - OLE stream: 'VBA/ThisDocument'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
(empty macro)
-------------------------------------------------------------------------------
VBA MACRO NewMacros.bas 
in file: word/vbaProject.bin - OLE stream: 'VBA/NewMacros'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Sub Format()
Dim a()
Dim b As String
a = Array(102, 109, 99, 100, 127, 100, 53, 62, 105, 57, 61, 106, 62, 62, 55, 110, 113, 114, 118, 39, 36, 118, 47, 35, 32, 125, 34, 46, 46, 124, 43, 124, 25, 71, 26, 71, 21, 88)
For i = 0 To UBound(a)
b = b & Chr(a(i) Xor i)
Next
End Sub
+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|Suspicious|Chr                 |May attempt to obfuscate specific strings    |
|          |                    |(use option --deobf to deobfuscate)          |
|Suspicious|Xor                 |May attempt to obfuscate specific strings    |
|          |                    |(use option --deobf to deobfuscate)          |
+----------+--------------------+---------------------------------------------+
```

We can see that there is a malicious obfuscated macro.
we can create a python script to decode it:
```python
# Define the array from the VBA code
initial_array = [102, 109, 99, 100, 127, 100, 53, 62, 105, 57, 61, 106, 62, 62, 55, 110, 113, 114, 118, 39, 36, 118, 47, 35, 32, 125, 34, 46, 46, 124, 43, 124, 25, 71, 26, 71, 21, 88]

# Initialize an empty string to store the result
decoded_data = ""

# Loop over the array and apply the XOR operation as described
for i in range(len(initial_array)):
    decoded_data += chr(initial_array[i] ^ i)  # XOR operation with the index

# Output the result
print(decoded_data)
```

Run the script:
```bash
python3 script.py
```

And the output is the flag, we have already finished this machine.

<br/>
<br/>

Congratulations you have successfully undcovered the malicious file an got the flag!

I hope you had a good completing the challenge and following along.

Catch you in the next CTF 😃
