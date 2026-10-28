import random

# ==========================================
# 1. MODULAR ARITHMETIC & NUMBER THEORY
# ==========================================

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

def lcm(a: int, b: int) -> int:
    """
    Menghitung Least Common Multiple (KPK).
    """
    return (a * b) // gcd(a, b)


# ==========================================
# 2. PRIMALITY TEST & PRIME GENERATION
# ==========================================

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
    Membangkitkan bilangan prima p berukuran `bits` dengan syarat p ≡ 2 (mod 3).
    Syarat ini memastikan gcd(3, p-1) = 1 untuk eksponen publik e = 3.
    """
    while True:
        # Pastikan bit tertinggi dan terendah bernilai 1 (ganjil)
        p = random.getrandbits(bits) | 1 | (1 << (bits - 1))
        if p % 3 == 2 and is_prime_miller_rabin(p):
            return p


# ==========================================
# 3. CHINESE REMAINDER THEOREM (CRT)
# ==========================================

def crt(residues: list[int], moduli: list[int]) -> int:
    """
    Menggabungkan sistem kongruensi modular menggunakan CRT:
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


# ==========================================
# 4. MULTI-PRIME RSA SIGNING ENGINE
# ==========================================

class CryptoEngine:
    """
    Engine kriptografi multi-prime RSA dengan dukungan:
    - Direct signing (tanpa CRT)
    - CRT signing (2-prime & 3-prime)
    - Verifikasi signature
    """
    def __init__(self, primes: list[int], e: int = 3):
        self.primes = primes
        self.e = e
        
        # Hitung modulus N = p1 * p2 * ... * pk
        self.n = 1
        for p in self.primes:
            self.n *= p
            
        # Hitung lambda(N) = lcm(p1-1, p2-1, ...)
        lcm_val = 1
        for p in self.primes:
            lcm_val = lcm(lcm_val, p - 1)
            
        self.d = mod_inverse(self.e, lcm_val)

    def sign_direct(self, hash_val: int) -> int:
        """
        Signing langsung pada modulus penuh: s = h^d mod N
        """
        return mod_pow(hash_val, self.d, self.n)

    def sign_crt(self, hash_val: int) -> int:
        """
        Signing menggunakan Chinese Remainder Theorem:
        1. Hitung s_i = h^(d mod (p_i-1)) mod p_i
        2. Rekonstruksi s mod N menggunakan CRT
        """
        residues = []
        for p in self.primes:
            d_i = self.d % (p - 1)
            s_i = mod_pow(hash_val, d_i, p)
            residues.append(s_i)
            
        return crt(residues, self.primes)

    def verify(self, hash_val: int, signature: int) -> bool:
        """
        Verifikasi signature: s^e mod N == hash_val
        """
        reconstructed_hash = mod_pow(signature, self.e, self.n)
        return reconstructed_hash == hash_val


# ==========================================
# DEMO PENGGUNAAN
# ==========================================
if __name__ == "__main__":
    print("=== Pembangkitan Kunci Multi-Prime (3 Prima) ===")
    bit_len = 170  # Total modulus ~ 512 bit (3 x 170 bit)
    p1 = generate_prime(bit_len)
    p2 = generate_prime(bit_len)
    p3 = generate_prime(bit_len)
    
    engine = CryptoEngine(primes=[p1, p2, p3], e=3)
    print(f"Modulus N ({engine.n.bit_length()} bits): {engine.n}")

    # Simulasi nilai hash SHA-256 (integer 256-bit)
    mock_hash = random.getrandbits(256) % engine.n
    print(f"\nNilai Hash Input: {mock_hash}")

    # 1. Direct Signing
    sig_direct = engine.sign_direct(mock_hash)
    valid_direct = engine.verify(mock_hash, sig_direct)
    print(f"Direct Signature Valid: {valid_direct}")

    # 2. CRT Signing
    sig_crt = engine.sign_crt(mock_hash)
    valid_crt = engine.verify(mock_hash, sig_crt)
    print(f"CRT Signature Valid: {valid_crt}")

    # Pengecekan konsistensi hasil signature
    print(f"Hasil Direct & CRT Identik: {sig_direct == sig_crt}")