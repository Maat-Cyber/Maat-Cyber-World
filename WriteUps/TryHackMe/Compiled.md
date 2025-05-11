# Compiled Walkthrough
<br/>

## Intro
Welcome to the Compiled challenge, here is the link to the [room](https://tryhackme.com/room/compiled) on TryHackMe.

This challenge is about reverse engineering a binary.

Whenever you feel ready download the task file on your machine.

Let's begin!

<br/>
<br/>

## The Challenge
We can start by checking the type of file we are dealing with:
```
file Compiled.Compiled
```

It is and ELF binary, let's make it executable and try to run it:
```bash
chmod +x Compiled.Compiled
```

```bash
./compiled
```

The proram asks for a password, sending a test input we get the message "Try Again!"

Let's decompile the binary:
```bash
r2 -A id Compiled.Compiled
```

List functions:
```
 afl
```

```
pdf @ main
```

Can decomile with a plugin: r2dec or using Ghidra. 

Here is the decompiled code:
```c
int main(void) {
    int iVar1;
    char local_28[32];

    fwrite("Password: ", 1, 10, stdout);
    __isoc99_scanf("DoYouEven%sCTF", local_28);

    iVar1 = strcmp(local_28, "__dso_handle");
    if (iVar1 >= 0 && iVar1 < 1) {
        printf("Try again!");
        return 0;
    }

    iVar1 = strcmp(local_28, "_init");
    if (iVar1 == 0) {
        printf("Correct!");
    } else {
        printf("Try again!");
    }
    return 0;
}

```

Here it checks if the input starts with `DoYouEven`, than `scanf` reads the input that come after `"DoYouEven"` and it gets stored in the `locale28` buffer.
Then the content of `local2_28` gets checked first against `__dso_handle`, if equal we fail, then with `_init`, if the string matches it prints "Correct"!

--> REDACTED

<br/>
<br/>

## Conclusion
Congratulations you have successfully reversed the application and found the vulnerable string to inject.

I hope you had fun doing the challenge and following along!

Catch you in the next CTF 😃 
