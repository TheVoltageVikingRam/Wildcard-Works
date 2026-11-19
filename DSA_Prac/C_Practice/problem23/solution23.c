#include <stdio.h>

char character;
int variable_num;
size_t space_req;
int size_in_bytes, size_in_KB, size_in_MB;



int size_calc(char Character, int Variable_num){
    if (Character == 'i'){
        return (sizeof(int) * Variable_num);
        
    }
    
    else if (Character == 's'){
        return (sizeof(short int) * Variable_num);
    }
    
    else if (Character == 'd' ){
        return (sizeof(double) * Variable_num);
        
    }
    return 0;
}



int main(void){
    scanf("%c", &character);
    scanf("%d", &variable_num);
    space_req = size_calc(character, variable_num);
    size_in_bytes = space_req % 1000;
    size_in_KB = (space_req % 1000000)/1000;
    size_in_MB = space_req/1000000;
    
    if ((size_in_KB == 0) && (size_in_MB == 0)){
        printf("%d B", size_in_bytes);
    }
    else if ((size_in_MB == 0)){
        printf("%d KB and %d B", size_in_KB, size_in_bytes);
    }
    
    else {
        printf("%d MB and %d KB and %d B", size_in_MB, size_in_KB, size_in_bytes);
    }
    
}
