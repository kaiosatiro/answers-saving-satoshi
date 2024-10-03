from hashlib import sha256

# Create a program that finds a sha256 hash starting with 5 zeroes.
# To submit your answer, return it from the function.

def find_hash(nonce: int):
    # Type your code here
    tmp = nonce
    i = 1
    hash_ = sha256(str(tmp).encode()).hexdigest()
    while not hash_.startswith('00000'):
        i += 1
        tmp = nonce
        tmp += i
        hash_ = sha256(str(tmp).encode()).hexdigest()
    
    return hash_
