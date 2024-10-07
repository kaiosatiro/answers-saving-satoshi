from libs.bitcoin_rpc import Bitcoin
Bitcoin = Bitcoin()

CODE_CHALLENGE_2_HEIGHT = 6929996
answer = None

def get_block_height(height):
  tx_count = float("inf")
  blocks = Bitcoin.rpc("getblocksbyheight", height)
  blk_with_less = None

  for b in blocks:
      block = Bitcoin.rpc("getblock", b)
      num = len(block["txs"])
      if num < tx_count:
          tx_count = num
          blk_with_less = b
          
  return blk_with_less

