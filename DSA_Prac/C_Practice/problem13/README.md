# Chemical Process Temperature Monitor

## Problem Description

A monitoring device reads the temperature of a chemical process. The program first reads the minimum and maximum safe temperatures, followed by a sequence of temperature measurements.

For each measurement:
- Print `Nothing to report` if the temperature is within the safe range, including the minimum and maximum values.
- Print `Alert!` and stop processing if the temperature is below the minimum or above the maximum.
- Stop reading when the sentinel value `-999` is received. The sentinel is not a temperature measurement and must not trigger an alert.

## Examples

### Example 1

**Input**
```text
10 20
15 10 20 0 15 -999
```

**Output**
```text
Nothing to report
Nothing to report
Nothing to report
Alert!
```

### Example 2

**Input**
```text
0 100
15 50 75 -999
```

**Output**
```text
Nothing to report
Nothing to report
Nothing to report
```

## Approach

1. Read the minimum and maximum safe temperatures.
2. Read temperature measurements until either:
   - `-999` is received, indicating that measurements are finished; or
   - a measurement falls outside the safe range.
3. For a safe measurement, print `Nothing to report`.
4. For an unsafe measurement, print `Alert!` and stop processing immediately.
5. Do not treat `-999` as an actual temperature measurement.

## Complexity Analysis

Let `N` be the number of measurements processed before termination or the first unsafe reading.

- **Time Complexity:** `O(N)`, because each processed measurement is checked once.
- **Space Complexity:** `O(1)`, because only a fixed number of variables are used.

## Build and Run

Compile with GCC:

```bash
gcc solution13.c -o solution13
```

Run:

```bash
./solution13
```

## Source Code

<!-- SOURCE_CODE_START -->

### `solution13.c`

```c
#include <stdio.h>

int main(void){
    
    int temp_min, temp_max;
    scanf("%d", &temp_min);
    scanf("%d", &temp_max);
    int temp_measured;
    scanf("%d", &temp_measured);
    while ( (temp_measured <= temp_max && temp_measured >= temp_min) && (temp_measured != -999) ){
        printf("Nothing to report\n");
        scanf("%d", &temp_measured);
      
        
    }
    
    if ((temp_measured != -999 ) && (temp_measured < temp_min || temp_measured > temp_max )) {
        printf("Alert!\n");
    }
    
}
```

<!-- SOURCE_CODE_END -->
