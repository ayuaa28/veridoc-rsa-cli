from hash_engine import sign_message, verify_message


def change_text(document: str, old_text: str, new_text: str) -> str:
    """Mengubah bagian tertentu pada dokumen."""
    if old_text not in document:
        raise ValueError(f"Teks '{old_text}' tidak ditemukan.")

    return document.replace(old_text, new_text, 1)


def add_text(document: str, extra_text: str) -> str:
    """Menambahkan teks pada dokumen."""
    return document + extra_text


def delete_text(document: str, target_text: str) -> str:
    """Menghapus bagian tertentu dari dokumen."""
    if target_text not in document:
        raise ValueError(f"Teks '{target_text}' tidak ditemukan.")

    return document.replace(target_text, "", 1)


def generate_tampered_documents(
    document: str,
    old_text: str,
    new_text: str,
    extra_text: str,
    target_text: str
) -> list[dict]:
    """Menghasilkan variasi dokumen untuk pengujian."""
    return [
        {
            "nama": "Dokumen asli",
            "isi": document
        },
        {
            "nama": "Perubahan teks",
            "isi": change_text(document, old_text, new_text)
        },
        {
            "nama": "Penambahan teks",
            "isi": add_text(document, extra_text)
        },
        {
            "nama": "Penghapusan teks",
            "isi": delete_text(document, target_text)
        }
    ]


def run_tamper_test(
    document: str,
    signature: int,
    public_key: dict,
    old_text: str,
    new_text: str,
    extra_text: str,
    target_text: str
) -> list[dict]:
    """Memverifikasi dokumen asli dan dokumen hasil perubahan."""

    test_documents = generate_tampered_documents(
        document,
        old_text,
        new_text,
        extra_text,
        target_text
    )

    results = []

    for test in test_documents:
        is_valid = verify_message(
            test["isi"],
            signature,
            public_key
        )

        results.append({
            "nama": test["nama"],
            "isi": test["isi"],
            "valid": is_valid,
            "status": "VALID" if is_valid else "INVALID"
        })

    return results

coba ini yu, YAALLAH MAAF