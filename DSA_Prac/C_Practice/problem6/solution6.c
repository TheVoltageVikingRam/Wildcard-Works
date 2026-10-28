#include <stdio.h>

int main(void){
    int boxcar_num=0;
    double car_weight=0.0;
    scanf("%d", &boxcar_num);
    double weight_reduce[boxcar_num];
    double weight_cars[boxcar_num];
    double weight_tot=0.0;
    double weight_opt=0.0;
    int carindex=0;
    int i=0;
    

    
    for (i=0; i<boxcar_num; i++){
        
    scanf("%lf\n", &car_weight);
    weight_cars[i]=car_weight;
    weight_tot=weight_tot+car_weight;
    
    
    
    }
    
    weight_opt=weight_tot/boxcar_num;
    
    for (carindex=0; carindex<boxcar_num; carindex++){
        weight_reduce[carindex] = weight_opt-weight_cars[carindex];
        printf("%.1lf\n", weight_reduce[carindex]);
    }
    
}
