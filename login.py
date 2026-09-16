"""Simple command-line login.

Demo accounts (change these before using this for anything real):
  admin / admin123
  guest / guest123
"""

from __future__ import annotations

import getpass
import hashlib
import hmac
import sys

MAX_ATTEMPTS = 3

# username -> sha256 hex digest of password
USERS = {
    "admin": hashlib.sha256(b"admin123").hexdigest(),
    "guest": hashlib.sha256(b"guest123").hexdigest(),
}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def check_credentials(username: str, password: str) -> bool:
    stored = USERS.get(username)
    if stored is None:
        return False
    return hmac.compare_digest(stored, hash_password(password))


def login() -> bool:
    print("=== Login ===")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")

        if check_credentials(username, password):
            print(f"Welcome, {username}.")
            return True

        remaining = MAX_ATTEMPTS - attempt
        if remaining:
            print(f"Invalid username or password. {remaining} attempt(s) left.")
        else:
            print("Invalid username or password. Too many failed attempts.")

    return False


if __name__ == "__main__":
    ok = login()
    sys.exit(0 if ok else 1)
