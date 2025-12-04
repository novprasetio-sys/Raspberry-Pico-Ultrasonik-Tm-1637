from machine import Pin, time_pulse_us
import utime
from tm1637 import TM1637

# Ultrasonic pins
TRIG = Pin(3, Pin.OUT)
ECHO = Pin(2, Pin.IN)

# TM1637 pins (CLK=GP4, DIO=GP5)
tm = TM1637(clk=Pin(4), dio=Pin(5))

def get_distance():
    TRIG.low()
    utime.sleep_us(5)
    TRIG.high()
    utime.sleep_us(10)
    TRIG.low()

    duration = time_pulse_us(ECHO, 1, 30000)
    distance = (duration / 2) / 29.1  # cm
    return distance

while True:
    d = get_distance()
    print(d)           # Kirim float murni ke serial
    tm.show_number(int(d))
    utime.sleep(0.3)