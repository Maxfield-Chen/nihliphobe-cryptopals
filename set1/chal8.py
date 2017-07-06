from Crypto.Cipher import AES



def test_decode():
    key = "YELLOW SUBMARINE"
    data = "d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a".decode("hex")
    IV = "\x00" * 16
    mode = AES.MODE_ECB
    crypt = AES.new(key, mode, IV=IV)
    print crypt.decrypt(data)

def detect_ecb(data):
    lines = data.readlines()
    for m in xrange(len(lines)):
        line = lines[m]
        blocks = [line[b*32:(b+1)*32] for b in xrange(10)]
        for i in xrange(10):
            for j in xrange(10):
                if i == j: 
                    continue
                b1 = blocks[i]
                b2 = blocks[j]
                if b1 == b2:
                    return (m, line, b1, b2)

print test_decode()
