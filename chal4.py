import mc_crypto

data = [line.rstrip('\n') for line in open('./4.txt')]

scores = []
for line in data:
    scores.append(mc_crypto.char_freq_hex(line))
scores.sort(key=lambda x: x[1])
for sc in scores[:10]:
    print sc[1], ": ", sc[0]
