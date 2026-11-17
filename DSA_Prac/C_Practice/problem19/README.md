# Metric to Imperial Conversion

## Problem Description

The program converts measurements from the metric system to the imperial system. It first reads the number of conversions to perform. Each subsequent input contains a numeric value followed by a unit:

- `m`: meters, converted to feet (`ft`)
- `g`: grams, converted to pounds (`lbs`)
- `c`: degrees Celsius, converted to degrees Fahrenheit (`f`)

The conversion formulas are:

- **Meters to feet:** `feet = meters * 3.2808`
- **Grams to pounds:** `pounds = grams * 0.002205`
- **Celsius to Fahrenheit:** `fahrenheit = 32 + 1.8 * celsius`

All values must be stored and displayed as `double` values. Each result is printed immediately, with six digits after the decimal point, followed by a space and its output unit.

## Example

**Input**
```text
4
10 m
1245.243 g
37.2 c
23 g
```

**Output**
```text
32.808000 ft
2.745761 lbs
98.960000 f
0.050715 lbs
```

## Approach

1. Read the number of conversions.
2. Process each conversion one at a time:
   - Read the numeric measurement as a `double`.
   - Read its unit as a `char`.
   - Use an `if` / `else if` structure to identify the unit.
   - Apply the corresponding conversion formula.
   - Print the converted value with `%.6f`, followed by the appropriate output unit.
3. Print each result immediately before reading the next measurement.

## Complexity Analysis

Let `N` be the number of conversions.

- **Time Complexity:** `O(N)`, because each conversion is processed once using a constant number of operations.
- **Space Complexity:** `O(1)`, because only a fixed number of variables are required.

## Build and Run

Compile with GCC:

```bash
gcc solution19.c -o solution19
```

Run:

```bash
./solution19
```

## Source Code

<!-- SOURCE_CODE_START -->

<!-- SOURCE_CODE_END -->
