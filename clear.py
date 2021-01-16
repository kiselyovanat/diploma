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

def get_vec(number,n):
    l = len(bin(number))
    bin_number = bin(number)[2:l]
    vec = [0]*n
    j = n-1
    for i in bin_number:
        vec[n-len(bin_number)-j-1] = int(i)
        j -=1
    return vec

def get_DDT_ai_xi(f,DDT_g,x):
    n = f.input_size()
    ncols = 1 << n
    similiars = []
    A = Matrix(ZZ, ncols, ncols)

    for j in range(n):
        ei = 1 << j
        bi = []
        for xi in x:
            fi = f(xi)
            b = fi^f(xi^ei)
            A[ei, b] +=1
            bi.append(b)
        part = find_similiar_rows_bi(DDT_g,bi,n)
        similiars.append(part)
    similiars_final = del_copy(similiars)
    return(A,similiars_final)

def find_similiar_rows_bi(DDT_g,b,n):
    similiars = []
    for j in range(n):
        ej = 1 << j
        q = 0
        for bi in b:
            if DDT_g[ej,bi]:
                q += 1
        if q == len(b):
            similiars.append(ej)
    return(similiars)

def del_copy(similiars):
    # print("hi!")
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

def get_permutation1(g,n):
    A = Matrix(mat(n))
    f = [0]*(2**n)
    # c = 0
    for i in range(2**n):
        x = i #^ c
        bin_x = get_vec(x,n)
        vec = vector(bin_x)
        new_vec = A*vec
        stri = ''
        for j in new_vec:
            stri+=str(j)
        new_x=int(stri,2)
        f[i] = g[new_x]
    return(f)


n=3
# file = open('1','r')
# g=file.read().splitlines()
# file.close()
# for i in range(0,len(g)):
#     g[i]=int(g[i],2)

f = SBox(get_permutation1(g,n))
print(f)
# g = SBox(g)
# ddt_g = difference_distribution_table(g)
# x = [5]
# ddt_f_part_x,similiars = get_DDT_ai_xi(f,ddt_g,x)
# print(similiars)



# ddt_g_part= get_DDT_ai(g)
# print('DDT_ai=')
# print(ddt_g_part)
