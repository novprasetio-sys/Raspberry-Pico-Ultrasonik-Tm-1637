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