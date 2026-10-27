# Tug of War — Team Weight Calculator

[![Language](https://img.shields.io/badge/Language-C-blue.svg)](https://en.wikipedia.org/wiki/C_(programming_language))
[![Time Complexity](https://img.shields.io/badge/Time-O(n)-brightgreen.svg)](#complexity-analysis)
[![Space Complexity](https://img.shields.io/badge/Space-O(1)-orange.svg)](#complexity-analysis)

## Problem Description

Given an equal number of players on two Tug of War teams, determine which team has the greater total weight.

Player weights are provided as integers in alternating order, starting with Team 1: Team 1 Player 1, Team 2 Player 1, Team 1 Player 2, Team 2 Player 2, and so on.

The program calculates each team's total weight, identifies the team with the advantage, and displays both totals.

## Approach

1. Read the number of players per team, `n`.
2. Initialize both team weight totals to zero.
3. Read `2n` player weights.
4. Assign even-indexed weights to Team 1 and odd-indexed weights to Team 2, because the first weight is for Team 1.
5. Compare the totals and print the team with the greater weight.
6. Display the total weight of both teams.

## Source Code

The source file is [`solution1.c`](./solution1.c). The code below is synchronized from that file by the repository workflow.

<!-- SOURCE_CODE_START -->

```c
#include <stdio.h>


int main(void){
    
    
    int numOfPlayers;
    int weight_team1=0;
    int weight_team2=0;
    int playerWeight;
    int i;
    scanf("%d", &numOfPlayers);
    
    for (i=0; i<(2*numOfPlayers) ; i++){
        
        scanf("%d", &playerWeight);
        
        if (i%2 == 0){
            weight_team1=weight_team1+playerWeight;
        }
            
        else {
            weight_team2=weight_team2+playerWeight;
        }
    }
    if (weight_team1 > weight_team2){
        printf("Team 1 has an advantage\n");
        
    } else{
        printf("Team 2 has an advantage\n");
    }
    
    printf("Total weight for team 1: %d\n", weight_team1);
    printf("Total weight for team 2: %d\n", weight_team2);
    
}
```

<!-- SOURCE_CODE_END -->

## Example

### Input

```text
4
110
106
113
102
112
121
117
111
```

### Output

```text
Team 1 has an advantage
Total weight for team 1: 452
Total weight for team 2: 440
```

## Complexity Analysis

- **Time Complexity:** `O(n)` — each of the `2n` player weights is processed once.
- **Space Complexity:** `O(1)` — the program uses a fixed number of variables.

## Build and Run

Compile with GCC from this folder:

```bash
gcc -Wall -Wextra -std=c11 solution1.c -o solution1
```

Run on Linux or macOS:

```bash
./solution1
```

The program reads input from standard input and prints only the required output.

## Assumptions

- Both teams have the same number of players.
- Player weights are integers in kilograms.
- The teams have different total weights, as guaranteed by the problem statement.
