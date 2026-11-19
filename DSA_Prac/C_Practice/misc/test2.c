#include <stdio.h>
void doSomething();

int main(){
	int a = 10;
	int b = 11;
	int f = 14;
	int g = 15;
	doSomething();
	
	printf("f : %d\n", f);
	return(0);

}


void doSomething()
{	 	int a = 20;
		int c = 12;
		int d = 13;
		int b = 11;
		int e = a + c;
		c = b + d ;

		printf("c : %d\n", c);
		printf("e : %d\n", e);

	}
