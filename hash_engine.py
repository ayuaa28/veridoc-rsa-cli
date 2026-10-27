
import hashlib


def hash_message(message, n):
    """
    Mengubah pesan teks menjadi nilai hash SHA-256,
    kemudian mengubahnya menjadi bilangan modulo n.
    """
    if not isinstance(message, str):
        raise TypeError("Pesan harus berupa teks.")

    if n <= 1:
        raise ValueError("Nilai n harus lebih besar dari 1.")

    digest = hashlib.sha256(message.encode("utf-8")).digest()
    hash_value = int.from_bytes(digest, byteorder="big")

    return hash_value % n


def sign_message(message, d, n):
    """
    Membuat tanda tangan digital dari pesan menggunakan
    eksponen privat d dan modulus n.
    """
    message_hash = hash_message(message, n)
    signature = pow(message_hash, d, n)

    return signature


def verify_signature(message, signature, e, n):
    """
    Memverifikasi tanda tangan digital dengan membandingkan
    hash pesan dan hasil operasi menggunakan kunci publik.
    """
    try:
        signature = int(signature)
    except (TypeError, ValueError):
        return False

    if n <= 1 or not (0 <= signature < n):
        return False

    message_hash = hash_message(message, n)
    verified_hash = pow(signature, e, n)

    return verified_hash == message_hash
