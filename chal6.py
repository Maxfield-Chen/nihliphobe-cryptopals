from __future__ import division
import base64
import itertools
import binascii
import mc_crypto


#Iterate over each byte and count distance.
def ham_distance(s1, s2):
    ham = 0
    s1_bin = bin(int(binascii.hexlify(s1), 16))[2:]
    s2_bin = bin(int(binascii.hexlify(s2), 16))[2:]

    #Now iterate over binary strings and find difference
    for f, b in itertools.izip(s1_bin, s2_bin):
        if f != b:
            ham += 1
    return ham

#Candidates are 2, 3, 15
def det_keysize(data):
    distances = []
    for key_size in xrange(2,40):
        b1 = data[0:key_size]
        b2 = data[key_size: key_size*2]
        b3 = data[key_size*2: key_size*3]
        b4 = data[key_size*3: key_size*4]
        hdn1 = ham_distance(b1, b2)/key_size
        hdn2 = ham_distance(b3, b4)/key_size
        hdn = (hdn1 + hdn2) / 2
        cur_dist = (hdn, key_size)
        #print b1, ":", b2, ":", b3, ":", b4
        #print hdn1, ":", hdn2, "|", cur_dist
        distances.append(cur_dist)
    distances.sort(key=lambda x: x[0])
    return distances

def blockify(data, block_size):
    #Left justify the data if block size doesn't match exactly.
    if (len(data) % block_size != 0):
        pad_len = int(len(data) + (block_size - (len(data) % block_size)))
        data = data.ljust(pad_len, '0')
    blocks = ["" for x in xrange(int(len(data)/block_size))]
    for index in xrange(len(data)):
        blocks[index // block_size] += data[index].encode("hex")
    return blocks

def transpose_blocks(data, block_size):
    #Divided by two to account for hex char length of 2
    transposed = ["" for x in xrange(0, block_size)]
    # For each block, grab 2 hex chars at a time
    for block in data:
        for index in xrange(0, len(block), 2):
            transposed[int(index //2)] += block[index]
            transposed[int(index //2)] += block[index+1]
    return transposed



data = (open("6.txt").read().rstrip('\n')).decode('base64')

block_size = 3
blocks = (transpose_blocks(blockify(data, block_size), block_size))
for block in blocks:
    print(mc_crypto.char_freq_hex(block))
