# City Population Threshold Counter

## Problem Description

Given the number of cities in a region and the population of each city, count how many cities have a population **strictly greater than 10,000**.

The program reads:

1. An integer representing the number of cities.
2. The population of each city, one integer at a time.

It outputs the number of cities whose population exceeds 10,000. A population equal to 10,000 does not count.

## Approach

1. Read the number of cities.
2. Initialize a counter to zero.
3. Read each city's population.
4. If the population is greater than 10,000, increment the counter.
5. Print the final counter.

## Source Code

The implementation is maintained in [`solution8.c`](./solution8.c).

<!-- SOURCE_CODE_START -->

### `solution8.c`

```c
#include <stdio.h>

int main(void)
{
    int city_num;
    scanf("%d", &city_num);
    int i;
    int city_pop;
    int pop_large=0;
    for (i=0; i<city_num; i++){
        scanf("%d", &city_pop);
        if (city_pop>10000){
            pop_large = pop_large+1;
        }
    }
    
    printf("%d", pop_large);
}
```

<!-- SOURCE_CODE_END -->

## Example

### Input

```text
6
1000
5000
15000
4780
0
23590
```

### Output

```text
2
```

## Complexity Analysis

- **Time Complexity:** `O(n)`, where `n` is the number of cities, because each population is checked once.
- **Space Complexity:** `O(1)`, because only a fixed number of variables is required.

## Build and Run

Compile with GCC:

```bash
gcc -Wall -Wextra -std=c11 solution8.c -o solution8
```

Run on Linux or macOS:

```bash
./solution8
```

The program reads from standard input and must print only the required result, without input prompts.
