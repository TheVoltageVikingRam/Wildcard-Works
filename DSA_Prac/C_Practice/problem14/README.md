# Correct Patron Name Order

## Problem Description

A library has patron index cards that should display each person's last name followed by their first name. Some cards were incorrectly recorded with the first name before the last name.

The program first reads the number of patrons. For each patron, it then reads the first name and last name and immediately prints them in the correct order: last name, followed by a space, followed by first name.

Each name contains no spaces and has at most 100 characters.

## Example

**Input**
```text
4
Alan Turing
Ada Lovelace
Donald Knuth
Claude Shannon
```

**Output**
```text
Turing Alan
Lovelace Ada
Knuth Donald
Shannon Claude
```

## Approach

1. Read the number of patrons.
2. Repeat once for each patron:
   - Read the first name.
   - Read the last name.
   - Print the last name followed by the first name, separated by one space.
3. Print each corrected name immediately after reading that patron's names.

## Complexity Analysis

Let `N` be the number of patrons.

- **Time Complexity:** `O(N)`, because each patron's two names are read and printed once.
- **Space Complexity:** `O(1)`, because only two fixed-size name buffers are needed at a time.

## Build and Run

Compile with GCC:

```bash
gcc solution14.c -o solution14
```

Run:

```bash
./solution14
```

## Source Code

<!-- SOURCE_CODE_START -->

### `solution14.c`

```c
#include <stdio.h>

int main(void){
    int num_tp;
    scanf("%d", &num_tp);
    char first_name[101];
    char second_name[101];
    int i;
    for (i=0; i < num_tp; i++){
        scanf("%s %s", first_name, second_name);
        printf("%s %s\n", second_name, first_name);
    }
    return 0;
}
```

<!-- SOURCE_CODE_END -->
