import hashlib
import hmac


def generate_sign(message: str, key: str) -> str:
    byte_key = bytes(key, 'UTF-8')
    message_bytes: bytes = message.encode()
    h = hmac.new(byte_key, message_bytes, hashlib.sha256)
    return h.hexdigest()
