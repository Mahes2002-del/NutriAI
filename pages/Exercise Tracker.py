import streamlit as st
import tempfile
import sqlite3
from datetime import datetime
import pytz
from process_video import count_reps_from_video

# Page setup
st.set_page_config(page_title="🏋️ Exercise Counter", layout="centered")
st.title("🏃 Exercise Counter")

# Supported exercises
exercise_display = ["Push-Up", "Pull-Up"]
exercise_map = {
    "Push-Up": "pushup",
    "Pull-Up": "pullup"
}

exercise = st.selectbox("Choose an exercise", exercise_display)

uploaded_video = st.file_uploader("📄 Upload a video", type=["mp4", "mov", "avi"])

if uploaded_video and st.button("▶️ Analyze Video"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_video.read())
        video_path = temp_video.name

    try:
        normalized_exercise = exercise_map[exercise]
        reps = count_reps_from_video(video_path, normalized_exercise)
        calories_per_rep = {
            "pushup": 0.3,
            "squat": 0.4,
            "pullup": 0.5
        }
        calories = round(reps * calories_per_rep[normalized_exercise], 2)
        st.success(f"✅ Detected {reps} {exercise.lower()}s. Calories burned: {calories}")

        # Save to SQLite DB
        conn = sqlite3.connect("exercise_log.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS exercise_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise TEXT,
                reps INTEGER,
                calories_burned REAL,
                timestamp TEXT
            )
        """)
        ist = pytz.timezone("Asia/Kolkata")
        timestamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("INSERT INTO exercise_log (exercise, reps, calories_burned, timestamp) VALUES (?, ?, ?, ?)",
                     (exercise, reps, calories, timestamp))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Show history
st.markdown("---")
st.subheader("📊 Last 5 Sessions")
conn = sqlite3.connect("exercise_log.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS exercise_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT,
        reps INTEGER,
        calories_burned REAL,
        timestamp TEXT
    )
""")
rows = conn.execute("SELECT * FROM exercise_log ORDER BY id DESC LIMIT 5").fetchall()
conn.close()

import pandas as pd
if rows:
    df = pd.DataFrame(rows, columns=["ID", "Exercise", "Reps", "Calories", "Timestamp"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No sessions logged yet.")
