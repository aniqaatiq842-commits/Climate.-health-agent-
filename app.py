import streamlit as st
import requests

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Climate Health Agent 🌿", layout="wide")

# -------------------- HEADER --------------------
st.markdown(
    "<h1 style='text-align:center; color:#2E8B57;'>🌿 Climate Health Agent</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align:center;'>🤖 Your AI partner that protects your health from changing weather.</h4>",
    unsafe_allow_html=True
)

st.image(
    "https://images.unsplash.com/photo-1612831197319-1833cd210dbf?auto=format&fit=crop&w=1000&q=80",
    width=550,
    use_container_width=False
)
st.divider()

# -------------------- SIDEBAR INPUT --------------------
st.sidebar.header("🌍 Enter Details")
city = st.sidebar.text_input("Enter your city:", "Karachi")
condition_text = st.sidebar.text_area("Describe your health condition:", "I have asthma")
analyze = st.sidebar.button("Check Climate Safety")

# -------------------- FETCH WEATHER --------------------
def fetch_weather(city):
    """Get weather data using free Open-Meteo API"""
    try:
        geo = requests.get(
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        ).json()

        if "results" not in geo or len(geo["results"]) == 0:
            return None

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        data = requests.get(
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weathercode"
        ).json()

        temp = data["current"]["temperature_2m"]
        humidity = data["current"]["relative_humidity_2m"]
        code = data["current"]["weathercode"]

        weather_map = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Rime fog", 51: "Drizzle", 61: "Rain",
            80: "Showers", 95: "Thunderstorm"
        }
        desc = weather_map.get(code, "Unknown")
        return temp, humidity, desc
    except Exception:
        return None

# -------------------- AGENTIC ANALYSIS --------------------
def analyze_health(temp, humidity, desc, condition_text):
    """Agentic AI reasoning: checks if weather is safe for user's condition"""
    text = condition_text.lower()
    risk = 0
    reasons = []

    # Base environmental risk
    if temp > 34:
        risk += 2; reasons.append("High temperature")
    if humidity > 75:
        risk += 1; reasons.append("High humidity")
    if "fog" in desc.lower() or "rain" in desc.lower():
        risk += 1; reasons.append("Moisture or fog may affect air quality")

    # Detect condition keywords (agentic reasoning)
    if any(word in text for word in ["asthma", "lung", "breath"]):
        if humidity > 70 or "fog" in desc.lower():
            risk += 2; reasons.append("Asthma-sensitive weather")
    elif any(word in text for word in ["heart", "cardio", "pressure"]):
        if temp > 33:
            risk += 2; reasons.append("Heat may stress the heart")
    elif any(word in text for word in ["migraine", "headache"]):
        if temp > 30 or humidity > 80:
            risk += 2; reasons.append("Possible migraine triggers")
    elif any(word in text for word in ["skin", "eczema", "rash"]):
        if "clear" in desc.lower() or temp > 30:
            risk += 1; reasons.append("High UV or heat risk for skin")
    elif any(word in text for word in ["diabetes", "sugar"]):
        if temp > 35:
            risk += 2; reasons.append("Heat and dehydration risk for diabetes")
    elif any(word in text for word in ["joint", "arthritis", "pain"]):
        if humidity > 70:
            risk += 1; reasons.append("Humidity may worsen joint pain")
    elif any(word in text for word in ["flu", "cold", "fever"]):
        if "rain" in desc.lower() or temp < 20:
            risk += 1; reasons.append("Cool or wet weather may trigger symptoms")

    # Verdict logic
    if risk <= 1:
        verdict = "✅ Safe to go outside"
        color = "#C8E6C9"
        message = "The climate looks friendly to your health today."
    elif 2 <= risk <= 3:
        verdict = "⚠️ Moderate Risk"
        color = "#FFF59D"
        message = "Take precautions — it may cause mild discomfort."
    else:
        verdict = "🚨 High Risk!"
        color = "#FFCDD2"
        message = "Avoid outdoor exposure; conditions may worsen your symptoms."

    # AI agent message
    ai_message = f"""
    <div style='background-color:{color}; padding:20px; border-radius:10px;'>
        <h3>🤖 ClimaHealth Agent Report</h3>
        <p><b>City:</b> {city}</p>
        <p><b>Condition:</b> {condition_text}</p>
        <p><b>Verdict:</b> {verdict}</p>
        <p><b>Weather:</b> {desc}, {temp}°C, {humidity}% humidity</p>
        <p><b>Reasoning:</b> {", ".join(reasons) if reasons else "No major risks detected."}</p>
        <p><b>Agent’s Advice:</b> {message}</p>
    </div>
    """
    return ai_message, risk

# -------------------- MAIN SECTION --------------------
if analyze:
    result = fetch_weather(city)
    if not result:
        st.error("❌ Couldn't fetch weather data. Try another city name.")
    else:
        temp, humidity, desc = result

        col1, col2, col3 = st.columns(3)
        col1.metric("🌡 Temperature", f"{temp} °C")
        col2.metric("💧 Humidity", f"{humidity} %")
        col3.metric("☁️ Condition", desc)
        st.divider()

        summary, risk = analyze_health(temp, humidity, desc, condition_text)
        st.markdown(summary, unsafe_allow_html=True)
        st.progress(min(1.0, risk / 4.0))
else:
    st.info("👈 Enter your city and describe your health condition to check climate safety.")

# -------------------- FOOTER --------------------
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>© 2025 ClimaHealth Agent — Powered by free Open-Meteo data 🌍</p>",
    unsafe_allow_html=True
)
