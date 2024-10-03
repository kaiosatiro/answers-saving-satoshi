import libs.secp256k1 as SECP256K1
# View the library source code
# https://github.com/saving-satoshi/secp256k1py/blob/main/secp256k1py/secp256k1.py


GE = SECP256K1.GE
G = SECP256K1.G
# Message digest from step 9:
msg = 0x73a16290e005b119b9ce0ceea52949f0bd4f925e808b5a54c631702d3fea1242

# Signature values from step 10:
sig_r = 0x8bd06d50f4a4b2bba64ccfb68f011e8babcec06b1cc07741fe686159abef8d69
sig_s = 0x3f0754da6e85699666c61e12707c45a037a5142f6a1b43e7014979a8c16d87c9

# Public key values
# Remember they need to be of the format new GE(new FE(x.hex()), new FE(y.hex())) to be read by verify()
keys = [
    "04bbb554daf8811b95c8af5272fa8b4e2d6335bf19fff24d3187b8781497299aa4d27c900c367e4e506d671a4ea3aa50843f182a090d701f3bc8e6578d2455d81e",
    "04cc679cd88b28444049aa9db8f88864ace38f79ba6310d0d3f027c9462a9f420befaaf888ce372cbf6f0ece99e5ada86436c960c1c0840a588ea7dbd78187445d",
    "049d57ded01d3a7652a957cf86fd4c3d2a76e76e83d3c965e1dca45f1ee06630636b8bcbc3df3fbc9669efa2ccd5d7fa5a89fe1c0045684189f01ea915b8a746a6",
    "0461bfb73040740c12f57146b3a7f2ccfd75b6cd2a0d5df7a789cfaeb77bda4dcd222df570946cb6de62d6b1a939f55da85859f575e84ba86c67c4aa97d85ba516",
    "042a87d97397b2c43dff63670e38e78db159daa0e1070ec42181d0ed44a7d1aa508d42bd9759659c4a3194dea56da71325fb25acda6ee931cd8b93172b5d0f3c8f",
    "04d1cdabaea3be5d8161b93b7e20b0375cefee0a36259d654185555deff881406a421384e927328e2dcb5ed87103365ef3007bd31e12591e5d1c56c83516db26ec"
]

def verify(r, s, key, msg):
    if r == 0 or r >= GE.ORDER:
        print("FALSE - invalid r value")
        return False

    if s == 0 or s >= GE.ORDER:
        print("FALSE - invalid s value")
        return False
    # Calculate the inverse of sig_s modulo ORDER
    sig_s_inverted = pow(sig_s, -1, GE.ORDER)

    # Calculate u1 and u2
    u1 = (msg * sig_s_inverted) % GE.ORDER
    u2 = (sig_r * sig_s_inverted) % GE.ORDER

    # Calculate R = u1 * G + u2 * public key
    # We need to use the appropriate methods for point multiplication and addition
    R1 = GE.mul((u1, G))
    R2 = GE.mul((u2, key))
    R = R1 + R2

    # Verify if the x-coordinate of R modulo ORDER is equal to sig_r2
    return sig_r == int(R.x) % GE.ORDER

def verify_keys(keys):
    # YOUR CODE HERE
    for k in keys:
        x, y = k[2:66], k[66:]
        key = GE(
            int(x, 16),
            int(y, 16),
		)
        if verify(sig_r, sig_s, key, msg):
            return k
