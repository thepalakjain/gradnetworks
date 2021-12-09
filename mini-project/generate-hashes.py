from string import ascii_lowercase
import hashlib
from itertools import product
import random

hashlist = []
strings = [''.join(i) for i in list(product(ascii_lowercase,repeat=5))]

for i in range(15):
	p = random.choice(strings)
	hashlist.append(hashlib.md5(p.encode()).hexdigest())

print(str(hashlist))