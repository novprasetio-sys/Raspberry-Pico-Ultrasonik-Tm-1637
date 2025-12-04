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

