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
        self.value = value
        dec = bech32.decode(addr[:2], addr)
        self.witness_version = dec[0]
        self.witness_data = bytes(dec[1])
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
