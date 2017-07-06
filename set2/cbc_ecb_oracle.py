import mccrypto as mc
import random

def offering(data):
    key = mc.srand(16)
    IV = mc.srand(16)
    pad = random.randint(5,10)
    offer = "A" * pad + data + "A" * pad
    if (random.randint(1,2)) == 1:
        print "CBC"
        return mc.encrypt_cbc(key, offer, IV).encode("hex")
    else:
        print "ECB"
        return mc.encrypt_ecb(key, mc.pkcs7(offer, 16)).encode("hex")

def cm_oracle(offering):
    seen = {}
    blocks = len(offer)/16
    for i in range(blocks):
        cb = offer[16*i:16*(i+1)]
        if seen.get(cb):
            return "ECB"
        else:
            seen[cb] = True
    return "CBC"




for i in xrange(100):
    offer = offering("B"*16*6) 
    print cm_oracle(offer)
    print "---"
    

        
    
