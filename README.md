#  PostureGuard AI  
### *Smart Monitoring. Smarter Habits. Healthier You.*

## Project Description

PostureGuard AI is an intelligent desktop application that uses computer vision to monitor a user’s posture in real time through a webcam. Built using MediaPipe and OpenCV, the system detects common posture issues such as hunched shoulders, uneven shoulders, forward head posture, and leaning too close to the screen. When poor posture is detected, the application provides instant alerts along with guided corrective exercises using animated demonstrations. The app runs locally as a standalone desktop application, ensuring privacy and offline functionality.



##  Tech Stack

- Python 3.10  
- OpenCV  
- MediaPipe  
- CustomTkinter  
- Pillow  
- PyInstaller  



##  Features

- Real-time posture detection using webcam  
- Smart interval-based posture monitoring  
- Animated corrective exercise guidance (GIF support)  
- Modern dark-themed graphical interface  
- Start and Stop monitoring controls  
- Countdown timer for posture checks  
- Deployable Windows `.exe` application  



## Project Structure
PostureGuard-AI/
│
├── main.py
├── posture.py
├── exercises.py
├── assets/
│ ├── shoulder_roll.gif
│ ├── side_stretch.gif
│ ├── Chin_tucks.gif
│ └── neck_stretch.gif
├── screenshots/
└── README.md


---

## Installation

###  Clone the Repository

https://github.com/Ridhi-anil/posture_project
cd PostureGuard-AI

## Create Virtual Environment
python -m venv venv
venv\Scripts\activate

## Install Dependencies
pip install opencv-python mediapipe customtkinter pillow

## Run the Application
python main.py

## Screenshots
<img width="527" height="470" alt="image" src="https://github.com/user-attachments/assets/c91aee4c-3d80-4f22-88ce-bda868d632ae" />
<img width="390" height="411" alt="image" src="https://github.com/user-attachments/assets/359adb89-1239-4be8-80c0-b7fbe70e8e54" />
<img width="384" height="409" alt="image" src="https://github.com/user-attachments/assets/b6535153-afc0-46fb-bc4f-559c462773b9" />

## Demo Video
https://drive.google.com/drive/folders/19ofq7STTSoya3ymqrhyxtQcqTPiKcgLB

## Architecture Diagram
Webcam Input
      ↓
MediaPipe Pose Detection
      ↓
Posture Classification Logic
      ↓
Exercise Recommendation Engine
      ↓
CustomTkinter UI + Alert System

## API Documentation
This project does not use any backend API.
It is a fully offline standalone desktop application.

 ## Team Members
1)Ridhi Anilkumar
2)Avantika Bizy Nair

## License
This project is developed for educational purposes.
You may use and modify it with proper attribution.

