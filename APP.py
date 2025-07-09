import streamlit as st

# 🛠️ Set up the page
st.set_page_config(
    page_title="AI Nutrition Assistant",
    page_icon="🥗",
    layout="centered"
)

# 🥗 Main Title
st.title("🥗 AI Nutrition Assistant")

# 📝 Description
st.markdown("""
Welcome to the **AI Nutrition Assistant** – your smart companion to help analyze meals and track your health journey.

This tool uses **AI-powered food detection** and **nutrition analysis** to provide detailed insights into what you eat.
""")

# 🌟 What You Can Do Section
st.markdown("""
### 🌟 What You Can Do:
- 📸 Upload food images (on the Upload page)  
- 🧠 Get calorie and nutrient breakdown  
- 📈 View your health dashboard  
- 🗓️ Track your daily meals and exercise history  

---

👉 **Use the sidebar to explore each section of the app!**
""")

# 📷 Optional Image or Icon
st.image("https://cdn-icons-png.flaticon.com/512/3172/3172880.png", width=150)
