"""Module for controlling a button using the machine.Pin class."""

from machine import Pin
import time


class Button:
    """A class to represent a button."""

    def __init__(self, pin, pull):
        """Initialize the button with the given pin and pull."""
        self.pin = Pin(pin, Pin.IN, pull)

    def is_pressed(self):
        """Check if the button is pressed."""
        return self.pin.value()

    def print_status(self, button_boot):
        """Print the status of the button."""
        while button_boot.pin.value() == 1:
            if self.pin.value() == 0:
                print(self.name + "the button is pressed")
            else:
                print(self.name + "the button is not pressed")
            time.sleep(0.1)
