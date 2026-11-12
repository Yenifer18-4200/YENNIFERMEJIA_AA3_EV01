"""Security helpers: password hashing and verification."""

import hashlib
import hmac
import os

# Number of PBKDF2 iterations (more iterations = harder to brute-force).
ITERATIONS = 100_000


def hash_password(plain_password: str) -> str:
    """Hash a password with PBKDF2-SHA256 and a random salt.

    Returns a string formatted as "salt$hash" (both in hexadecimal),
    ready to be stored in the password column of the User table.
    """
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", plain_password.encode("utf-8"), salt, ITERATIONS
    )
    return f"{salt.hex()}${digest.hex()}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Check whether a password matches the stored hash."""
    try:
        salt_hex, digest_hex = stored_hash.split("$")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except ValueError:
        # The stored value does not have the expected format.
        return False

    candidate = hashlib.pbkdf2_hmac(
        "sha256", plain_password.encode("utf-8"), salt, ITERATIONS
    )
    # compare_digest prevents timing attacks.
    return hmac.compare_digest(candidate, expected)