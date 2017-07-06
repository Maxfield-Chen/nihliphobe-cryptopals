import mccrypto as mc
import unittest as ut
import struct

def encrypt_cbc(key, data, IV):
    #print "ENCRYPT"
    KEYSIZE = len(IV)
    data = mc.pkcs7(data, KEYSIZE)
    num_blocks = len(data) / KEYSIZE
    fcb = ""
    for i in range(num_blocks):
        sb = i*KEYSIZE
        pb = data[sb:sb+KEYSIZE]
        #print "PB: ", pb.encode("hex"), len(pb)
        #print "IV: ",IV.encode("hex"), len(IV)
        npb = mc.xor_equalLen(pb.encode("hex"), IV.encode("hex"))
        #if (pb.encode("hex") != mc.xor_equalLen(npb, IV.encode("hex"))):
                #print "ENCRYPT XOR ERROR!"
        #print "NPB:", npb, len(npb.decode("hex"))
        ncb = mc.encrypt_ecb(key, npb.decode("hex"))
        #print "NCB:", ncb.encode("hex") 
        IV = ncb
        fcb += ncb
        #print fcb.encode("hex")
        #print "---"
    #print "FCB:",fcb.encode("hex")
    return fcb

def decrypt_cbc(key, data, IV):
    #print "DECRYPT"
    oIV = IV
    KEYSIZE = len(IV)
    num_blocks = len(data) / KEYSIZE
    #Deal with single block case
    if (num_blocks != 1):
        IV = data[len(data)-KEYSIZE*2:len(data)-KEYSIZE]
    fcb = ""
    for i in range(num_blocks-1, -1, -1):
        sb = i*KEYSIZE
        cb = data[sb:sb+KEYSIZE]
        #print "CB: ", cb.encode("hex"), len(cb)
        ncb = mc.decrypt_ecb(key, cb)
        #print "DB: ", ncb.encode("hex")
        #print "IV: ",IV.encode("hex"), len(IV)
        ncb = mc.xor_equalLen(ncb.encode("hex"), IV.encode("hex")).decode("hex")
        #print "pb: ", ncb.encode("hex"), len(ncb) 
        if (i == 1):
            IV = oIV
        else:
            IV = data[sb-KEYSIZE*2:sb-KEYSIZE]
        fcb = ncb + fcb
        #print fcb.encode("hex")
        #print "---"
    #print "FCB:", fcb.encode("hex")
    return fcb

class TestEncryptCBC(ut.TestCase): 
    key = '\x42'*16
    data = '\x62'*32
    IV = '\x90'*16
    def test_full(self):
        self.assertEqual(decrypt_cbc(self.key, encrypt_cbc(self.key, self.data, self.IV), self.IV)[:len(self.data)], self.data)
    def test_given(self):
        with open("10.txt", "r+") as fd:
            data = fd.read().decode("base-64")
            print decrypt_cbc("YELLOW SUBMARINE", data, "\x00"*16)
            

if __name__ == '__main__':
    ut.main()
