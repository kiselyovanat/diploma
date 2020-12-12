import numpy as np
import copy
import sage.all
from sage.crypto.sbox import SBox
n=3
g=[7, 4, 0, 1, 6, 3, 5, 2]
s=SBox(g)

lat = s.linear_approximation_table()
ddt = s.difference_distribution_table()

print('function =')
print(g)

print('DDT=')
print(ddt)
