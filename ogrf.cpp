//вывод в файл
#include <iostream>
#include <iterator>
#include <ctime>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <cstdlib>
#include <time.h>
#include <iomanip>
#include <math.h>
#include <cmath>

#include <fstream>


using namespace std;

//F -векторная функция
//M -множество {0, 1, ..., (2^n)-1}
//n <= 5
//F[i] -значение на наборе i
//if ((M &(1 << i))!=0) -i-й набор выбран, выбранный набор помечаем 1
//a -случайный набор
//b - набор, отличающийся только в i-ой компоненте
//msk = 1 << n -2^n


void green(int *f, int n) {
  int maxstep = 1 << n;
    for (int step = 1; step < maxstep; step <<= 1) {
        int dubstep = step << 1;
        for (int i = 0; i < maxstep; i += dubstep) {
          for (int j = 0; j < step; j++){
                int plus = f[i + j] + f[i + j + step];
                int minus = f[i + j] - f[i + j + step];
                f[i + j] = plus;
                f[i + j + step] = minus;
            }
        }
    }
}


void walsh(unsigned int *f, int n, int *g, int i){
  int msk = 1 << n;
    for (int j = 0; j < msk; j++) {
        if (f[j] & (1 << i))
            g[j] = -1;
         else
            g[j] = 1;

    }
green(g, n);
//for (int j = 0; j < msk; ++j)
//{
 // cout << g[j] << ' ';
//}
//cout << endl;
}



//abs Функция вычисляет абсолютное значение и возвращает модуль значения val (|val|).
int max(int *f, int n) {
  int msk = 1 << n;
  int m = abs(f[0]);
    for (int arg = 1; arg < msk; arg++) {
        if (abs(f[arg]) > m) {
            m = abs(f[arg]);
        }
    }
    return m;
}




int Nf(unsigned int *f, int n, int i){
    int msk = 1 << n;
    int max_el = 0;
    int result;
    int *g = new int [msk];
    walsh(f, n, g, i);
    result = (1 << (n - 1)) - (max(g, n) >> 1);
    return result;
}




int weight_i(unsigned int x){
  int w = 0;
  while(x != 0){
    x = x & (x - 1);
    w++;
  }
return w;
}


int deg_i(unsigned int *f, int n, int i){
  int w;
  int msk = 1 << n;
  int max = 0;
  int mask = 1 << i;
  for (int j = 0; j < msk; ++j)
  {
    if (f[j] & mask)
    {
      w = weight_i(j);
      if (w > max) max = w;
    }


  }
  return max;
}


void mobius(unsigned int *f, int n){
  int msk = 1 << n;
  for (int size = 1; size < msk; size <<= 1)
  {
    //cout << "s= " << size << endl;

    for (int j = 0; j < msk; j += (size << 1))
    {
      //cout << "j= " << j << endl;

      for (int i = j; i < (size + j); i++)
      {
        //cout << "i= " << i << endl;

        f[i + size] ^= f[i];
      }
    }
  }
}


int kolvosperem(unsigned int *f, int i, int n){
  //f - mobius
  int msk = 1 << n;
  int mask = 1 << i;
  int dis = 0;
  for (int j = 0; j < msk; ++j)
  {
    if (f[j] & mask)
    //cout << "j =" << j << endl;
    { dis |=j;
    }
  }
  //cout << "dis =" << dis << endl;
  return weight_i(dis);

}



int* kolvosperemall(unsigned int *f, int n){
  //f - mobius
  int* a = new int [n];
  for (int i = 0; i < n; ++i)
  {
    a[i] =  kolvosperem(f, i, n);
  }
return a;
}

int out2(unsigned int x, int n, ofstream& fout){

  int mask = 1 << (n - 1);
  while (mask){
    if (x & mask) fout << '1';
      else fout << '0';
      mask >>= 1;
  }
  fout << endl;

}

int outFunc(unsigned int *x, int n, ofstream& fout){
  //ofstream fut("ogrf.txt");
  int msk = 1 << n;

  for (int i = 0; i < msk; ++i){
  out2(x[i], n, fout);
  }
  //fut.close();
}



unsigned int * MobiusFunc(unsigned int *f, int n) {
  unsigned int l; //= 1 << n;
  unsigned int a;

  if (n < 5) l = 1;
  else l = 1 << (n-5);
  unsigned int *g = new unsigned int [l];
  for(int i = 0; i < l; i++) {
    a = f[i];
    a = a ^ ((a << 1) & 0xAAAAAAAA);
    a = a ^ ((a << 2) & 0xCCCCCCCC);
    a = a ^ ((a << 4) & 0xF0F0F0F0);
    a = a ^ ((a << 8) & 0xFF00FF00);
    g[i] = a ^ ((a << 16) & 0xFFFF0000);
    }

    if(n < 5) {
      g[0] &= (1 << (1 << n)) - 1;//1<<len
    }

    if (n > 5) {
      for(int k = 1; k < l; k*=2 ) {
        //cout << "k = " << k << endl;
        for(int m = 0; m < l / (2*k); m++) { //len = 1 << n;
          for(int j = 2*k*m; j < 2*k*m+k; j++ ) {
            g[j + k] ^= g[j];

          }
        }
      }
    }

  //cout << "MobiusFunc:" << g;
  return g;
}


//Построение случайной g, существенно зависящей от k переменных
unsigned int * random_k(int k) {
  //cout << "random_k" << endl;
  unsigned int dis;
  unsigned int l = ((1 << k) + 31) >> 5;
  //unsigned int * C = new unsigned int [l];
  unsigned int * D = new unsigned int [l];
  unsigned int * B = new unsigned int [l];
  int s = (k >= 5)? 32: (1 << k);
  do {
    for (int i = 0; i < l; ++i)
    {
      B[i] = rand() - rand();
    }
      //cout << "B:  " << B <<endl;
    if (k < 5) B[0] &= ((1 << s)-1);
    //cout << hex << B[0] <<endl;

    dis = 0;
    for(int i = 0; i < l; i++) {
      for(int j = 0; j < s; j++) {
        if (B[i] & (1 << j)) {
          dis |= ((i << 5) + j);
        }
      }
        //cout << "i:  " << i <<endl;
    }
      //cout << "dis:  " << dis <<endl;

  }
  while(dis != (1 << k) - 1);
  //cout << "C:  " << C <<endl;
  D = MobiusFunc(B, k);
  return D;
}


unsigned int preobr(unsigned short x, int r) {
  unsigned int z = 0, j = 0;
  unsigned short mask = (1 << r) - 1, a;
  while(mask) {
    a = (x & mask) >> j;
    z |= (a << (2*j)) | (a << (2*j + r));
    j += r;
    mask <<= r;
  }
  return z;
}



unsigned int * fict(unsigned int *f, int n, int i) {
  int r, k, b;
  int len = 1<<n;
  int m = (len + 31) >> 5 ;
  int m1 = 2*m;
  //cout << "m: " << m << endl;
  //BoolFunc g(n + 1);
  unsigned int *g = new unsigned int [m1];
  //cout << "g: " << g << endl;
  if(i >= 5) {
    r = 1 << (i - 5);
    for(k = b = 0; b < m1 ; b += 2*r) {
      //cout << "b " << b << endl;
      for(int j = b; j < b + r; j++, k++) {
        g[j] = g[j + r] = f[k];
        //cout << "k: " << k << endl;
      }
    }
    return g;
  }
  //i < 5;
  r = 1 << i;
  for(int j = 0; j < m; j++) {
    g[2*j] = preobr(f[j], r);
    g[2*j + 1] = preobr(f[j] >> 16, r);
  }
  return g;
}

unsigned int * make_g (int k, int n){
  //cout << "make_g" << endl;
  unsigned int *a;// = new unsigned int [((1 << n) +31) >> 5];
  unsigned int *b;// = new unsigned int [((1 << n) +31) >> 5];
  unsigned int *tmp;// = new unsigned int [((1 << n) +31) >> 5];
  a = random_k(k); //g зависит от всех 2^k бит
  //cout << "a" << hex << a[0] << std::endl;
  for (int i = k; i < n; ++i)
  {
    int j = rand()%(i+1); //номер добавл фикт переменной
    b = fict(a, i, j);
    //tmp = a;
    a=b;
    //delete[] tmp;
  }
  //cout << "b[0]";
  //cout << hex << b[0]<< endl;
return b;
}


//стартуем с тождественной подстановки,
//случайно выбираем первый набор -a,
//b- отличается от a в i-ой компоненте
int alg(unsigned int *F, int n){

unsigned int M;
M = 0;

int mask = (1 << n)-1;
int msk = 1 << n;
unsigned int a;
unsigned int b;

//F -тождественная подстановка

for (int i = 0; i < msk; ++i)
{
  F[i] = i;
}
//outFunc(F, n);

//выбираем наборы
for (int i = 0; i < n; ++i)
{
  do
  {
    a = rand() & mask;
    //cout << "a=" << a;
    b = a^(1 << i);
    //cout << "b=" << b;
  } while (((M & (1 << a))!=0) || ((M & (1 << b))!=0));

  //F[i] swap F[j]
  unsigned int buff = F[b];
      F[b] = F[a];
      F[a] = buff;

  M |= 1 << a;
  M |= 1 << b;

}

return 0;
}

int funcn1(unsigned int *F, int n, int k){

int m = 1 << n;
int msk = 2 * m;
int mask = (1 << n)-1;
int leng = ((1 << n)+31) >> 5;
unsigned int* g;
//g = new unsigned int [leng];

for (int i = 0; i < m; ++i)
{
  F[i+m] = F[i];
}

//for (int i = 0; i < leng; ++i)
//{
//  g[i] = rand() - rand();
//}
//cout << "make" << endl;
g = make_g(k-1, n);
//cout << " g[0]" << hex << g[0] << endl;


for (int j = 0; j < m; ++j)
{
  if (g[j >> 5] & (1 << (j%32)))
    F[j] |= (1 << n);
  else
    F[j+m] |= (1 << n);
}
}

unsigned int * create_g(int k, int n){

  unsigned int *F;
  F = new unsigned int [1 << n];
  alg(F,k);
  //cout << "alg: " << std::endl;

  for (int i = k; i < n; ++i)
  {
    funcn1(F,i,k);
  }

  return F;

}




int main()
{

srand(time(NULL));
unsigned int *F;
unsigned int *G;
int n;
int k;
int d;
//int* a;
//a = new int [n];
char file_name[10];
cout << "Введите имя файла: ";
cin >> file_name;

cout << "Введите количество переменных: " << std::endl;
cin >> n;
cout << "Введите k: " << std::endl;
cin >> k;
int msk = 1 << n;
int mask = 2 * msk;
//F = new unsigned int [msk];
//G = new unsigned int[msk];
//unsigned int *H = new unsigned int[msk];
//cout << "G: " << std::endl;



F = create_g(k, n);
ofstream fout(file_name);
outFunc(F, n, fout);
fout.close();




}
