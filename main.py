import tkinter as tk
from tkinter import messagebox
import threading
import time
from posture import detect_posture
from exercises import get_exercise

# Change to 10 for testing, 1800 for 30 mins
CHECK_INTERVAL = 10


def run_detection():

    posture = detect_posture()
    exercise = get_exercise(posture)

    messagebox.showinfo(
        "Posture Alert",
        f"Detected Posture: {posture}\n\nSuggested Exercise:\n{exercise}"
    )


def background_timer():
    while True:
        time.sleep(CHECK_INTERVAL)
        run_detection()


def start_monitoring():
    threading.Thread(target=background_timer, daemon=True).start()
    status_label.config(text="Monitoring Started ✅")

# -------- GUI --------


root = tk.Tk()
root.title("AI Smart Posture Monitor")
root.geometry("400x250")

title = tk.Label(root, text="Smart Posture Monitor", font=("Arial", 16))
title.pack(pady=20)

start_button = tk.Button(root, text="Start Monitoring",
                         command=start_monitoring)
start_button.pack(pady=10)

status_label = tk.Label(root, text="Not Started")
status_label.pack(pady=10)

root.mainloop()
