import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
from database import create_table, insert_data, get_emotion_data
from ml_model import predict_emotion

# Initialize
create_table()
analyzer = SentimentIntensityAnalyzer()

st.set_page_config(page_title="AI Mental Health Companion", layout="wide")
st.title("🧠 AI-Based Mental Health Companion Chatbot")
st.markdown("### Supporting Student Mental Well-being 💙")

menu = st.sidebar.selectbox("Menu", ["Chat", "Analytics"])

crisis_words = ["suicide", "die", "kill myself", "end my life", "harm myself"]

def generate_response(text, sentiment, emotion):
    text_lower = text.lower()

    for word in crisis_words:
        if word in text_lower:
            return ("🚨 Emergency Alert!\n\n"
                    "Please contact:\n"
                    "📞 Kiran Mental Health Helpline: 1800-599-0019\n\n"
                    "You are not alone.")

    if sentiment > 0.05:
        return f"😊 You seem {emotion}. That's wonderful! Keep it up!"

    elif sentiment < -0.05:
        return (f"💙 You seem {emotion}. I'm here for you.\n\n"
                "Try breathing exercise:\n"
                "Inhale 4 sec → Hold 4 sec → Exhale 6 sec.")

    else:
        return "😌 I understand. Tell me more."

# ---------------- CHAT PAGE ----------------
if menu == "Chat":

    user_input = st.text_area("How are you feeling today?")

    if st.button("Submit"):
        if user_input:

            sentiment_score = analyzer.polarity_scores(user_input)['compound']
            emotion = predict_emotion(user_input)

            insert_data(user_input, sentiment_score, emotion)

            response = generate_response(user_input, sentiment_score, emotion)

            st.subheader("🤖 Chatbot Response:")
            st.write(response)

            st.markdown(f"**Detected Emotion:** {emotion}")
            st.markdown(f"**Sentiment Score:** {sentiment_score}")

    st.markdown("---")
    st.caption("⚠️ This chatbot does not replace professional therapy.")

# ---------------- ANALYTICS PAGE ----------------
elif menu == "Analytics":

    st.subheader("📊 Emotion Analytics Dashboard")

    data = get_emotion_data()

    if data:
        df = pd.DataFrame(data, columns=["Emotion", "Count"])

        fig, ax = plt.subplots()
        ax.bar(df["Emotion"], df["Count"])
        ax.set_title("Emotion Distribution")
        ax.set_xlabel("Emotion")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)
    else:
        st.info("No data available yet.")
