#include <stdio.h>

int main(void){
    
    int temp_min, temp_max;
    scanf("%d", &temp_min);
    scanf("%d", &temp_max);
    int temp_measured;
    scanf("%d", &temp_measured);
    while ( (temp_measured <= temp_max && temp_measured >= temp_min) && (temp_measured != -999) ){
        printf("Nothing to report\n");
        scanf("%d", &temp_measured);
      
        
    }
    
    if ((temp_measured != -999 ) && (temp_measured < temp_min || temp_measured > temp_max )) {
        printf("Alert!\n");
    }
    
}
