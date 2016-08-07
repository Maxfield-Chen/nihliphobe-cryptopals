# Assumes plaintext, xor's each byte with the modded position of the key.
def rk_xor(data, key):
    result = ""
    for index in range(0, len(data)):
        result += hex(ord(data[index]) ^ ord(key[index % len(key)]))[2:].zfill(2)
    return result

# Encode a string as hex bytewise.
def str_hexStr(data):
    retVal = []
    bytes = [data[j:j+2] for j in range(0, len(data), 2)]
    for byte in bytes:
        retVal.append(chr(int(byte, 16)))
    return ''.join(retVal)

#Converts a string into base-64
def str_b64(data):
    return str_hexStr(data).encode("base-64")


#Xors 2 equal length strings with each other and returns the result
def xor_equalLen(s1, s2):
    s1_xorables = [int(s1[i:i+2], 16) for i in range(0, len(s1), 2)]
    s2_xorables = [int(s2[i:i+2], 16) for i in range(0, len(s2), 2)]
    result = ""
    for index in range(len(s1_xorables)):
        result += hex(s1_xorables[index] ^ s2_xorables[index])[2::]
    return result

# Treats a string as a representation of hex bytes and returns that
# hex xored with a character as a string.
def xor_single_char_hex(data, char):
    xorables = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
    result = ""
    for byte in xorables:
        result += chr(byte ^ char)
    return result

# Xors characters as written with the specified char and returns the result
def xor_single_char(data, char):
    xorables = [ord(data[i]) for i in range(0, len(data), 1)]
    result = ""
    for byte in xorables:
        result += chr(byte ^ char)
    return result


# Scores a string based on closeness to average english character frequency.
def score_str(data):
    exp_freq_per = [8.04, 1.54, 3.06, 3.99, 12.51, 2.30, 1.96, 5.49, 7.26, 0.16, 0.67, 4.14, 2.53, 7.09, 7.60, 2.00, 0.11, 6.12, 6.54, 9.25, 2.71, 0.99, 1.92, 0.19, 1.73, 0.09]
    act_freq = [0.0]*26
    act_freq_per = [0.0]*26
    score = 0
    bc = 0
    ldata = data.lower()

    for letter in ldata:
        index = ord(letter) - 97
        if index > 0 and index < 26:
            act_freq[index] += 1
        else:
            bc += 1

    for index in range(0, 25):
        act_freq_per[index] = (act_freq[index]/len(ldata)) * 100
        #print chr(index + 97), ", ", act_freq_per[index]
        score += abs(exp_freq_per[index] - act_freq_per[index])
    score += bc * 10
    return score

# Xors the string specified with all characters and returns the 30 
# strings whose character frequency are closest to expected.
def char_freq(data):
    scores = []
    for char in range(0, 255):
        cur_str = xor_single_char(data, char)
        cur_score = score_str(cur_str)
        cur_tup = (cur_str, cur_score)
        scores.append(cur_tup)
    scores.sort(key=lambda x: x[1])
    return scores[0]

# Xors the string specified (treated as a rep of hex) with all characters and returns the 30 
# strings whose character frequency are closest to expected.
def char_freq_hex(data):
    scores = []
    for char in range(0, 255):
        cur_str = xor_single_char_hex(data, char)
        cur_score = score_str(cur_str)
        cur_tup = (cur_str, cur_score)
        scores.append(cur_tup)
    scores.sort(key=lambda x: x[1])
    return scores[0:3]

# Xors the string specified (treated as a rep of hex) with all characters and returns the
# character which most closely matched a frequency analysis.
def char_freq_hex_key(data):
    scores = []
    for char in range(0, 255):
        cur_str = xor_single_char_hex(data, char)
        cur_score = score_str(cur_str)
        cur_tup = (chr(char), cur_score)
        scores.append(cur_tup)
    scores.sort(key=lambda x: x[1])
    return scores[0]
