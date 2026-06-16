"""Data transformation and PII masking — NexaCorp pipeline."""
import re
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, secrets

KEY = bytes.fromhex(os.environ.get("DATA_ENCRYPTION_KEY", "0" * 64))
_gcm = AESGCM(KEY)

def mask_email(email: str) -> str:
    local, domain = email.split("@")
    return f"{local[:2]}***@{domain}"

def encrypt_pii(value: str) -> str:
    nonce = secrets.token_bytes(12)
    ct    = _gcm.encrypt(nonce, value.encode(), None)
    return (nonce + ct).hex()

def transform_batch(rows):
    out = []
    for cid, name, email, phone, score in rows:
        out.append({
            "customer_id": cid,
            "name_masked":  name[:1] + "." + name.split()[-1] if " " in name else name,
            "email_masked": mask_email(email),
            "phone_masked": re.sub(r"\d(?=\d{4})", "*", phone),
            "credit_tier":  "prime" if score >= 720 else "subprime",
        })
    return out
