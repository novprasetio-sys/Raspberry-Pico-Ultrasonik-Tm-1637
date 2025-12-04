from machine import Pin
import time

ir_sensor = Pin(2, Pin.IN, Pin.PULL_UP)
led_builtin = Pin(25, Pin.OUT)
buzzer = Pin(4, Pin.OUT)

state = 0  # 0=LOCKED, 1=UNLOCKED
led_builtin.value(0)
buzzer.value(1)  # inactive

def buzzer_beep(duration=3):
    buzzer.value(0)
    time.sleep(duration)
    buzzer.value(1)

def unlock_sequence():
    global state
    state = 1
    led_builtin.value(1)
    buzzer_beep()
    print("UNLOCKED")  # dikirim ke GUI
    time.sleep(5)      # pintu terbuka selama 5 detik
    lock_sequence()

def lock_sequence():
    global state
    state = 0
    led_builtin.value(0)
    buzzer_beep()
    print("LOCKED")    # dikirim ke GUI

while True:
    if ir_sensor.value() == 0 and state == 0:
        unlock_sequence()
    time.sleep(0.1)
