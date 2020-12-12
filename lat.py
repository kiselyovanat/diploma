import numpy as np

comp_y1 = 0b10110100
comp_y2 = 0b11100001
comp_y3 = 0b00111001

comp_x = ['0b01010101', '0b00110011', '0b00001111']

n=3

def weight(vector):
    w = 0
    for ones in vector:
        if ones == '1':
            w += 1
    #print w
    return w

def print_bin(matr):
    for i in matr:
        print bin(i)

def get_y(f):
    y = []
    for j in (1,2,4):
        row = ''
        for i in f:
            row = row + str(int((i & j) != 0))
        y.append(row)
    return y

def get_comp(comp):
    comp_func = []
    for i in range(1,8):

        i_1 = int((i & 0b001) != 0)
        i_2 = int((i & 0b010) != 0)
        i_3 = int((i & 0b100) != 0)
        func = i_1 * int(comp[0],2) ^ i_2 * int(comp[1],2) ^ i_3 * int(comp[2],2)
        comp_func.append(func)
    return comp_func

def lat(a,b):
    lat = np.zeros((7,7))
    for i in range(0,7):
        for j in range(0,7):
            vec = a[i] ^ b[j]
            lat[i][j] = 2**(n-1) - weight(str(bin(vec)))
    return lat


g = [3,2,7,5,4,1,0,6]
comp_g = get_y(g)
a = get_comp(comp_x)
b = get_comp(comp_g)
lat_g = lat(a,b)
print 'LAT_g='
print lat_g
print '----------'

f = [0,7,6,5,4,3,1,2]
comp_f = get_y(f)
print comp_f
print '**********'
b = get_comp(comp_f)
print_bin(b)
lat_f = lat(a,b)
print 'LAT_f='
print lat_f
