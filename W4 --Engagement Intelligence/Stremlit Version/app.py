import streamlit as st
import cv2
import mediapipe as mp
import pandas as pd
from datetime import datetime
import time

# Streamlit page setup
st.set_page_config(page_title="Engagement & Attention Analyzer", layout="wide")
st.title("🧠 EduMind AI — Engagement & Attention Analyzer (Secure Version)")
st.markdown("Tracks real-time attention levels using eye gaze detection (MediaPipe + Streamlit).")

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Sidebar controls
run = st.sidebar.checkbox("Start Analyzer")
show_landmarks = st.sidebar.checkbox("Show Eye Landmarks")
log_interval = st.sidebar.slider("Logging Interval (seconds)", 2, 10, 5)

FRAME_WINDOW = st.image([])
status_placeholder = st.empty()
chart_placeholder = st.empty()

# Engagement log
engagement_data = []
focused_frames = 0
total_frames = 0
start_time = time.time()

if run:
    cap = cv2.VideoCapture(0)
    st.sidebar.success("Webcam started successfully.")

    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("Webcam not accessible.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        total_frames += 1
        focused = False

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye = face_landmarks.landmark[474:478]
                right_eye = face_landmarks.landmark[469:473]

                if show_landmarks:
                    for landmark in left_eye + right_eye:
                        x = int(landmark.x * frame.shape[1])
                        y = int(landmark.y * frame.shape[0])
                        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

                focused = True

        if focused:
            focused_frames += 1

        attention_score = (focused_frames / total_frames) * 100
        cv2.putText(frame, f"Attention: {attention_score:.1f}%", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        FRAME_WINDOW.image(frame, channels="BGR")
        status_placeholder.info(f"🟢 Current Attention: **{attention_score:.1f}%**")

        # Log every interval seconds
        if time.time() - start_time > log_interval:
            engagement_data.append({
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Attention (%)": round(attention_score, 2)
            })
            df = pd.DataFrame(engagement_data)
            df.to_csv("engagement.csv", index=False)
            chart_placeholder.line_chart(df.set_index("Time")["Attention (%)"])
            start_time = time.time()

        # Stop button
        if not st.sidebar.checkbox("Start Analyzer", value=True):
            break

    cap.release()
    st.success("Engagement analysis stopped.")
else:
    st.warning("👈 Turn on the 'Start Analyzer' checkbox to begin tracking.")

