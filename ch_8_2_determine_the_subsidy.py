def get_subsidy(height):
    # YOUR CODE HERE
    halving =  height // 210000
    coinbase = 5000000000
    coinbase >>= halving

    return coinbase

print(get_subsidy(210000 * 10))