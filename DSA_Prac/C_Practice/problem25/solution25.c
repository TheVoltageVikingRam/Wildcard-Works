#include <stdio.h>

void reverseArray(int *);

int main(void){
    int i;
    int arr[6];
    for (i=0; i<6; i++){
        scanf("%d", &arr[i]);
        
    }
    
    reverseArray(arr);
    
    for (i=0; i<6; i++){
        printf("%d ", arr[i]);
        
    }
    
}

void reverseArray(int * ptr){
    
    int tmp;
    tmp = (ptr[0]);
    ptr[0]=ptr[5];
    ptr[5]=tmp;
    
    tmp = ptr[1];
    ptr[1] = ptr[4];
    ptr[4] = tmp;
    
    tmp = ptr[2];
    ptr[2] = ptr[3];
    ptr[3] = tmp;
    
}
