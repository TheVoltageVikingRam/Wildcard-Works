#include <stdio.h>
// 5! = 1*2*3*4*5

int main(void){
	int n,  i;
	long double facto;
	printf("NOTE: Please keep in mind it can only print upto the factorial of 1754.\n");
	printf("Please enter a positive integer: ");

	scanf("%d", &n);
	facto = 1;

	for(i=1; i<=n; i++){

	facto = i*facto;

	}


	if (n<0) {
		printf("%d is negative! Aborting....\n",  n);

	}

	else  {

		printf("%d! = %Lf.\n", n, facto);

	}

	return 0;
}










