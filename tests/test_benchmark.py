import sys
import os
import time

# Memastikan Python dapat menemukan modul di luar folder tests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import rumus
import hash_engine

# 1. Inisialisasi Kunci RSA (512-bit)
p = rumus.generate_prime(512)
q = rumus.generate_prime(512)
n = p * q
phi = (p - 1) * (q - 1)
e = 3
d = rumus.mod_inverse(e, phi)

# Pre-komputasi Eksponen & Invers CRT
dp = d % (p - 1)
dq = d % (q - 1)
q_inv = rumus.mod_inverse(q, p)

# 2. Hash Dokumen Uji
doc = "Dokumen Resmi VeriDoc-CLI 2026"
m = hash_engine.prepare_message_hash(doc, n)

# 3. Pengujian RSA Standar (1.000 Iterasi)
t0 = time.perf_counter()
for _ in range(1000):
    sig_std = rumus.mod_pow(m, d, n)
t1 = time.perf_counter()
time_std = (t1 - t0) * 1000

# 4. Pengujian RSA-CRT (1.000 Iterasi)
t2 = time.perf_counter()
for _ in range(1000):
    sp = rumus.mod_pow(m, dp, p)
    sq = rumus.mod_pow(m, dq, q)
    h = (q_inv * (sp - sq)) % p
    sig_crt = sq + h * q
t3 = time.perf_counter()
time_crt = (t3 - t2) * 1000

# 5. Output Hasil
print("\n" + "="*45)
print("     HASIL UJI PERFORMA KOMPUTASI (BENCHMARK)")
print("="*45)
print(f"Waktu RSA Standar : {time_std:.4f} ms")
print(f"Waktu RSA-CRT     : {time_crt:.4f} ms")
print(f"Peningkatan       : {time_std/time_crt:.2f}x Lebih Cepat!")
print("="*45 + "\n")