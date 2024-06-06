import network
import socket
from machine import Pin, PWM
from zadanie_3.serialrgbled_class import SerialRGBLed

serial_led = SerialRGBLed(Pin(13), 3)
serial_led.set_all_color(0, 0, 0)

sensor = UltrasonicSensor(12, 14)

pwmLB = PWM(Pin(0), duty = 0, freq = 500)
pwmLF = PWM(Pin(4), duty = 0, freq = 500)
pwmRB = PWM(Pin(2), duty = 0, freq = 500)
pwmRF = PWM(Pin(15), duty = 0, freq = 500)

pin5 = Pin(5, Pin.OUT)
pin5.value(1)

pin22 = Pin(22, Pin.OUT)
pin22.value(1)

nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect('wifi','kuraciabageta')
while nic.isconnected()==False:
    pass
print(nic.status())
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 234))
s.connect(('192.168.4.1', 234))

full_speed = 300
half_speed = 200

full_speed_left = full_speed;
full_speed_right = full_speed + 110;

half_speed_left = half_speed;
half_speed_right = half_speed + 65;

def stop_all_motors():
    pwmLF.duty(0)
    pwmRF.duty(0)
    pwmLB.duty(0)
    pwmRB.duty(0)

def check_distance():
    sensor.print_distance()
    if sensor.get_distance() <= 8:
        return False
    else: 
        return True


max_duty_cycle = 1023  # Replace with your motor controller's max duty cycle
current_duty_cycle = 0  # Replace with your current duty cycle
max_speed_kmph = 10

while True:

    #s.write(str(sensor.get_distance()))
    text = str(s.recv(1023),'UTF-8')
    if text == 'Up':
        stop_all_motors()
        pwmRF.duty(full_speed_right)
        pwmLF.duty(full_speed_left)
        #pwmLB.duty(0)
        #pwmRB.duty(0)
        serial_led.set_color(0, 255, 0, 0)
        serial_led.set_color(0, 0, 0, 2)
        current_duty_cycle = full_speed
        estimated_speed_kmph = (current_duty_cycle / max_duty_cycle) * max_speed_kmph
        s.write(str(estimated_speed_kmph))
        #print(f"Estimated speed: {estimated_speed_kmph} km/h")
    elif text == 'Down':
        #pwmLF.duty(0)
        #pwmRF.duty(0)
        stop_all_motors()
        pwmRB.duty(full_speed_right)
        pwmLB.duty(full_speed_left)
        serial_led.set_color(0, 0, 0, 0)
        serial_led.set_color(255, 0, 0, 2)
        current_duty_cycle = full_speed
        estimated_speed_kmph = (current_duty_cycle / max_duty_cycle) * max_speed_kmph
        s.write(str(estimated_speed_kmph))
        #print(f"Estimated speed: {estimated_speed_kmph} km/h")
    elif text == 'Left':
        stop_all_motors()
        pwmRF.duty(half_speed_right)
        #pwmLF.duty(0)
        #pwmRB.duty(0)
        #pwmLB.duty(0)
        current_duty_cycle = half_speed_right
        estimated_speed_kmph = (current_duty_cycle / max_duty_cycle) * max_speed_kmph
        s.write(str(estimated_speed_kmph))
        #print(f"Estimated speed: {estimated_speed_kmph} km/h")
    elif text == 'Right':
        stop_all_motors()
        pwmLF.duty(half_speed_left)
        #pwmRF.duty(0)
        #pwmRB.duty(0)
        #pwmLB.duty(0)
        current_duty_cycle = half_speed_right
        estimated_speed_kmph = (current_duty_cycle / max_duty_cycle) * max_speed_kmph
        s.write(str(estimated_speed_kmph))
        #print(f"Estimated speed: {estimated_speed_kmph} km/h")
    elif text == 'UpLeft':
        stop_all_motors()
        pwmRF.duty(full_speed_right)
        pwmLF.duty(half_speed_left)
        #pwmRB.duty(0)
        #pwmLB.duty(0)
        current_duty_cycle = full_speed - (full_speed - half_speed) / 2
        serial_led.set_color(0, 0, 0, 2)
        serial_led.set_color(0, 255, 0, 0)
        estimated_speed_kmph = (current_duty_cycle / max_duty_cycle) * max_speed_kmph
        s.write(str(estimated_speed_kmph))
        #print(f"Estimated speed: {estimated_speed_kmph} km/h")
    elif text == 'UpRight':
        stop_all_motors()
        pwmLF.duty(full_speed_left)
        pwmRF.duty(half_speed_right)
        #pwmRB.duty(0)
        #pwmLB.duty(0)
        current_duty_cycle = full_speed - (full_speed - half_speed) / 2
        serial_led.set_color(0, 0, 0, 2)
        serial_led.set_color(0, 255, 0, 0)
        estimated_speed_kmph = (current_duty_cycle / max_duty_cycle) * max_speed_kmph
        s.write(str(estimated_speed_kmph))
        #print(f"Estimated speed: {estimated_speed_kmph} km/h")
    elif text == 'DownLeft':
        stop_all_motors()
        #pwmLF.duty(0)
        #pwmRF.duty(0)
        pwmLB.duty(half_speed_left)
        pwmRB.duty(full_speed_right)
        current_duty_cycle = full_speed - (full_speed - half_speed) / 2
        serial_led.set_color(0, 0, 0, 0)
        serial_led.set_color(255, 0, 0, 2)
        estimated_speed_kmph = (current_duty_cycle / max_duty_cycle) * max_speed_kmph
        s.write(str(estimated_speed_kmph))
        #print(f"Estimated speed: {estimated_speed_kmph} km/h")
    elif text == 'DownRight':
        stop_all_motors()
        #pwmLF.duty(0)
        #pwmRF.duty(0)
        pwmLB.duty(full_speed_left)
        pwmRB.duty(half_speed_right)
        current_duty_cycle = full_speed - (full_speed - half_speed) / 2
        serial_led.set_color(0, 0, 0, 0)
        serial_led.set_color(255, 0, 0, 2)
        estimated_speed_kmph = (current_duty_cycle / max_duty_cycle) * max_speed_kmph
        s.write(str(estimated_speed_kmph))
        #print(f"Estimated speed: {estimated_speed_kmph} km/h")
    else:
        #print('NONE')
        stop_all_motors()
        current_duty_cycle = 0
        estimated_speed_kmph = (current_duty_cycle / max_duty_cycle) * max_speed_kmph
        s.write(str(estimated_speed_kmph))
        #print(f"Estimated speed: {estimated_speed_kmph} km/h")
        serial_led.set_all_color(0, 0, 0)
    
s.close()
