from struct import pack
import libs.bech32py as bech32
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
        # YOUR CODE HERE
        tp = bech32.bech32_decode(addr)
        self.witness_version = tp[0]
        self.witness_data = tp[1]
        self.value = value
        return self

    def serialize(self):
        # YOUR CODE HERE
        value = int.to_bytes(self.value, 8)
        version = bytes(self.witness_version, 'ascii')
        length = len(self.witness_data)
        # length = len(self.witness_data).to_bytes(1)
        index = bytearray(self.witness_data)
        total_length = len(self.witness_version) + length + len(self.witness_data)
        # total_length = len(version + length + index)
        # total_length = len(version + length + index).to_bytes(1)

        byte_array = pack(
            f'2iBsB{length}s', 
            self.value,
            total_length, 
            self.witness_version,
            length,
            self.witness_data.encode() if isinstance(self.witness_data, str) else self.witness_data
            )
        # byte_array = pack(value + total_length + version + length + index)

        return byte_array