// Fibonacci numbers : 0,1,1,2,3,5,8,13,21,34,55,...




#include <stdio.h>

long double fibonacci(int);

int main(void) {
	int N;
	long double fib;
	printf("Which fibnacci number would you like: ");
	if ( scanf("%d", &N) !=1 ){
		fprintf(stderr, "Error: Invalid input. Please enter an integer.\n");
		return 1;
	}



	if (N<=0) {
	printf("%d number is not positive. Aborting!\n", N);

	}
	else {
		fib = fibonacci(N);
		printf("The %dth Fibonacci number is %Lf.\n", N, fib);

	}


	return 0;
}


long double fibonacci(int n) {
	if (n==1) {

	return 0;
	}
	else if (n==2) {
	return 1;

	}
	else {

	return  ( fibonacci(n-1) + fibonacci(n-2) );
	}


}



