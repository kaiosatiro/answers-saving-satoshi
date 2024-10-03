uncompressed_key = ("38a7fe5735b82adf8134b7354175a94cc596de7468e86e51db16ee0810eca456,0468f3f9c168aa8b6e9f715d0c576e8eed10bb559449707c355a1e469619d6f7")

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

    
