import hashlib
import math as py_math
import importlib


# Mengimpor file math.py
rsa_math = importlib.import_module("math")


def hash_message(message: str) -> int:
    """Menghasilkan integer dari hash SHA-256."""
    if not isinstance(message, str):
        raise TypeError("Pesan harus berupa teks.")

    digest = hashlib.sha256(message.encode("utf-8")).digest()
    return int.from_bytes(digest, byteorder="big")


def prepare_message_hash(message: str, n: int) -> int:
    """Memetakan hash ke rentang modulus RSA untuk demonstrasi."""
    if n <= 1:
        raise ValueError("Modulus RSA harus lebih besar dari 1.")

    return hash_message(message) % n


def mod_inverse(a: int, m: int) -> int:
    """Menghitung invers modular tanpa bergantung pada extgcd."""
    if py_math.gcd(a, m) != 1:
        raise ValueError("Invers modular tidak tersedia.")

    return pow(a, -1, m)


def sign_message(
    message: str,
    private_key: dict,
    crt_params: dict
) -> int:
    """Membuat tanda tangan digital RSA menggunakan CRT."""

    n = private_key["n"]
    d = private_key["d"]
    p = crt_params["p"]
    q = crt_params["q"]

    message_hash = prepare_message_hash(message, n)

    d_p = d % (p - 1)
    d_q = d % (q - 1)

    # Tanda tangan dihitung pada dua modulus yang lebih kecil
    s_p = pow(message_hash, d_p, p)
    s_q = pow(message_hash, d_q, q)

    # Menggabungkan hasil menggunakan CRT
    q_inv = mod_inverse(q, p)
    h = (q_inv * (s_p - s_q)) % p
    signature = (s_q + h * q) % n

    return signature


def verify_message(
    message: str,
    signature: int,
    public_key: dict
) -> bool:
    """Memverifikasi tanda tangan dengan kunci publik."""

    n = public_key["n"]
    e = public_key["e"]

    if not isinstance(signature, int) or not (0 <= signature < n):
        return False

    message_hash = prepare_message_hash(message, n)
    recovered_hash = pow(signature, e, n)

    return recovered_hash == message_hash
