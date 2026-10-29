# Ingredient Shopping Cost Calculator

## Problem Description

You are preparing a meal and know the price per pound of each ingredient and the amount of each ingredient required by the recipe.

The program must:

1. Read the number of ingredients, `n`, where `n` is at most 10.
2. Read the price per pound for each ingredient.
3. Read the required weight for each ingredient, in the same order.
4. Calculate the total cost of the ingredients and print it with exactly six digits after the decimal point.

Do not print input prompts or any extra text in the program output.

## Approach

For each ingredient, multiply its price per pound by the required weight. Add each product to the running total, then display the total using six decimal places.

## Source Code

The implementation is maintained in [`solution7.c`](./solution7.c).

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->

## Example

### Input

```text
4
9.90 5.50 12.0 15.0
0.250 1.5 0.300 1.0
```

### Output

```text
29.325000
```

## Complexity Analysis

- **Time Complexity:** `O(n)` — each ingredient's price and required weight are processed once.
- **Space Complexity:** `O(n)` — arrays store the prices and required weights for up to 10 ingredients.

## Build and Run

Compile with GCC:

```bash
gcc -Wall -Wextra -std=c11 solution7.c -o solution7
```

Run on Linux or macOS:

```bash
./solution7
```

The program reads input from standard input and prints only the total cost.

## Submission Status

The submitted solution received **100%**, passing **1 out of 1 tests**.
