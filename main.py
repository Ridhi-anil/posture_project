import customtkinter as ctk
import threading
import time
from posture import detect_posture
from exercises import get_exercise

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CHECK_INTERVAL = 10   # Change to 10 for testing

running = False
time_left = CHECK_INTERVAL

# ---------------- ALERT WINDOW ---------------- #


def show_alert(posture, exercise):
    alert = ctk.CTkToplevel()
    alert.geometry("400x300")
    alert.title("Posture Alert")

    alert_label = ctk.CTkLabel(
        alert,
        text=f"Detected: {posture}",
        font=("Arial", 20, "bold"),
        text_color="red"
    )
    alert_label.pack(pady=20)

    exercise_label = ctk.CTkLabel(
        alert,
        text=f"Suggested Exercise:\n\n{exercise}",
        font=("Arial", 16),
        wraplength=350
    )
    exercise_label.pack(pady=10)

    close_button = ctk.CTkButton(alert, text="OK", command=alert.destroy)
    close_button.pack(pady=20)


# ---------------- DETECTION ---------------- #

def run_detection():
    posture = detect_posture()
    exercise = get_exercise(posture)
    show_alert(posture, exercise)


# ---------------- TIMER ---------------- #

def countdown():
    global time_left

    while running:
        mins, secs = divmod(time_left, 60)
        timer_label.configure(text=f"Next Check In: {mins:02d}:{secs:02d}")
        time.sleep(1)
        time_left -= 1

        if time_left <= 0:
            run_detection()
            time_left = CHECK_INTERVAL


def start_monitoring():
    global running
    global time_left

    if not running:
        running = True
        time_left = CHECK_INTERVAL
        threading.Thread(target=countdown, daemon=True).start()
        status_label.configure(text="Monitoring Active", text_color="green")


# ---------------- MAIN WINDOW ---------------- #

app = ctk.CTk()
app.geometry("500x350")
app.title("AI Smart Posture Monitor")

title = ctk.CTkLabel(
    app,
    text="AI Smart Posture Monitor",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)

status_label = ctk.CTkLabel(
    app,
    text="Not Started",
    font=("Arial", 16),
    text_color="red"
)
status_label.pack(pady=10)

timer_label = ctk.CTkLabel(
    app,
    text="Next Check In: --:--",
    font=("Arial", 18)
)
timer_label.pack(pady=10)

start_button = ctk.CTkButton(
    app,
    text="Start Monitoring",
    command=start_monitoring,
    height=40,
    width=200
)
start_button.pack(pady=20)

app.mainloop()
