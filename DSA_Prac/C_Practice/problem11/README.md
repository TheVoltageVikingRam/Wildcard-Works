# Epidemic Spread

## Problem Description

A region has a population of `N` people. One person is infected on day 1. Each infected person infects two new people every following day.

Determine the first day on which the entire population has been infected. On the final day, the number of potential new infections may exceed the number of people remaining.

## Examples

| Input | Output |
|---:|---:|
| `3` | `2` |
| `10` | `4` |
| `100` | `6` |

## Approach

- Start with `1` infected person on day `1`.
- Each infected person infects two additional people the following day.
- Therefore, the total infected population triples each day.
- Continue until the infected count is greater than or equal to the total population.
- Print the day number.

The recurrence is:

\[
I_{d+1} = 3I_d, \qquad I_1 = 1
\]

## Complexity Analysis

- **Time Complexity:** \(O(\log_3 N)\), because the infected population triples each day.
- **Space Complexity:** \(O(1)\), because only a fixed number of variables are used.

## Build and Run

Compile with GCC:

```bash
gcc solution10.c -o solution10
```

Run:

```bash
./solution10
```

## Source Code

<!-- SOURCE_CODE_START -->

### `solution11.c`

```c
#include <stdio.h>
int main(void){
    int tot_pop;
    scanf("%d", &tot_pop);
    int person_infected=1;
    int day=1;
    int new_infected=1;
    
    while (person_infected < tot_pop){
        new_infected = 2*person_infected;
        person_infected = person_infected+new_infected;
        day++;
    }
    
    printf("%d", day);
    
}
```

<!-- SOURCE_CODE_END -->
