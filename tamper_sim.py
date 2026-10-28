import rsa_math
from hash_engine import sign_message, verify_message


def change_text(document: str, old_text: str, new_text: str) -> str:
    """Mengubah bagian tertentu pada dokumen."""
    if old_text not in document:
        raise ValueError(f"Teks '{old_text}' tidak ditemukan.")

    return document.replace(old_text, new_text, 1)


def add_text(document: str, extra_text: str) -> str:
    """Menambahkan teks ke dokumen."""
    return document + extra_text


def delete_text(document: str, target_text: str) -> str:
    """Menghapus bagian tertentu dari dokumen."""
    if target_text not in document:
        raise ValueError(f"Teks '{target_text}' tidak ditemukan.")

    return document.replace(target_text, "", 1)


def generate_tampered_documents(document: str) -> list[dict]:
    """Membuat variasi dokumen untuk pengujian."""
    return [
        {
            "nama": "Dokumen asli",
            "isi": document
        },
        {
            "nama": "Perubahan nilai",
            "isi": change_text(document, "Nilai: 85", "Nilai: 95")
        },
        {
            "nama": "Penambahan teks",
            "isi": add_text(document, "\nCatatan: Dokumen direvisi.")
        },
        {
            "nama": "Penghapusan teks",
            "isi": delete_text(document, "Status: Lulus")
        }
    ]


def run_tamper_test(
    document: str,
    private_key: dict,
    public_key: dict,
    crt_params: dict
) -> list[dict]:
    """Menguji tanda tangan dokumen asli dan dokumen yang diubah."""

    signature = sign_message(document, private_key, crt_params)
    test_documents = generate_tampered_documents(document)
    results = []

    print("\n=== RSA TAMPER SIMULATION ===")

    for test in test_documents:
        is_valid = verify_message(
            test["isi"],
            signature,
            public_key
        )

        status = "VALID" if is_valid else "INVALID"

        result = {
            "nama": test["nama"],
            "status": status,
            "valid": is_valid
        }

        results.append(result)

        print(f"\nPengujian: {test['nama']}")
        print(f"Isi dokumen:\n{test['isi']}")
        print(f"Hasil verifikasi: {status}")

    return results