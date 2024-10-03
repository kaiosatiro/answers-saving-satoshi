# Import from python standard libraries
import hashlib

def msg_to_integer(msg):
    # Given a hex string to sign, convert that string to bytes,
    # double-SHA256 the bytes and then return an integer from the 32-byte digest.
    sha256 = hashlib.new('sha256', bytes.fromhex(msg)).digest()
    sha256B = hashlib.new('sha256', sha256).digest()
    return int.from_bytes(sha256B)
