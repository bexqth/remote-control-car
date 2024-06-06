"""Module for controlling a serial led light."""

from machine import Pin
import neopixel


class SerialRGBLed:
    """Module for controlling a serial led light."""

    def __init__(self, pin, number):
        """Set pins of the serial led light."""
        self.led = neopixel.NeoPixel(Pin(pin), number)

    def set_color(self, r, g, b, number):
        """Change the color of selected one."""
        self.led[number] = (r, g, b)
        self.led.write()

    def set_all_color(self, r, g, b):
        """Change color of all of them."""
        self.led.fill((r, g, b))
        self.led.write()
