# Recipe Ingredient Quantity Lookup

## Problem Description

A recipe contains 10 ingredients. The required quantity of each ingredient, in grams, is provided as input in order. Read the 10 quantities into an array, then read an ingredient ID from `0` to `9` and print the quantity associated with that ID.

## Input

- Ten integers representing ingredient quantities in grams, in order.
- One integer representing the requested ingredient ID, from `0` through `9`.

## Output

Print the quantity corresponding to the requested ingredient ID.

## Example

### Input

```text
500 180 650 25 666 42 421 1 370 211
3
```

### Output

```text
25
```

## Approach

Store the ten input quantities in an array. Read the ingredient ID and use it as the array index to retrieve and print the corresponding quantity. Since valid IDs range from `0` to `9`, they directly match the array's indices.

## Source Code

The implementation is maintained in [`solution4.c`](./solution4.c).

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->

## Build and Run

Compile with GCC:

```bash
gcc -Wall -Wextra -std=c11 solution4.c -o solution4
```

Run on Linux or macOS:

```bash
./solution4
```

The program reads from standard input and must print only the required quantity, with no input prompts.

## Complexity Analysis

- **Time Complexity:** `O(1)` — the program reads a fixed number of quantities and performs a single indexed lookup.
- **Space Complexity:** `O(1)` — the array always contains exactly ten integers.
