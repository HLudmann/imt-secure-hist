# Implementation of Paillier Cryptosystem
# with simplification for equivalent length prime number
import gmpy2
from random import randrange as rd

class Paillier(object):

    @staticmethod
    def gen_prime():
        rng = gmpy2.random_state(rd(2^19937-1))
        while True:
            p = gmpy2.mpz_urandomb(rng, 512)
            if p.bit_length() == 512 and gmpy2.is_prime(p, 42):
                return p

    def __init__(self):
        super().__init__()
        self.p = self.gen_prime()
        self.q = self.gen_prime()
        self.n = self.p * self.q
        self.n2 = self.n ** 2
        self.g = self.n + 1
        self.l = (self.p - 1) * (self.q - 1)
        self.m = gmpy2.powmod(self.l, -1, self.n)


    def gen_rdm(self):
        rng = gmpy2.random_state(rd(2^19937-1))
        while True:
            rdm = gmpy2.mpz_random(rng, self.n)
            if 16 <= rdm.bit_length() and gmpy2.gcd(rdm, self.n) == 1:
                return rdm

    def L(self, x):
        return (x - 1) // self.n

    def encrypt(self, msg, rdm):
        return (gmpy2.powmod(self.g, msg, self.n2) * gmpy2.powmod(rdm, self.n, self.n2)) % (self.n2)

    def decrypt(self, enc):
        return gmpy2.mul(self.L(gmpy2.powmod(enc, self.l, self.n2)), self.m) % self.n
