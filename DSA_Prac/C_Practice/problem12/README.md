# More or Less — Number Guessing Game

## Problem Description

The program reads a secret integer, followed by the player's guesses. For each incorrect guess, it prints:

- `it is more` if the guess is smaller than the secret number.
- `it is less` if the guess is larger than the secret number.

When the player guesses the secret number correctly, the program prints `Number of tries needed:` on one line, followed by the total number of guesses on the next line.

The correct guess is included in the number of tries.

## Examples

### Example 1

**Input**
```text
5
1 2 3 4 5
```

**Output**
```text
it is more
it is more
it is more
it is more
Number of tries needed:
5
```

### Example 2

**Input**
```text
10
5 15 8 12 11 10
```

**Output**
```text
it is more
it is less
it is more
it is less
it is less
Number of tries needed:
6
```

## Approach

1. Read the secret number.
2. Initialise the number of tries to `0`.
3. Repeatedly read a guess and increment the try counter.
4. Compare the guess with the secret number:
   - If the guess is smaller, print `it is more`.
   - If the guess is larger, print `it is less`.
   - If the guess is equal, stop the loop.
5. Print the required heading and the number of tries.

## Complexity Analysis

Let `T` be the number of guesses made, including the correct guess.

- **Time Complexity:** \(O(T)\), because each guess is read and processed once.
- **Space Complexity:** \(O(1)\), because only a fixed number of variables are used.

## Build and Run

Compile with GCC:

```bash
gcc solution12.c -o solution12
```

Run:

```bash
./solution12
```

## Source Code

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->
