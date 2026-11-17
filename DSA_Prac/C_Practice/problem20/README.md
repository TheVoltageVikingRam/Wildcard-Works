# Find the Minimum Integer

## Problem Description

The program reads an integer `N` representing the number of values in a list, followed by `N` integers. It must find and print the smallest integer in the list.

The solution must include a function named `min()` that takes two integers and returns the smaller one. A function prototype must be provided before `main()`.

## Example

**Input**
```text
10
4 3 6 2 6 8 9 8 5 4
```

**Output**
```text
2
```

## Approach

1. Declare the prototype for `min()`, which accepts two integers and returns the smaller integer.
2. Read the number of elements, `N`.
3. Read the first element and use it to initialise the current minimum.
4. Read each remaining element one at a time.
5. Compare the current minimum with the new value by calling `min()`, and update the current minimum with the returned value.
6. Print the final minimum.

Initialising the minimum with the first input value also handles lists containing only negative numbers.

## Complexity Analysis

Let `N` be the number of integers in the list.

- **Time Complexity:** `O(N)`, because each element is processed once and each call to `min()` takes constant time.
- **Space Complexity:** `O(1)`, because only a fixed number of variables are needed, regardless of the list size.

## Build and Run

Compile with GCC:

```bash
gcc solution20.c -o solution20
```

Run:

```bash
./solution20
```

## Source Code

<!-- SOURCE_CODE_START -->

### `solution20.c`

```c
#include <stdio.h>

int num_of_int;
int i;
int given_num;
int minimum_num;
int min_num;
int min(int number_given);

int main(void){
    scanf("%d", &num_of_int);
    scanf("%d", &minimum_num);
    for (i=1; i<num_of_int ; i++){
        scanf("%d", &given_num);
        minimum_num = min(given_num);
    }
    
    printf("%d", minimum_num);
    
    return 0;
}



int min(int number_given){
    if (number_given >= minimum_num) {
        min_num = minimum_num;
        
    }
    
    else if (minimum_num > number_given){
        min_num =  number_given;
        
    }
  return min_num;
    
}
```

<!-- SOURCE_CODE_END -->
