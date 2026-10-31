# MOOC Registration Line

## Problem Description

A fan must choose one of two registration lines based on the number of letters in their name.

- **Line 1:** Names containing an even number of letters.
- **Line 2:** Names containing an odd number of letters.

The program reads a name (without spaces and containing fewer than 50 characters) and prints `1` if its length is even or `2` if its length is odd.

## Examples

### Example 1

**Input**
```text
Sharrock
```

**Output**
```text
1
```

### Example 2

**Input**
```text
Bonfert
```

**Output**
```text
2
```

## Approach

1. Read the name into a character array.
2. Determine the number of characters in the name.
3. Check the length using the modulo operator:
   - If `length % 2 == 0`, print `1`.
   - Otherwise, print `2`.

## Complexity Analysis

Let `N` be the number of characters in the name.

- **Time Complexity:** `O(N)`, because the name length must be determined by examining its characters.
- **Space Complexity:** `O(N)`, because the input name is stored in a character array.

## Build and Run

Compile with GCC:

```bash
gcc solution15.c -o solution15
```

Run:

```bash
./solution15
```

## Source Code

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->
