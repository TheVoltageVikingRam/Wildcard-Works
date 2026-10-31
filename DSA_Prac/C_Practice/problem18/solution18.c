#include <stdio.h>
#include <string.h>

int main(void){
    
    char word[51];
    scanf("%s", word);
    int letter_counter=0;
    int swap=0;
    int length = strlen(word);
    int i, j, k, l;
    for (j=0; j<length-1; j++){
        
        for (i=0; i<length-1; i++){
            
            if (word[i] > word[i+1]){
                swap=word[i];
                word[i]=word[i+1];
                word[i+1]=swap;
            }
            
        }
    }
   

   
   k=0;
   
   while (k<length){
       l = k+1;
       while ((l<length) && (word[k] == word[l])){
           l++;
           
       }
       if (l-k >=2 ){
           letter_counter++;
       }
       k=l;
   }
   
    printf("%d", letter_counter);
}
