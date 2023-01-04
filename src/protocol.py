from Crypto.Util import number
from Crypto.Random import random
from math import floor
import hashlib


def setup():
    N = 64  # Set to 64 just for faster testing (in real scenario use 1028 or 2048)
    while True:
        p = number.getPrime(N=N)
        print(p)
        q = 2*p+1
        print(q)
        if number.isPrime(q):
            break
    generator = ((random.randrange(floor(q/2))) ^ 2) % q
    print(f'Generator: {generator}')
    return q


def hash_func(x, q):
    m = hashlib.sha256()
    m.update(b'{x}')
    res = m.hexdigest()
    num = int(res, base=16) % (floor(q/2))
    num = num ^ 2 % q
    return num


q = setup()
hash_func(996, q)
