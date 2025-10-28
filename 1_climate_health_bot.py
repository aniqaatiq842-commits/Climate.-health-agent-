import streamlit as st
import random
import time

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="💬 Climate Health Assistant", layout="wide")

# -------------------- CUSTOM CSS FOR STYLE --------------------
st.markdown("""
<style>
.chat-container {
    background-color: #f5fff7;
    border-radius: 12px;
    padding: 15px;
    margin-top: 10px;
}
.user-msg {
    background-color: #d1f0d1;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 5px;
    text-align: right;
}
.bot-msg {
    background-color: #e8f5e9;
    border-left: 5px solid #2E8B57;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("<h1 style='text-align:center; color:#2E8B57;'>🌍 Climate Health Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Ask how weather, pollution, or climate conditions affect your health.</h4>", unsafe_allow_html=True)
st.divider()

# -------------------- MEMORY --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- MINI INTELLIGENCE ENGINE --------------------
def analyze_query(query):
    query = query.lower()
    if any(word in query for word in ["pollution", "smog", "air quality"]):
        return random.choice([
            "😷 Air pollution can irritate your lungs, worsen asthma, and increase heart disease risk.",
            "💨 Long exposure to pollution affects your respiratory and cardiovascular systems.",
            "🚫 Try to stay indoors during smog alerts or use an N95 mask outside."
        ])
    elif any(word in query for word in ["heat", "temperature", "hot"]):
        return random.choice([
            "🥵 High heat can cause dehydration and heatstroke — drink plenty of water!",
            "🔥 Hot climates increase stress on the heart and kidneys, especially for elderly people.",
            "💧 Avoid outdoor activity in peak sun hours and wear light clothes."
        ])
    elif any(word in query for word in ["cold", "chill", "winter"]):
        return random.choice([
            "❄️ Cold weather tightens blood vessels — risky for heart patients.",
            "🤧 Sudden chills can weaken immunity — keep your chest and feet warm.",
            "🧣 Layer your clothing and stay active indoors to improve circulation."
        ])
    elif any(word in query for word in ["humidity", "humid", "moisture"]):
        return random.choice([
            "💦 High humidity makes breathing hard — avoid outdoor exertion.",
            "🌫️ Humidity worsens allergies by promoting mold and dust mites.",
            "😮‍💨 Use a dehumidifier and keep air flow steady indoors."
        ])
    elif any(word in query for word in ["dust", "sand", "allergy"]):
        return random.choice([
            "🌪️ Dust exposure can irritate your eyes and lungs.",
            "🫁 For asthma patients, dusty air can trigger wheezing or coughing.",
            "😷 Keep windows closed and clean air filters regularly."
        ])
    elif any(word in query for word in ["rain", "monsoon", "storm"]):
        return random.choice([
            "🌧️ Rain improves air but increases humidity — risky for arthritis or asthma.",
            "💧 Avoid wet shoes and puddles to prevent infections.",
            "☔ Keep yourself dry; sudden temperature changes can cause colds."
        ])
    elif any(word in query for word in ["climate change", "global warming"]):
        return random.choice([
            "🌎 Climate change worsens respiratory diseases due to rising pollution.",
            "🔥 Heatwaves and bad air quality increase hospital visits for heart and lung problems.",
            "💡 Reducing plastic and fuel usage helps your health *and* the planet!"
        ])
    else:
        return random.choice([
            "🤔 That’s interesting! Climate factors like heat, humidity, and pollution all impact human health.",
            "🌿 Generally, cleaner air and stable weather improve heart, lung, and mental health.",
            "💚 Could you tell me more about your condition or environment?"
        ])

# -------------------- CHAT SYSTEM --------------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"<div class='user-msg'><b>You:</b> {chat['message']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'><b>AI:</b> {chat['message']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

user_input = st.text_input("💬 Ask a climate or health question:")

if st.button("Ask 🌿"):
    if user_input.strip():
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        with st.spinner("Thinking... 🤔"):
            time.sleep(1)
            ai_reply = analyze_query(user_input)
        st.session_state.chat_history.append({"role": "bot", "message": ai_reply})
        st.rerun()
    else:
        st.warning("Please type something before asking.")

# -------------------- FOOTER --------------------
st.divider()
st.markdown("<p style='text-align:center; color:gray;'>© 2025 Climate Health Assistant — Offline Smart Chatbot</p>", unsafe_allow_html=True)
