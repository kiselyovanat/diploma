import random
import sage.all
from sage.matrix.constructor import Matrix
from sage.rings.integer_ring import ZZ
from sage.crypto.sbox import SBox
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

def get_DDT_ai_xi(f,DDT_g,x):
    print('----')
    print(DDT_g)
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
    #     print('----')
    #     print(A)
    # print("before:")
    # print(similiars)
    similiars_final = del_copy(similiars)
    return(A,similiars_final)

def find_similiar_rows_bi(DDT_g,b,n):
    similiars = []
    for j in range(n):
        ej = 1 << j
        l = 0
        while l < len(b) and DDT_g[ej,b[l]]:
        # for bi in b:
        #     if DDT_g[ej,bi]:
            l+= 1
        if l == len(b):
            p = 1 << n-1-j
            similiars.append(p)
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


def get_permutation1(g,n):
    '''
    f=g(A(x+c))
    A =
    001
    100
    010
    c = 101
    '''
    A = Matrix([[0,0,1],[1,0,0],[0,1,0]])
    c = 5
    f = [0]*(2**n)
    for i in range(2**n):
        x = i ^ c
        bin_x = get_vec(x,n)
        vec = vector(bin_x)
        new_vec = A*vec
        stri = ''
        for j in new_vec:
            stri+=str(j)
        new_x=int(stri,2)
        f[i] = g[new_x]
    print('A =')
    print(A)
    # print(c)
    return(f)

#
n=3
file = open('1','r')
g=file.read().splitlines()
file.close()
for i in range(0,len(g)):
    g[i]=int(g[i],2)
# g = [3,7,5,6,2,0,4,1]
# f = [7,6,2,4,5,1,0,3]
# g= [0, 3, 6, 1, 4, 13, 2, 7, 8, 9, 10, 11, 12, 5, 15, 14]
g = [3,2,7,5,4,1,0,6]
f = get_permutation1(g,n)
# g = [11, 5, 9, 6, 12, 14, 10, 13, 7, 4, 1, 0, 3, 2, 15, 8]
# f = SBox([0,7,6,5,4,3,1,2])

f = SBox(f)
g = SBox(g)
ddt_g = g.difference_distribution_table()
# ddt_f = f.difference_distribution_table()
print("g = " + str(g))
print('DDT_g=')
print(ddt_g)
print("f = " + str(f))
print('DDT_f=')
print(ddt_f)


# unic(ddt_f)
#
#
# # for i in range(2**n):
x = [5]
ddt_f_part_x,similiars = get_DDT_ai_xi(f,ddt_g,x)
# print('x = ' + str(x))
# # print(ddt_f_part_x)
# # # print("after:")
print(similiars)
print("-------")



# ddt_g_part= get_DDT_ai(g)
# print('DDT_ai=')
# print(ddt_g_part)
