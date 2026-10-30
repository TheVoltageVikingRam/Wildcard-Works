#include <stdio.h>

int main(void){
    int num_tp;
    scanf("%d", &num_tp);
    char first_name[101];
    char second_name[101];
    int i;
    for (i=0; i < num_tp; i++){
        scanf("%s %s", first_name, second_name);
        printf("%s %s\n", second_name, first_name);
    }
    return 0;
}
