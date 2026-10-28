# Rail Convoy — Boxcar Weight Balancing

## Problem Description

A train consists of several boxcars carrying different weights. The goal is to redistribute the load so that every boxcar has exactly the same weight, without changing the total weight of the train.

The program reads the number of boxcars, followed by the weight of each boxcar as a double. It then calculates how much weight must be added to or removed from each boxcar so that all boxcars reach the same target weight.

Each adjustment must be printed on a separate line with **one digit after the decimal point**:

- A **positive** value means weight must be added.
- A **negative** value means weight must be removed.
- A value of `0.0` means no adjustment is needed.

## Approach

1. Read the number of boxcars, `n`.
2. Read and store the weight of each boxcar in an array, while calculating the total weight.
3. Calculate the target weight per boxcar by dividing the total weight by `n`.
4. For each boxcar, calculate the adjustment as `target weight - current weight`.
5. Print each adjustment on its own line to one decimal place.

## Source Code

The implementation is maintained in [`solution6.c`](./solution6.c). The code below is populated automatically by the repository's GitHub Actions workflow.

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->

## Example

### Input

```text
5
40.0
12.0
20.0
5.0
33.0
```

### Output

```text
-18.0
10.0
2.0
17.0
-11.0
```

The total weight is `110.0`, so each of the five boxcars should carry `22.0` units of weight. The adjustments sum to zero, preserving the train's total weight.

## Constraints and Assumptions

- There are no more than 50 boxcars.
- The number of boxcars is a positive integer.
- Boxcar weights are provided as double-precision values.
- All adjustments must preserve the total weight of the train.

## Complexity Analysis

- **Time Complexity:** `O(n)` — the weights are read once and each adjustment is calculated once.
- **Space Complexity:** `O(n)` — an array stores the weights of the boxcars, with at most 50 entries.

## Build and Run

Compile with GCC:

```bash
gcc -Wall -Wextra -std=c11 solution6.c -o solution6
```

Run on Linux or macOS:

```bash
./solution6
```

The program reads from standard input and must print only the required adjustments, without input prompts or additional messages.
