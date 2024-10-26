uncompressed_key = ("5a8af0297898ead26badeb4ca31235b7b7c3a40d42b6934184bf25914de9a9eb,dc44cd0eb080220c5ab24899e7010d13cdfbe6c54031ed75e1732a5ae6abf0d7")

# Determine if the y coordinate is even or odd and prepend
# the corresponding header byte to the x coordinate.
# Return a hex string
def compress_publickey(public_key):
    header_byte = {
        "y_is_even": "02",
        "y_is_odd":  "03"
    }
    # YOUR CODE HERE
    uncompressed_key = public_key
    x, y = uncompressed_key.split(",")[0], uncompressed_key.split(",")[1]
    if int(y, 16) % 2 == 0:
        return header_byte["y_is_even"] + x
    else:
        return header_byte["y_is_odd"] + x

    
