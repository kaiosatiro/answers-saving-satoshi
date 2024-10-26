import hashlib

compressed_public_key = '035a8af0297898ead26badeb4ca31235b7b7c3a40d42b6934184bf25914de9a9eb'

# Get the sha256 digest of the compressed public key.
# Then get the ripemd160 digest of that sha256 hash
# Return 20-byte array
def hash_compressed(compressed_public_key):
    sha256 = hashlib.new('sha256', bytes.fromhex(compressed_public_key)).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).hexdigest()
    return ripemd160