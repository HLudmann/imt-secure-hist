# Compute given matrix/png image into a bar chart
from gmpy2 import invert, mpz, mul
from src.paillier import Paillier
from tqdm import tqdm
import matplotlib.pyplot as plt

class Histo(object):

    def __init__(self, ref_points, matrix):
        super().__init__()
        self.system = Paillier()
        self.ref = ref_points
        self.freq = [0] * len(self.ref)
        self.mtx = matrix
        self.ilen = len(matrix)
        self.jlen = len(matrix[0])
        self.size = self.ilen * self.jlen
    
    def arg_min(self, px):
        r = self.system.gen_rdm()
        c = self.system.encrypt(mpz(px), r)
        index = None
        mini = None
        for i, t in enumerate(self.ref):
            val0 = mul(c, self.system.encrypt(-t, invert(r, self.system.n2))) % self.system.n2
            valn2 = self.system.n2 - val0
            val = min(val0, valn2)
            
            if mini == None or val <= mini:
                index = i
                mini = val
        return index

    def compute_freq(self):
        for i in tqdm(range(self.ilen)):
            for j in range(self.jlen):
                self.freq[self.arg_min(self.mtx[i][j])]+=1/self.size
        

    def plot_secure(self):
        print(self.ref)
        self.compute_freq()
        print(self.freq)
        plt.bar(self.ref, height=self.freq, width=10)
        plt.xticks(self.ref, self.ref)
        plt.xlabel("Reference pixels")
        plt.ylabel("Frequences")
        plt.title("Pixels Repartition (w/ encryption)")
        plt.show()

    def plot_unsecure(self):
        print(self.ref)
        freq = [0] * len(self.ref)
        for i in tqdm(range(self.ilen)):
            for j in range(self.jlen):
                c = self.mtx[i][j]
                index = None
                mini = None
                for idx, t in enumerate(self.ref):
                    val = abs(c - t)
                    if mini == None or val <= mini:
                        index = idx
                        mini = val
                freq[index] += 1/self.size
        print(freq)
        plt.bar(self.ref, height=freq, width=10)
        plt.xticks(self.ref, self.ref)
        plt.xlabel("Reference pixels")
        plt.ylabel("Frequences")
        plt.title("Pixels Repartition (w/ encryption)")
        plt.show()