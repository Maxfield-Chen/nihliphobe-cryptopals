from Crypto.Cipher import AES

key = "YELLOW SUBMARINE"
data = (open("7.txt").read()).decode("base64")
IV = "\x00" * 16
mode = AES.MODE_ECB

crypt = AES.new(key, mode, IV=IV)
print crypt.decrypt(data)
