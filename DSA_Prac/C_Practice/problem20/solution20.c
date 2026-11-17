#include <stdio.h>

int num_of_int;
int i;
int given_num;
int minimum_num;
int min_num;
int min(int number_given);

int main(void){
    scanf("%d", &num_of_int);
    scanf("%d", &minimum_num);
    for (i=1; i<num_of_int ; i++){
        scanf("%d", &given_num);
        minimum_num = min(given_num);
    }
    
    printf("%d", minimum_num);
    
    return 0;
}



int min(int number_given){
    if (number_given >= minimum_num) {
        min_num = minimum_num;
        
    }
    
    else if (minimum_num > number_given){
        min_num =  number_given;
        
    }
  return min_num;
    
}


