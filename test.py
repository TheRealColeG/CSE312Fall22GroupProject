import numpy as np
import random




def trySalt():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(16):
        chars.append(random.choice(ALPHABET))
    ret_val = ""
    for char in chars:
        ret_val = ret_val + char
    print(ret_val)

def aids(input):
    keys = input.keys()
    ret_val = {}
    for key in keys:
        if key != "_id":
            ret_val[key] = input[key]
    return ret_val

def diceRoll():
	#The list of possible die roll
	support = "123456"
	#Choose two die outcomes. (This ensures rolling a 7 still remains higher probability than a 12)
	firstRoll = int(random.choice(support))
	secondRoll = int(random.choice(support))
	return (firstRoll, secondRoll)

arr = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
print(arr)
arr[10] = "9"
print(arr)
print("Length: "+str(len(arr)))