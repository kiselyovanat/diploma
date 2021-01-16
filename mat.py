import numpy as np
import random
import sage.all
from sage.matrix.constructor import Matrix

def get_vec(number,n):
    l = len(bin(number))
    bin_number = bin(number)[2:l]
    vec = [0]*n
    j = n-1
    for i in bin_number:
        vec[n-len(bin_number)-j-1] = int(i)
        j -=1
    return vec

def mat(n):
    matr = []
    for i in range(n):
        a = 1 << i
        row = get_vec(a,n)
        matr.append(row)
    random.shuffle(matr)
    return(matr)
n = int(input())
print(mat(n))
