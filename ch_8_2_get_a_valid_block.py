from libs.bitcoin_rpc import Bitcoin
Bitcoin = Bitcoin()

def get_tx_fee(tx):
    fee = 0
    total_output = 0
    for op in tx['outputs']:
        total_output += op['value']
    
    total_input = 0
    for ip in tx['inputs']:
        total_input += ip['value']

    fee = total_input - total_output

    return fee
  
def get_subsidy(height):

    halving =  height // 210000
    coinbase = 5000000000
    coinbase >>= halving

    return coinbase


def validate_block(block):
    fee = 0
    coinbase = get_subsidy(block["height"])

    for tx in block["txs"][1:]:
        fee += get_tx_fee(tx)

    total = coinbase + fee
    block_total = block["txs"][0]["outputs"][0]["value"]
    return total == block_total

