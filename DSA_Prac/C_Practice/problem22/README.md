# Problem 22: Calculate Tracking Code Memory

## Problem Description

A system stores several tracking codes. Each tracking code is described by:
- An integer representing the number of elements to store.
- A character representing the data type of those elements.

The supported data types are:
- `i` — integer (`int`)
- `d` — decimal (`double`)
- `c` — character (`char`)

Calculate the total memory required to store all tracking codes, in bytes.

If an unsupported type is encountered, print `Invalid tracking code type` and terminate the program.

## Examples

### Example 1

**Input**
```text
3
10 i
7 c
12 d
```

**Output**
```text
143 bytes
```

**Explanation**

- 10 integers × 4 bytes = 40 bytes
- 7 characters × 1 byte = 7 bytes
- 12 doubles × 8 bytes = 96 bytes

Total = 40 + 7 + 96 = **143 bytes**.

### Example 2

**Input**
```text
2
3 c
20 d
```

**Output**
```text
163 bytes
```

**Explanation**

- 3 characters × 1 byte = 3 bytes
- 20 doubles × 8 bytes = 160 bytes

Total = 3 + 160 = **163 bytes**.

### Example 3

**Input**
```text
4
5 i
2 d
10 a
3 c
```

**Output**
```text
Invalid tracking code type
```

**Explanation**

The type `a` is not supported, so the program reports the error and terminates.

## Approach

1. Read the number of tracking codes, `N`.
2. For each tracking code, read its element count and type character.
3. Use a separate function, `size_for_code()`, to calculate the memory required:
   - `i`: count × `sizeof(int)`
   - `d`: count × `sizeof(double)`
   - `c`: count × `sizeof(char)`
4. Add each valid result to the running total.
5. If the type is unsupported, print `Invalid tracking code type` and terminate.
6. Print the total memory in bytes.

The program uses `sizeof()` so that the calculation follows the sizes of the C data types on the system where it is compiled. The sample calculations assume `int` is 4 bytes, `double` is 8 bytes, and `char` is 1 byte.

## Complexity Analysis

- **Time Complexity:** O(N), because each tracking code is processed once.
- **Space Complexity:** O(1), because only a fixed number of variables are used.

## Build and Run

Compile the program:

```bash
gcc solution22.c -o solution22
```

Run it:

```bash
./solution22
```

## Source Code

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->
