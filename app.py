import streamlit as st
from PIL import Image
import requests
import geocoder
from streamlit_mic_recorder import speech_to_text
import google.generativeai as genai

# PAGE SETTINGS
st.set_page_config(
    page_title="AI Farming Assistant",
    page_icon="🌱",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>

body {
    background-color: #f4fff4;
}

.main {
    background-color: #f4fff4;
}

h1 {
    color: #1b5e20;
    font-size: 50px;
    text-align: center;
    font-weight: bold;
}

h2, h3 {
    color: #2e7d32;
}

.stButton>button {
    background-color: #2e7d32;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    border: none;
}

.stButton>button:hover {
    background-color: #1b5e20;
    color: white;
}

.stTextInput>div>div>input {
    border-radius: 10px;
    border: 2px solid #81c784;
}

.result-box {
    background-color: #edf7ed;
    padding: 25px;
    border-radius: 15px;
    margin-top: 20px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("🌱 Farming Assistant")

st.sidebar.info(
    "AI Powered Crop Disease Detection System"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Disease Detection",
        "Fertilizer Recommendation",
        "AI Chatbot",
        "About"
    ]
)

# TITLE
st.title("🌱 AI Farming Assistant")

st.write(
    "Upload a crop image to detect possible disease."
)

# GEMINI API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("models/gemini-1.5-flash")

# HUGGING FACE API
API_URL = "https://router.huggingface.co/hf-inference/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"

headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}",
    "Content-Type": "image/jpeg"
}

# =========================
# DISEASE INFORMATION DATABASE
# =========================

disease_info = {

    "rust": {

        "cause": "Rust fungus spreads in wet and humid conditions.",

        "treatment": "Spray Mancozeb or Copper Oxychloride fungicide.",

        "fertilizer": "Use Potash rich fertilizer and balanced NPK.",

        "organic": "Use neem oil spray every 7 days.",

        "prevention": "Avoid excess watering and improve airflow."
    },

    "blight": {

        "cause": "Blight disease spreads due to fungus and humidity.",

        "treatment": "Use Chlorothalonil fungicide spray.",

        "fertilizer": "Apply Nitrogen and Potassium carefully.",

        "organic": "Remove infected leaves and use compost tea spray.",

        "prevention": "Keep leaves dry and maintain plant spacing."
    },

    "leaf scorch": {

        "cause": "Leaf scorch occurs because of heat stress or fungal infection.",

        "treatment": "Use balanced fertilizer and fungicide spray.",

        "fertilizer": "Apply organic compost and micronutrients.",

        "organic": "Use vermicompost and proper irrigation.",

        "prevention": "Avoid water stress and extreme heat."
    },

    "healthy": {

        "cause": "Your crop is healthy.",

        "treatment": "No treatment needed.",

        "fertilizer": "Continue balanced fertilizer schedule.",

        "organic": "Maintain organic compost usage.",

        "prevention": "Regular monitoring and irrigation."
    }
}
# =========================
# FERTILIZER DATABASE
# =========================

fertilizer_data = {

    "Wheat": {
        "Black Soil": "Use Urea + DAP + Potash",
        "Sandy Soil": "Use Organic Compost + NPK",
        "Clay Soil": "Use Nitrogen rich fertilizer"
    },

    "Rice": {
        "Black Soil": "Use NPK 10-26-26",
        "Sandy Soil": "Use Vermicompost + Potash",
        "Clay Soil": "Use Urea in small amounts"
    },

    "Maize": {
        "Black Soil": "Use Nitrogen and Potassium",
        "Sandy Soil": "Use Compost and Urea",
        "Clay Soil": "Use Balanced NPK"
    },

    "Sugarcane": {
        "Black Soil": "Use Potassium rich fertilizer",
        "Sandy Soil": "Use Organic manure",
        "Clay Soil": "Use Nitrogen fertilizer"
    }
}

# IMAGE UPLOAD
uploaded_file = st.file_uploader(
    "Upload Crop Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    if st.button("Detect Disease"):

        with st.spinner("Detecting disease..."):

            image_bytes = uploaded_file.getvalue()

            response = requests.post(
                API_URL,
                headers=headers,
                data=image_bytes
            )

            try:

                result = response.json()

                if isinstance(result, list):

                    disease = result[0]['label']
                    confidence = result[0]['score']

                    st.markdown(f"""
                    <div class="result-box">
                        <h1>🌱 Disease Detected</h1>
                        <h2 style="color:red;">{disease}</h2>
                        <h3>Confidence Score: {round(confidence * 100, 2)}%</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    found = False

                    for key in disease_info:

                        if key in disease.lower():

                            info = disease_info[key]

                            st.warning(
                                f"Cause: {info['cause']}"
                            )
                            st.info(f"Treatment: {info['treatment']}")

                            st.success(f"Recommended Fertilizer: {info['fertilizer']}")

                            st.success(f"Organic Solution: {info['organic']}")

                            st.warning(f"Prevention: {info['prevention']}")

                            st.info(
                                f"Treatment: {info['treatment']}"
                            )

                            st.success(
                                f"Organic Solution: {info['organic']}"
                            )

                            st.error(
                                f"Prevention: {info['prevention']}"
                            )

                            found = True

                            break

                    if not found:

                        st.warning(
                            "Disease information currently unavailable."
                        )

                else:

                    st.error("API Error")
                    st.write(result)

            except Exception as e:

                st.error("Something went wrong.")
                st.write(e)
# WEATHER SECTION

st.markdown("---")

st.header("🌦 Live Weather")

# AUTO LOCATION DETECTION

g = geocoder.ip('me')

city = g.city

st.success(f"📍 Detected Location: {city}")

if city:

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={st.secrets['WEATHER_API_KEY']}&units=metric"

    weather_response = requests.get(weather_url)

    weather_data = weather_response.json()

    if weather_response.status_code == 200:

        temperature = weather_data["main"]["temp"]

        humidity = weather_data["main"]["humidity"]

        weather_condition = weather_data["weather"][0]["description"]

        wind_speed = weather_data["wind"]["speed"]

        st.markdown(f"""
        <div style="
            background-color:#edf7ed;
            padding:25px;
            border-radius:15px;
            margin-top:20px;
            box-shadow:0px 0px 10px rgba(0,0,0,0.1);
        ">
            <h2 style="color:#1b5e20;">📍 {city.title()}</h2>

            <h3>🌡 Temperature: {temperature} °C</h3>

            <h3>💧 Humidity: {humidity}%</h3>

            <h3>☁ Weather: {weather_condition.title()}</h3>

            <h3>🌬 Wind Speed: {wind_speed} m/s</h3>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.error("City not found.")
        
# CHATBOT SECTION
st.markdown("---")

st.header("🤖 Farming Chatbot")

# Voice Input
voice_text = speech_to_text(
    language='en',
    use_container_width=True,
    just_once=True,
    key='voice'
)

# Text Input
user_question = st.text_input(
    "Ask farming related questions",
    value=voice_text if voice_text else ""
)

# AI RESPONSE
if user_question:

    try:

        prompt = f"""
        You are an expert AI farming assistant.

        Rules:
        - Give short and practical farming advice.
        - Support Hindi and English.
        - Help farmers with crops, fertilizer, disease,
          irrigation, pesticides, weather and soil.

        User Question:
        {user_question}
        """

        response = model.generate_content(prompt)

        st.markdown(f"""
        <div style="
            background-color:#edf7ed;
            padding:20px;
            border-radius:15px;
            margin-top:15px;
            box-shadow:0px 0px 10px rgba(0,0,0,0.1);
        ">
            <h3 style="color:#1b5e20;">
            🤖 AI Farming Advice
            </h3>

            <p style="font-size:18px;">
            {response.text}
            </p>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:

        st.error("Gemini AI Error")

        st.write(e)

# FOOTER
st.markdown("---")

st.markdown(
    "<div class='footer'>Made with ❤️ for Farmers</div>",
    unsafe_allow_html=True
)
# =========================
# FERTILIZER RECOMMENDATION
# =========================

elif page == "Fertilizer Recommendation":

    st.title("🌾 Smart Fertilizer Recommendation")

    crop = st.selectbox(

        "Select Crop",

        ["Wheat", "Rice", "Maize", "Sugarcane"]

    )

    soil = st.selectbox(

        "Select Soil Type",

        ["Black Soil", "Sandy Soil", "Clay Soil"]

    )

    if st.button("Get Fertilizer Recommendation"):

        recommendation = fertilizer_data[crop][soil]

        st.success(f"Recommended Fertilizer: {recommendation}")
