# Tree Identification

## Problem Description

Determine the type of a tree using its height in meters and the number of leaflets on its leaves. Both inputs are integers.

The tree is classified using these rules:

| Tree type | Height | Number of leaflets |
|---|---:|---:|
| **Tinuviel** | 5 meters or less | 8 or more |
| **Calaelen** | 10 meters or more | 10 or more |
| **Falarion** | 8 meters or less | 5 or fewer |
| **Dorthonion** | 12 meters or more | 7 or fewer |

If the tree does not match any of these descriptions, print `Uncertain`.

The program must read the height first and the number of leaflets second. It must print only the tree name or `Uncertain`, with no input prompts.

## Source Code

The implementation is maintained in [`solution4.c`](./solution4.c). The code below is inserted automatically by the repository's GitHub Actions workflow.

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->

## Examples

### Example 1

**Input**

```text
12
12
```

**Output**

```text
Calaelen
```

### Example 2

**Input**

```text
4
9
```

**Output**

```text
Tinuviel
```

### Example 3

**Input**

```text
4
6
```

**Output**

```text
Uncertain
```

## Build and Run

Compile with GCC:

```bash
gcc -Wall -Wextra -std=c11 solution4.c -o solution4
```

Run on Linux or macOS:

```bash
./solution4
```

The program reads from standard input and prints the required result to standard output.
