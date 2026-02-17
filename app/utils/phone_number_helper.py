import re


def validate_and_format_phone(phone: str) -> dict:

    if not phone:
        return {
            "is_wa_active": "non-active",
            "normalized_phone": None,
            "wa_link": None,
            "is_office_number": True
        }

    # Hilangkan spasi, strip, kurung
    clean_phone = re.sub(r"[^\d+]", "", phone)

    # Deteksi nomor kantor
    # Biasanya:
    # - Awalan 021, 022, dll
    # - Tidak diawali 08 / 62
    # - Panjang < 10 digit

    if clean_phone.startswith("0") and not clean_phone.startswith("08"):
        return {
            "is_wa_active": "non-active",
            "normalized_phone": clean_phone,
            "wa_link": None,
            "is_office_number": True
        }

    # Nomor HP (Mobile)

    normalized = None

    if clean_phone.startswith("08"):
        normalized = "+62" + clean_phone[1:]

    elif clean_phone.startswith("62"):
        normalized = "+62" + clean_phone[2:]

    elif clean_phone.startswith("+62"):
        normalized = clean_phone

    else:
        # Tidak valid untuk WA
        return {
            "is_wa_active": "non-active",
            "normalized_phone": clean_phone,
            "wa_link": None,
            "is_office_number": True
        }

    # Hapus tanda + untuk link wa.me
    wa_number = normalized.replace("+", "")

    return {
        "is_wa_active": "active",
        "normalized_phone": normalized,
        "wa_link": f"https://wa.me/{wa_number}",
        "is_office_number": False
    }
