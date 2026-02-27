import cv2
import mediapipe as mp
import time


def detect_posture():

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    start_time = time.time()
    posture_counts = {}

    while time.time() - start_time < 5:   # Run detection for 5 seconds
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        h, w, _ = frame.shape
        posture_text = "Good Posture"

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]
            left_ear = landmarks[7]
            right_ear = landmarks[8]

            ls_y = int(left_shoulder.y * h)
            rs_y = int(right_shoulder.y * h)
            le_y = int(left_ear.y * h)
            re_y = int(right_ear.y * h)

            ear_avg_y = (le_y + re_y) // 2
            shoulder_avg_y = (ls_y + rs_y) // 2

            ear_mid_x = int((left_ear.x + right_ear.x) * w / 2)
            shoulder_mid_x = int((left_shoulder.x + right_shoulder.x) * w / 2)

            ear_shoulder_vertical = abs(ear_avg_y - shoulder_avg_y)
            shoulder_diff = abs(ls_y - rs_y)

            # ---- POSTURE LOGIC ----
            if ear_shoulder_vertical < h * 0.15:
                posture_text = "Hunched Shoulders"

            elif shoulder_diff > h * 0.04:
                posture_text = "Uneven Shoulders"

            elif abs(ear_mid_x - shoulder_mid_x) > w * 0.05:
                posture_text = "Forward Head"

            elif left_shoulder.z < -0.35 and right_shoulder.z < -0.35:
                posture_text = "Leaning Too Close"

            else:
                posture_text = "Good Posture"

        # Count occurrences
        posture_counts[posture_text] = posture_counts.get(posture_text, 0) + 1

    cap.release()
    cv2.destroyAllWindows()

    # Return most frequent posture detected
    if posture_counts:
        return max(posture_counts, key=posture_counts.get)
    else:
        return "Good Posture"
