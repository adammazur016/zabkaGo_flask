import hashlib


def hash_password(password: str) -> str:
    """
    Hashes a password using the SHA256 algorithm.

    :param password: The password to be hashed.
    :return: The hashed password.
    """
    # Convert password to bytes encoded in utf-8
    password_bytes = password.encode('utf-8')

    # Hash password with sha256
    hashed_password = hashlib.sha256(password_bytes).hexdigest()

    return hashed_password
