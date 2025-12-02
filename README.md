# Raspberry Pico — Ultrasonik + TM1637 (MicroPython)

Project ini menjelaskan cara setup dan debugging **Raspberry Pi Pico** menggunakan:
- Sensor Ultrasonik HC-SR04  
- Display 7-segment TM1637  
- MicroPython (tanpa proses compile seperti Arduino)  

Pada MicroPython, kode disimpan sebagai file `.py` di penyimpanan Pico.  
File utama yang akan dieksekusi otomatis adalah **main.py**.

---

## 📁 File 1 — tm1637.py  
Buat file bernama **tm1637.py** dan upload ke Pico.

```python
from machine import Pin
from time import sleep_us

SEGMENTS = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F]

class TM1637:
    def __init__(self, clk, dio, brightness=7):
        self.clk = Pin(clk, Pin.OUT)
        self.dio = Pin(dio, Pin.OUT)
        self.brightness = brightness

    def start(self):
        self.dio(1)
        self.clk(1)
        self.dio(0)

    def stop(self):
        self.clk(0)
        self.dio(0)
        self.clk(1)
        self.dio(1)

    def write_byte(self, data):
        for i in range(8):
            self.clk(0)
            self.dio((data >> i) & 1)
            self.clk(1)

        self.clk(0)
        self.dio.init(Pin.IN)
        self.clk(1)
        ack = self.dio()
        self.dio.init(Pin.OUT)
        return ack

    def show_number(self, num):
        s = "{:0>4}".format(int(num))[-4:]
        data = [SEGMENTS[int(c)] for c in s]

        self.start()
        self.write_byte(0x40)
        self.stop()

        self.start()
        self.write_byte(0xC0)
        for d in data:
            self.write_byte(d)
        self.stop()

        self.start()
        self.write_byte(0x88 | self.brightness)
        self.stop()



# main.py code

from machine import Pin, time_pulse_us
import utime
from tm1637 import TM1637

# Ultrasonic pins
TRIG = Pin(3, Pin.OUT)
ECHO = Pin(2, Pin.IN)

# TM1637 pins (GP4 = CLK, GP5 = DIO)
tm = TM1637(4, 5)

def get_distance():
    TRIG.low()
    utime.sleep_us(5)
    TRIG.high()
    utime.sleep_us(10)
    TRIG.low()

    duration = time_pulse_us(ECHO, 1, 30000)
    distance = (duration / 2) / 29.1
    return distance

while True:
    d = get_distance()
    print("Jarak:", d)
    tm.show_number(int(d))
    utime.sleep(0.3)