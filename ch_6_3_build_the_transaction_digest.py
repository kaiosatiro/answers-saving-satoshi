from struct import pack
import hashlib

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
