#include <stdio.h>


int num_codes;
int i;
int num;
char character;
size_t size_needed;

size_t size_for_code(int number, char letter){
    if (letter == 'i'){
        return (number * sizeof(int));
    }
    else if (letter == 'c'){
        return (number * sizeof(char));
    }
    else if (letter == 'd'){
        return (number * sizeof(double));
        
    }
    else {
        return 0;
    }
    
}

int main(void){
    
    scanf("%d", &num_codes);
    
    for (i=0; i<num_codes; i++){
        scanf("%d %c", &num, &character);
        
    if (character == 'c' || character == 'd' || character == 'i'){
    size_needed =  size_needed + size_for_code(num, character);
    }
    else{
        printf("Invalid tracking code type\n");
        return 1;
    }
    }
 
    printf("%zu bytes\n", size_needed);
    return 0;
}
