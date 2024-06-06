import network
from machine import Pin, PWM, SoftI2C
import time
import socket
from GameConsole.Button import Button
import ssd1306
import gfx

button_up = Button(14, Pin.PULL_DOWN)
button_down = Button(15, Pin.PULL_DOWN)
button_left = Button(2, Pin.PULL_DOWN)
button_right = Button(4, Pin.PULL_DOWN)

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled  = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
graphics = gfx.GFX(oled_width, oled_height, oled.pixel)

oled.fill(0)
oled.text("Connecting", oled_width // 4 - 10, oled_height // 2, 1)
oled.show()

nic = network.WLAN(network.AP_IF)
nic.active(True)
nic.config(essid='wifi', authmode = 3, password = 'kuraciabageta')
print(nic.ifconfig())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.4.1', 234))
s.listen()

conn, address = s.accept()
print('Got a connection from %s' % str(address))
oled.fill(0)
oled.text("Connected", oled_width // 4, oled_height // 2, 1)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()
last_button_state = None

while True:
    current_button_state = None
        
    if button_up.pin.value() == 1 and button_left.pin.value() == 1:
        current_button_state = 'UpLeft'

    elif button_up.pin.value() == 1 and button_right.pin.value() == 1:
        current_button_state = 'UpRight'

    elif button_down.pin.value() == 1 and button_left.pin.value() == 1:
        current_button_state = 'DownLeft'

    elif button_down.pin.value() == 1 and button_right.pin.value() == 1:
        current_button_state = 'DownRight'

    elif button_up.pin.value() == 1:
        current_button_state = 'Up'
    elif button_down.pin.value() == 1:
        current_button_state = 'Down'
        
    elif button_left.pin.value() == 1:
        current_button_state = 'Left'
        
    elif button_right.pin.value() == 1:
        current_button_state = 'Right'
    else:
        current_button_state = 'Stop'

    if current_button_state != last_button_state:
        conn.send(current_button_state)
        estimated_speed_kmph = str(conn.recv(1024), 'UTF-8')
        estimated_speed_kmph = round(float(estimated_speed_kmph), 2)
        #print(f"Received estimated speed: {estimated_speed_kmph} km/h")  # Print the received speed
        last_button_state = current_button_state
        oled.fill(0)
        oled.text(str(estimated_speed_kmph) + " km/h", oled_width // 4, oled_height // 2, 1)
        oled.show()
    time.sleep(0.2)

conn.close()