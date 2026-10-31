# Find `t` or `T` in a Word

## Problem Description

The program reads a word containing at most 50 letters and checks where the letter `t` or `T` appears.

- Print `1` if `t` or `T` occurs in the first half of the word.
- If it does not occur in the first half but occurs in the second half, print `2`.
- If it does not occur anywhere in the word, print `-1`.

For a word with an odd number of letters, the middle letter belongs to the first half.

## Examples

### Example 1

**Input**
```text
apple
```

**Output**
```text
-1
```

### Example 2

**Input**
```text
raincoat
```

**Output**
```text
2
```

### Example 3

**Input**
```text
enter
```

**Output**
```text
1
```

### Example 4

**Input**
```text
Taylor
```

**Output**
```text
1
```

## Approach

1. Read the word into a character array.
2. Find its length.
3. Calculate the size of the first half as `(length + 1) / 2`. This includes the middle character when the length is odd.
4. Search the first half for either `t` or `T`. If found, print `1`.
5. Otherwise, search the remaining characters. If either letter is found, print `2`.
6. If neither half contains `t` or `T`, print `-1`.

Checking the first half before the second ensures that the output is `1` whenever the letter occurs in both halves.

## Complexity Analysis

Let `N` be the length of the word.

- **Time Complexity:** `O(N)`, because each character is examined at most once.
- **Space Complexity:** `O(N)`, because the input word is stored in a character array. The maximum length is bounded by 50 characters.

## Build and Run

Compile with GCC:

```bash
gcc solution17.c -o solution17
```

Run:

```bash
./solution17
```

## Source Code

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->
