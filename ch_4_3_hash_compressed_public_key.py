import hashlib

compressed_public_key = '0338a7fe5735b82adf8134b7354175a94cc596de7468e86e51db16ee0810eca456'

# Get the sha256 digest of the compressed public key.
# Then get the ripemd160 digest of that sha256 hash
# Return 20-byte array
def hash_compressed(compressed_public_key):
    sha256 = hashlib.new('sha256', bytes.fromhex(compressed_public_key)).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).hexdigest()
    return ripemd160