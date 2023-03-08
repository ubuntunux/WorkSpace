// set_difference example
#include <iostream>     // cout
#include <algorithm>    // set_difference, sort
#include <vector>       // vector
#include <cmath>

using namespace std;

int Generator(int n) {
	int sum = n;
	for(int l=log10(n);l>=0;--l) {
		int p = n % 10;
		sum += p;
		n = (int)(n / 10);
	}
	return sum + n;
}

int main () {
  int generator[5000];
  int generated[5000];

  for(int i=0;i<5000;++i){
	  generator[i] = i+1;
	  generated[i] = Generator(i+1);
  }

  int sum = 0;
  for(int i=0;i<5000;++i) {
	  bool bFind = false;
	  for(int j=0;j<5000;++j) {
		  if(generator[i] == generated[j]) {
			  bFind = true;
		  }
	  }
	  if(!bFind) {
		  sum +=generator[i];
		  cout << generator[i] << endl;
	  }
  }
  cout << sum;
  return 0;
}
