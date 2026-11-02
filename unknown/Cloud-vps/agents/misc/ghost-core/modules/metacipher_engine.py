import base64
def generate_cipher(raw_text):
    return f"[CIPHER_TRACE: ACTIVE] Hex: {base64.b16encode(raw_text.encode('utf-8')).decode('utf-8')}"
