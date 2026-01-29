import hashlib

def calculate_checksum(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def get_next_version(current_version: int) -> int:
    return (current_version or 0) + 1
