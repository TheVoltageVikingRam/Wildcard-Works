#include <stdio.h>


int main(void){
    
    
    int numOfPlayers;
    int weight_team1=0;
    int weight_team2=0;
    int playerWeight;
    int i;
    scanf("%d", &numOfPlayers);
    
    for (i=0; i<(2*numOfPlayers) ; i++){
        
        scanf("%d", &playerWeight);
        
        if (i%2 == 0){
            weight_team1=weight_team1+playerWeight;
        }
            
        else {
            weight_team2=weight_team2+playerWeight;
        }
    }
    if (weight_team1 > weight_team2){
        printf("Team 1 has an advantage\n");
        
    } else{
        printf("Team 2 has an advantage\n");
    }
    
    printf("Total weight for team 1: %d\n", weight_team1);
    printf("Total weight for team 2: %d\n", weight_team2);
    
}
