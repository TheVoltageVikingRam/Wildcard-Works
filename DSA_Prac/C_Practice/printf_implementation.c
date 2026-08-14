#include <stdio.h>
#include <stdarg.h>




void myprintf(char *fmt, ...)

{
    va_list ap;
    char *p, *sval;
    int iVal;
    double dVal;
    char cVal;
    va_start(ap, fmt);
    for (p=fmt; *p; p++){
        if(*p != '%')
        {
            putchar(*p);
            continue;
        }

        switch(*(++p))
        {
            case 'd' :
                iVal = va_arg(ap, int);
                printf("%d", iVal);
                break;
            case 'f':
                dVal = va_arg(ap, double);
                printf("%f", dVal);
                break;

            case 'c':
                cVal = va_arg(ap, char);
                printf("%c", cVal);
            
            default:
                putchar(*p);
                break;
        }
    }



}





void main() {

    char ch = 'a';
    int x1=20, x2=40;
    double y1=30.567, y2=40.97;
    myprintf("\n this is the value of printf: X=%d Y=%d Ch=%c",x1,x2,ch);
    myprintf("\n This is the value of printf: X=%f, Y=%f", y1, y2);
    myprintf("\n This is the value of printf: X=%d, Y=%f", x1, y1);

}
