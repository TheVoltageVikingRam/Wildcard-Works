#include <stdio.h>

int main() {


	int a = 42;
	double d = 58.394;
	char c = 'r';
//	short s = 12;

	int * addressOfA = &a;
	printf("address of A is: %p\n", addressOfA);
	double * addressOfD = &d;
	printf("address of D is: %p\n", addressOfD);
	char * addressOfC = &c;
	printf("address of C is: %p\n", addressOfC);
//	short * addressOfS = &s;
//	printf("address of S is: %p\n", addressOfS);


	return 0;


}
