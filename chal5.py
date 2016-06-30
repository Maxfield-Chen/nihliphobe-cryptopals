def rk_xor(data, key):
    result = ""
    for index in range(0, len(data)):
        result += hex(ord(data[index]) ^ ord(key[index % len(key)]))[2:].zfill(2)
    return result

print(rk_xor("Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal", "ICE"))
