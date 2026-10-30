#include <stdio.h>

int main(void){
    int expense;
    scanf("%d", &expense);
    int sumOfexpense=0;
    sumOfexpense = sumOfexpense + expense;
    
    while (expense != (-1)){
        
       
        scanf("%d", &expense);
        
         sumOfexpense = sumOfexpense + expense;
    }
    
    printf("%d", sumOfexpense+1);
}
