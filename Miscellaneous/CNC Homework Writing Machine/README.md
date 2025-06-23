# CNC Plotter – Arduino-Based Homework Writing Machine ✍️

![CNC Plotter Thumbnail](https://img.youtube.com/vi/Tq1Xrh2ECn4/maxresdefault.jpg)

## 🎥 Demonstration Video

Watch it in action here: [📺 CNC Plotter on YouTube](https://youtu.be/Tq1Xrh2ECn4?feature=shared)

---

## 📌 Project Overview

This project is a **CNC Plotter**, also referred to as an **Arduino-based Homework Writing Machine**. It automates the writing of text and drawing of images by mimicking the motion of human handwriting using stepper motors and a servo mechanism.

The plotter is controlled using an **Arduino Uno** and a **CNC Shield**, driving two **NEMA 17 stepper motors** for the X and Y axes and one **SG90 servo motor** for pen up/down motion.

### ✨ Key Features

- ✅ 3D-printed frame using PLA material
- ✅ Arduino Uno + CNC Shield based control system
- ✅ Writes any **text** or **image** via G-code
- ✅ Servo-controlled pen lift mechanism
- ✅ Supports conversion of text/images into G-code using tools like Inkscape + plugins

---

## 🛠️ Hardware Used

- 🧠 Arduino Uno
- 🛡 CNC Shield (compatible with A4988 drivers)
- ⚙️ 2 × NEMA 17 Stepper Motors
- 🔄 1 × SG90 Servo Motor (for Z-axis pen lift)
- 🔧 3D Printed parts (PLA material)
- 💡 Power supply (12V recommended)

---

## 🧩 Software & Tools

- Arduino IDE (for firmware)
- GRBL firmware (loaded onto Arduino)
- Universal G-code Sender (UGS) for sending G-code
- Inkscape with G-code plugin (for converting text/images to G-code)

---

## 📐 How It Works

1. Design or write your desired text/image in Inkscape.
2. Convert the design to G-code using the G-code extension plugin.
3. Upload GRBL firmware to Arduino Uno using Arduino IDE.
4. Use Universal G-code Sender to send the G-code to Arduino via USB.
5. The CNC Plotter writes/draws the content by moving the pen with precision.
