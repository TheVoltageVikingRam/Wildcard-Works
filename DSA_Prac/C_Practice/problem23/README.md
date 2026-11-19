# Memory Usage Calculator

## Problem Description

The program calculates the total memory required to store a given number of variables of a specified data type. It first reads a character identifying the data type and then an integer representing the number of variables.

The supported data types are:

- `i`: Integer (`int`)
- `s`: Short integer (`short int`)
- `c`: Character (`char`)
- `d`: Double (`double`)

The program uses the `sizeof()` operator to determine the memory occupied by an individual variable of the specified type. This ensures that the program works across different computer architectures without hard-coding data type sizes.

The total memory required is calculated by multiplying the size of one variable by the number of variables.

The final memory requirement is displayed in a human-readable format using the following units:

- Bytes (`B`)
- Kilobytes (`KB`), where 1 KB = 1000 bytes
- Megabytes (`MB`), where 1 MB = 1000 KB

Only the necessary units are displayed in the output.

## Example

**Input**
```text
d 654250
```

**Output**
```text
5 MB and 234 KB and 0 B
```

## Approach

1. Read the data type identifier as a `char`.
2. Read the number of variables as an `int`.
3. Define a function `size_calc()` that:
   - Accepts the data type identifier and the number of variables as arguments.
   - Uses an `if` / `else if` structure to identify the data type.
   - Uses `sizeof()` to determine the size of the corresponding data type.
   - Returns the total memory required in bytes.
4. Calculate the memory distribution:
   - **Bytes:** `total_memory % 1000`
   - **Kilobytes:** `(total_memory % 1000000) / 1000`
   - **Megabytes:** `total_memory / 1000000`
5. Use conditional statements to determine which units need to be displayed.
6. Print the final memory requirement in a human-readable format.

## Complexity Analysis

Let `N` be the number of variables.

- **Time Complexity:** `O(1)`, because the program performs a fixed number of operations regardless of the number of variables.
- **Space Complexity:** `O(1)`, because only a fixed number of variables are required.

## Build and Run

Compile with GCC:

```bash
gcc solution20.c -o solution20
```

Run:

```bash
./solution20
```

## Source Code

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->
