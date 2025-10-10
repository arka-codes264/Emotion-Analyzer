import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

st.set_page_config(page_title="Emotion Trend Dashboard", layout="wide")

st.title("🎭 Emotion Trend Logger Dashboard")
st.markdown("Visualize real-time student emotion data (Week 3 of EduMind AI).")

# Load Data
df = pd.read_csv("emotions.csv")

if df.empty:
    st.warning("No emotion data found. Please run Week 2 project first.")
else:
    # Summary Stats
    emotion_counts = Counter(df["Dominant Emotion"])
    st.subheader("📊 Emotion Frequency Summary")
    st.write(pd.DataFrame(list(emotion_counts.items()), columns=["Emotion", "Count"]))

    # Bar Chart
    bar_chart = px.bar(x=emotion_counts.keys(), y=emotion_counts.values(),
                       labels={'x': 'Emotion', 'y': 'Count'},
                       title="Emotion Frequency Distribution")
    st.plotly_chart(bar_chart, use_container_width=True)

    # Time Trend Chart
    st.subheader("⏳ Emotion Change Over Time")
    line_chart = px.line(df, x="Time", y="Dominant Emotion",
                         title="Emotion Trend Over Time",
                         markers=True)
    st.plotly_chart(line_chart, use_container_width=True)

    # Top emotion
    top_emotion = df["Dominant Emotion"].mode()[0]
    st.success(f"🧠 Most Common Emotion Detected: **{top_emotion.upper()}**")
