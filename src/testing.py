import unittest
from protocol import setup, input_generator, hash_func, aggr_dec, noisy_enc

time_stamps = 1
num_part = 3


class TestProtocol(unittest.TestCase):

    def setUp(self):
        self.generator, self.secrets, self.q, self.p = setup()

    # Check if the sum of the secret keys is 0 modulo p
    def test_sk(self):
        self.assertEqual(0, sum(self.secrets) % self.p)
    
     # Check if the product of the hashes raised to the secret keys is 1
    def test_product(self):
        prod = 1
        for elem in self.secrets:
            prod = (prod * (hash_func(8, self.p, self.q, self.generator)**elem)) % self.q
        self.assertEqual(1, prod)

    # Check if the result obtained is equal to the expected result
    def test_result(self):
        for t in range(time_stamps):
            data, input = input_generator(self.p, num_part)
            result = sum(data)
            ciphertexts = []
            for i in range(num_part):
                ciphertexts.append(noisy_enc(param=self.generator, ski=self.secrets[i+1], t=1500, data=input[i],
                                             q=self.q, p=self.p))
            res, v_value = aggr_dec(param=self.generator, sk0=self.secrets[0], t=1500, c=ciphertexts,
                                    q=self.q, p=self.p)
            self.assertEqual(result, res)

    # Check the discrete log 
    def test_dlog(self):
        for t in range(time_stamps):
            data, input = input_generator(self.p, num_part)
            ciphertexts = []
            for i in range(num_part):
                ciphertexts.append(noisy_enc(param=self.generator, ski=self.secrets[i+1], t=1500, data=input[i],
                                             q=self.q, p=self.p))
            res, v_value = aggr_dec(param=self.generator, sk0=self.secrets[0], t=1500, c=ciphertexts,
                                    q=self.q, p=self.p)
            self.assertEqual(v_value, pow(self.generator, sum(input), self.q))

if __name__ == '__main__':
    unittest.main()
