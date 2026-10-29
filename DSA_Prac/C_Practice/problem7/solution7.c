#include <stdio.h>

int main(void){
    int num_ing;
    scanf("%d", &num_ing);
    int i;
    
    double ing_per_pound[num_ing];
    double ing_weight[num_ing];
    double price_ing[num_ing];
    double total_price=0.000000;
    
    for (i=0; i<num_ing ; i++){
    scanf("%lf", &ing_per_pound[i]);
    }
    
    for (i=0; i<num_ing; i++){
        scanf("%lf", &ing_weight[i]);
    }
    
    
    for(i=0; i<num_ing; i++){
        price_ing[i] = ing_per_pound[i] * ing_weight[i];
        total_price = total_price + price_ing[i];
    }
    
    printf("%.6lf", total_price);
    
    return 0;
    
}
