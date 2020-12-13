import numpy as np
import copy
import sage.all
from sage.matrix.constructor import Matrix
from sage.rings.integer_ring import ZZ
from sage.crypto.sbox import SBox
from itertools import *
from sage.modules.free_module_element import vector

def get_comp_func(s,i):
    func_i = s.component_function(i)
    comp_func=[]
    for j in func_i:
        if j:
            comp_func.append(1)
        else:
            comp_func.append(0)
    return(comp_func)
# def get_DDT_ai(f):
#     n = f.input_size()
#     ncols = 1 << n
#     A = Matrix(ZZ, ncols, ncols)
#     for i in range(ncols):
#         fi = f(i)
#         for j in range(n):
#             ei = 1 << j
#             A[ei, fi^f(i^ei)] +=1
#     return(A)

def get_DDT_ai_x(f,DDT_g,x):
    n = f.input_size()
    ncols = 1 << n
    similiars = []
    A = Matrix(ZZ, ncols, ncols)
    fi = f(x)
    for j in range(n):
        ei = 1 << j
        b = fi^f(x^ei)
        A[ei, b] +=1
        part = find_similiar_rows(DDT_g,b,n)
        similiars.append(part)
    # print(A)
    return(A,similiars)

def find_similiar_rows(DDT_g,b,n):
    similiars = []
    for j in range(n):
        ej = 1 << j
        if DDT_g[ej,b]:
            similiars.append(ej)
    return(similiars)

def get_permutation1(g,n):
    '''
    f=g(A(x+c))
    A =
    001
    100
    010
    c = 101
    '''
    # V = VectorSpace(GF(2),n)
    # A = Matrix([[0,0,1],[1,0,0],[0,1,0]])
    # c = 5
    # for i in range(2**n):
    #     # f[i] = g[]
    #     vec = vector([i^c])
    #     print(A*vec)

    f = [0]*8
    f[0] = g[6]
    f[1] = g[2]
    f[2] = g[7]
    f[3] = g[3]
    f[4] = g[4]
    f[5] = g[0]
    f[6] = g[5]
    f[7] = g[1]
    return(f)
#
n=3
# file = open('1','r')
# g=file.read().splitlines()
# file.close()
# for i in range(0,len(g)):
#     g[i]=int(g[i],2)
# # print('function =')
# # print(g)
g = [3,2,7,5,4,1,0,6]
# f = SBox([0,7,6,5,4,3,1,2])
f = SBox(get_permutation1(g,n))
g = SBox(g)
print("g=")
print(g)
print("f=")
print(f)

ddt_g = g.difference_distribution_table()
ddt_f = f.difference_distribution_table()
# print('DDT_f=')
# print(ddt_f)
print('DDT_g=')
print(ddt_g)
x = 3
ddt_f_part_x,similiars = get_DDT_ai_x(f,ddt_g,x)
print(ddt_f_part_x)
print(similiars)
print("-------")
# print('DDT_ai_x=')
# print(ddt_f_part_x)

# ddt_g_part= get_DDT_ai(g)
# print('DDT_ai=')
# print(ddt_g_part)




# print('function =')
# print(g)
#
