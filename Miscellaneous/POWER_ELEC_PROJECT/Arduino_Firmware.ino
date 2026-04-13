/*
 * -------------------------------------------------------------------------
 * Single-Phase Fully Controlled SCR Bridge Rectifier 
 * Target Hardware: ATmega328P (Arduino Uno Rev3)
 * Power Stage: 4x TYN612 SCRs, 4x MOC3021 Optoisolators
 * ZCD: PC817 Module via Center-Tapped 9-0-9V Full-Wave Rectifier
 * Load: 6V N20 DC Motor (with parallel dummy bleed resistor)
 * -------------------------------------------------------------------------
 */

// --- Pin Definitions ---
const int ZCD_PIN = 2;   // INT0: Hardware Interrupt for Zero-Crossing
const int SCR1_PIN = 4;  // D4: MOC3021 #1
const int SCR2_PIN = 5;  // D5: MOC3021 #2
const int SCR3_PIN = 6;  // D6: MOC3021 #3
const int SCR4_PIN = 7;  // D7: MOC3021 #4
const int POT_PIN = A0;  // A0: 10kΩ Potentiometer for Speed Control

// --- Global Volatile Variables ---
// Shared between the main loop and the Interrupt Service Routines (ISRs)
volatile unsigned int timerCompareValue = 0;

void setup() {
  // 1. Configure I/O Pins
  // ZCD pin uses internal pull-up. The PC817 pulls it LOW during the cycle
  // and releases it HIGH precisely at the zero-crossing.
  pinMode(ZCD_PIN, INPUT_PULLUP);

  pinMode(SCR1_PIN, OUTPUT);
  pinMode(SCR2_PIN, OUTPUT);
  pinMode(SCR3_PIN, OUTPUT);
  pinMode(SCR4_PIN, OUTPUT);

  // 2. Ensure all SCR gates are definitively OFF at boot
  digitalWrite(SCR1_PIN, LOW);
  digitalWrite(SCR2_PIN, LOW);
  digitalWrite(SCR3_PIN, LOW);
  digitalWrite(SCR4_PIN, LOW);

  // 3. Suspend global interrupts to configure hardware registers safely
  noInterrupts();

  // --- Timer1 Configuration (16-bit Timer) ---
  TCCR1A = 0;  // Clear Timer1 Control Register A
  TCCR1B = 0;  // Clear Timer1 Control Register B (Ensures timer is stopped)
  TCNT1 = 0;   // Initialize counter value to 0

  // --- External Interrupt Configuration ---
  // Attach interrupt to D2 (INT0). Trigger on RISING edge when AC hits 0V.
  attachInterrupt(digitalPinToInterrupt(ZCD_PIN), zeroCrossingISR, RISING);

  // 4. Re-enable global interrupts
  interrupts();
}

void loop() {
  // 1. Read the user throttle input (Values: 0 to 1023)
  int potValue = analogRead(POT_PIN);

  // 2. Map the ADC value to a safe firing angle (α) delay window
  // 50Hz AC frequency = 10,000 µs per half-cycle.
  // 9000 µs = Late firing (Motor OFF or very slow)
  // 1000 µs = Early firing (Motor at maximum speed)
  long delayUs = map(potValue, 0, 1023, 9000, 1000);

  // 3. Convert Microsecond Delay to Timer Ticks
  // ATmega328P clock is 16 MHz. With a prescaler of 8, the timer runs at 2 MHz.
  // 2 MHz = 2 ticks per microsecond.
  unsigned int calculatedTicks = delayUs * 2;

  // 4. Safely update the shared volatile variable
  noInterrupts();
  timerCompareValue = calculatedTicks;
  interrupts();

  // Short blocking delay to stabilize the ADC readings and prevent register thrashing
  delay(10);
}

// -------------------------------------------------------------------------
// ISR 1: Zero-Crossing Detector
// Executes instantly when the AC wave hits 0V
// -------------------------------------------------------------------------
void zeroCrossingISR() {
  TCCR1B = 0;                           // Stop Timer1
  TCNT1 = 0;                            // Reset counter to 0
  OCR1A = timerCompareValue;            // Load the target delay duration
  TIFR1 |= (1 << OCF1A);                // Clear any pending compare match flags
  TIMSK1 |= (1 << OCIE1A);              // Enable Timer1 Compare Match A Interrupt
  TCCR1B = (1 << WGM12) | (1 << CS11);  // Start Timer1 in CTC Mode with Prescaler = 8
}

// -------------------------------------------------------------------------
// ISR 2: Timer1 Compare Match
// Executes instantly when the precise firing angle (α) delay has elapsed
// -------------------------------------------------------------------------
ISR(TIMER1_COMPA_vect) {
  TCCR1B = 0;  // Stop Timer1 so it does not cycle again until the next zero-crossing

  // Direct Port Manipulation: Turn D4, D5, D6, and D7 HIGH simultaneously.
  // Binary 11110000 (0xF0) sets pins 4 through 7 high in exactly one clock cycle.
  PORTD |= 0b11110000;

  // Gate Trigger Pulse Width: Hold the logic HIGH for 200 microseconds.
  // This provides sufficient charge injection to confidently latch the TYN612 SCRs.
  // Note: delayMicroseconds is safe inside an ISR for brief, deterministic intervals.
  delayMicroseconds(200);

  // Direct Port Manipulation: Turn D4, D5, D6, and D7 LOW simultaneously.
  // Binary 00001111 (0x0F) clears pins 4 through 7 instantly.
  PORTD &= 0b00001111;
}
