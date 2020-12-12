import numpy as np
import copy
import sage.all
from sage.crypto.sbox import SBox

def newLAT(oldLAT,n):
    len = 2**n
    nLAT=copy.copy(oldLAT)
    for i in range(0,len):
        for j in range(0,len):
            nLAT[i,j]=(2*oldLAT[i,j]) ** 2
    return nLAT

n=4
# file = open('1','r')
# g=file.read().splitlines()
# file.close()
# for i in range(0,len(g)):
#     g[i]=int(g[i],2)
# print('function =')
# print(g)
g=[13,10,8,5,7,1,2,11,0,4,12,6,3,14,15,9]
s=SBox(g)
lat = s.linear_approximation_table()
ddt = s.difference_distribution_table()
# print('LAT =')
# print(lat)
# print(lat[][])
nLAT = newLAT(lat,n)

# # print('LAT mini=')
# mini = []
# for i in range(0,n):
#     a = 1 << i
#     mini.append(lat[a])
# # print(mini)
# if len(mini) == len(set(mini)):
print('function =')
print(g)
flag_ddt = False
flag_lat = False
print(len(set(nLAT.columns())))
for i in set(nLAT.columns()):
    print(i)
if nLAT.ncols() == len(set(nLAT.columns())):
    print("В LAT нет повторяющихся столбцов")
else:
    print("В LAT есть повторяющиеся столбцы")
    flag_lat = True


if ddt.nrows() == len(set(ddt.rows())):
    print("В DDT нет повторяющихся строк")
else:
    print("В DDT есть повторяющиеся строки")
    flag_ddt = True

if flag_ddt != flag_lat:
    print("LAT =")
    print(nLAT)
    print("DDT =")
    print(ddt)




# print('LAT =')
# for i in range(0,n):
#     a = 1 << i
#     print(lat[a])

# print('f=')
# print(s)
#
# print('DDT=')
# print(ddt)
