import unittest
from protocol import setup


class TestProtocol(unittest.TestCase):

    def setUp(self):
        self.generator, self.secrets, self.q, self.p = setup()

    # Check if the sum of the secret keys is 0 modulo p
    def test_sk(self):
        self.assertEqual(0, sum(self.secrets) % self.p)


if __name__ == '__main__':
    unittest.main()
