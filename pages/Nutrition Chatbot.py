import streamlit as st
import openai

# Page setup
st.set_page_config(page_title="🤖 Nutrition Chatbot", layout="centered")
st.title("🥦 AI Nutrition Assistant")

# OpenRouter API setup
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# Initialize chat session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly AI nutrition assistant. You can respond to greetings like 'hi', 'hello', and also answer questions ONLY about nutrition, food, calories, protein, fat, carbs, or vitamins. "
                "If the user asks something unrelated (like sports, math, weather, or general questions), reply: '❌ I'm a nutrition assistant. I cannot help with that.'"
            )
        },
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I'm your personal AI Nutrition Assistant. Ask me anything about food, calories, protein, fat, carbs, or vitamins!"
            )
        }
    ]

# Show conversation (only user + assistant messages)
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"]:
        st.chat_message(msg["role"]).markdown(msg["content"])

# Input box
user_input = st.chat_input("Ask a nutrition question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="meta-llama/llama-3.2-11b-vision-instruct:free",
                messages=st.session_state.messages,
                max_tokens=500,
                extra_headers={
                    "HTTP-Referer": "https://your-app.com",
                    "X-Title": "NutriBot"
                }
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"❌ API Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)