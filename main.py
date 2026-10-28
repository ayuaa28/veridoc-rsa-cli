import sys
import os

import rumus
import hash_engine
import tamper_sim

# Kode Warna ANSI
CLR = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

# State global untuk menyimpan kunci dan signature aktif
current_state = {
    "public_key": None,
    "private_key": None,
    "crt_params": None,
    "last_signature": None,
    "last_document": None
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    clear_screen()
    print(f"{BLUE}╔══════════════════════════════════════════════════════════════════╗{CLR}")
    print(f"{BLUE}║{CLR}                      {BOLD}{CYAN}VeriDoc VeriDoc RSA-CRT{CLR}                     {BLUE}║{CLR}")
    print(f"{BLUE}║{CLR}     {DIM}Sistem Verifikasi Integritas Dokumen & Kriptografi RSA{CLR}       {BLUE}║{CLR}")
    print(f"{BLUE}╚══════════════════════════════════════════════════════════════════╝{CLR}")

def print_box(title, content_list, color=CYAN):
    width = 66
    print(f"\n{color}┌─ {BOLD}{title}{CLR}{color} " + "─" * (width - len(title) - 4) + f"┐{CLR}")
    for line in content_list:
        print(f"{color}│{CLR} {line:<{width-3}} {color}│{CLR}")
    print(f"{color}└" + "─" * (width - 2) + f"┘{CLR}")


def generate_keys_menu():
    show_header()
    print(f"\n{BOLD}{YELLOW}[1] GENERATE PASANGAN KUNCI RSA{CLR}\n")
    
    try:
        raw_bits = input(f"Masukkan panjang bit prima [{GREEN}default: 512{CLR}]: ").strip()
        bits = int(raw_bits) if raw_bits else 512

        if bits < 16:
            print(f"\n{BOLD}{RED}[!] Bit terlalu kecil. Gunakan minimal 16 bit.{CLR}")
            input("\nTekan Enter untuk kembali...")
            return

        print(f"\n{DIM}[*] Mengenerate bilangan prima p, q dan parameter CRT...{CLR}")
        
        p = rumus.generate_prime(bits)
        q = rumus.generate_prime(bits)
        while p == q:
            q = rumus.generate_prime(bits)

        n = p * q
        phi_n = (p - 1) * (q - 1)
        e = 3

        d = rumus.mod_inverse(e, phi_n)

        current_state["public_key"] = {"e": e, "n": n}
        current_state["private_key"] = {"d": d, "n": n}
        current_state["crt_params"] = {"p": p, "q": q}

        content = [
            f"{BOLD}Status:{CLR} {GREEN}Kunci Berhasil Dibuat!{CLR}",
            "",
            f"{CYAN}Modulus (n):{CLR}        {n}",
            f"{CYAN}Public Exp (e):{CLR}     {e}",
            f"{CYAN}Private Exp (d):{CLR}    {d}",
            f"{CYAN}Prime 1 (p):{CLR}        {p}",
            f"{CYAN}Prime 2 (q):{CLR}        {q}",
        ]
        print_box("PARAMETER KUNCI RSA-CRT", content, color=GREEN)

    except Exception as err:
        print(f"\n{BOLD}{RED}[!] Terjadi kesalahan:{CLR} {err}")

    input("\nTekan Enter untuk kembali ke menu utama...")


def sign_document_menu():
    show_header()
    print(f"\n{BOLD}{YELLOW}[2] TANDA TANGAN DOKUMEN (SIGNING){CLR}\n")

    if not current_state["private_key"]:
        print(f"{BOLD}{RED}[!] Silakan generate kunci terlebih dahulu di Menu 1.{CLR}")
        input("\nTekan Enter untuk kembali...")
        return

    doc = input(f"Masukkan teks/dokumen yang akan ditandatangani:\n{BOLD}> {CLR}")
    if not doc.strip():
        print(f"\n{BOLD}{RED}[!] Dokumen tidak boleh kosong.{CLR}")
        input("\nTekan Enter untuk kembali...")
        return

    sig = hash_engine.sign_message(
        doc,
        current_state["private_key"],
        current_state["crt_params"]
    )

    current_state["last_document"] = doc
    current_state["last_signature"] = sig

    content = [
        f"{BOLD}Dokumen Asli:{CLR} {doc}",
        "",
        f"{BOLD}Digital Signature (Decimal):{CLR}",
        f"{YELLOW}{sig}{CLR}"
    ]
    print_box("HASIL PENANDATANGANAN", content, color=GREEN)

    input("\nTekan Enter untuk kembali ke menu utama...")


def verify_document_menu():
    show_header()
    print(f"\n{BOLD}{YELLOW}[3] VERIFIKASI TANDA TANGAN (VERIFICATION){CLR}\n")

    if not current_state["public_key"]:
        print(f"{BOLD}{RED}[!] Silakan generate kunci terlebih dahulu di Menu 1.{CLR}")
        input("\nTekan Enter untuk kembali...")
        return

    doc = input(f"Masukkan teks/dokumen yang ingin diverifikasi:\n{BOLD}> {CLR}")
    sig_input = input(f"Masukkan nilai Signature (integer decimal):\n{BOLD}> {CLR}")

    try:
        sig = int(sig_input)
        is_valid = hash_engine.verify_message(
            doc,
            sig,
            current_state["public_key"]
        )

        if is_valid:
            content = [
                f"{BOLD}{GREEN}✔ STATUS: VALID{CLR}",
                "",
                "Dokumen terverifikasi asli dan tidak mengalami perubahan."
            ]
            print_box("HASIL VERIFIKASI", content, color=GREEN)
        else:
            content = [
                f"{BOLD}{RED}✘ STATUS: INVALID{CLR}",
                "",
                "Tanda tangan salah atau dokumen telah dimanipulasi!"
            ]
            print_box("HASIL VERIFIKASI", content, color=RED)

    except ValueError:
        print(f"\n{BOLD}{RED}[!] Nilai signature harus berupa angka integer.{CLR}")

    input("\nTekan Enter untuk kembali ke menu utama...")


def run_simulation_menu():
    show_header()
    print(f"\n{BOLD}{YELLOW}[4] SIMULASI TAMPERING DOKUMEN{CLR}\n")

    if not current_state["private_key"]:
        print(f"{BOLD}{RED}[!] Silakan generate kunci terlebih dahulu di Menu 1.{CLR}")
        input("\nTekan Enter untuk kembali...")
        return

    # Cek apakah pengguna sudah pernah menandatangani dokumen di Menu 2
    if current_state["last_document"]:
        doc = current_state["last_document"]
        print(f"Menggunakan dokumen dari Menu 2: {CYAN}\"{doc}\"{CLR}\n")
    else:
        # Jika belum pernah di Menu 2, baru minta input dokumen asli
        doc = input(f"Masukkan dokumen asli:\n{BOLD}> {CLR}")
        if not doc.strip():
            print(f"\n{BOLD}{RED}[!] Dokumen tidak boleh kosong.{CLR}")
            input("\nTekan Enter untuk kembali...")
            return

    # Cukup minta parameter manipulasi yang ingin diuji
    old_text = input(f"Teks yang ingin diubah pada dokumen:\n{BOLD}> {CLR}")
    new_text = input(f"Teks penggantinya:\n{BOLD}> {CLR}")
    extra_text = input(f"Teks tambahan (penambahan teks):\n{BOLD}> {CLR}")
    target_text = input(f"Teks yang ingin dihapus (penghapusan teks):\n{BOLD}> {CLR}")

    try:
        # Gunakan signature yang sudah ada jika ada, atau buat baru dari dokumen tersebut
        if current_state["last_signature"] and current_state["last_document"] == doc:
            signature = current_state["last_signature"]
        else:
            signature = hash_engine.sign_message(
                doc, 
                current_state["private_key"], 
                current_state["crt_params"]
            )

        # Jalankan simulasi tamper
        test_results = tamper_sim.run_tamper_test(
            document=doc,
            signature=signature,
            public_key=current_state["public_key"],
            old_text=old_text,
            new_text=new_text,
            extra_text=extra_text,
            target_text=target_text
        )

        print(f"\n{BOLD}{CYAN}=== HASIL SIMULASI UJI INTEGRITAS DOKUMEN ==={CLR}\n")
        print(f"{'Skenario Pengujian':<25} | {'Isi Ringkas Dokumen':<30} | {'Hasil Verifikasi'}")
        print("-" * 75)

        for res in test_results:
            status_str = f"{GREEN}VALID{CLR}" if res["valid"] else f"{RED}INVALID{CLR}"
            isi_clean = res["isi"].replace("\n", " ")
            if len(isi_clean) > 28:
                isi_clean = isi_clean[:25] + "..."
            
            print(f"{res['nama']:<25} | {isi_clean:<30} | {status_str}")

        print("-" * 75)

    except ValueError as err:
        print(f"\n{BOLD}{RED}[!] Gagal menjalankan simulasi:{CLR} {err}")
    except Exception as err:
        print(f"\n{BOLD}{RED}[!] Terjadi kesalahan:{CLR} {err}")

    input("\nTekan Enter untuk kembali ke menu utama...")


def main():
    while True:
        show_header()

        status_kunci = f"{GREEN}Tersedia{CLR}" if current_state["public_key"] else f"{RED}Belum Dibuat{CLR}"
        print(f" Status Kunci RSA: [{status_kunci}]\n")

        print(f"{BOLD} PILIHAN MENU:{CLR}")
        print(f"  {CYAN}1.{CLR} Generate Pasangan Kunci RSA")
        print(f"  {CYAN}2.{CLR} Tanda Tangan Dokumen (Sign)")
        print(f"  {CYAN}3.{CLR} Verifikasi Tanda Tangan (Verify)")
        print(f"  {CYAN}4.{CLR} Simulasi Tampering Dokumen")
        print(f"  {CYAN}5.{CLR} Keluar dari Program\n")

        choice = input(f"Pilih menu (1-5): {BOLD}").strip()
        print(CLR, end="")

        if choice == "1":
            generate_keys_menu()
        elif choice == "2":
            sign_document_menu()
        elif choice == "3":
            verify_document_menu()
        elif choice == "4":
            run_simulation_menu()
        elif choice == "5":
            print(f"\n{GREEN}Terima kasih telah menggunakan sistem ini!{CLR}\n")
            sys.exit(0)


if __name__ == "__main__":
    main()