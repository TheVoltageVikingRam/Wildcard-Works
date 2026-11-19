# Elixir of Youth

## Problem Description

The program calculates a person's new age after drinking a fictional elixir of youth. The elixir follows two simple rules depending on the person's current age:

- If the person is **21 years old or older**, the elixir makes them 10 years younger.
- If the person is **20 years old or younger**, the elixir doubles their age.

The program uses pointers to modify the original age variable directly rather than returning a new value.

A pointer to the integer variable `age` is declared using `ageAddr`. The function accepts this integer pointer as an argument and modifies the value stored at the memory address it points to.

Since the function modifies the original variable directly through a pointer, it uses a `void` return type.

## Example

**Input**
```text
55
```

**Output**
```text
Your current age is 55.
Your new age will be 45!
```

## Approach

1. Declare an integer variable `age` and a pointer `ageAddr` that stores its memory address.
2. Read the user's age using `scanf()` and the pointer `ageAddr`.
3. Define a function that:
   - Accepts an integer pointer `ageAddr` as an argument.
   - Uses an `if` / `else` structure to check the person's age.
   - Uses the dereference operator (`*`) to access and modify the value stored at the address.
   - If the age is 21 or greater, subtract 10 from it.
   - Otherwise, multiply the age by 2.
4. Call the function from `main()` by passing `ageAddr` as the argument.
5. Print the modified age.

## Complexity Analysis

- **Time Complexity:** `O(1)`, because the function performs a constant number of operations regardless of the person's age.
- **Space Complexity:** `O(1)`, because only a fixed number of variables and a pointer are used.

## Build and Run

Compile with GCC:

```bash
gcc solution21.c -o solution21
```

Run:

```bash
./solution21
```

## Source Code

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->
