# Compute given matrix/png image into a bar chart
from paillier import Paillier
import matplotlib.pyplot as plt

class Histo(object):

    def __init__(self, ref_points, matrix):
        super().__init__()
        self.system = Paillier()

        self.ref = ref_points
        self.freq = [0 for _d in range(len(self.ref))]
        
        self.mtx = matrix
        self.ilen = len(matrix)
        self.jlen = len(matrix[0])
        self.size = self.ilen * self.jlen
        
        # self.r_mtx = [[self.system.gen_r() for _j in range(self.jlen)] for _i in range(self.ilen)]
    
    def arg_min(self, i, j):
        r = self.r_mtx[i][j]
        c = self.system.enc(self.mtx[i][j], r)
        index = None
        val = None
        for i, t in enumerate(self.ref):
            aux_val = c / self.system.enc(t, r)
            if val == None or aux_val <= val:
                index = i
                val = aux_val
        return index

    def compute_freq(self):
        for i in range(self.ilen):
            for j in range(self.jlen):
                self.freq[self.arg_min(i, j)] += 1/self.size

    def plot(self):
        plt.bar(self.ref, self.freq)
        plt.show()

    def plot_unsecure(self):
        freq = [0 for _d in range(len(self.ref))]
        for i in range(self.ilen):
            for j in range(self.jlen):
                c = self.mtx[i][j]
                index = None
                val = None
                for i, t in enumerate(self.ref):
                    aux_val = abs(c - t)
                    if val == None or aux_val <= val:
                        index = i
                        val = aux_val
                freq[index] += 1/self.size
        print(freq)
        plt.bar(self.ref, height=freq, width=10)
        plt.show()