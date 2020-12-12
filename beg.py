import numpy as np

def print_bin(matr,n):
    for i in range(0,n):
        print "{0:05b}".format(int(matr[i][0]))

def begunok(A,B,n):
    beg = np.zeros((n,1))
    for j in range (0,n):
        c = 0
        for i in range (0,n):
            if B[j] == A[i]:
                c = c  | (1 << i)
        beg[j] = c
    print_bin(beg,n)
    return beg

def getMatPermut(beg,n):
    matPermut = np.zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            if int(beg[i][0]) & (1<<j):
                matPermut[i][j] = 1
    printMat(matPermut)
    return matPermut

def getPermut(beg,n):
    permut = np.zeros((n,n))
    for j in range(0,n):
        weight = bin(int(beg[j][0])).count('1')
        if weight == 1:
            permut[j][0] = beg[j][0]
        elif weight > 1:
            for i in range(0,weight):
                print 'i='
                print i
                position = n - 1 - "{0:05b}".format(int(beg[j][0])).rfind('1')
                permut[j][i] = 1 << position
                print "{0:05b}".format(int(beg[j][0]))
                print position
                print "{0:05b}".format(int(permut[i][j]))
                print '------'
                beg[j][0] = int(beg[j][0]) ^ int(permut[j][i])
                print "{0:05b}".format(int(beg[j][0]))
                print '******'
            print "done"
    print permut


def printMat(A):
    for i in A:
        print is
n=5
A = [[2,3,4,1,5],[3,2,5,1,4],[2,3,4,1,5],[4,1,2,5,3],[4,1,2,5,3]]
B = [[4,1,2,5,3],[3,2,5,1,4],[4,1,2,5,3],[2,3,4,1,5],[2,3,4,1,5]]
beg = begunok(A,B,n)
printMat(B)
matPermut = getMatPermut(beg,n)
getPermut(beg,n)


# mas = [[0,0,0,0,1],[0,1,0,0,0],[0,0,0,1,0],[1,0,0,0,0],[0,0,1,0,0]]
# C = np.dot(mas, A)
# print Cn

# 11000
# 00010
# 11000
# 00101
# 00101
#
# 10000
# 00010
# 01000
# 00100
# 00001
#
# 10000
# 00010
# 01000
# 00001
# 00100
#
# 01000
# 00010
# 10000
# 00001
# 00100
#
# 01000
# 00010
# 10000
# 00100
# 00001
