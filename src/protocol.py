from Crypto.Util import number
from Crypto.Random import random
from math import ceil, sqrt
import hashlib

num_part = 3
time_stamps = 1

# Create the cyclic group, generator and the secret keys
# Return the generator, secret keys and two prime number used to define the group
def setup():
    n = 16  # Set to 16 just for faster testing (can be used higher values)
    while True:
        p = number.getPrime(N=n)
        # print(p)
        q = 2*p+1
        # print(q)
        if number.isPrime(q):
            break
    generator = (random.randrange(1, p+1)**2) % q
    # print(f'Generator: {generator}')
    s = []
    while True:
        for i in range(num_part+1):
            s.append(random.randrange(p))
        # print(f'Secret random {s}')
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
            randoms.append(random.randrange(1, p))
        if sum(randoms) % p == 0:
            break
        else:
            randoms = []
    while True:
        for i in range(n):
            values.append(random.randrange(1, p))
        if sum(values) <= p:
            break
        else:
            values = []
    for i in range(n):
        input.append((values[i] + randoms[i]) % p)
    #print(f'Values: {values}')
    return values, input

# Hash function that takes an integer as input and output an element of the cyclic group acting as random oracle
def hash_func(x, p, q, gen):
    m = hashlib.sha256()
    m.update(b'{x}')
    res = m.hexdigest()
    num = int(res, base=16) % p
    num = (gen**num) % q
    return num

# Encryption of one user's data
def noisy_enc(param, ski, t, data, q, p):
    c = ((param**data) * (hash_func(t, p, q, param)**ski)) % q
    return c

# Decryption function that takes all the users ciphertexts and output the decrypted sum of the randomized input
def aggr_dec(param, sk0, t, c, q, p):
    prod = 1
    for values in c:
        prod *= values
    v = ((hash_func(t, p, q, param)**sk0) * prod) % q
    decr_sum = bsgs(param, v, p, q)
    return decr_sum, v

# Implementation of the Baby step Giant step algorithm to solve discrete log problem
# For discrete log equation V = g^(x) output the value of x
def bsgs(gen, h, p, q):
    result = []
    m = ceil(sqrt(p))
    precomp_pair = {pow(gen, i, q): i for i in range(m)}
    c = pow(gen, m * (q-2), q)
    for j in range(m):
        y = (h * pow(c, j, q)) % q
        if y in precomp_pair:
            #result.append(j * m + precomp_pair[y])
            return j * m + precomp_pair[y]
    #return result
    return None


#secrets = []
#generator, secrets, q, p = setup()
#print(f'Generator {generator}')
#print(f'Random secrets {secrets}')
#print(f'Prime number q {q}')
#print(f'Prime number p {p}')
#print(f'Check {sum(secrets)%p}')
#
#prod = 1
#for elem in secrets:
#    prod = (prod * (hash_func(8, p, q, generator)**elem)) % q
#print(f'Prod {prod}')
#
## Create numbers for multiple timestamps
#for t in range(time_stamps):
#    data, input = input_generator(p, num_part)
#    result = sum(data)
#    print(f'Timestamp {t+1}: Random input {input}')
#    print(f'Timestamp {t+1}: Expected result {result}')
#
#    ciphertexts = []
#    for i in range(num_part):
#        ciphertexts.append(noisy_enc(param=generator, ski=secrets[i+1], t=1500, data=input[i], q=q, p=p))
#
#    print(f"Timestamp {t+1}: Encrypted value {ciphertexts}")
#    res, v_value = aggr_dec(param=generator, sk0=secrets[0], t=1500, c=ciphertexts, q=q, p=p)
#    print(f'Timestamp {t+1}: Check V value: {(generator**(sum(input)))%q == v_value}')
#    print(f'Timestamp {t+1}: Result {res}')
