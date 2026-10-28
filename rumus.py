import random

# 1. MODULAR ARITHMETIC

def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Binary Modular Exponentiation: menghitung (base^exp) % mod
    secara efisien dengan kompleksitas O(log exp).
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def gcd(a: int, b: int) -> int:
    """
    Cari Greates Common Divisor (FPB) menggunakan algoritma Euclidean.
    """
    while b:
        a, b = b, a % b
    return a

def extendgcd(a: int, b: int):
    """
    Extended Euclidean Algorithm: mencari g, x, y sedemikian hingga:
    a*x + b*y = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extgcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def mod_inverse(a: int, m: int) -> int:
    """
    Hitung invers modular (a^-1 mod m) menggunakan Extended GCD.
    """
    g, x, _ = extgcd(a, m)
    if g != 1:
        raise ValueError("Inversi modular tidak ada karena gcd(a, m) != 1")
    return (x % m + m) % m

# 2. PRIMALITY TEST & PRIME GENERATION
def is_prime_miller_rabin(n: int, k: int = 40) -> bool:
    """
    Uji primalitas probabilistik Miller-Rabin.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Tulis n - 1 sebagai (2^s) * d
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = mod_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(s - 1):
            x = mod_pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

def generate_prime(bits: int) -> int:
    """
    Generate bilangan prima p dengan syarat p ≡ 2 (mod 3).
    Untuk memastikan gcd(3, p-1) = 1 untuk eksponen publik e = 3.
    """
    while True:
        # Pastikan bit tertinggi dan terendah bernilai 1 (ganjil)
        p = random.getrandbits(bits) | 1 | (1 << (bits - 1))
        if p % 3 == 2 and is_prime_miller_rabin(p):
            return p

# 3. CHINESE REMAINDER THEOREM (CRT)
def crt(residues: list[int], moduli: list[int]) -> int:
    """
    Gabungkan sistem kongruensi modular menggunakan CRT:
    x ≡ a_i (mod p_i) untuk setiap i.
    """
    N = 1
    for m in moduli:
        N *= m

    result = 0
    for a_i, p_i in zip(residues, moduli):
        N_i = N // p_i
        inv = mod_inverse(N_i, p_i)
        result = (result + a_i * N_i * inv) % N
    return result
