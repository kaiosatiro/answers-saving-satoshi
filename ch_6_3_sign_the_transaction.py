from struct import pack
from struct import pack
import libs.bech32py as bech32
from random import randrange
import libs.secp256k1 as secp256k1
import hashlib

# UTXO from chapter 6 step 1 (mining pool payout)
txid = "8a081631c920636ed71f9de5ca24cb9da316c2653f4dc87c9a1616451c53748e"
vout = 1
value = 161000000

# From chapter 4 (we will reuse address for change)
priv = 0x93485bbe0f0b2810937fc90e8145b2352b233fbd3dd7167525401dd30738503e
compressed_pub = bytes.fromhex("038cd0455a2719bf72dc1414ef8f1675cd09dfd24442cb32ae6e8c8bbf18aaf5af")
pubkey_hash = "b234aee5ee74d7615c075b4fe81fd8ace54137f2"
addr = "bc1qkg62ae0wwntkzhq8td87s87c4nj5zdlj2ga8j7"

# Explained in step 6
scriptcode = "1976a914" + pubkey_hash + "88ac"

class Outpoint:
    def __init__(self, txid: bytes, index: int):
        assert isinstance(txid, bytes)
        assert len(txid) == 32
        assert isinstance(index, int)
        self.txid = txid
        self.index = index

    def serialize(self):
        r = b""
        r += self.txid
        r += pack("<I", self.index)
        return r

class Input:
    def __init__(self):
        self.outpoint = None
        self.script = b""
        self.sequence = 0xffffffff
        self.value = 0
        self.scriptcode = b""

    @classmethod
    def from_output(cls, txid: str, vout: int, value: int, scriptcode: bytes):
        self = cls()
        self.outpoint = Outpoint(bytes.fromhex(txid)[::-1], vout)
        self.value = value
        self.scriptcode = bytes.fromhex(scriptcode)
        return self

    def serialize(self):
        r = b""
        r += self.outpoint.serialize()
        r += pack("<B", len(self.script))
        r += pack("<I", self.sequence)
        return r

# Use the bech32 library to find the version and data components from the address
# See the library source code for the exact definition
# https://github.com/saving-satoshi/bech32py/blob/main/bech32py/bech32.py

class Output:
    def __init__(self):
      self.value = 0
      self.witness_version = 0
      self.witness_data = b""

    @classmethod
    def from_options(cls, addr: str, value: int):
        assert isinstance(value, int)
        self = cls()
        self.value = value
        dec = bech32.decode(addr[:2], addr)
        self.witness_version = dec[0]
        self.witness_data = bytearray(dec[1])
        return self


    def serialize(self):
        wp = b""
        wp += pack("<B", self.witness_version)
        wp += pack("<B", len(self.witness_data))
        wp += self.witness_data

        r = b""
        r += pack("<Q", self.value)
        r += pack("<B", len(wp))
        r += wp

        return r


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
        s = ((r * key) + int.from_bytes(self.digest(index))) * k_inv % GE.ORDER
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

        input_sig = self.compute_input_signature(index, priv)
        der = encode_der(input_sig[0], input_sig[1])
        der += pack('B', sighash)
        wit_obj = Witness()
        wit_obj.push_item(der)
        wit_obj.push_item(pub)
        self.witnesses.append(wit_obj)

    def serialize(self):
        b = b""
        b += pack("<I", self.version)
        b += self.flags
        b += pack("<B", len(self.inputs))
        for i in self.inputs:
            b += i.serialize()
        b += pack("<B", len(self.outputs))
        for o in self.outputs:
            b += o.serialize()
        for w in self.witnesses:
            b += w.serialize()
        b += pack("<I", self.locktime)
        return b


tx = Transaction()
in0 = Input.from_output(txid, vout, value, scriptcode)
out0 = Output.from_options("bc1qgghq08syehkym52ueu9nl5x8gth23vr8hurv9dyfcmhaqk4lrlgs28epwj", 100000000)
# The output below is all the remaining change from this transaction, are you sure you want to send yourself all the change?
out1 = Output.from_options(addr, 60999000)
tx.inputs.append(in0)
tx.outputs.append(out0)
tx.outputs.append(out1)
tx.sign_input(0, priv, compressed_pub)

print(tx.serialize().hex())