import Encrypt
import KeyExpansion

plaintext = "3243f6a8885a308d313198a2e0370734"
key = "2b7e151628aed2a6abf7158809cf4f3c"
key_words = KeyExpansion.key_expansion(key, 4, 10)
ciphertext = Encrypt.encrypt(plaintext, key_words, 10)

print(ciphertext)