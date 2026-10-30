# Expense Sequence Sum

## Problem Description

A university administration needs to calculate the total of a sequence of recorded expenses.

The program must read a sequence of positive integers and display their sum. The number of expenses is not known in advance. The sequence always ends with `-1`, which is a termination marker and must not be included in the sum.

If the first value is `-1`, there are no expenses and the program must output `0`.

## Input

A sequence of integers, one per line or separated by whitespace.

- Each expense is represented by a positive integer.
- The sequence terminates when the value `-1` is read.
- The terminating value is not part of the sum.

## Output

Print one integer: the sum of all expense values before the `-1` terminator.

## Examples

### Example 1

**Input**
```text
1000
2000
500
-1
```

**Output**
```text
3500
```

### Example 2

**Input**
```text
-1
```

**Output**
```text
0
```

### Example 3

**Input**
```text
150
250
350
4500
240
120
-1
```

**Output**
```text
5610
```

## Approach

Read integers until the termination marker `-1` is encountered. Maintain a running total by adding each expense value to the sum. Stop when `-1` is read, then print the accumulated sum.

Do not print input prompts or any additional explanatory text in the program output.

## Source Code

The implementation is maintained in [`solution9.c`](./solution9.c).

<!-- SOURCE_CODE_START -->

### `solution10.c`

```c
#include <stdio.h>

int main(void){
    int expense;
    scanf("%d", &expense);
    int sumOfexpense=0;
    sumOfexpense = sumOfexpense + expense;
    
    while (expense != (-1)){
        
       
        scanf("%d", &expense);
        
         sumOfexpense = sumOfexpense + expense;
    }
    
    printf("%d", sumOfexpense+1);
}
```

<!-- SOURCE_CODE_END -->

## Complexity Analysis

- **Time Complexity:** `O(n)`, where `n` is the number of expense values before the terminator. Each value is read and processed once.
- **Space Complexity:** `O(1)`, because only a fixed number of variables (such as the current input value and running sum) are needed.

## Build and Run

Compile with GCC:

```bash
gcc -Wall -Wextra -std=c11 solution9.c -o solution9
```

Run on Linux or macOS:

```bash
./solution9
```

The program reads from standard input and prints only the required sum.
