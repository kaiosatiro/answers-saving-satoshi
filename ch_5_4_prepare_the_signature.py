import base64

# Vanderpoole's signature
vp_sig = "H4vQbVD0pLK7pkzPto8BHourzsBrHMB3Qf5oYVmr741pPwdU2m6FaZZmxh4ScHxFoDelFC9qG0PnAUl5qMFth8k="

def decode_sig(vp_sig:str):
    # Decode a base64-encoded signature string into its ECDSA signature elements r and s, returned as a tuple of integers.
    # Remember to throw away the first byte of metadata from the signature string!
    decoded_msg = base64.b64decode(vp_sig)[1:]

    sig = (
        int.from_bytes(decoded_msg[:32]),
        int.from_bytes(decoded_msg[32:])
    )

    return sig
