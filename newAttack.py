import random
import sage.all
from sage.matrix.constructor import Matrix
from sage.rings.integer_ring import ZZ
from sage.crypto.sbox import SBox
from sage.modules.free_module_element import vector

def difference_distribution_table(g):
    m = g.input_size()
    n = g.output_size()

    nrows = 1<<m
    ncols = 1<<n

    A = Matrix(ZZ, nrows, ncols)

    for i in range(nrows):
        si = g(i)
        for di in range(nrows):
            A[ di , si^g(i^di)] += 1

    return A

def get_DDT_ai_yi(f1,DDT_g,y):
    n = f1.input_size()
    ncols = 1 << n
    similiars = []
    A = Matrix(ZZ, ncols, ncols)

    for j in range(n):
        ei = 1 << j
        ai = []
        for yi in y:
            f1i = f1(yi)
            a = f1i^f1(yi^ei)
            ai.append(a)
        part = find_similiar_cols_ai(DDT_g,ai,n)
        similiars.append(part)
    similiars_final = del_copy(similiars)
    similiars_final.reverse()
    return(similiars_final)

def find_similiar_cols_ai(DDT_g,a,n):
    similiars = []
    for j in range(n):
        ej = 1 << j
        l = 0
        while l < len(a) and DDT_g[a[l],ej]:
            l+= 1
        if l == len(a):
            similiars.append(ej)
    return(similiars)

def get_vec(number,n):
    l = len(bin(number))
    bin_number = bin(number)[2:l]
    vec = [0]*n
    j = n-1
    for i in bin_number:
        vec[n-len(bin_number)-j-1] = int(i)
        j -=1
    return vec

def del_copy(similiars):
    for i in similiars:
        if len(i) == 1:
            for j in similiars:
                if (i[0] in j) & (i != j):
                    j.remove(i[0])
                    if len(j)==1:
                        similiars = del_copy(similiars)
    return(similiars)

def mat(n):
    matr = []
    for i in range(n):
        a = 1 << i
        row = get_vec(a,n)
        matr.append(row)
    random.shuffle(matr)
    return(matr)


def get_permutation2(g,n):
    B = Matrix([[0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0]])
    #B = Matrix(mat(n))
    #print(B)
    # d = 4
    f = [0]*(2**n)
    for i in range(2**n):
        x = g[i]# ^ d
        bin_x = get_vec(x,n)
        vec = vector(bin_x)
        new_vec = B*vec
        stri = ''
        for j in new_vec:
            stri+=str(j)
        new_x=int(stri,2)
        f[i] = new_x
    # print('B =')
    # print(B)
    # print(c)
    return(f)

def get_reverse_f(f):
    f1=[0]*len(f)
    for i in range(len(f)):
        f1[i]=f.index(i)
    return f1


#
n=7
file = open('1','r')
g=file.read().splitlines()
file.close()
for i in range(0,len(g)):
    g[i]=int(g[i],2)
# g = [3,7,5,6,2,0,4,1]
# f = [7,6,2,4,5,1,0,3]
# g= [0, 3, 6, 1, 4, 13, 2, 7, 8, 9, 10, 11, 12, 5, 15, 14]
f = get_permutation2(g,n)
f1 = get_reverse_f(f)
# g = [11, 5, 9, 6, 12, 14, 10, 13, 7, 4, 1, 0, 3, 2, 15, 8]
# f = SBox([0,7,6,5,4,3,1,2])
f = SBox(f)
g = SBox(g)
f1 = SBox(f1)
ddt_g = difference_distribution_table(g)
# ddt_f = difference_distribution_table(f)
# ddt_f1 = difference_distribution_table(f1)


print("g = " + str(g))
# print('DDT_g=')
# print(ddt_g)
print("f = " + str(f))
# print('DDT_f=')
# print(ddt_f)
# print("f1 = " + str(f1))
# print('DDT_f1=')
# print(ddt_f1)

y = [8,32,59,123]
similiars = get_DDT_ai_yi(f1,ddt_g,y)
print(similiars)
print("-------")
