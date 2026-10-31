# Longest Word Length

## Problem Description

The program reads an integer representing the number of words in a text, followed by that many words. It must determine and print the length of the longest word.

The text contains only words, without punctuation or special characters. The longest word is guaranteed not to exceed 100 characters.

## Examples

### Example 1

**Input**
```text
14
This is a simple example text
we have to find the largest word length
```

**Output**
```text
7
```

### Example 2

**Input**
```text
7
All cats are grey in the dark
```

**Output**
```text
4
```

## Approach

1. Read the number of words.
2. Initialise a variable to store the maximum word length.
3. Read each word into a character array.
4. Determine its length using `strlen()`.
5. Update the maximum length whenever the current word is longer.
6. Print the maximum length after all words have been processed.

## Complexity Analysis

Let `N` be the number of words and `L` be the maximum length of a word.

- **Time Complexity:** `O(N × L)`, because each word is read and its characters are examined to determine its length.
- **Space Complexity:** `O(L)`, because only one word is stored at a time. Since the maximum word length is bounded by 100 characters, this is constant auxiliary space for the given constraints.

## Build and Run

Compile with GCC:

```bash
gcc solution16.c -o solution16
```

Run:

```bash
./solution16
```

## Source Code

<!-- SOURCE_CODE_START -->

### `solution16.c`

```c
#include <stdio.h>

int main(void){
    int i=0;
    int t=0;
    int k=0;
    int l=0;

    
    int maxLen=0;
    int nbWords=0;
    char word[100];
    int length[100];
    
    for (i=0; i<100; i++){
        length[i]=0;
    }
    
    
    scanf("%d", &nbWords);
    for (t=0; t<nbWords; t++){
        
        scanf("%s", word);
        l=0;
        while (word[l] != '\0'){
            l++;
        }
        length[l] = length[l]+1;
        
        
    }
    
    for (k=0; k<100; k++){
        
        if (k > maxLen && length[k] !=0 ){
            maxLen=k;
        }
    }
    printf("%d", maxLen);
    
}
```

<!-- SOURCE_CODE_END -->
