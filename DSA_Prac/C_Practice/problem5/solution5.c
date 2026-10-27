#include <stdio.h>
int main(void){
    
    int ingInd;
    int ingredient[10];
    int i;
    for (i=0; i<10; i++){
    scanf("%d", &ingredient[i]);
    }
    
    scanf("%d", &ingInd);
    printf("%d\n", ingredient[ingInd]);
}
