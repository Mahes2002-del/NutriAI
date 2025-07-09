import streamlit as st
import pandas as pd
import mysql.connector
import altair as alt
import plotly.express as px

# ----------------- Page Setup -----------------
st.set_page_config(
    page_title="AI Nutrition Dashboard",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Fetch Data from MySQL -----------------
@st.cache_data
def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",             # 🔁 Replace with your DB username
        password="1234",         # 🔁 Replace with your DB password
        database="fp"            # 🔁 Your database name
    )
    query = "SELECT * FROM FitnessNutrition ORDER BY timestamp DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load the data
df = get_data()

# ----------------- Title and Description -----------------
st.title("📊 Smartest AI Nutrition Dashboard")
st.markdown("A comprehensive view of fitness activity and nutritional insights.")

# ----------------- Pull-ups & Push-ups Bar Chart -----------------
st.subheader("🔥 Calories Burned by Exercise")
st.markdown("**Pull-ups and Push-ups (Calories)**")

calories_by_type = {
    "Pull-ups": df["pull_up_calories"].sum(),
    "Push-ups": df["push_up_calories"].sum()
}

bar_data = pd.DataFrame({
    "Exercise": list(calories_by_type.keys()),
    "Calories": list(calories_by_type.values())
})

fig_bar = px.bar(
    bar_data,
    x="Exercise",
    y="Calories",
    color="Exercise",
    title="Calories Burned - Pull-ups vs Push-ups",
    color_discrete_sequence=["#1f77b4", "#ff7f0e"]
)

st.plotly_chart(fig_bar, use_container_width=True)

# ----------------- Top 5 Detected Foods Pie Chart -----------------
st.subheader("🍽️ Top Detected Foods")

top_foods = df['detected_foods'].dropna().value_counts().head(5)

fig_foods = px.pie(
    names=top_foods.index,
    values=top_foods.values,
    title="Top 5 Detected Foods",
    hole=0.3,
    color_discrete_sequence=px.colors.sequential.RdBu
)

fig_foods.update_traces(textinfo='label+percent')
st.plotly_chart(fig_foods, use_container_width=True)

# ----------------- Nutrient Trend Over Time -----------------
st.subheader("⏳ Nutrient Trends Over Time")

nutrient = st.selectbox("Select a nutrient to view trends:", ["calories", "protein_g", "carbs_g", "fat_g"])

line_chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('timestamp:T', title='Timestamp'),
    y=alt.Y(nutrient, title=nutrient.capitalize()),
    color=alt.value("#636EFA"),
    tooltip=['timestamp', nutrient]
).properties(
    title=f"{nutrient.capitalize()} Over Time",
    height=400
).interactive()

st.altair_chart(line_chart, use_container_width=True)

# ----------------- Footer -----------------
st.markdown("---")
st.caption(f"📅 Last updated: {df['timestamp'].max().strftime('%Y-%m-%d %H:%M')}")
st.caption("© 2025 Smartest AI Nutrition")
