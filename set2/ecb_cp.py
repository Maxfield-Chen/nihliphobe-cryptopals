import mccrypto as mc

def parse_kv(data): 
    data = data.split("&")
    pairs = {}
    for i in xrange(len(data)):
        kp = data[i].split("=")
        key = kp[0]
        val = kp[1]
        pairs[key] = val
    return pairs

key = mc.srand(16)
poison = mc.pkcs7("role=admin", 16)
email = "email=aaaaaaaaaa"
system =  "&uid=0&role=user"
system1 = "&uid=1&role=user"
user = email + poison + system
enc_user = mc.encrypt_ecb(key, mc.pkcs7(user, 16))
treasure = enc_user[16:32]
admin = email + "A"*(16-7) + system1
e_admin = mc.encrypt_ecb(key, mc.pkcs7(admin, 16))
e_admin = e_admin[:32] + treasure

treasure_admin = mc.decrypt_ecb(key, e_admin)
print treasure_admin
