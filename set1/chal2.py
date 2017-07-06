def xor_equalLen(s1, s2):
    s1_xorables = [int(s1[i:i+2], 16) for i in range(0, len(s1), 2)]
    s2_xorables = [int(s2[i:i+2], 16) for i in range(0, len(s2), 2)]
    result = ""
    for index in range(len(s1_xorables)):
        result += hex(s1_xorables[index] ^ s2_xorables[index])[2::]
    return result
