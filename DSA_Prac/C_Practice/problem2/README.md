# Carpool Trip Cost Calculator

## Problem Description

Calculate how much you must pay for a car trip when sharing the cost through a carpooling website.

The program reads:

- The number of passengers, as an integer.
- The cost of gas for the trip, as a decimal number.

If there are no passengers, you pay the full gas cost. If there is at least one passenger, the website adds a $1 fee and divides the total cost equally among you and all passengers.

Print the amount you must pay with exactly two digits after the decimal point. Do not print prompts or other text in the program output.

## Source Code

The implementation is maintained in [`solution2.c`](./solution2.c). The code below is populated automatically by the repository's GitHub Actions workflow.

<!-- SOURCE_CODE_START -->

### `solution2.c`

```c
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
```

<!-- SOURCE_CODE_END -->

## Examples

### Example 1

**Input**

```text
0 23.9
```

**Output**

```text
23.90
```

### Example 2

**Input**

```text
2 45.5
```

**Output**

```text
15.50
```

### Example 3

**Input**

```text
3 34.8
```

**Output**

```text
8.95
```

## Build and Run

Compile with GCC:

```bash
gcc -Wall -Wextra -std=c11 solution2.c -o solution2
```

Run on Linux or macOS:

```bash
./solution2
```

The program reads from standard input and must print only the required result.
