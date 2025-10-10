import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load logged emotions from Week 2
df = pd.read_csv('emotions.csv')

# Extract dominant emotion
dominant_emotions = df["Dominant Emotion"]

# Count frequency of each emotion
emotion_counts = Counter(dominant_emotions)

# Display counts
print("Emotion Frequency Summary:")
for emotion, count in emotion_counts.items():
    print(f"{emotion}: {count}")

# Plot frequency of emotions
plt.figure(figsize=(8, 5))
plt.bar(emotion_counts.keys(), emotion_counts.values())
plt.title("Overall Emotion Frequency")
plt.xlabel("Emotion Type")
plt.ylabel("Count")
plt.show()

# Emotion trend over time
plt.figure(figsize=(10, 5))
plt.plot(df["Time"], df["Dominant Emotion"], marker='o', color='purple')
plt.title("Emotion Trend Over Time")
plt.xlabel("Time")
plt.ylabel("Dominant Emotion")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
