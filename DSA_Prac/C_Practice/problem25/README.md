# Reverse Array

## Problem Description

The program reverses an array containing 6 integers by swapping its elements in pairs.

The program uses a function called `reverseArray()` to perform the reversal. The function accepts an integer array as its parameter and has a `void` return type, since the modifications are made directly to the original array.

The reversal is performed by swapping the corresponding elements from opposite ends of the array:

- The first element is swapped with the last element.
- The second element is swapped with the second-to-last element.
- The third element is swapped with the third-to-last element.

Since arrays are passed to functions through their memory address, changes made to the array inside the function are reflected in the original array in `main()`.

## Example

**Input**
```text
1 2 3 4 5 6
```

**Output**
```text
6 5 4 3 2 1
```

## Approach

1. Declare an integer array of size 6 in the `main()` function.
2. Read 6 integers from the input and store them in the array.
3. Define a function called `reverseArray()` that:
   - Accepts the integer array as its parameter.
   - Uses a temporary integer variable to facilitate swapping.
   - Swaps the first element (`arr[0]`) with the last element (`arr[5]`).
   - Swaps the second element (`arr[1]`) with the second-to-last element (`arr[4]`).
   - Swaps the third element (`arr[2]`) with the third-to-last element (`arr[3]`).
4. Call `reverseArray()` from `main()`, passing the array as an argument.
5. Print all 6 elements of the modified array in order.

## Complexity Analysis

- **Time Complexity:** `O(1)`, because the array always contains exactly 6 elements and the function performs exactly 3 swaps.
- **Space Complexity:** `O(1)`, because only a fixed-size array and a temporary variable are used.

## Build and Run

Compile with GCC:

```bash
gcc solution22.c -o solution22
```

Run:

```bash
./solution22
```

## Source Code

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->
