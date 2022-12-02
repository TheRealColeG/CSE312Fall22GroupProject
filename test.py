import random
def getRoll():
    possible = "123456"
    rollOne = int(random.choice(possible))
    rollTwo = int(random.choice(possible))
    return (rollOne, rollTwo)

print(getRoll())