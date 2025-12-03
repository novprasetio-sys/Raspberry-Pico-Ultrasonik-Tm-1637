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
        print("Invalid data:", …
