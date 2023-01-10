from Crypto.Util import number
from Crypto.Random import random
from math import floor, ceil, sqrt
import hashlib
from functools import reduce

num_part = 4
time_stamps = 5


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
        if sum(s) % (p-1) == 0:
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
            randoms.append(random.randrange(1, p))
        if sum(randoms) % (2*p) == 0:
            break
        else:
            randoms = []
    for i in range(n):
        data = random.randrange(1, p)
        values.append(data)
        input.append((data + randoms[i]) % p)
    print(f'Values: {values}')
    return values, input

def hash_func(x, p, q):
    m = hashlib.sha256()
    m.update(b'{x}')
    res = m.hexdigest()
    num = int(res, base=16) % p
    #num = int(res, base=16)
    #num = (num ^ 2) % q
    return num


# Encryption of one participant
def noisy_enc(param, ski, t, data, q, p):
    c = ((param**data) * hash_func(t, p, q)**ski) % p
    return c


def aggr_dec(param, sk0, t, c, q, p):
    prod = 1
    for values in c:
        prod *= values
    v = ((hash_func(t, p, q)**sk0) * prod) % p
    decr_sum = bsgs(param, v, p)
    return decr_sum, v


def bsgs(gen, h, p):
    result = []
    m = ceil(sqrt(p))
    precomp_pair = {pow(gen, i, p): i for i in range(m)}
    #print(f'V is {h} Table is {precomp_pair}')
    c = pow(gen, m * (p-2), p)
    for j in range(m):
        y = (h * pow(c, j, p)) % p
        if y in precomp_pair:
            result.append(j * m + precomp_pair[y])
            #return j * m + precomp_pair[y]
    return result
    return None


secrets = []
generator, secrets, q, p = setup()
print(f'Generator {generator}')
print(f'Random secrets {secrets}')
print(f'Prime number q {q}')
print(f'Prime number p {p}')
print(f'Check {sum(secrets)%(p-1)}')

prod = 1
for elem in secrets:
    prod = (prod * (hash_func(8, p, q)**elem)) % p
print(f'Prod {prod}')

# Create numbers for multiple timestamps
for t in range(time_stamps):
    data, input = input_generator(p, num_part)
    result = sum(data)
    print(f'Timestamp {t+1}: Random input {input}')
    print(f'Timestamp {t+1}: Expected result {result} or {result % p}')

    ciphertexts = []
    for i in range(num_part):
        ciphertexts.append(noisy_enc(param=generator, ski=secrets[i+1], t=1500, data=input[i], q=q, p=p))

    print(f"Timestamp {t+1}: Encrypted value {ciphertexts}")
    res, v_value = aggr_dec(param=generator, sk0=secrets[0], t=1500, c=ciphertexts, q=q, p=p)
    print(f'Timestamp {t+1}: Check V value: {(generator**(sum(input)))%p == v_value}')
    print(f'Timestamp {t+1}: Result {res}')
