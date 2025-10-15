import gradio as gr
import cv2
import mediapipe as mp
import time

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

def analyze(frame):
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    focused = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye = face_landmarks.landmark[474:478]
            right_eye = face_landmarks.landmark[469:473]

            for lm in left_eye + right_eye:
                x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            focused = True

    text = "Focused" if focused else "Distracted"
    color = (0, 255, 0) if focused else (0, 0, 255)
    cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    return frame

gr.Interface(
    fn=analyze,
    inputs=gr.Image(source="webcam", streaming=True),
    outputs="image",
    title="EduMind AI - Engagement Analyzer",
    description="Real-time focus detection using MediaPipe + OpenCV"
).launch()
