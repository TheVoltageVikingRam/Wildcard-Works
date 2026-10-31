#include <stdio.h>

int main(void){
    
    int i=0;
    char name[50];
    scanf("%s", name);
    
    
    while (name[i] != '\0'){
        i++;
    }
    if (i % 2 ==0){
        printf("%d", 1);
    }
    else {
        printf("%d", 2);
    }
    
}
