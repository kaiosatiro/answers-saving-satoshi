from libs.bech32py import encode
# from bech32py.bech32 import encode

compressed_public_key_hash = bytes.fromhex('b0f880b9c70a9729e16842aa76d923631db8188a')

# Insert checksum and metadata, encode using bech32 and return a string
# See the library source code for the exact API.
# https://github.com/saving-satoshi/bech32py/blob/main/bech32py/bech32.py
def hash_to_address(hash):
    ad = encode('tb', 0, hash)
    return ad
