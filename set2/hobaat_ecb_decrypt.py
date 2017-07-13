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

def ecb_oracle_attack():
    mystery = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK".decode("base-64")
    block_size = 16
    pre = mc.srand(1)*random.randint(0,15)
    key = mc.srand(16)
    offset = -1

    # Determine offset
    for cur_byte in xrange(block_size-1, -1, -1):
        peek = offering(pre + "A" * cur_byte + mystery, key)[:block_size]
        for cur_char in xrange(256):
            poison = pre + "A" * cur_byte + chr(cur_char)
            possible = offering(poison, key)[:block_size]
            if possible == peek:
                offset = cur_byte + 1
                break

    # Offend the Oracle
    pre_block = pre + "A"*offset
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
            peek = offering(pre_block + "A" * cur_byte + cur_mystery, key)[block_size:block_size*2]
            for cur_char in xrange(256):
                poison = pre_block + "A" * cur_byte + cur_answer + chr(cur_char)
                possible = offering(poison, key)[block_size:block_size*2]
                if possible == peek:
                    cur_answer = cur_answer + chr(cur_char)
                    answer = answer + chr(cur_char)
                    break

    print "Message Decoded Sucessfully:\n", answer

ecb_oracle_attack()
    
