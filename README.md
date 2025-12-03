# MicPySer Gateway – Raspberry Pico → Python → Thingspeak

MicPySer Gateway adalah integrasi lengkap antara Raspberry Pi Pico (MicroPython), sensor ultrasonik, TM1637 seven-segment, dan Python sebagai data gateway ke Thingspeak menggunakan PySerial.

## 🔌 Arsitektur Sistem

## 📂 Struktur Project
### Folder micropython/
Kode MicroPython untuk:
- Membaca sensor HC-SR04
- Menampilkan jarak di TM1637
- Mengirim data ke serial dalam bentuk *float murni*

### Folder python_gateway/
Kode Python untuk:
- Membaca serial COM
- Menyimpan "last value" terbaru
- Mengirim nilai terbaru ke Thingspeak setiap 15 detik

## ▶️ Menjalankan Project

### 1. Upload MicroPython ke Pico
Gunakan Thonny → Upload file main.py ke root Pico.

### 2. Jalankan Python Gateway
Sesuaikan COM port & API Key:

## 📡 Thingspeak
- field1 = jarak (cm), nilai terbaru yang dibaca Pico

## 📊 Fitur Utama
✔ Anti-lag: hanya kirim *nilai terbaru* ke Thingspeak  
✔ Serial reading cepat, upload lambat (15s)  
✔ Tidak perlu modifikasi kode MicroPython  
✔ Akurat & stabil meski sensor cepat berubah  

---

## ✨ MicPySer = MicroPython + Python Serial Gateway  
Versi pertama dari framework IoT ringan berbasis MicroPython dan PySerial.

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




## 📁 File 2 — main.py  
Buat file bernama **main.py** dan upload ke Pico.

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


## python code gateway kirim data ke thingspeak


import serial
import time
import requests

SERIAL_PORT = "COM8"       # sesuaikan
BAUD_RATE = 115200

API_KEY = "YOUR_API_KEY"   # ganti pakai write API key Thingspeak
TS_URL = "https://api.thingspeak.com/update"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

last_value = None
last_upload = time.time()

def upload(value):
    try:
        r = requests.get(TS_URL, params={"api_key": API_KEY, "field1": value})
        print(f"Uploaded to Thingspeak: {value} cm")
    except Exception as e:
        print("Upload error:", e)

while True:
    raw = ser.readline().decode().strip()

    if raw == "":
        continue

    try:
        last_value = float(raw)
        print("New reading:", last_value)
    except:
        print("Invalid data:", raw)
        continue

    if time.time() - last_upload >= 15:
        if last_value is not None:
            upload(last_value)
            last_upload = time.time()