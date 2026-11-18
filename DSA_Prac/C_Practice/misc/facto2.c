#include <stdio.h>

// Recursion :  one function calls itself
long double factorial(int);


int main(void){

	int n, i;
	long double facto;
	printf("Please enter a positive integer: ");
	scanf("%d", &n);

	if(n<0) {
	printf("%d is negative! Aborting..\n", n);
	}
	else {

	facto = factorial(n); 
	printf("%d! = %Lf.\n", n , facto);

	}
}

long double factorial(int n) {
	long double result;
	if (n==0) {
		result=1;
	}

	else {
	result = n*factorial(n-1);

	}
	return result;
}
