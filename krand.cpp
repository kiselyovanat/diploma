#include <iostream>
#include <iterator>
#include <ctime>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <cstdlib>
#include <time.h>
#include <fstream>

using namespace std;


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

int weight_i(unsigned int x){
  int w = 0;
  while(x != 0){
    x = x & (x - 1);
    w++;
  }
return w;
}


bool test_i(unsigned int *f, int i, int n){
  int msk = 1 << n;
  int d = (1 << n)-1; // 1...1 (n штук)
  int mask = 1 << i;
  int dis = 0;
  for (int j = 0; j < msk; ++j)
  {
    if (f[j] & mask)
    //cout << "j =" << j << endl;
    { dis |=j;
    }
  }
  if(dis == d)return 1;
  else return 0;
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

bool test(unsigned int *f, int n){
	//f - mobius
  for (int i = 0; i < n; ++i)
  {
    if (test_i(f, i, n) == 0) return 0;
  }
return 1;
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



int	obrat(unsigned int *F,unsigned int *F1, int n){
	int msk = 1 << n;
	for (int i = 0; i < msk; ++i)
	{
		F1[F[i]] = i;
	}
}


//стартуем с тождественной подстановки,
int krand(unsigned int *F, int n){

int mask = (1 << n)-1;
int msk = 1 << n;
unsigned int a;
unsigned int b;

//F -тождественная подстановка 
for (int i = 0; i < msk; ++i)
{
	F[i] = i;
}

//k
for (int i = mask; i > 1; --i) //n-1
{
	int k = rand()%i;
	//F[i] swap F[j]
	unsigned int buff = F[k];
			F[k] = F[i];
			F[i] = buff;
}


return 0;
}


int main()
{
srand(time(NULL));
unsigned int *f;
unsigned int *g;
unsigned int *g1;
int* a;
int n;

char file_name[6];
cout << "Введите имя файла: ";
cin >> file_name;
cout << "Введите количество переменных: " << std::endl;
cin >> n;
f = new unsigned int [1 << n];
g = new unsigned int [1 << n];
g1 = new unsigned int [1 << n];
a = new int [n];
int msk = 1 << n;

krand(f, n);
//cout << "krand: " << std::endl;
//outFunc(f, n);
cout << std::endl;


ofstream fout(file_name);
outFunc(f, n, fout);
fout.close();
}
