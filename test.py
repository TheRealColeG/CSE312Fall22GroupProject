import random
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
chars = []
for i in range(16):
    chars.append(random.choice(ALPHABET))
ret_val = ""
for char in chars:
    ret_val = ret_val + char
print(ret_val)
