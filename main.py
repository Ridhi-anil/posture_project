import customtkinter as ctk
import threading
import time
from posture import detect_posture
from exercises import get_exercise, get_exercise_media

from PIL import Image, ImageTk, ImageSequence

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CHECK_INTERVAL = 10   # Change to 1800 for 30 mins

running = False
paused = False
time_left = CHECK_INTERVAL


# ---------------- ALERT WINDOW ---------------- #

def show_alert(posture, exercise):
    global paused

    paused = True  # Pause timer

    alert = ctk.CTkToplevel(app)
    alert.geometry("520x520")
    alert.title("Posture Alert")
    alert.grab_set()

    card = ctk.CTkFrame(alert, corner_radius=20)
    card.pack(fill="both", expand=True, padx=20, pady=20)

    alert_title = ctk.CTkLabel(
        card,
        text="⚠ POSTURE ALERT",
        font=("Arial", 24, "bold"),
        text_color="red"
    )
    alert_title.pack(pady=(20, 10))

    posture_label = ctk.CTkLabel(
        card,
        text=f"Issue Detected: {posture}",
        font=("Arial", 18)
    )
    posture_label.pack(pady=5)

    exercise_label = ctk.CTkLabel(
        card,
        text=f"Recommended Exercise:\n{exercise}",
        font=("Arial", 15),
        wraplength=420,
        text_color="gray"
    )
    exercise_label.pack(pady=10)

    # ----------- LOAD & PLAY GIF -----------
    gif_path = get_exercise_media(posture)

    gif_label = ctk.CTkLabel(card, text="")
    gif_label.pack(pady=10)

    if gif_path:
        gif = Image.open(gif_path)
        frames = [
            ImageTk.PhotoImage(frame.copy().resize((280, 280)))
            for frame in ImageSequence.Iterator(gif)
        ]

        def animate(index=0):
            if paused:  # Keep animating while paused
                gif_label.configure(image=frames[index])
                alert.after(100, animate, (index + 1) % len(frames))

        animate()

    # ----------- CLOSE BUTTON -----------

    def close_alert():
        global paused
        paused = False
        alert.destroy()

    ok_button = ctk.CTkButton(
        card,
        text="I Will Fix It 💪",
        height=45,
        width=220,
        corner_radius=25,
        font=("Arial", 15, "bold"),
        command=close_alert
    )
    ok_button.pack(pady=15)


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
    global running, time_left

    if not running:
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


# ---------------- MAIN WINDOW ---------------- #

app = ctk.CTk()
app.geometry("650x450")
app.title("AI Posture Guardian")
app.resizable(False, False)

main_frame = ctk.CTkFrame(app, corner_radius=0)
main_frame.pack(fill="both", expand=True)

title = ctk.CTkLabel(
    main_frame,
    text="AI POSTURE GUARDIAN",
    font=("Arial", 32, "bold")
)
title.pack(pady=(30, 5))

subtitle = ctk.CTkLabel(
    main_frame,
    text="Smart Monitoring • Smart Correction • Smart You",
    font=("Arial", 14),
    text_color="gray"
)
subtitle.pack(pady=(0, 30))

status_card = ctk.CTkFrame(main_frame, corner_radius=20)
status_card.pack(padx=40, fill="x")

status_label = ctk.CTkLabel(
    status_card,
    text="Monitoring Not Started",
    font=("Arial", 18),
    text_color="red"
)
status_label.pack(pady=15)

timer_card = ctk.CTkFrame(main_frame, corner_radius=20)
timer_card.pack(padx=40, pady=25, fill="x")

timer_label = ctk.CTkLabel(
    timer_card,
    text="00:00",
    font=("Arial", 48, "bold"),
    text_color="#00FFAA"
)
timer_label.pack(pady=15)

timer_sub = ctk.CTkLabel(
    timer_card,
    text="Next Posture Check",
    font=("Arial", 14),
    text_color="gray"
)
timer_sub.pack(pady=(0, 10))

button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
button_frame.pack(pady=20)

start_button = ctk.CTkButton(
    button_frame,
    text="START MONITORING",
    command=start_monitoring,
    height=50,
    width=200,
    corner_radius=25,
    font=("Arial", 16, "bold")
)
start_button.grid(row=0, column=0, padx=15)

stop_button = ctk.CTkButton(
    button_frame,
    text="STOP",
    command=stop_monitoring,
    height=50,
    width=150,
    corner_radius=25,
    fg_color="#aa2222",
    hover_color="#cc3333",
    font=("Arial", 16, "bold")
)
stop_button.grid(row=0, column=1, padx=15)

app.mainloop()
