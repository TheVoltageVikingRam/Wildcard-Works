# Tug of War — Team Weight Calculator

[![Language](https://img.shields.io/badge/Language-C-blue.svg)](https://en.wikipedia.org/wiki/C_(programming_language))
[![Complexity](https://img.shields.io/badge/Time-O(n)-brightgreen.svg)](#complexity-analysis)
[![Space](https://img.shields.io/badge/Space-O(1)-orange.svg)](#complexity-analysis)

## Problem Description

Given an equal number of players on two Tug of War teams, determine which team has the greater total weight.

Player weights are provided as integers in alternating order, starting with Team 1:

1. Team 1, Player 1
2. Team 2, Player 1
3. Team 1, Player 2
4. Team 2, Player 2
5. Continue until all players have been recorded.

The program calculates each team's total weight, identifies the team with the advantage, and displays both totals.

## Approach

- Read the number of players per team, `n`.
- Initialize both team weight totals to zero.
- Read `2n` player weights.
- Use the player's index to assign each weight to the correct team: even indices belong to Team 1, and odd indices belong to Team 2.
- Compare the totals and print the team with the greater weight.
- Display the total weight of both teams.

## Source Code

The implementation is maintained in [`solution1.c`](./solution1.c).

<!-- SOURCE_CODE_START -->

*The source code will be inserted here automatically by the repository workflow.*

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

## Assumptions

- Both teams have the same number of players.
- Player weights are integer values in kilograms.
- The two teams have different total weights, as guaranteed by the problem statement.

## Build and Run

Compile with GCC:

```bash
gcc -Wall -Wextra -std=c11 solution1.c -o solution1
```

Run on Linux or macOS:

```bash
./solution1
```

On Windows, run the generated executable:

```powershell
.\solution1.exe
```

The program reads input from standard input and prints only the required output.
