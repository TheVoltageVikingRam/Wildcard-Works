#include <stdio.h>

int main(void){
    char word[50];
    scanf("%s", word);
    
    int i=0;
    int j=0;
    int word_size=0;
    
    while ( word[j] != '\0'){
        j++;
    }
    
    word_size = j;
    
    int found=0;
    while (word[i] != '\0' && !found){
        if ( word[i] == 't' || word[i] == 'T'){
            found=1;
        }
        else {
            i++;
        }
        
    }
    
   if (found && (i <= word_size/2)){
       printf("%d", 1);
   }
   else if ( found && (i>word_size/2)){
       printf("%d", 2);
   }
   else printf("%d", -1);
    
}
