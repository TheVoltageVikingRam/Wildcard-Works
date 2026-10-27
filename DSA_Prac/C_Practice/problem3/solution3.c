#include <stdio.h>

int main(void){
    
    int customerAge;
    int luggageWeight;
    int amountToPay;
    
    scanf("%d", &customerAge);
    scanf("%d", &luggageWeight);
    
    
    if (customerAge == 60){
        amountToPay=0;
        printf("%d\n", amountToPay);
        
    }
    else if (customerAge < 10){
        
        amountToPay=5;
        printf("%d\n", amountToPay);
    }
    
    else if ((customerAge>=10 || customerAge !=60) && (luggageWeight>20))
    { 
        
    
        amountToPay=40;
        printf("%d\n", amountToPay);
    }
    else {
        amountToPay = 30;
        printf("%d\n", amountToPay);
    }
    }
