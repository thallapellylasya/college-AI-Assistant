import hashlib
import hmac
import json
import os
import re
from pathlib import Path

USERS_PATH = Path(__file__).parent / "data" / "users.json"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _load_users():
    if not USERS_PATH.exists():
        return {}
    with open(USERS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _save_users(users):
    with open(USERS_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def _hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000).hex()


def register_user(email, password, confirm):
    """Create an account. Returns (success, message)."""
    email = email.strip().lower()
    if not EMAIL_RE.match(email):
        return False, "Please enter a valid email address."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if password != confirm:
        return False, "Passwords do not match."

    users = _load_users()
    if email in users:
        return False, "This email is already registered. Please log in."

    salt = os.urandom(16)
    users[email] = {"salt": salt.hex(), "hash": _hash_password(password, salt)}
    _save_users(users)
    return True, "Account created! Now go to the Login tab."


def verify_user(email, password):
    """Check email and password. Returns True or False."""
    user = _load_users().get(email.strip().lower())
    if not user:
        return False
    salt = bytes.fromhex(user["salt"])
    return hmac.compare_digest(_hash_password(password, salt), user["hash"])