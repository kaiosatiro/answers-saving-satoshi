from random import randrange
import libs.secp256k1 as secp256k1
from struct import pack
import hashlib


class Witness:
    def __init__(self):
        self.items = []

    def push_item(self, data):
        self.items.append(data)

    def serialize(self):
        r = b""
        r += pack("<B", len(self.items))
        for item in self.items:
            r += pack("<B", len(item))
            r += item
        return r


class Transaction:
    def __init__(self):
        self.version = 2
        self.flags = bytes.fromhex("0001")
        self.inputs = []
        self.outputs = []
        self.witnesses = []
        self.locktime = 0

    def digest(self, input_index: int):
        # Start with an empty bytes object
        main_b = b""
        # Append the transaction version in little endian
        main_b += pack('<I', self.version)
        # Create a temporary bytes object and write the serialized outpoints of every input
        temp = b""
        for i in self.inputs:
            s_outpoint = i.outpoint.serialize()
            temp += s_outpoint
        # double-SHA256 the serialized outpoints and append that to the main buffer
        db_hash = hashlib.sha256(hashlib.sha256(temp).digest()).digest()
        main_b += db_hash
        # Create a temporary bytes object and write the sequences of every input in little endian
        temp = b""
        for i in self.inputs:
            seq = i.sequence
            temp += pack('<I', seq)
        # double-SHA256 the serialized sequences and append that to the main buffer
        db_hash = hashlib.sha256(hashlib.sha256(temp).digest()).digest()
        main_b += db_hash
        # Serialize the outpoint of the one input we are going to sign and add it to the main buffer
        inpt = self.inputs[input_index]
        main_b += inpt.outpoint.serialize()
        # Serialize the scriptcode of the one input we are going to sign and add it to the main buffer
        main_b += inpt.scriptcode
        # Append the value of the input we are going to spend in little endian to the main buffer
        main_b += pack('<q', inpt.value)
        # Append the sequence of the input we are going to spend in little endian to the main buffer
        main_b += pack('<I', inpt.sequence)
        # Create a temporary bytes object and write all the serialized outputs of this transaction
        temp = b""
        for o in self.outputs:
            s_output = o.serialize()
            temp += s_output
        # double-SHA256 the serialized outputs and append that to the main buffer
        db_hash = hashlib.sha256(hashlib.sha256(temp).digest()).digest()
        main_b += db_hash
        # Append the transaction locktime in little endian to the main buffer
        main_b += pack('<I', self.locktime)
        # Append the sighash flags in little endian to the main buffer
        main_b += pack("<I", int.from_bytes(self.flags))
        # Finally, return the double-SHA256 of the entire main buffer
        return hashlib.sha256(hashlib.sha256(main_b).digest()).digest()
        

# YOUR CODE HERE
    def compute_input_signature(self, index: int, key: int):
        assert isinstance(key, int)
        GE = secp256k1.GE
        G = secp256k1.G
        # The math:
        #   k = random integer in [1, n-1]
        k = randrange(1, GE.ORDER)
        #   R = G * k
        R = k * G
        #   r = x(R) mod n
        r = R.x.__int__() % GE.ORDER
        #   s = (r * a + m) / k mod n
        k_inv = pow(k, -1, GE.ORDER)
        s = ((r * key) + int.from_bytes(self.digest(index))) * k % GE.ORDER
        #   Extra Bitcoin rule from BIP 146:
        #     if s > n / 2 then s = n - s mod n
        # return (r, s)
        if s > GE.ORDER / 2:
            s = GE.ORDER - s % GE.ORDER
        # Hints:
        #   n = the order of the curve secp256k1.GE.ORDER
        #   a = the private key
        #   m = the message value returned by digest()
        #   x(R) = the x-coordinate of the point R
        #   Use the built-in pow() function to turn division into multiplication!
        return (r, s)

    def sign_input(self, index, priv, pub, sighash=1):
        def encode_der(r, s):
            # Represent in DER format. Thebyte representations of r and s have length rounded up
            # (255 bits becomes 32 bytes and 256 bits becomes 33 bytes).
            # See BIP66
            # https://github.com/bitcoin/bips/blob/master/bip-0066.mediawiki
            rb = r.to_bytes((r.bit_length() + 8) // 8, 'big')
            sb = s.to_bytes((s.bit_length() + 8) // 8, 'big')
            return b'\x30' + bytes([4 + len(rb) + len(sb), 2, len(rb)]) + rb + bytes([2, len(sb)]) + sb
        # YOUR CODE HERE
        input_sig = self.compute_input_signature(index, priv)
        der = encode_der(input_sig[0], input_sig[1])
        der += pack('B', sighash)
        wit_obj = Witness()
        wit_obj.push_item(der)
        wit_obj.push_item(bytes.fromhex(pub))
        self.witnesses.append(wit_obj)

if __name__ == '__main__':
    import ecdsa
    from ecdsa import VerifyingKey, SECP256k1
    from ch_6_3_lib import Input, Output

    priv_dsljfohd = 0x93485bbe0f0b2810937fc90e8145b2352b233fbd3dd7167525401dd30738503e
    compressed_pub_agfwuebb = bytes.fromhex("038cd0455a2719bf72dc1414ef8f1675cd09dfd24442cb32ae6e8c8bbf18aaf5af")
    txid_noiewnoa = "8a081631c920636ed71f9de5ca24cb9da316c2653f4dc87c9a1616451c53748e"
    valueOne_aelfhasc = 650000000
    scriptcode_iabsvalb = "1976a914b234aee5ee74d7615c075b4fe81fd8ace54137f288ac"
    vout_bucbsncc = 1
    input_bauoevbs = Input.from_output(txid_noiewnoa, vout_bucbsncc, valueOne_aelfhasc, scriptcode_iabsvalb)
    addr_pqvejvea = "bc1qgghq08syehkym52ueu9nl5x8gth23vr8hurv9dyfcmhaqk4lrlgs28epwj"
    valueTwo_jhcermcr = 100000000
    output_uhmhvgcw = Output.from_options(addr_pqvejvea, valueTwo_jhcermcr)
    tx_eagmcued = Transaction()
    tx_eagmcued.inputs.append(input_bauoevbs)
    tx_eagmcued.outputs.append(output_uhmhvgcw)
    (r, s) = tx_eagmcued.compute_input_signature(0, priv_dsljfohd)

    sig_string_oiadhald = f'{r:064x}{s:064x}'
    sig_bytes_ayeqncas = bytes.fromhex(sig_string_oiadhald)
    hashed_message_bytes_ywienvsd = tx_eagmcued.digest(0)
    verifying_key_dojssdfo = VerifyingKey.from_string(compressed_pub_agfwuebb, curve=SECP256k1)
    print(verifying_key_dojssdfo.verify_digest(sig_bytes_ayeqncas, hashed_message_bytes_ywienvsd) and 'true')