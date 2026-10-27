# Hostel Room Price Calculator

## Problem Description

Calculate the price for one night at a hostel based on the customer's age and the weight of their luggage.

The program reads two integers from standard input, in this order:

1. The customer's age.
2. The weight of their luggage in pounds.

Apply the following pricing rules:

- If the customer is exactly 60 years old, the price is **$0**.
- Otherwise, if the customer is younger than 10 years old, the price is **$5**.
- For everyone else, the price is **$30**.
- For customers in the last category, add **$10** if their luggage weighs more than 20 pounds.

Print only the resulting price as an integer. Do not print an input prompt or a currency symbol.

## Source Code

The implementation is maintained in [`solution3.c`](./solution3.c). The source code below is inserted automatically by the repository's GitHub Actions workflow.

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->

## Example

### Input

```text
22
25
```

### Output

```text
40
```

## Build and Run

Compile with GCC:

```bash
gcc -Wall -Wextra -std=c11 solution3.c -o solution3
```

Run on Linux or macOS:

```bash
./solution3
```

The program reads from standard input and prints only the required price.

## Important Cases to Consider

- Age is exactly 60.
- Age is less than 10.
- Luggage weighs exactly 20 pounds (the additional fee applies only above 20 pounds).
- Age is 10 or older but not 60, with luggage weighing more than 20 pounds.
