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
