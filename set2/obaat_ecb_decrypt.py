import mccrypto as mc
import random


def offering(data, key):
    return mc.encrypt_ecb(key, mc.pkcs7(data, 16))

def cm_oracle(offer):
    seen = {}
    blocks = len(offer)/16
    for i in range(blocks):
        cb = offer[16*i:16*(i+1)]
        if seen.get(cb):
            return False
        else:
            seen[cb] = True
    return True

def ecb_oracle_attack(mystery):
    #Detect Block Size
    key = mc.srand(16)
    ioffer = offering("B", key)
    iol = len(ioffer)
    block_size = -1
    for i in xrange(128):
        offer = offering("B"*i,key)
        if len(offer) > iol:
            block_size = i
            print "BLOCK SIZE:", block_size
            break
    if (block_size == -1):
        print "UNABLE TO DETECT BLOCK SIZE!"

    # Detect Mode
    if (cm_oracle(offering("B"*96, key).encode("hex"))):
        print "CBC MODE"
    else:
        print "ECB MODE"

    # Offend the Oracle
    cur_mystery = ""
    answer = ""

    num_blocks = len(mystery)/block_size
    if (num_blocks * block_size != len(mystery)):
        num_blocks += 1
    for block in xrange(num_blocks):
        block = block * block_size
        cur_mystery = mystery[block:block+block_size]
        cur_answer = ""
        for cur_byte in xrange(block_size-1, -1, -1):
            peek = offering("A" * cur_byte + cur_mystery, key)[:block_size]
            for cur_char in xrange(256):
                poison = "A" * cur_byte + cur_answer + chr(cur_char)
                possible = offering(poison, key)[:block_size]
                if possible == peek:
                    cur_answer = cur_answer + chr(cur_char)
                    answer = answer + chr(cur_char)
                    break
    print "Message Decoded Sucessfully:", answer

ecb_oracle_attack("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK".decode("base-64"))
    
