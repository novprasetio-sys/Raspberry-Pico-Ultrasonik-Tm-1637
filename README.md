MicPySer Embedded – Auto Door Lock System
Lightweight • Industrial Concept • Serial-Based Automation

MicPySer Embedded adalah sistem automatic electronic door lock berbasis Raspberry Pico dan MicroPython. Sistem ini membaca objek lewat IR sensor, mengaktifkan buzzer, menyalakan LED built-in, mengirimkan status via serial, dan ditampilkan secara real-time melalui GUI Python.

🚀 Fitur
- IR sensor mendeteksi objek → pintu UNLOCK otomatis
- LED built-in menyala saat UNLOCK dan mati saat LOCK
- Buzzer aktif 3 detik pada proses unlock & lock
- Pintu otomatis LOCK kembali setelah 5 detik
- Status real-time (UNLOCKED / LOCKED) dikirim ke PC
- GUI Python menampilkan status terbaru tanpa lag
- Komunikasi stabil via PySerial (COM10 @ 115200)

🛠️ Wiring Komponen
Raspberry Pico	Pin
IR Sensor OUT	GP2
Buzzer	GP4
LED Built-in	GP25
GND	GND
VCC	5V / 3.3V (sesuai sensor)
📟 Kode MicroPython – Raspberry Pico
pico_doorlock.py

from machine import Pin
import time

ir_sensor = Pin(2, Pin.IN, Pin.PULL_UP)
led_builtin = Pin(25, Pin.OUT)
buzzer = Pin(4, Pin.OUT)
state = 0 # 0=LOCKED, 1=UNLOCKED

led_builtin.value(0)
buzzer.value(1) # inactive

def buzzer_beep(duration=3):
    buzzer.value(0)
    time.sleep(duration)
    buzzer.value(1)

def unlock_sequence():
    global state
    state = 1
    led_builtin.value(1)
    buzzer_beep()
    print("UNLOCKED") # dikirim ke GUI
    time.sleep(5) # pintu terbuka selama 5 detik
    lock_sequence()

def lock_sequence():
    global state
    state = 0
    led_builtin.value(0)
    buzzer_beep()
    print("LOCKED") # dikirim ke GUI

while True:
    if ir_sensor.value() == 0 and state == 0:
        unlock_sequence()
    time.sleep(0.1)

🖥️ Kode GUI Python – PC/SBC
gui_door_status.py

import serial
import tkinter as tk
from tkinter import ttk
from threading import Thread

ser = serial.Serial("COM10", 115200, timeout=0.1)

root = tk.Tk()
root.title("MicPySer • Door Status")
root.geometry("350x200")

status_label = ttk.Label(root, text="WAITING...", font=("Arial", 28), foreground="gray")
status_label.pack(pady=40)

def update_status(text):
    if text == "UNLOCKED":
        status_label.config(text="UNLOCKED", foreground="green")
    elif text == "LOCKED":
        status_label.config(text="LOCKED", foreground="red")

def read_serial_loop():
    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                update_status(line)
        except:
            pass

thread = Thread(target=read_serial_loop, daemon=True)
thread.start()

root.mainloop()


▶️ Cara Menjalankan
1. Upload kode MicroPython
- Buka Thonny
- Pilih interpreter “Raspberry Pi Pico”
- Upload & Run pico_doorlock.py
2. Install PySerial di PC
- `pip install pyserial`
3. Jalankan GUI
- `python gui_door_status.py`
- GUI akan langsung membaca status UNLOCKED atau LOCKED setiap kali Pico mengirimkan print ke serial.

🔄 Alur Kerja Sistem
1. IR mendeteksi objek → state berubah menjadi UNLOCKED
2. LED menyala, buzzer aktif 3 detik
3. GUI menampilkan UNLOCKED (green)
4. Setelah 5 detik, Pico mengunci kembali otomatis
5. Buzzer aktif 3 detik → kirim LOCKED
6. GUI menampilkan LOCKED (red)