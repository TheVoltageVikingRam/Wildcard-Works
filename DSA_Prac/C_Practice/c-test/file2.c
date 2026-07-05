#include <stdio.h>
#include "file1.c"

int main()
{
	int x =20, y =30, z;
	z=fn1(x,y);
	printf("\n%d x %d x MACRO_VAL = %d\n", x, y, z);
return 0;


}
