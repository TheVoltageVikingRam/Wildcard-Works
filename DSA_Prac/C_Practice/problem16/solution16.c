#include <stdio.h>

int main(void){
    int i=0;
    int t=0;
    int k=0;
    int l=0;

    
    int maxLen=0;
    int nbWords=0;
    char word[100];
    int length[100];
    
    for (i=0; i<100; i++){
        length[i]=0;
    }
    
    
    scanf("%d", &nbWords);
    for (t=0; t<nbWords; t++){
        
        scanf("%s", word);
        l=0;
        while (word[l] != '\0'){
            l++;
        }
        length[l] = length[l]+1;
        
        
    }
    
    for (k=0; k<100; k++){
        
        if (k > maxLen && length[k] !=0 ){
            maxLen=k;
        }
    }
    printf("%d", maxLen);
    
}
