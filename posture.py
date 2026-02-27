import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    h, w, _ = frame.shape

    posture_text = "Good Posture"
    color = (0, 255, 0)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # -------- Get Important Landmarks --------
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_ear = landmarks[7]
        right_ear = landmarks[8]

        # Convert normalized coords to pixel coords
        ls_x, ls_y = int(left_shoulder.x * w), int(left_shoulder.y * h)
        rs_x, rs_y = int(right_shoulder.x * w), int(right_shoulder.y * h)
        le_x, le_y = int(left_ear.x * w), int(left_ear.y * h)
        re_x, re_y = int(right_ear.x * w), int(right_ear.y * h)

        # Averages
        ear_avg_y = (le_y + re_y) // 2
        shoulder_avg_y = (ls_y + rs_y) // 2
        ear_mid_x = (le_x + re_x) // 2
        shoulder_mid_x = (ls_x + rs_x) // 2

        # Differences
        ear_shoulder_vertical = abs(ear_avg_y - shoulder_avg_y)
        shoulder_diff = abs(ls_y - rs_y)

        # -----------------------------
        # POSTURE DETECTION LOGIC
        # -----------------------------

        # 1️⃣ Hunched Shoulders (shoulders too close to ears)
        if ear_shoulder_vertical < h * 0.15:
            posture_text = "Hunched Shoulders"
            color = (0, 0, 255)

        # 2️⃣ Uneven Shoulders
        elif shoulder_diff > h * 0.04:
            posture_text = "Uneven Shoulders"
            color = (0, 0, 255)

        # 3️⃣ Forward Head
        elif abs(ear_mid_x - shoulder_mid_x) > w * 0.05:
            posture_text = "Forward Head"
            color = (0, 0, 255)

        # 4️⃣ Leaning Too Close (Depth using Z axis)
        elif left_shoulder.z < -0.35 and right_shoulder.z < -0.35:
            posture_text = "Leaning Too Close"
            color = (0, 0, 255)

        else:
            posture_text = "Good Posture"
            color = (0, 255, 0)

        # Draw pose landmarks
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # Display posture text
    cv2.putText(frame, posture_text, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, color, 3)

    cv2.imshow("Posture Correction System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
