import sys
import os
import customtkinter as ctk
import threading
import time
from posture import detect_posture
from exercises import get_exercise, get_exercise_media
from PIL import Image, ImageTk, ImageSequence

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- DEFAULTS ---------------- #

CHECK_INTERVAL = 600  # default 10 minutes (in seconds)
running = False
paused = False
time_left = CHECK_INTERVAL


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ---------------- ALERT WINDOW ---------------- #

def show_alert(posture, exercise):
    global paused
    paused = True

    alert = ctk.CTkToplevel(app)
    alert.geometry("520x520")
    alert.title("Posture Alert")
    alert.grab_set()

    card = ctk.CTkFrame(alert, corner_radius=20)
    card.pack(fill="both", expand=True, padx=20, pady=20)

    ctk.CTkLabel(
        card,
        text="⚠ POSTURE ALERT",
        font=("Arial", 24, "bold"),
        text_color="red"
    ).pack(pady=(20, 10))

    ctk.CTkLabel(
        card,
        text=f"Issue Detected: {posture}",
        font=("Arial", 18)
    ).pack(pady=5)

    ctk.CTkLabel(
        card,
        text=f"Recommended Exercise:\n{exercise}",
        font=("Arial", 15),
        wraplength=420,
        text_color="gray"
    ).pack(pady=10)

    gif_path = get_exercise_media(posture)
    gif_label = ctk.CTkLabel(card, text="")
    gif_label.pack(pady=10)

    if gif_path:
        gif = Image.open(resource_path(gif_path))
        frames = [
            ImageTk.PhotoImage(frame.copy().resize((280, 280)))
            for frame in ImageSequence.Iterator(gif)
        ]

        def animate(index=0):
            if paused:
                gif_label.configure(image=frames[index])
                alert.after(100, animate, (index + 1) % len(frames))

        animate()

    def close_alert():
        global paused
        paused = False
        alert.destroy()

    ctk.CTkButton(
        card,
        text="I Will Fix It 💪",
        height=45,
        width=220,
        corner_radius=25,
        font=("Arial", 15, "bold"),
        command=close_alert
    ).pack(pady=15)


# ---------------- DETECTION ---------------- #

def run_detection():
    posture = detect_posture()

    if posture != "Good Posture":
        exercise = get_exercise(posture)
        show_alert(posture, exercise)
    else:
        status_label.configure(text="Perfect Posture ✅", text_color="#00FFAA")


# ---------------- TIMER ---------------- #

def countdown():
    global time_left, running, paused

    while running:
        if not paused:
            mins, secs = divmod(time_left, 60)
            timer_label.configure(text=f"{mins:02d}:{secs:02d}")

            time.sleep(1)
            time_left -= 1

            if time_left <= 0:
                status_label.configure(
                    text="Checking posture...", text_color="orange")
                run_detection()
                time_left = CHECK_INTERVAL
        else:
            time.sleep(1)


def start_monitoring():
    global running, time_left, CHECK_INTERVAL

    if running:
        return

    user_input = interval_entry.get().strip()

    if user_input == "":
        show_error("Enter interval in seconds (10 - 1800).")
        return

    try:
        seconds = int(user_input)

        if seconds < 10 or seconds > 1800:
            raise ValueError

        CHECK_INTERVAL = seconds

    except:
        show_error("Enter value between 10 and 1800 seconds.")
        return

    running = True
    time_left = CHECK_INTERVAL
    threading.Thread(target=countdown, daemon=True).start()
    status_label.configure(text="Monitoring Active", text_color="#00FFAA")


def stop_monitoring():
    global running, time_left
    running = False
    time_left = CHECK_INTERVAL
    timer_label.configure(text="00:00")
    status_label.configure(text="Monitoring Stopped", text_color="red")


# ---------------- ERROR POPUP ---------------- #

def show_error(message):
    error = ctk.CTkToplevel(app)
    error.geometry("350x150")
    error.title("Input Error")
    error.grab_set()

    ctk.CTkLabel(
        error,
        text=message,
        font=("Arial", 14)
    ).pack(pady=20)

    ctk.CTkButton(
        error,
        text="OK",
        command=error.destroy
    ).pack(pady=10)


# ---------------- MAIN WINDOW ---------------- #

app = ctk.CTk()
app.geometry("700x600")  # Increased height
app.title("AI Posture Guardian")
app.resizable(False, False)

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True)
main_frame.pack_propagate(False)

ctk.CTkLabel(
    main_frame,
    text="AI POSTURE GUARDIAN",
    font=("Arial", 32, "bold")
).pack(pady=(30, 5))

ctk.CTkLabel(
    main_frame,
    text="Smart Monitoring • Smart Correction • Smart You",
    font=("Arial", 14),
    text_color="gray"
).pack(pady=(0, 30))

# -------- INTERVAL INPUT --------

ctk.CTkLabel(
    main_frame,
    text="Monitoring Interval (seconds):",
    font=("Arial", 14)
).pack(pady=(10, 5))

interval_entry = ctk.CTkEntry(
    main_frame,
    width=200
)
interval_entry.insert(0, "600")  # 10 minutes default
interval_entry.pack(pady=(0, 20))

# -------- STATUS --------

status_card = ctk.CTkFrame(main_frame, corner_radius=20)
status_card.pack(padx=40, fill="x")

status_label = ctk.CTkLabel(
    status_card,
    text="Monitoring Not Started",
    font=("Arial", 18),
    text_color="red"
)
status_label.pack(pady=15)

# -------- TIMER --------

timer_card = ctk.CTkFrame(main_frame, corner_radius=20)
timer_card.pack(padx=40, pady=25, fill="x")

timer_label = ctk.CTkLabel(
    timer_card,
    text="00:00",
    font=("Arial", 48, "bold"),
    text_color="#00FFAA"
)
timer_label.pack(pady=15)

ctk.CTkLabel(
    timer_card,
    text="Next Posture Check",
    font=("Arial", 14),
    text_color="gray"
).pack(pady=(0, 10))

# -------- BUTTONS --------

button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
button_frame.pack(pady=30)

ctk.CTkButton(
    button_frame,
    text="START MONITORING",
    command=start_monitoring,
    height=50,
    width=220,
    corner_radius=25,
    font=("Arial", 16, "bold")
).grid(row=0, column=0, padx=15)

ctk.CTkButton(
    button_frame,
    text="STOP",
    command=stop_monitoring,
    height=50,
    width=180,
    corner_radius=25,
    fg_color="#aa2222",
    hover_color="#cc3333",
    font=("Arial", 16, "bold")
).grid(row=0, column=1, padx=15)

app.mainloop()
