# Count Repeated Letters in a Word

## Problem Description

The program reads a lowercase word containing at most 50 letters and determines how many **distinct letters** occur more than once.

The letters must first be sorted in ascending ASCII order. The program then examines adjacent letters to identify repeated-letter groups. Each letter is counted only once, even if it appears three or more times.

## Examples

### Example 1

**Input**
```text
apple
```

**Output**
```text
1
```

### Example 2

**Input**
```text
keeper
```

**Output**
```text
1
```

### Example 3

**Input**
```text
erroneousnesses
```

**Output**
```text
5
```

### Example 4

**Input**
```text
taylor
```

**Output**
```text
0
```

## Approach

1. Read the word into a character array.
2. Sort the characters in ascending order (ASCII order).
3. Traverse the sorted word and compare each character with the next one.
4. When two adjacent characters are equal, increment the counter once for that repeated letter.
5. Skip the rest of that same-character group so a letter appearing more than twice is not counted repeatedly.
6. Print the counter, which represents the number of distinct letters that occur multiple times.

For example, after sorting `apple`, the word becomes `aelpp`. The adjacent `pp` group contributes exactly `1` to the result.

## Complexity Analysis

Let `N` be the number of characters in the word.

- **Time Complexity:** `O(N log N)` for comparison-based sorting, followed by an `O(N)` traversal.
- **Space Complexity:** `O(N)` for storing the input word. The sorting method may require additional implementation-dependent space.

## Build and Run

Compile with GCC:

```bash
gcc solution18.c -o solution18
```

Run:

```bash
./solution18
```

## Source Code

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->
