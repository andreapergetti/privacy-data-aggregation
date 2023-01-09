from Crypto.Util import number
from Crypto.Random import random
from math import floor, ceil, sqrt
import hashlib
from functools import reduce

num_part = 3


def setup():
    n = 16  # Set to 16 just for faster testing (in real scenario use 1028 or 2048)
    while True:
        p = number.getPrime(N=n)
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
    return generator, s, q, p

# Generate input for a specific timestamp
# Returns a list that contains x_hat (noisy version of data) of the n participants
def input_generator(p, n):
    values = []
    randoms = []
    input = []
    while True:
        for i in range(n):
            randoms.append(random.randrange(p))
        if sum(randoms) % p == 0:
            break
        else:
            randoms = []
    for i in range(n):
        data = random.randrange(p)
        values.append(data)
        input.append((data + randoms[i]) % p)
    return input

def hash_func(x, p, q):
    m = hashlib.sha256()
    m.update(b'{x}')
    res = m.hexdigest()
    num = int(res, base=16) % p
    #num = int(res, base=16)
    num = (num ^ 2) % q
    return num


# Encryption of one participant
def noisy_enc(param, ski, t, data, q, p):
    c = ((param ^ data) * hash_func(t, p, q) ^ ski) % p
    return c


def aggr_dec(param, sk0, t, c, q, p):
    prod = 1
    for values in c:
        prod *= values
    v = ((hash_func(t, p, q) ^ sk0) * prod) % p
    decr_sum = bsgs(param, v, p)
    return decr_sum


def bsgs(gen, h, p):
    m = ceil(sqrt(p-1))
    precomp_pair = {pow(gen, i, p): i for i in range(m)}
    print(f'V is {h} Table is {precomp_pair}')
    c = pow(gen, m * (p-2), p)
    for j in range(m):
        y = (h * pow(c, j, p)) % p
        if y in precomp_pair:
            return j * m + precomp_pair[y]
    return None


secrets = []
generator, secrets, q, p = setup()
input = input_generator(p, num_part)
print(f'Random input {input}')
print(f'Generator {generator}')
print(f'Random secrets {secrets}')
print(f'Prime number q {q}')
print(f'Prime number p {p}')
print(f'Check {sum(secrets)%p}')

prod = 1
for elem in secrets:
    prod = (prod * (hash_func(8, p, q) ^ elem)) % p
print(prod)
#ciphertexts = []
#ciphertexts.append(noisy_enc(param=generator, ski=secrets[1], t=1500, data=657, q=q, p=p))
#ciphertexts.append(noisy_enc(param=generator, ski=secrets[2], t=1500, data=343, q=q, p=p))
#ciphertexts.append(noisy_enc(param=generator, ski=secrets[3], t=1500, data=500, q=q, p=p))
#print(f"Encrypted value {ciphertexts}")
#res = aggr_dec(param=generator, sk0=secrets[0], t=1500, c=ciphertexts, q=q, p=p)
#print(res)
#print(hash_func(996, p, q))
