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
# LANGUAGE SELECTOR

language = st.sidebar.selectbox(

    "🌍 Select Language",

    [
        "English",
        "हिन्दी",
        "भोजपुरी",
        "अवधी"
    ]
)
# =========================================
# LANGUAGE TRANSLATIONS
# =========================================

translations = {

    "English": {

        "home": "Home",
        "disease": "Disease Detection",
        "fertilizer": "Fertilizer Recommendation",
        "soil": "Soil Health",
        "irrigation": "Smart Irrigation",
        "chatbot": "AI Chatbot",
        "about": "About"
    },

    "हिन्दी": {

        "home": "होम",
        "disease": "रोग पहचान",
        "fertilizer": "उर्वरक सुझाव",
        "soil": "मिट्टी स्वास्थ्य",
        "irrigation": "सिंचाई सलाह",
        "chatbot": "एआई चैटबॉट",
        "about": "जानकारी"
    },

    "भोजपुरी": {

        "home": "घर",
        "disease": "रोग पहचान",
        "fertilizer": "खाद सलाह",
        "soil": "मिट्टी जाँच",
        "irrigation": "सिंचाई सलाह",
        "chatbot": "एआई चैट",
        "about": "जानकारी"
    },

    "अवधी": {

        "home": "घर",
        "disease": "रोग पहिचान",
        "fertilizer": "खाद सलाह",
        "soil": "मिट्टी जाँच",
        "irrigation": "सिंचाई सलाह",
        "chatbot": "एआई चैट",
        "about": "जानकारी"
    }
}

st.sidebar.info(
    "AI Powered Crop Disease Detection System"
)

page = st.sidebar.radio(

    "Navigation",

    [

        translations[language]["home"],

        translations[language]["disease"],

        translations[language]["fertilizer"],

        translations[language]["soil"],

        translations[language]["irrigation"],

        translations[language]["chatbot"],

        translations[language]["about"]
    ]
)
# =========================================
# LANGUAGE PAGE MAPPING
# =========================================

page_mapping = {

    "Home": "Home",
    "होम": "Home",
    "घर": "Home",

    "Disease Detection": "Disease Detection",
    "रोग पहचान": "Disease Detection",
    "रोग पहिचान": "Disease Detection",

    "Fertilizer Recommendation": "Fertilizer Recommendation",
    "उर्वरक सुझाव": "Fertilizer Recommendation",
    "खाद सलाह": "Fertilizer Recommendation",

    "Soil Health": "Soil Health",
    "मिट्टी स्वास्थ्य": "Soil Health",
    "मिट्टी जाँच": "Soil Health",

    "Smart Irrigation": "Smart Irrigation",
    "सिंचाई सलाह": "Smart Irrigation",

    "AI Chatbot": "AI Chatbot",
    "एआई चैटबॉट": "AI Chatbot",
    "एआई चैट": "AI Chatbot",

    "About": "About",
    "जानकारी": "About"
}

page = page_mapping.get(page, "Home")

# TITLE
st.title("🌱 AI Farming Assistant")

st.write(
    "Upload a crop image to detect possible disease."
)

# GEMINI API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-pro")

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

        "English": {
            "cause": "Rust fungus spreads in wet and humid conditions.",
            "treatment": "Spray Mancozeb or Copper Oxychloride fungicide.",
            "fertilizer": "Use Potash rich fertilizer and balanced NPK.",
            "organic": "Use neem oil spray every 7 days.",
            "prevention": "Avoid excess watering and improve airflow."
        },

        "हिन्दी": {
            "cause": "रस्ट फंगस गीले और नमी वाले मौसम में फैलता है।",
            "treatment": "मैनकोजेब या कॉपर ऑक्सीक्लोराइड का छिड़काव करें।",
            "fertilizer": "पोटाश युक्त और संतुलित एनपीके खाद का उपयोग करें।",
            "organic": "हर 7 दिन पर नीम तेल का छिड़काव करें।",
            "prevention": "अधिक पानी देने से बचें और हवा का प्रवाह बनाए रखें।"
        },

        "भोजपुरी": {
            "cause": "रस्ट फंगस गीलापन आ नमी में तेजी से फइलाला।",
            "treatment": "मैनकोजेब या कॉपर दवाई के छिड़काव करीं।",
            "fertilizer": "पोटाश वाला खाद आ संतुलित एनपीके डालल जरूरी बा।",
            "organic": "हर 7 दिन पर नीम तेल छिड़कीं।",
            "prevention": "ज्यादा पानी मत दीं आ हवा के रास्ता खुला रखीं।"
        }
    },

    "blight": {

        "English": {
            "cause": "Blight disease spreads due to fungus and humidity.",
            "treatment": "Use Chlorothalonil fungicide spray.",
            "fertilizer": "Apply Nitrogen and Potassium carefully.",
            "organic": "Remove infected leaves and use compost tea spray.",
            "prevention": "Keep leaves dry and maintain plant spacing."
        },

        "हिन्दी": {
            "cause": "ब्लाइट रोग फंगस और नमी के कारण फैलता है।",
            "treatment": "क्लोरोथालोनिल फफूंदनाशक का छिड़काव करें।",
            "fertilizer": "नाइट्रोजन और पोटाश संतुलित मात्रा में दें।",
            "organic": "संक्रमित पत्तियां हटाएं और कम्पोस्ट चाय स्प्रे करें।",
            "prevention": "पत्तियों को सूखा रखें और दूरी बनाए रखें।"
        },

        "भोजपुरी": {
            "cause": "ब्लाइट रोग फंगस आ नमी से फइलाला।",
            "treatment": "क्लोरोथालोनिल दवाई के छिड़काव करीं।",
            "fertilizer": "नाइट्रोजन आ पोटाश संतुलित मात्रा में दीं।",
            "organic": "बीमार पत्तियां हटाईं आ कम्पोस्ट स्प्रे करीं।",
            "prevention": "पत्तियां सूखी रखीं आ दूरी बनाके रखीं।"
        }
    },

    "leaf scorch": {

        "English": {
            "cause": "Leaf scorch occurs because of heat stress or fungal infection.",
            "treatment": "Use balanced fertilizer and fungicide spray.",
            "fertilizer": "Apply organic compost and micronutrients.",
            "organic": "Use vermicompost and proper irrigation.",
            "prevention": "Avoid water stress and extreme heat."
        },

        "हिन्दी": {
            "cause": "लीफ स्कॉर्च गर्मी और फंगल संक्रमण के कारण होता है।",
            "treatment": "संतुलित उर्वरक और फफूंदनाशक का उपयोग करें।",
            "fertilizer": "जैविक खाद और सूक्ष्म पोषक तत्व डालें।",
            "organic": "वर्मी कम्पोस्ट और सही सिंचाई करें।",
            "prevention": "पानी की कमी और अधिक गर्मी से बचाएं।"
        },

        "भोजपुरी": {
            "cause": "ई रोग गर्मी आ फंगस संक्रमण से होला।",
            "treatment": "संतुलित खाद आ फफूंद दवाई के छिड़काव करीं।",
            "fertilizer": "जैविक खाद आ सूक्ष्म पोषक तत्व डालीं।",
            "organic": "वर्मी कम्पोस्ट आ सही सिंचाई करीं।",
            "prevention": "बहुत गर्मी आ पानी के कमी से बचाईं।"
        }
    },

    "healthy": {

        "English": {
            "cause": "Your crop is healthy.",
            "treatment": "No treatment needed.",
            "fertilizer": "Continue balanced fertilizer schedule.",
            "organic": "Maintain organic compost usage.",
            "prevention": "Regular monitoring and irrigation."
        },

        "हिन्दी": {
            "cause": "आपकी फसल स्वस्थ है।",
            "treatment": "किसी उपचार की आवश्यकता नहीं है।",
            "fertilizer": "संतुलित खाद देना जारी रखें।",
            "organic": "जैविक खाद का उपयोग बनाए रखें।",
            "prevention": "नियमित निगरानी और सिंचाई करें।"
        },

        "भोजपुरी": {
            "cause": "रउआ के फसल स्वस्थ बा।",
            "treatment": "कवनो इलाज के जरूरत नइखे।",
            "fertilizer": "संतुलित खाद देते रहीं।",
            "organic": "जैविक खाद के उपयोग जारी रखीं।",
            "prevention": "नियमित देखभाल आ सिंचाई करीं।"
        }
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

# =========================
# SOIL HEALTH DATABASE
# =========================

soil_data = {

    "Black Soil": {

        "nutrients": "Rich in Potassium, Calcium and Magnesium",

        "best_crops": "Cotton, Wheat, Soybean, Maize",

        "fertilizer": "Use Phosphorus and Nitrogen fertilizers",

        "irrigation": "Moderate irrigation required"
    },

    "Sandy Soil": {

        "nutrients": "Low nutrients and poor water retention",

        "best_crops": "Groundnut, Watermelon, Coconut",

        "fertilizer": "Use Organic Compost and Potassium",

        "irrigation": "Frequent irrigation required"
    },

    "Clay Soil": {

        "nutrients": "Rich in nutrients and holds water well",

        "best_crops": "Rice, Broccoli, Cabbage",

        "fertilizer": "Use Organic Matter and Gypsum",

        "irrigation": "Low irrigation required"
    }
}
# =========================
# IRRIGATION DATABASE
# =========================

irrigation_data = {

    "Black Soil": {
        "Sunny": "Irrigate every 4-5 days",
        "Rainy": "No irrigation needed",
        "Cloudy": "Light irrigation after 6 days"
    },

    "Sandy Soil": {
        "Sunny": "Irrigate daily due to low water retention",
        "Rainy": "Minimal irrigation needed",
        "Cloudy": "Irrigate every 2-3 days"
    },

    "Clay Soil": {
        "Sunny": "Irrigate every 6-7 days",
        "Rainy": "Avoid irrigation",
        "Cloudy": "Moderate irrigation after 5 days"
    }
}

# =========================================
# HOME PAGE
# =========================================

if page == "Home":

    st.subheader("🏠 Welcome Farmer")

    st.write("""
    This AI Farming Assistant helps farmers with:

    ✅ Crop Disease Detection  
    ✅ Weather Information  
    ✅ Smart Fertilizer Recommendation  
    ✅ AI Farming Chatbot  
    """)

# =========================================
# DISEASE DETECTION
# =========================================

elif page == "Disease Detection":

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

                                info = disease_info[key][language]

                                st.warning(f"Cause: {info['cause']}")

                                st.info(f"Treatment: {info['treatment']}")

                                st.success(f"Recommended Fertilizer: {info['fertilizer']}")

                                st.success(f"Organic Solution: {info['organic']}")

                                st.error(f"Prevention: {info['prevention']}")

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

# =========================================
# FERTILIZER RECOMMENDATION
# =========================================

elif page == "Fertilizer Recommendation":

    st.header("🌾 Smart Fertilizer Recommendation")

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
        
        # =========================================
# SOIL HEALTH ANALYSIS
# =========================================

elif page == "Soil Health":

    st.header("🌱 Soil Health Analysis")

    soil = st.selectbox(

        "Select Soil Type",

        ["Black Soil", "Sandy Soil", "Clay Soil"]

    )

    if st.button("Analyze Soil"):

        data = soil_data[soil]

        st.success(f"🧪 Nutrients: {data['nutrients']}")

        st.info(f"🌾 Best Crops: {data['best_crops']}")

        st.warning(f"💊 Fertilizer Advice: {data['fertilizer']}")

        st.success(f"💧 Irrigation Advice: {data['irrigation']}")
        # =========================================
# SMART IRRIGATION SYSTEM
# =========================================

elif page == "Smart Irrigation":

    st.header("💧 Smart Irrigation System")

    soil = st.selectbox(

        "Select Soil Type",

        ["Black Soil", "Sandy Soil", "Clay Soil"]

    )

    weather = st.selectbox(

        "Select Weather Condition",

        ["Sunny", "Rainy", "Cloudy"]

    )

    if st.button("Get Irrigation Advice"):

        advice = irrigation_data[soil][weather]

        st.success(f"💧 Irrigation Advice: {advice}")


# =========================================
# AI CHATBOT
# =========================================

elif page == "AI Chatbot":

    st.header("🤖 Farming Chatbot")

    voice_text = speech_to_text(
        language='en',
        use_container_width=True,
        just_once=True,
        key='voice'
    )

    user_question = st.text_input(
        "Ask farming related questions",
        value=voice_text if voice_text else ""
    )

    if user_question:

        try:

            prompt = f"""
            You are an expert AI farming assistant.

            Give practical farming advice in simple language.

            User Question:
            {user_question}
            """

            response = model.generate_content(prompt)

            st.success(response.text)

        except Exception as e:

            st.error("Gemini AI Error")
            st.write(e)

# =========================================
# ABOUT PAGE
# =========================================

elif page == "About":

    st.header("ℹ About")

    st.write("""
    AI Farming Assistant Project

    Features:
    - Disease Detection
    - Weather Information
    - Fertilizer Recommendation
    - AI Chatbot

    Built using:
    - Streamlit
    - Hugging Face API
    - Gemini AI
    """)
    weather_labels = {

    "English": {
        "temp": "Temperature",
        "humidity": "Humidity",
        "weather": "Weather",
        "wind": "Wind Speed"
    },

    "हिन्दी": {
        "temp": "तापमान",
        "humidity": "नमी",
        "weather": "मौसम",
        "wind": "हवा की गति"
    },

    "भोजपुरी": {
        "temp": "तापमान",
        "humidity": "नमी",
        "weather": "मौसम",
        "wind": "हवा के रफ्तार"
    },

    "अवधी": {
        "temp": "तापमान",
        "humidity": "नमी",
        "weather": "मौसम",
        "wind": "हवा की रफ्तार"
    }
}

# =========================================
# WEATHER SECTION
# =========================================

st.markdown("---")

st.header("🌦 Live Weather")

city = st.selectbox(
    "Select Your City",
    [
        "Lucknow",
        "Delhi",
        "Mumbai",
        "Patna",
        "Bhopal",
        "Jaipur",
        "Kolkata",
        "Pune"
    ]
)

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
">

<h2 style="color:#1b5e20;">📍 {city.title()}</h2>

<h3>🌡 {weather_labels[language]['temp']}: {temperature} °C</h3>

<h3>💧 {weather_labels[language]['humidity']}: {humidity}%</h3>

<h3>☁ {weather_labels[language]['weather']}: {weather_condition}</h3>

<h3>🌬 {weather_labels[language]['wind']}: {wind_speed} m/s</h3>

</div>
""", unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.markdown(
    "<div class='footer'>Made with ❤️ for Farmers</div>",
    unsafe_allow_html=True
)
