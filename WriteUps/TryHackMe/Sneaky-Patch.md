# Sneaky Patch
<br/>

## Intro
Welcome to the "Sneaky Patch" challenge, here is the link to the [room](https://tryhackme.com/room/hfb1sneakypatch) on TryHackMe.

In this room we will have to investigate a live compromised system which contains a kernel backdoor and find the hidden flag.

Whenever you feel ready press on "Start Machine" and the VM will appear in your browser in "split-view"

Let's begin!

<br/>
<br/>

## The Challenge
We can check loaded kernel modules both via:
```bash
sudo lsmod
```
and :
```bash
sudo cat /proc/modules
```

One grubs our attention: `spatch`, let's get some more info:
```bash
sudo modinfo spatch
```

> [!Note]
> Finding the odd kernel module may not comes always natural or easy like this. For the challenge the author decided to set the module name as "s(patch)" which is part of the title of the challege, hence easy to spot.
> 
> A good way to recognize it otherwise is by listing the modules and invesigating their names, are they common? does anything stand out?
>
> Obviously in a real scenario the attacker could hijack a "trusted" module or choose a very similar name, maybe a typo, or there are even techniques to make it not appears when listing the modules and more..., but thats out of scope in this easy challenge.

We find the following filename to investigate:
```bash
sudo strings /lib/modules/6.8.0-1016-aws/kernel/drivers/misc/spatch.ko
```

Already within the first 50 lines we can understand that this is the right direction:
```
inux
Linux
AUATL
[A\A]]1
AUATL
get_flagH9
[A\A]]1
cipher_bd
/tmp/cipher_output.txt
/bin/sh
%s > %s 2>&1
get_flag
/root/src/spatch.c
HOME=/root
3[CIPHER BACKDOOR] Failed to create /proc entry
6[CIPHER BACKDOOR] Module loaded. Write data to /proc/%s
6[CIPHER BACKDOOR] Module unloaded.
3[CIPHER BACKDOOR] Failed to read output file
6[CIPHER BACKDOOR] Command Output: %s
3[CIPHER BACKDOOR] No output captured.
6[CIPHER BACKDOOR] Executing command: %s
3[CIPHER BACKDOOR] Failed to setup usermode helper.
6[CIPHER BACKDOOR] Format: echo "COMMAND" > /proc/cipher_bd
6[CIPHER BACKDOOR] Try: echo "%s" > /proc/cipher_bd
6[CIPHER BACKDOOR] Here's the secret: 54484d7b73757033725f-REDACTED-FOR-THE-WRITEUP
PATH=/sbin:/bin:/usr/sbin:/usr/bin
description=Cipher is always root
author=Cipher
license=GPL
srcversion=81BE8A2753A1D8A9F28E91E
depends=
retpoline=Y
name=spatch
vermagic=6.8.0-1016-aws SMP mod_unload modversions 
[__x86_return_thunk
proc_remove
filp_open

```

There we find a secret `54484d7b73757033725f-REDACTED-FOR-THE-WRITEUP`, which is an hex encoded string.
Let's decode it:
```bash
echo "54484d7b73757033725-REDACTED-FOR-THE-WRITEUP" | xxd -r -p
```

And there we have our flag:
--> REDACTED

<br/>
<br/>

## Conclusion
Congratulations you have successfully found the hidden kernel backdoor in this linux system, practicing with some basic investigation of a live compromised host. 

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
