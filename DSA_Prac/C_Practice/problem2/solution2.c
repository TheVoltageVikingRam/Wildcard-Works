#include <stdio.h>
int passengerNum;
float costgas;
float topay;

int main(void){
// printf("Enter the number of passengers. \n");
scanf("%d", &passengerNum);
scanf("%f", &costgas);
if (passengerNum==0)
{
    topay=costgas;
    printf("%.2f", topay);
}

else {
    topay=((costgas+1)/(passengerNum+1));
    printf("%.2f", topay);
}

return 0;
}
