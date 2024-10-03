from libs.bech32py import encode

compressed_public_key_hash = bytes.fromhex('47ad01928998a36ea12d7d2fa85670ebe3c4093e')

# Insert checksum and metadata, encode using bech32 and return a string
# See the library source code for the exact API.
# https://github.com/saving-satoshi/bech32py/blob/main/bech32py/bech32.py
def hash_to_address(hash):
    ad = encode('tb', 0, hash)
    return ad
