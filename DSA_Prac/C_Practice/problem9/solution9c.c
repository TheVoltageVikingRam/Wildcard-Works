// searching a sorted list using bisection 

#include <stdio.h>
int main(void){
  int list[] = {-10, -3, 2, 5, 8, 14, 77, 106, 759, 900};
  int n = 10;
  int item;
  int ia, ib, mid, found;

  printf("Which mumber are you looking for ?");
  scanf("%d", &item  );
  ia = 0;
  ib = n-1;
  found = 0;

  while (!found && (ia <= ib) ) {
    mid = (ia + ib)/2;
    if (item == list[mid]){
      found = 1;
    }
    else if (item < list[mid] ) {
      ib = mid-1;
    }
    else {
      ia = mid+1;

    }

  }

  if (!found) {
  printf("Number %d was not found in the array. \n", item);
  }

  else{
  printf("Number %d was found at the index %d in the array.\n", item, mid);
  }


}
