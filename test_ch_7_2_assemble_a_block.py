from collections import Counter
from delete import import_mempool_from_json_file, run
MAX_BLOCK_WEIGHT = 4000000

mempool_test = import_mempool_from_json_file("mempool.json")

def test_block(mempool, block):
    """Read a list of transactions from stdin and check that they form a valid block."""
    block_weight = 0
    block_fees = 0
    txs_in_block = []
    # Construct dictionary for fast lookup
    mempool_txs = {tx.txid: tx for tx in mempool}
    lines_to_test = block

    duplicate_txs = [k for k, count in Counter(lines_to_test).items() if count > 1]

    if duplicate_txs:
        print("Invalid block!")
        count = len(duplicate_txs)
        txs = duplicate_txs[:2] + ["..."] if count > 2 else []
        return f"{count} duplicate txs found: {txs}"

    for tx in lines_to_test:
        if tx not in mempool_txs.keys():
            return f"Invalid tx {tx} in block!"

        for parent in mempool_txs[tx].parents:
            if parent not in txs_in_block:
                return f"Block contains transaction {tx} with unconfirmed parent {parent}!"

        txs_in_block.append(tx)
        block_weight += mempool_txs[tx].weight
        block_fees += mempool_txs[tx].fee

    if block_weight > MAX_BLOCK_WEIGHT:
        return f"Too large block! Weight: {block_weight}"

    return f"Total fees: {block_fees} Total weight: {block_weight}"

print(test_block(mempool_test, run()))