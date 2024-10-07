from libs.bitcoin_rpc import Bitcoin
Bitcoin = Bitcoin()

BLOCK_HASH = "dab5708b1b3db05407e35b2004156d74f7bb5bed7f677743945cac1465b5838f"
TX_HASH = "7bd09aa3b4795be2839d9159edff0811d6d4ec5a64abd81c0da1e73ab00bf520"

# First we need to find the transaction with the corresponding tx hash
# build a function that will call get_tx_Fee when it finds a transaction with the correct TX_HASH
# this is the function that we will call for validation
def get_block_tx_fee():
    block = Bitcoin.rpc("getblock", BLOCK_HASH)
    # YOUR CODE HERE
    fee = 0
    for tx in block['txs']:
        if tx['txid'] == TX_HASH:
            fee = get_tx_fee(tx)
    return fee

# Now let's find the miner's fee for this transaction.
# with the transaction from above determine the fee paid to miners
def get_tx_fee(tx):
    fee = 0
    # YOUR CODE HERE
    total_output = 0
    for op in tx['outputs']:
        total_output += op['value']
    total_input = 0
    for ip in tx['inputs']:
        total_input += ip['value']
    fee = total_input - total_output
    return fee
