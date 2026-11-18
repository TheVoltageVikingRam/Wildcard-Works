#include <stdio.h>

int sumOfDigits(int given_num);
int num;
int sum_of_digits;
int digit_sum;

int main(void){

	scanf("%d", &num);
	sum_of_digits = sumOfDigits(num);
	printf("%d", sum_of_digits);

}

int sumOfDigits(int given_num){
	if (given_num == 0){
	    return 0;
	}
	else {
	digit_sum = (given_num % 10) + sumOfDigits((given_num/10));
	return digit_sum;
}
}
