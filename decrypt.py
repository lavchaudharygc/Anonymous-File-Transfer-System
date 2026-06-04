import base64
from Crypto.Cipher import AES

key_b64 = input("Enter key: ")
filename = input("Encrypted file: ")

key = base64.b64decode(key_b64)

with open(filename, "rb") as f:
    data = f.read()

iv = data[:12]
ciphertext = data[12:]

cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
plaintext = cipher.decrypt(ciphertext)

with open("decrypted_output", "wb") as f:
    f.write(plaintext)

print("Decryption done")
