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
            score += 5

    for index in range(0, 25):
        act_freq_per[index] = (act_freq[index]/len(ldata)) * 100
        #print chr(index + 97), ", ", act_freq_per[index]
        score += abs(exp_freq_per[index] - act_freq_per[index])
    return score

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
    for sc in scores[:30]:
        print sc[2],":", sc[1], ": ",sc[0]

char_freq_hex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
