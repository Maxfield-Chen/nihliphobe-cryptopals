from __future__ import division
import base64
import itertools
import binascii
import mc_crypto


def xor_single_char_hex(data, char):
    xorables = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
    result = ""
    for byte in xorables:
        result += chr(byte ^ char)
    return result

def xor_single_char(data, char):
    xorables = [ord(data[i]) for i in range(0, len(data), 1)]
    result = ""
    for byte in xorables:
        result += chr(byte ^ char)
    return result


def score_str(data):
    exp_freq_per = [8.04, 1.54, 3.06, 3.99, 12.51, 2.30, 1.96, 5.49, 7.26, 0.16, 0.67, 4.14, 2.53, 7.09, 7.60, 2.00, 0.11, 6.12, 6.54, 9.25, 2.71, 0.99, 1.92, 0.19, 1.73, 0.09]
    act_freq = [0.0]*26
    act_freq_per = [0.0]*26
    score = 0
    ldata = data.lower()

    for letter in ldata:
        index = ord(letter) - 97
        if index > 0 and index < 26:
            act_freq[index] += 1
        else:
            score += 0

    for index in range(0, 25):
        act_freq_per[index] = (act_freq[index]/len(ldata)) * 100
        #print chr(index + 97), ", ", act_freq_per[index]
        score += abs(exp_freq_per[index] - act_freq_per[index])
    return score

def char_freq_key(data):
    scores = []
    for char in range(0, 255):
        cur_str = xor_single_char(data, char)
        cur_score = score_str(cur_str)
        cur_tup = (chr(char), cur_score)
        scores.append(cur_tup)
    scores.sort(key = lambda x: x[1])
    return scores[:3]

def char_freq(data):
    scores = []
    for char in range(0, 255):
        cur_str = xor_single_char(data, char)
        cur_score = score_str(cur_str)
        cur_tup = (cur_str, cur_score)
        scores.append(cur_tup)
    scores.sort(key = lambda x: x[1])
    for sc in scores[:30]:
        print sc[1], ": ",sc[0]

def char_freq_hex(data):
    scores = []
    for char in range(0, 255):
        cur_str = xor_single_char_hex(data, char)
        cur_score = score_str(cur_str)
        cur_tup = (cur_str, cur_score, chr(char))
        scores.append(cur_tup)
    scores.sort(key = lambda x: x[1])
    for sc in scores[:5]:
        print sc[2]


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

#Candidates are 10, 31, 9, 20, 5
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
        blocks[index // block_size] += data[index]
    return blocks

def transpose_blocks(data, block_size):
    transposed = ["" for x in xrange(0, block_size)]
    # For each block, move a char to corresponding transposed block
    for block in data:
        for index in xrange(0, len(block)):
            transposed[index] += block[index]
    return transposed


def det_key(data):
    print det_keysize(data)
    key_size = 29
    blocks = transpose_blocks(blockify(data, key_size), key_size)
    pot_keys = ["" for x in xrange(3)]
    for block in blocks:
        ccs = (char_freq_key(block))
        for cci in xrange(len(ccs)):
           pot_keys[cci] += ccs[cci][0]

def rk_xor(data, key):
    result = ""
    for index in range(0, len(data)):
        result += hex(ord(data[index]) ^ ord(key[index % len(key)]))[2:].zfill(2)
    return result

key = "Terminator X: Bring the noise"
data = (open("6.txt").read()).decode('base64')
print rk_xor(data, key).decode("hex")

