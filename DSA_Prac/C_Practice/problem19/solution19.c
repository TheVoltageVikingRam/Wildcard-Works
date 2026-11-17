#include <stdio.h>

int con_num;
int i;
double value_to_con;
char unit;
double converted_val;
double val_to_con;
double conv_m_to_ft(double val_to_con){
    return (val_to_con*3.2808);
}

double conv_g_to_lbs(double val_to_con){
    return (val_to_con*0.002205);
}


double conv_c_to_f(double val_to_con){
    return (32 + val_to_con*1.8);
}

int main(void){
    scanf("%d", &con_num);
    for (i=0; i<con_num; i++){
        scanf("%lf %c", &value_to_con, &unit);
        if (unit == 'm'){
             converted_val = conv_m_to_ft(value_to_con);
             printf("%.6f %s\n", converted_val, "ft");
        }
        else if (unit == 'g'){
             converted_val = conv_g_to_lbs(value_to_con);
             printf("%.6f %s\n", converted_val, "lbs");
        }
        
        else if (unit == 'c'){
            converted_val = conv_c_to_f(value_to_con);
            printf("%.6f %s\n", converted_val, "f");
        }
        
    }
    
}
