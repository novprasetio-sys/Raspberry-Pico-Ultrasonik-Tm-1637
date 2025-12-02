# Raspberry-Pico-Ultrasonik-Tm-1637
# Berikut ini adalah cara setup dan debug raspberry pico + ultrasonik + tm 1637
# berbeda dengan Arduino, micro python tidak mengompile code
# kode disimpan di raspberry pico sebagai file py

# berikut kodenya
# buat file tm1637.py dan simpan di raspberry pico

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


#setelah itu buat kembali file main. py yang berfungsi sebagai file utama eksekusi mikrokontroler
# simpan kode ini di raspberry pico dengan nama main. py

from machine import Pin, time_pulse_us
import utime
from tm1637 import TM1637

# Ultrasonic pins
TRIG = Pin(3, Pin.OUT)
ECHO = Pin(2, Pin.IN)

# TM1637 pins (GP4=CLK, GP5=DIO)
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

# jalankan pico dengan adapter
# pico akan membaca sensor dan menampilkan ke 7 segment



