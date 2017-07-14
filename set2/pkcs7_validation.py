import mccrypto as mc

def pkcs7_strip(data, n):
    if len(data) == 0:
        raise ValueError('Data cannot be null')
    fb = ord(data[-1])
    if len(data) < fb:
        raise ValueError('Data cannot be shorter than padding')
    split = ""
    ret = ""
    for i in xrange(len(data)-1, len(data)-1-fb, -1):
        cur_char = data[i]
        if ord(cur_char) != fb:
            raise ValueError('Incorrect value found in padding')
        split += cur_char
    ret = data.split(split)[0]
    if mc.pkcs7(ret, n) != data:
        raise ValueError('Invalid Padding')
    return ret
