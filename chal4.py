import mc_crypto

data = "CLGSJULHJQKELK:UHWFOHTH"
data = data.encode("hex")
print data

data1 = "ELK: U HWFO HTH"

scores = mc_crypto.char_freq_hex(data)
for score in scores:
    print score
