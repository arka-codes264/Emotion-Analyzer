 import cv2
import mediapipe as mp
import pandas as pd
from datetime import datetime

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

engagement_data = []
focused_frames = 0
total_frames = 0

print("Starting Secure Engagement Analyzer (MediaPipe)... Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    total_frames += 1
    focused = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get landmarks for eyes (left & right iris center)
            left_eye = face_landmarks.landmark[474:478]
            right_eye = face_landmarks.landmark[469:473]

            # Draw eye landmarks
            for landmark in left_eye + right_eye:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            focused = True

    if focused:
        focused_frames += 1

    # Calculate attention percentage
    attention_score = (focused_frames / total_frames) * 100
    cv2.putText(frame, f"Attention: {attention_score:.1f}%", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Engagement & Attention Analyzer (Secure)", frame)

    # Log every 60 frames
    if total_frames % 60 == 0:
        engagement_data.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Attention (%)": round(attention_score, 2)
        })

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save data
df = pd.DataFrame(engagement_data)
df.to_csv("engagement.csv", index=False)
print("Engagement data saved successfully.")
