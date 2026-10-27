#include <stdio.h>

int main(void){
    
    int heightOftree;
    int number_leaflets;
    scanf("%d", &heightOftree);
    scanf("%d", &number_leaflets);
    
    if ((heightOftree <=5 ) && (number_leaflets >=8 )){
        printf("Tinuviel\n");
    }
    
    else if ((heightOftree >= 10 ) && (number_leaflets >= 10 )){
        printf("Calaelen\n");
    }
    
    else if ((heightOftree <=8 ) && (number_leaflets <= 5 )){
        printf("Falarion\n");
    }
    
    else if ((heightOftree >= 12 ) && (number_leaflets <=7  )) {
        printf("Dorthonion\n");
    }
    
    else {
        printf("Uncertain\n");
    }
}
