# 🤖 Kode Pengukur Jarak Ultrasonik dengan Raspberry Pi Pico dan Display TM1637

Kode ini ditulis dalam **MicroPython** dan dirancang untuk **Raspberry Pi Pico**.

## ⚙️ Keterangan Pin dan Inisialisasi

* **Sensor Ultrasonik (HC-SR04):** Menggunakan pin GPIO 2 (ECHO) dan GPIO 3 (TRIG).
* **Display 4 Digit 7-Segment (TM1637):** Menggunakan pin GPIO 4 (CLK) dan GPIO 5 (DIO).

```python
from machine import Pin, time_pulse_us
import utime
from tm1637 import TM1637 # Memerlukan library tm1637.py

# Pin Ultrasonik
TRIG = Pin(3, Pin.OUT)
ECHO = Pin(2, Pin.IN)

# Pin TM1637 (GP4 = CLK, GP5 = DIO)
tm = TM1637(4, 5)

def get_distance():
    # Trigger pulsa
    TRIG.low()
    utime.sleep_us(5)
    TRIG.high()
    utime.sleep_us(10)
    TRIG.low()

    # Hitung durasi pulsa balikan (maks 30ms)
    duration = time_pulse_us(ECHO, 1, 30000)
    
    # Konversi durasi menjadi jarak (cm)
    # 29.1 µs/cm adalah waktu tempuh suara untuk 1 cm
    distance = (duration / 2) / 29.1 
    return distance
while True:
    d = get_distance()
    print("Jarak:", d)
    # Tampilkan jarak (dibulatkan ke integer terdekat) pada display TM1637
    tm.show_number(int(d)) 
    utime.sleep(0.3) # Jeda 0.3 detik sebelum pengukuran berikutnya
