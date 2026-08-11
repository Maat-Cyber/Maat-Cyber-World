# Management Wants a Word Walkthrough
<br/>

## Intro
Welcome to the *Management Wants a Word* challenge, here is the link to the [room](https://tryhackme.com/room/hh-managementwantsaword-6bf3cc41) on TryHackMe.

This is flagged as an hard challenge about forensics investigation of a Windows machine memory dump.

This is am hard challenge about forensics

"*Housekeeping found a guest's laptop left behind after an early checkout, Room 214, registered to a "Vera." IT pulled a full triage before wiping it for the next guest.
Hunt down the artifacts scattered across her machine and figure out how they fit together. Somewhere in that trail is a password she never meant to leave behind. Follow it, and it'll open a door to something she was keeping very quiet.*"

Whenever you feel ready download the tasks file.

Let's begin!

<br/>
<br/>

## The Challenge
We can start by unpacking the zip archive containing the challenge files:
```bash
unzip management-wants-a-word-forensics-hh-day-14.zip
```

There are just a tiny bunch of files to check:
```bash
tree -a management-wants-a-word-forensics-hh-day-14 | wc -l
626
```

Only about 600.

Looking at them we can see KAPE dumps, containg a tons of files, including SAM db and other important directories.
Note also the room comment:

> [!Comment] Comment
> "ok so apparently a browser will remember things for you that you never told anyone else 💀 not every hidden file needs a password cracker, some of them just need a really good memory also why did Patch tell me this version number 1.26.29 idk what it means :( #HackerHolidays"

There is also a single blob at: `C/Users/vera/AppData/Roaming/Microsoft/Protect/S-1-5-21-2529683458-431225740-1723070931-1000/c90719ef-5b98-474e-b934-136d606a702a`

Finally looking around we can spot a directory called "backup" in Vera's document folder `C:\Users\vera\Documents`.
```bash
file backup
backup: data
```

I wanted to check the entropy of the file to know if it was encrypted, we can use *ent* command:
```bash
ent backup
Entropy = 7.999998 bits per byte.

Optimum compression would reduce the size
of this 104857600 byte file by 0 percent.

Chi square distribution for 104857600 samples is 254.32, and randomly
would exceed this value 50.02 percent of the times.

Arithmetic mean value of data bytes is 127.5028 (127.5 = random).
Monte Carlo value for Pi is 3.141542020 (error 0.00 percent).
Serial correlation coefficient is 0.000052 (totally uncorrelated = 0.0).
```

And as guessed it encrypted, entropy is high.
This makes sense or it would have been too easy to solve.

We can now put into use the memory dump we have and extract vera's secrets.

<br/>

### Secretsdump
We go to `./C:/Windows/System32/config` and use *secretsdump.py*
If you do not have *impacket* installed and want only this script:
```bash
wget https://raw.githubusercontent.com/fortra/impacket/impacket_0_12_0/examples/secretsdump.py
chmod +x secretsdump.py
```

Run it:
```bash
python3 ./secretsdump.py -sam SAM -system SYSTEM -security SECURITY LOCAL
```

We get:
```
[*] Target system bootKey: 0x0f6f73ce89c8cda52d06fcc5131e040f
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b
--- REDACTED --- 

[*] Cleaning up...
```

We not have vera NTLM hash, save it into a file and then we'll crack it:
```bash
echo "1241186a4aac4f34fREDACTED" > hash.txt
```

Now we use *Hashcat* to crack it:
```bash
hashcat -a 0 -m 1000 hash.txt --wordlist /usr/share/SecLists/rockyou.txt 
```

And we get the password --REDACTED--.

<br/>

### DPAPI Master Password Extraction
Now we can move to Vera’s DPAPI master key blob, use impacket again, this time the `dpapi` one:
```bash
cd ./C/Users/vera/AppData/Roaming/Microsoft/Protect/S-1-5-21-2529683458-431225740-1723070931-1000
```

```bash
wget https://raw.githubusercontent.com/fortra/impacket/impacket_0_12_0/examples/dpapi.py
chmod +x dpapi.py
```
```bash
python3 dpapi.py masterkey -file "./c90719ef-5b98-474e-b934-136d606a702a" \
  -sid "S-1-5-21-2529683458-431225740-1723070931-1000" \
  -password REDACTED
```

We get the following decrypted key: `0x5e5715ecREDACTED`.

<br/>

### Browser Data Dump
Now is time do dump the browser's data.

I worked with on this script to automate the extraction and decryption of Chrome db with the DPAPI master key.
- (after a bunch of fixes this one works perfectly).

Here is the script:
```python
#!/usr/bin/env python3
# chrome_logins_decrypt.py
#
# Decrypt Chrome Login Data passwords from a forensic copy / KAPE extraction.
#
# Usage examples:
#   Live Windows:
#     python chrome_logins_decrypt.py --local-state "C:\...\Local State" --login-data "C:\...\Login Data" --csv out.csv
#
#   Offline with already-decrypted Chrome AES key:
#     python3 chrome_logins_decrypt.py --login-data "/path/Login Data" --aes-key-hex <64-hex-chars> --csv out.csv
#
#   Offline with Impacket DPAPI masterkey:
#     python3 chrome_logins_decrypt.py --local-state "/path/Local State" --login-data "/path/Login Data" --masterkey-hex <hex> --csv out.csv

import argparse
import base64
import csv
import json
import os
import shutil
import sqlite3
import sys
import tempfile

# ------------------------------------------------------------------
# Crypto imports
# ------------------------------------------------------------------
AES = None
AESGCM = None

try:
    from Cryptodome.Cipher import AES
except Exception:
    try:
        from Crypto.Cipher import AES
    except Exception:
        AES = None

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except Exception:
    AESGCM = None


def log(msg):
    print(msg, file=sys.stderr)


# ------------------------------------------------------------------
# AES-GCM helper
# ------------------------------------------------------------------
def decrypt_aes_gcm(key: bytes, nonce: bytes, payload: bytes) -> bytes:
    """
    payload = ciphertext + 16-byte tag
    """
    if AESGCM:
        return AESGCM(key).decrypt(nonce, payload, None)

    if AES:
        if len(payload) < 16:
            raise ValueError("ciphertext too short for AES-GCM tag")
        ciphertext, tag = payload[:-16], payload[-16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)

    raise RuntimeError(
        "No AES-GCM library available. Install pycryptodome or cryptography.\n"
        "Example: python3 -m pip install --user --break-system-packages pycryptodome"
    )


# ------------------------------------------------------------------
# Windows live DPAPI helper
# ------------------------------------------------------------------
def dpapi_decrypt_windows(data: bytes) -> bytes:
    """
    Decrypt DPAPI blob using CryptUnprotectData.
    Only works on Windows in the correct user context.
    """
    if os.name != "nt":
        raise RuntimeError(
            "Windows DPAPI CryptUnprotectData is only available on Windows. "
            "For offline analysis provide --aes-key-hex/--aes-key-file or --masterkey-hex/--masterkey-file."
        )

    import ctypes
    import ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
            ("cbData", ctypes.wintypes.DWORD),
            ("pbData", ctypes.POINTER(ctypes.c_char)),
        ]

    buf = ctypes.create_string_buffer(data, len(data))
    blob_in = DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()

    result = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blob_in),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(blob_out),
    )

    if not result:
        raise OSError("CryptUnprotectData failed. Wrong user context or DPAPI key unavailable.")

    out = ctypes.string_at(blob_out.pbData, blob_out.cbData)
    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
    return out


# ------------------------------------------------------------------
# Optional Impacket DPAPI helper for offline masterkey usage
# ------------------------------------------------------------------
def decrypt_dpapi_blob_with_impacket(blob: bytes, masterkey: bytes) -> bytes:
    """
    Best-effort DPAPI blob decryption using impacket.dpapi.

    This is useful offline if you already recovered the DPAPI masterkey.
    Different Impacket versions may have slightly different APIs, so this
    tries a few common patterns.
    """
    try:
        from impacket.dpapi import DPAPI_BLOB
    except Exception as e:
        raise RuntimeError(f"Could not import impacket.dpapi: {e}")

    obj = None

    try:
        obj = DPAPI_BLOB(blob)
    except Exception:
        try:
            obj = DPAPI_BLOB()
            obj.fromString(blob)
        except Exception as e:
            raise RuntimeError(f"Could not parse DPAPI blob with impacket.dpapi: {e}")

    last_exc = None

    for meth_name in ("decrypt", "Decrypt"):
        meth = getattr(obj, meth_name, None)
        if not meth:
            continue

        # Try common signatures:
        #   decrypt(key)
        #   decrypt(key, entropy)
        #   decrypt(key, entropy, something_else)
        for args in ((masterkey,), (masterkey, None), (masterkey, b"", None)):
            try:
                res = meth(*args)

                if isinstance(res, bytes):
                    return res
                if isinstance(res, bytearray):
                    return bytes(res)
                if hasattr(res, "getData"):
                    return res.getData()

                return bytes(res)

            except TypeError as e:
                last_exc = e
                continue
            except Exception as e:
                last_exc = e

    raise RuntimeError(f"Impacket DPAPI blob decryption failed: {last_exc}")


# ------------------------------------------------------------------
# Key parsing helpers
# ------------------------------------------------------------------
def decode_key_material(data: bytes) -> bytes:
    """
    Accepts:
      - raw binary key
      - hex string
      - base64 encoded 16/24/32 byte key
    """
    try:
        text = data.decode("utf-8").strip()
        compact = "".join(text.split())

        # Hex?
        if compact and all(c in "0123456789abcdefABCDEF" for c in compact):
            try:
                return bytes.fromhex(compact)
            except ValueError:
                pass

        # Base64?
        try:
            decoded = base64.b64decode(compact, validate=True)
            if len(decoded) in (16, 24, 32):
                return decoded
        except Exception:
            pass

    except Exception:
        pass

    return data


def read_key_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return decode_key_material(f.read().strip())


def normalize_aes_key(key: bytes, source: str) -> bytes:
    if key is None:
        return None

    if len(key) in (16, 24, 32):
        return key

    if len(key) > 32:
        log(f"[!] {source} returned {len(key)} bytes; using first 32 bytes.")
        return key[:32]

    raise RuntimeError(f"{source} returned invalid AES key length: {len(key)} bytes")


# ------------------------------------------------------------------
# Chrome Local State helpers
# ------------------------------------------------------------------
def get_chrome_encrypted_key_blob(local_state_path: str) -> bytes:
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    try:
        b64_key = local_state["os_crypt"]["encrypted_key"]
    except KeyError:
        raise RuntimeError("Could not find os_crypt.encrypted_key in Local State")

    blob = base64.b64decode(b64_key)

    # Chrome prefixes the blob with ASCII "DPAPI"
    if blob.startswith(b"DPAPI"):
        blob = blob[5:]

    return blob


def get_aes_key(args, masterkey: bytes):
    if args.aes_key_hex:
        key_hex = "".join(args.aes_key_hex.split())
        key = bytes.fromhex(key_hex)
        return normalize_aes_key(key, "--aes-key-hex")

    if args.aes_key_file:
        key = read_key_file(args.aes_key_file)
        return normalize_aes_key(key, "--aes-key-file")

    if masterkey is not None:
        if not args.local_state:
            raise RuntimeError("Using --masterkey requires --local-state so the Chrome key can be extracted.")

        blob = get_chrome_encrypted_key_blob(args.local_state)
        key = decrypt_dpapi_blob_with_impacket(blob, masterkey)
        return normalize_aes_key(key, "DPAPI/masterkey")

    if args.local_state:
        blob = get_chrome_encrypted_key_blob(args.local_state)
        key = dpapi_decrypt_windows(blob)
        return normalize_aes_key(key, "Windows DPAPI")

    raise RuntimeError(
        "No key source provided.\n"
        "Use one of:\n"
        "  --aes-key-hex <hex>\n"
        "  --aes-key-file <file>\n"
        "  --local-state on live Windows\n"
        "  --masterkey-hex/--masterkey-file with --local-state for offline Impacket DPAPI"
    )


# ------------------------------------------------------------------
# Login Data helper
# ------------------------------------------------------------------
def fetch_logins(login_data_path: str):
    """
    Copy Login Data to temp file first to avoid SQLite locking issues.
    """
    tmp_path = None

    try:
        fd, tmp_path = tempfile.mkstemp(suffix=".sqlite")
        os.close(fd)
        shutil.copy2(login_data_path, tmp_path)
        db_path = tmp_path
    except Exception as e:
        log(f"[!] Could not copy Login Data ({e}); opening directly.")
        db_path = login_data_path

    conn = sqlite3.connect(db_path)

    try:
        cur = conn.cursor()
        cur.execute("SELECT origin_url, username_value, password_value FROM logins")
        return cur.fetchall()
    finally:
        conn.close()
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


def decrypt_login_password(blob, aes_key: bytes, masterkey: bytes):
    if blob is None:
        return ""

    if isinstance(blob, str):
        return blob

    if len(blob) == 0:
        return ""

    prefix = blob[:3]

    # Chrome v80+ style AES-GCM blob
    if prefix in (b"v10", b"v11"):
        if aes_key is None:
            return "<no AES key available>"

        # v10/v11 format:
        # 3-byte prefix | 12-byte nonce | ciphertext + 16-byte tag
        if len(blob) < 3 + 12 + 16:
            return "<truncated v10/v11 blob>"

        nonce = blob[3:15]
        payload = blob[15:]

        try:
            return decrypt_aes_gcm(aes_key, nonce, payload).decode("utf-8", errors="replace")
        except Exception as e:
            return f"<AES-GCM decrypt failed: {e}>"

    # Chrome 127+ app-bound encryption marker, often seen on modern Windows
    if prefix == b"v20":
        return "<v20 app-bound encrypted password: not supported by this script>"

    # Older Chrome passwords were raw DPAPI blobs.
    if os.name == "nt":
        try:
            return dpapi_decrypt_windows(blob).decode("utf-8", errors="replace")
        except Exception as e:
            return f"<DPAPI decrypt failed: {e}>"

    if masterkey is not None:
        try:
            return decrypt_dpapi_blob_with_impacket(blob, masterkey).decode("utf-8", errors="replace")
        except Exception as e:
            return f"<offline DPAPI decrypt failed: {e}>"

    # Maybe plaintext?
    try:
        s = blob.decode("utf-8")
        if all(32 <= ord(c) < 127 for c in s):
            return s
    except Exception:
        pass

    return f"<encrypted/unsupported blob {len(blob)} bytes prefix={prefix!r}>"


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Decrypt Chrome Login Data passwords from Local State + Login Data."
    )

    parser.add_argument("--login-data", required=True, help="Path to Chrome Login Data SQLite DB")
    parser.add_argument("--local-state", help="Path to Chrome Local State JSON file")

    parser.add_argument("--aes-key-hex", help="Already-decrypted Chrome AES key as hex")
    parser.add_argument("--aes-key-file", help="File containing decrypted Chrome AES key: raw, hex, or base64")

    parser.add_argument("--masterkey-hex", help="DPAPI masterkey hex for offline decryption via impacket")
    parser.add_argument("--masterkey-file", help="File containing DPAPI masterkey: raw or hex")

    parser.add_argument("--csv", help="Write results to CSV file")
    parser.add_argument("--show-key", action="store_true", help="Print decrypted Chrome AES key")
    parser.add_argument(
        "--print-encrypted-key",
        action="store_true",
        help="Print base64 of DPAPI-protected Chrome key from Local State and exit",
    )

    args = parser.parse_args()

    if args.print_encrypted_key:
        if not args.local_state:
            parser.error("--print-encrypted-key requires --local-state")

        blob = get_chrome_encrypted_key_blob(args.local_state)
        print(base64.b64encode(blob).decode())
        return

    masterkey = None

    if args.masterkey_hex:
        masterkey = bytes.fromhex("".join(args.masterkey_hex.split()))
    elif args.masterkey_file:
        masterkey = read_key_file(args.masterkey_file)

    aes_key = None

    try:
        aes_key = get_aes_key(args, masterkey)
        log(f"[*] Loaded Chrome AES key: {len(aes_key)} bytes")
        if args.show_key:
            log(f"[*] AES key hex: {aes_key.hex()}")
    except Exception as e:
        log(f"[!] {e}")
        aes_key = None

    try:
        rows = fetch_logins(args.login_data)
    except Exception as e:
        log(f"[!] Failed to read Login Data: {e}")
        sys.exit(1)

    if not rows:
        log("[!] No rows found in Login Data.")
        return

    csv_file = None
    csv_writer = None

    if args.csv:
        csv_file = open(args.csv, "w", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["origin_url", "username", "password"])

    count = 0

    for origin_url, username, password_blob in rows:
        password = decrypt_login_password(password_blob, aes_key, masterkey)

        origin_url = origin_url or ""
        username = username or ""

        print(f"{origin_url}\t{username}\t{password}")

        if csv_writer:
            csv_writer.writerow([origin_url, username, password])

        count += 1

    if csv_file:
        csv_file.close()
        log(f"[*] CSV written to: {args.csv}")

    log(f"[*] Processed {count} login entries.")


if __name__ == "__main__":
    main()
```

Navigate to chrome's dir:
```bash
cd "C/Users/vera/AppData/Local/Google/Chrome For Testing/User Data"
```

Execute the script:
```bash
 python3 ./chrome_logins_decrypt.py \
  --local-state './Local State' \
  --login-data './Default/Login Data' \
  --masterkey-hex 5e5715ec9b6df5a86e97902---- REDACTED---- \
  --csv chrome_logins.csv
```

We get a bunch of other credentials:
```
--csv chrome_logins.csv
[*] Loaded Chrome AES key: 32 bytes
http://bytelotus.thm:8080/      VeraSecretVault REDACTED
[*] CSV written to: chrome_logins.csv
[*] Processed 1 login entries.
```

Thats nice another password, the one for the vault this time.

<br/>

### Decrypt the Backup
Now to decrypt the backup we firstly need to know which ws used to encrypt it, after spending some time, following this table:

|Magic / check|Meaning|
|---|---|
|`4c 55 4b 53 ba be` = `LUKS\xba\xbe`|LUKS|
|`53 61 6c 74 65 64 5f 5f` = `Salted__`|OpenSSL `enc` salted format|
|`50 4b 03 04`|ZIP|
|`37 7a bc af 27 1c`|7z|
|`03 d9 a2 9a 67 fb 4b b5`|KeePass KDBX|
|`-FVE-FS-` somewhere early|BitLocker metadata|
|completely random first 512 bytes + disk-aligned size|VeraCrypt/TrueCrypt/raw dm-crypt candidate|

In our case the first bytes were completely random, no sign that could point us to any of the elements.
I came to the conclusion that it was probably TrueCrypt or VeraCrytp, since dm-crypt is on Linux and we have a Windows dump.

We can use *cryptsetup* with a special flag to tell it is veracrypt, but first we prepare the directory where we will mount it:
```bash
sudo mkdir -p /mnt/veradata
sudo cryptsetup open --type tcrypt --veracrypt "./backup" veracontainer
sudo mount -o ro /dev/mapper/veracontainer /mnt/vera
```
- when prompted provide the vault password.

Then list content:
```bash
sudo ls /mnt/vera/secret_financial_documents
```

There are 2 files:
- important_invoice_byte_lotus.pdf  
- transactions_q3.csv

Flag must be in one of them, open with your PDF editor the first file:
```bash
 sudo -i flatpak run org.kde.okular /mnt/vera/secret_financial_documents/important_invoice_byte_lotus.pdf
```

And yep, is right there:
--> ==REDACTED==

<br/>
<br/>

Congratulations, you have successfully found the flag by putting into practice your Windows memory forensics skills, going from credentials DBs dumping, password cracking, decryption and script creation!


Hope you had fun following along and completing the challenge.

Catch you in the next CTF 😃 
