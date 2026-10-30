#include <stdio.h>

int main(void){
    
    int num_to_find;
    scanf("%d", &num_to_find);
    int guess_num=0;
    int guess=0;
    while (guess_num != num_to_find){
        scanf("%d", &guess_num);
        
        guess ++;
        
        if(guess_num < num_to_find){
            printf("it is more\n");
        }
        else if (guess_num > num_to_find){
            printf("it is less\n");
        }
        else {
            printf("Number of tries needed:\n");
            printf("%d", guess);
        }
    }
}
