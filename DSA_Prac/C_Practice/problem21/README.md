# Sum of Digits Using Recursion

## Problem Description

The program reads an integer and calculates the sum of its digits using a recursive function named `sumOfDigits()`.

The function repeatedly separates the last digit from the number and adds it to the result of calling itself with the remaining digits. Recursion stops when no digits remain.

For example:

\[
\text{sumOfDigits}(6452) = 2 + \text{sumOfDigits}(645)
\]

## Examples

### Example 1

**Input**
```text
47253
```

**Output**
```text
21
```

### Example 2

**Input**
```text
643
```

**Output**
```text
13
```

## Approach

1. Read the integer from standard input.
2. Call the recursive function `sumOfDigits()` with the input number.
3. In each recursive call:
   - Extract the last digit using the remainder operator (`% 10`).
   - Remove the last digit using integer division (`/ 10`).
   - Add the extracted digit to the result of `sumOfDigits()` called with the remaining number.
4. Use a base case to return `0` when the number has no digits left.
5. Print the returned sum.

## Complexity Analysis

Let `D` be the number of digits in the input integer.

- **Time Complexity:** `O(D)`, because each recursive call processes one digit.
- **Space Complexity:** `O(D)`, because the recursion call stack can contain up to one call per digit.

## Build and Run

Compile with GCC:

```bash
gcc solution21.c -o solution21
```

Run:

```bash
./solution21
```

## Source Code

<!-- SOURCE_CODE_START -->

### `solution21.c`

```c
#include <stdio.h>

int sumOfDigits(int given_num);
int num;
int sum_of_digits;
int digit_sum;

int main(void){

	scanf("%d", &num);
	sum_of_digits = sumOfDigits(num);
	printf("%d", sum_of_digits);

}

int sumOfDigits(int given_num){
	if (given_num == 0){
	    return 0;
	}

	digit_sum = (given_num % 10) + sumOfDigits((given_num/10));
	return digit_sum;

}
```

<!-- SOURCE_CODE_END -->
