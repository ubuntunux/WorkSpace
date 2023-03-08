#include <stdio.h>

int main() {
	int n = 0;
	for(int i=1;i<10000;++i) {
		for(int j=i; j>0; j /= 10) {
			if( j % 10 == 8) {
				n += 1;
			}
		}
	}
	printf("%d", n);
	return 0;
}