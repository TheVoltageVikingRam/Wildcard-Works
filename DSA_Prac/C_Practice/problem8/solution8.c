#include <stdio.h>

int main(void)
{
    int city_num;
    scanf("%d", &city_num);
    int i;
    int city_pop;
    int pop_large=0;
    for (i=0; i<city_num; i++){
        scanf("%d", &city_pop);
        if (city_pop>10000){
            pop_large = pop_large+1;
        }
    }
    
    printf("%d", pop_large);
}
