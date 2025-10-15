import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="EduMind AI Dashboard", layout="wide")
st.title("🎓 EduMind AI - Student Emotion & Attendance Dashboard (Week 5)")

# --- Load Data ---
if os.path.exists("attendance.csv"):
    attendance_df = pd.read_csv("attendance.csv")
else:
    attendance_df = pd.DataFrame(columns=["Name", "Time"])

if os.path.exists("emotions.csv"):
    emotion_df = pd.read_csv("emotions.csv")
else:
    emotion_df = pd.DataFrame(columns=["Time", "Dominant Emotion", "All Emotions"])

if os.path.exists("attention.csv"):
    attention_df = pd.read_csv("attention.csv")
else:
    attention_df = pd.DataFrame(columns=["Student", "Attention %"])

# --- Layout ---
col1, col2, col3 = st.columns(3)
col1.metric("👨‍🎓 Total Students Present", len(attendance_df["Name"].unique()))
col2.metric("😊 Most Common Emotion", emotion_df["Dominant Emotion"].mode()[0] if not emotion_df.empty else "N/A")
col3.metric("🧠 Avg Attention Score", f"{attention_df['Attention %'].mean():.1f}%" if not attention_df.empty else "N/A")

st.divider()

# --- Attendance Section ---
st.subheader("📅 Attendance Summary")
st.dataframe(attendance_df)

# --- Emotion Analytics ---
st.subheader("💬 Emotion Frequency Distribution")
if not emotion_df.empty:
    emotion_counts = emotion_df["Dominant Emotion"].value_counts().reset_index()
    emotion_counts.columns = ["Emotion", "Count"]
    fig1 = px.bar(emotion_counts, x="Emotion", y="Count", color="Emotion", title="Emotion Frequency")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📈 Emotion Trend Over Time")
    fig2 = px.line(emotion_df, x="Time", y="Dominant Emotion", title="Emotion Trend Timeline", markers=True)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Run Week 2 Emotion Detector first to view this data.")

# --- Engagement Analysis ---
st.subheader("🧭 Attention & Engagement Levels")
if not attention_df.empty:
    fig3 = px.bar(attention_df, x="Student", y="Attention %", color="Attention %", title="Attention Scores")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Run Week 4 Engagement Analyzer to generate attention.csv.")

st.divider()
st.caption("© 2025 EduMind AI | Built by Arka Patra")
