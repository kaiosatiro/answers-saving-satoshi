import hashlib
# Defined by Bitcoin message signing protocol
# Provided by Vanderpoole
text = "I am Vanderpoole and I have control of the private key Satoshi\n"
text += "used to sign the first-ever Bitcoin transaction confirmed in block #170.\n"
text += "This message is signed with the same private key."

"[size of prefix][prefix][size of message][message]"
def encode_message(text):
    # Given an ascii-encoded text message, serialize a byte array
    # with the Bitcoin protocol prefix string followed by the text
    # and both components preceded by a length byte.
    # Returns a 32-byte hex value.
    prefix = "Bitcoin Signed Message:\n"

    prefix_bytes = prefix.encode('ascii')
    text_bytes = text.encode('ascii')
    
    serialized_message = bytes([len(prefix_bytes)]) + prefix_bytes + bytes([len(text_bytes)]) + text_bytes
    
    sha256_hash = hashlib.sha256(serialized_message).digest()
    sha256_double_hash = hashlib.sha256(sha256_hash).hexdigest()
    
    return sha256_double_hash
