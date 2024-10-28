import json
from collections import OrderedDict

class MempoolTransaction:
    def __init__(self, json):
        self.txid = json["txid"]
        self.weight = json["weight"]
        self.fee = json["fee"]
        self.parents = json["parents"]

# Fix this!
def assemble_block(mempool):
    MAX_WEIGHT = 4000000
    ordered_max_gain = sorted(mempool, key=lambda x: x.fee / x.weight, reverse=True)
    weight = 0

    ordered_block = OrderedDict()
    for tx in ordered_max_gain:
        if weight + tx.weight <= MAX_WEIGHT:
            if any(p not in ordered_block.keys() for p in tx.parents):
                continue
            ordered_block[tx.txid] = tx
            weight += tx.weight
    
    ordered_block_list = []
    for tx in ordered_block:
        ordered_block_list.append(tx)
        
    return ordered_block_list

def import_mempool_from_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    mempool = []
    for tx in data:
        mempool.append(MempoolTransaction(tx))
    return mempool

def run():
    mempool = import_mempool_from_json_file("mempool.json")
    block = assemble_block(mempool)
    return block
