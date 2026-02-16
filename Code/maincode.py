import board
import digitalio
import neopixel
import time
import usb_hid
import displayio
import adafruit_displayio_ssd1306
import os
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from i2cdisplaybus import I2CDisplayBus
what 
# ==========================================
# CONFIGURATION
# ==========================================
# Pins
ROW_PINS = (board.D10, board.D9, board.D8)
COL_PINS = (board.D0, board.D1, board.D2, board.D3)
NEOPIXEL_PIN = board.D6

# Display Settings
ANIMATION_FOLDER = "/animation_bmps"
FRAME_DURATION = 0.2  # Seconds between animation frames

# Lighting Physics
LED_BRIGHTNESS = 0.3    # Base brightness
MAX_BRIGHTNESS = 1.0    # Peak brightness on press
FADE_SPEED = 0.008      # How fast the main key fades out
RIPPLE_SPEED = 0.02     # How fast the neighbor keys fade out
SPREAD_DELAY = 0.01     # Delay before light spreads to neighbors

# Key Map: (Column, Row) -> Keycode
KEY_MAP = {
    (0, 0): Keycode.SEVEN,   (0, 1): Keycode.EIGHT, (0, 2): Keycode.NINE,
    (1, 0): Keycode.FOUR,    (1, 1): Keycode.FIVE,  (1, 2): Keycode.SIX,
    (2, 0): Keycode.ONE,     (2, 1): Keycode.TWO,   (2, 2): Keycode.THREE,
    (3, 0): Keycode.WINDOWS, (3, 1): Keycode.ZERO,  (3, 2): Keycode.PERIOD
}

# LED Map: (Column, Row) -> NeoPixel Index
# Adjust this based on your wiring order
LED_MAP = {
    (0, 0): 9, (0, 1): 10, (0, 2): 11,
    (1, 0): 8, (1, 1): 7,  (1, 2): 6,
    (2, 0): 3, (2, 1): 4,  (2, 2): 5,
    (3, 0): 2, (3, 1): 1,  (3, 2): 0
}

class MacropadInput:
    """Handles scanning the matrix and sending HID commands."""
    def __init__(self):
        self.keyboard = Keyboard(usb_hid.devices)
        
        # Setup Rows (Inputs with Pull Up)
        self.rows = []
        for pin in ROW_PINS:
            r = digitalio.DigitalInOut(pin)
            r.direction = digitalio.Direction.INPUT
            r.pull = digitalio.Pull.UP
            self.rows.append(r)

        # Setup Cols (Outputs, default High)
        self.cols = []
        for pin in COL_PINS:
            c = digitalio.DigitalInOut(pin)
            c.direction = digitalio.Direction.OUTPUT
            c.value = True
            self.cols.append(c)

        self.previously_pressed = set()

    def scan_matrix(self):
        """Scans the physical matrix and returns a set of (col, row) tuples."""
        current_pressed = set()

        for c_index, col_pin in enumerate(self.cols):
            # Drive column low
            col_pin.value = False
            
            # Check rows
            for r_index, row_pin in enumerate(self.rows):
                # If row is low, the switch connects them
                if not row_pin.value:
                    current_pressed.add((c_index, r_index))
            
            # Reset column high
            col_pin.value = True
            
        return current_pressed

    def update(self):
        """Main update loop: reads matrix and sends keycodes."""
        pressed_keys = self.scan_matrix()
        
        # Determine changes
        new_presses = pressed_keys - self.previously_pressed
        released_keys = self.previously_pressed - pressed_keys

        # Send KeyDown events
        for key in new_presses:
            if key in KEY_MAP:
                self.keyboard.press(KEY_MAP[key])

        # Send KeyUp events
        for key in released_keys:
            if key in KEY_MAP:
                self.keyboard.release(KEY_MAP[key])

        self.previously_pressed = pressed_keys
        return pressed_keys

class ReactiveLighting:
    """Manages NeoPixel animations based on key activity."""
    def __init__(self):
        self.num_pixels