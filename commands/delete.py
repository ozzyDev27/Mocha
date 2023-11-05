import random
import string
def randomChars():
    ''.join(random.choice(string.ascii_letters) for i in range(3))