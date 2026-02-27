import cv2
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


def calculate_angle(a, b):
    return abs(a - b)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    h, w, _ = frame.shape

    posture_text = "Good Posture"
    color = (0, 255, 0)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Get important landmarks
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_ear = landmarks[7]
        right_ear = landmarks[8]

        # Convert to pixel coords
        ls_x, ls_y = int(left_shoulder.x * w), int(left_shoulder.y * h)
        rs_x, rs_y = int(right_shoulder.x * w), int(right_shoulder.y * h)
        le_x, le_y = int(left_ear.x * w), int(left_ear.y * h)
        re_x, re_y = int(right_ear.x * w), int(right_ear.y * h)

        # 1️⃣ Uneven shoulders
        shoulder_diff = abs(ls_y - rs_y)
        if shoulder_diff > 20:
            posture_text = "Uneven Shoulders"
            color = (0, 0, 255)

        # 2️⃣ Forward head
        shoulder_mid_x = (ls_x + rs_x) // 2
        ear_mid_x = (le_x + re_x) // 2

        if abs(ear_mid_x - shoulder_mid_x) > 40:
            posture_text = "Forward Head Posture"
            color = (0, 0, 255)

        # 3️⃣ Slouch (shoulders too low)
        ear_avg_y = (le_y + re_y) // 2
        shoulder_avg_y = (ls_y + rs_y) // 2

        if ear_avg_y > shoulder_avg_y - 30:
            posture_text = "Slouching"
            color = (0, 0, 255)

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    cv2.putText(frame, posture_text, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                color, 3)

    cv2.imshow("Posture Correction System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
