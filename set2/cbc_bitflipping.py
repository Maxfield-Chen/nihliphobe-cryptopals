import mccrypto as mc
from Crypto.Cipher import AES

def get_admin():
   pre = "comment1=cooking%20MCs;userdata="
   post = ";comment2=%20like%20a%20pound%20of%20bacon"
   data = "A"*16
   offer = pre + data + post
   key = mc.srand(16)
   IV = mc.srand(16)
   enc = mc.encrypt_cbc(key, offer, IV) 
   to_flip = mc.xor_equalLen(post[0:16].encode("hex"), enc[32:48].encode("hex")).decode("hex")
   answer = ";admin=true;"
   answer = answer + "A"*(16-len(answer))
   corrupt = ""
   for i in xrange(len(answer)):
       corrupt += chr(ord(to_flip[i]) ^ ord(answer[i]))
   #print mc.xor_equalLen(corrupt.encode("hex"), post[0:16].encode("hex")).decode("hex")
   poison = enc[0:32] + corrupt + enc[48:]
   treasure = mc.decrypt_cbc(key, poison, IV)
   return treasure



treasure =  get_admin()
print treasure, len(treasure)

