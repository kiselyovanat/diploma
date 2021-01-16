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

def difference_distribution_table_rows(g):
    m = g.input_size()
    n = g.output_size()

    nrows = 1<<m
    ncols = 1<<n

    A = Matrix(ZZ, nrows, ncols)

    for i in range(nrows):
        si = g(i)
        for j in range(n):
            ej = 1 << j
            A[ej,si^g(i^ej)] += 1
    return A

def linear_approximation_table_rows(g):
    m = g.input_size()
    n = g.output_size()

    nrows = 1<<m
    ncols = 1<<n
    A = Matrix(ZZ, ncols, nrows, 0)
    for i in range(ncols):
        for j in range(n):
            ej = 1 << j
            A[i,ej]=g.component_function(i).walsh_hadamard_transform()[ej]
    A = A.transpose()/2

    return A

def linear_approximation_table_cols(g):
    m = g.input_size()
    n = g.output_size()

    nrows = 1<<m
    ncols = 1<<n
    A = Matrix(ZZ, ncols, nrows, 0)
    for i in range(n):
        ei = 1 << i
        A[ei] = g.component_function(ei).walsh_hadamard_transform()
    A = A.transpose()/2

    return A

def alg1(LAT_f,LAT_g,n): #3.1.1 from diploma
    P = []
    for i in range(n):
        pi=0
        for j in range(n):
            if LAT_f[1<<i]==LAT_g[1<<j]:
                pi = pi | 1<<n-1-j
            elif LAT_f[1<<i]==-1*LAT_g[1<<j]:
                pi = pi | 1<<n-1-j
        P.append(pi)
    return(P)

def alg2(LAT_f,LAT_g,n): #3.1.2 from diploma
    P = []
    for i in range(n):
        pi=0
        for j in range(n):
            if LAT_g.column(1<<i)==LAT_f.column(1<<j):
                pi = pi | 1<<n-1-j
            elif LAT_g.column(1<<i)==-1*LAT_f.column(1<<j):
                pi = pi | 1<<n-1-j
        P.append(pi)
    return(P)

def alg3(DDT_f,DDT_g,n): #3.2.1 from diploma
    P = []
    for i in range(n):
        pi=0
        for j in range(n):
            if DDT_f[1<<i]==DDT_g[1<<j]:
                pi = pi | 1<<n-1-j
        P.append(pi)
    return(P)


def alg4(DDT_f,DDT_g,n): #3.2.2 from diploma
    P = []
    for i in range(n):
        pi=0
        for j in range(n):
            if DDT_g.column(1<<i)==DDT_f.column(1<<j):
                pi = pi | 1<<n-1-j
        P.append(pi)
    return(P)

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

def get_permutation2(g,n):
    B = Matrix(mat(n))
    f = [0]*(2**n)
    # d = 4
    for i in range(2**n):
        x = g[i] #^ d
        bin_x = get_vec(x,n)
        vec = vector(bin_x)
        new_vec = B*vec
        stri = ''
        for j in new_vec:
            stri+=str(j)
        new_x=int(stri,2)
        f[i] = new_x
    return(f)

n=3
file = open('1','r')
g=file.read().splitlines()
file.close()
for i in range(0,len(g)):
    g[i]=int(g[i],2)
f = SBox(get_permutation1(g,n))
g = SBox(g)

print(g.difference_distribution_table())
print('-----')
lat_g = difference_distribution_table_rows(g)
print(lat_g)

# lat_f = linear_approximation_table(f)
# print(g.linear_approximation_table())
# print('-----')
# lat_g = linear_approximation_table_rows(g)
# print(lat_g)
# print('-----')
# lat_g = linear_approximation_table_cols(g)
# print(lat_g)
# print(alg1(lat_f,lat_g,n))
