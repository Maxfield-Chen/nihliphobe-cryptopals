import mccrypto as mc
import random


def offering(data, key):
    mystery = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    offer = data + mystery.decode("base-64")
    return mc.encrypt_ecb(key, mc.pkcs7(offer, 16))

def pure_offering(data, key):
    return mc.encrypt_ecb(key, mc.pkcs7(data, 16))

def cm_oracle(offering):
    seen = {}
    blocks = len(offer)/16
    for i in range(blocks):
        cb = offer[16*i:16*(i+1)]
        if seen.get(cb):
            return False
        else:
            seen[cb] = True
    return True



def ecb_oracle_attack():
    #Detect Block Size
    key = mc.srand(16)
    ioffer = pure_offering("B", key)
    iol = len(ioffer)
    block_size = -1
    for i in xrange(128):
        offer = pure_offering("B"*i,key)
        if len(offer) > iol:
            block_size = i
            break
    if (block_size == -1):
        print "UNABLE TO DETECT BLOCK SIZE!"

    # Detect Mode
    if (cm_oracle(offering("B"*96, key).encode("hex"))):
        print "ECB MODE"
    else:
        print "CBC MODE"
    # Offend the Oracle
    



