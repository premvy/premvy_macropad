# ⌨️ Macropad

A custom 12-key macropad with per-key RGB lighting and an OLED display, powered by the Seeed XIAO RP2040. Designed with KiCad, SolidWorks, and Python.

Bill of Materials (BOM)

- 1x Seeed XIAO RP2040
- 12x Mechanical Switches
- 12x 1N4148 Diodes
- 12x SK6812 MINI-E RGB LEDs
- 1x 0.91" OLED Display (I2C)
- 1x Custom 3D Printed Case

# Project Gallery

1. System Schematic

![Description](https://github.com/premvy/premvy_macropad/blob/main/Images/Screenshot%202026-02-16%20122518.png)


The electrical blueprint detailing the RP2040 pinout, the 3x4 diode matrix logic, and I2C bus wiring for the peripherals.

2. PCB Layout & Routing

2-layer PCB routing in KiCad. Significant focus was placed on trace management for the addressable LED data line and maintaining a clean ground plane.

3. Enclosure CAD

Mechanical enclosure modeled in SolidWorks. The design features internal standoffs for the PCB and a precision-cut port for the XIAO’s USB-C interface.
