#include <stdio.h>
int main(void){
    int tot_pop;
    scanf("%d", &tot_pop);
    int person_infected=1;
    int day=1;
    int new_infected=1;
    
    while (person_infected < tot_pop){
        new_infected = 2*person_infected;
        person_infected = person_infected+new_infected;
        day++;
    }
    
    printf("%d", day);
    
}
