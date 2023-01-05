from Crypto.Util import number
from Crypto.Random import random
from math import floor
import hashlib

num_part = 5

def setup():
    N = 16  # Set to 16 just for faster testing (in real scenario use 1028 or 2048)
    while True:
        p = number.getPrime(N=N)
        # print(p)
        q = 2*p+1
        # print(q)
        if number.isPrime(q):
            break
    generator = ((random.randrange(floor(q/2) + 1)) ^ 2) % q
    # print(f'Generator: {generator}')
    s = []
    while True:
        for i in range(num_part+1):
            s.append(random.randrange(p))
        # print(f'Secret random {s}')
        # print(f'Is zero {sum(s) % p}   {p}')
        if sum(s) % p == 0:
            break
        else:
            s = []
    return generator, s, q


def hash_func(x, q):
    m = hashlib.sha256()
    m.update(b'{x}')
    res = m.hexdigest()
    num = int(res, base=16) % (floor(q/2))
    num = num ^ 2 % q
    return num


s = []
generator, s, q = setup()
print(f'Generator {generator}')
print(f'Random secrets {s}')
print(f'Prime number q {q}')
#hash_func(996, q)
