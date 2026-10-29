#include <stdio.h>
int main(void){
    int nbThrows = 0;
    int nbdice = 0;
    int i,j,k;
    int MaxRes=0;
    int Maxthrow=0;
    int dice_res;
    scanf("%d", &nbThrows);
    scanf("%d", &nbdice);
    int player_Sum[nbThrows];
    
    for (i=0; i<nbThrows ; i++){
        for (j=0; j<nbdice ; j++){
            scanf("%d", &dice_res);
            player_Sum[i] = player_Sum[i] + dice_res;
        }
        
    }
    
    for (i=0; i<nbThrows; i++){
    if (player_Sum[i]>MaxRes){
        MaxRes=player_Sum[i];
        Maxthrow=i;
        }
    }
    printf("Player at index %d has the maximum throw with sum %d", Maxthrow, MaxRes);
    
}
