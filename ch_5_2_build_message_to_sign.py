def create_tx_message():
    msg = ""

    # version:
    msg += "01000000"

    # number of inputs:
    msg += "01"

    # hash of tx being spent by input #0:
    msg += "c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd3704"

    # index of output of tx being spent by input #0:
    msg += "00000000"

    # scriptPubKey of output being spent by input #0:
    msg += "43410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac"

    # input #0 sequence:
    msg += "ffffffff"

    # number of outputs:
    msg += "02"

    # output #0 value (10 BTC or 1,000,000,000 satoshis):
    msg += "00ca9a3b00000000"

    # output #0 scriptPubKey (Hal Finney's public key plus OP_CHECKSIG):
    msg += "434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302f"
    msg += "a28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e"
    msg += "6cd84cac"

    # output #1 value (40 BTC or 4,000,000,000 satoshis):
    msg += "00286bee00000000"

    # output #1 scriptPubKey (Satoshi's own public key again, for change):
    msg += "43410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6"
    msg += "909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656"
    msg += "b412a3ac"

    # locktime:
    msg += "00000000"

    # SIGHASH FLAG GOES HERE!
    msg += "01000000"

    return msg
