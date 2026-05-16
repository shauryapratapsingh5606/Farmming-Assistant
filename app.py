import streamlit as st
import requests
import sqlite3

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Farming Assistant",
    page_icon="🌱",
    layout="wide"
)
# =========================================
# DATABASE CONNECTION
# =========================================

conn = sqlite3.connect("farmers.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS farmers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    mobile TEXT,

    village TEXT,

    crop TEXT
)
""")

conn.commit()

# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("🌱 Farming Assistant")

# =========================================
# LANGUAGE SELECT
# =========================================

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
# LANGUAGE LABELS
# =========================================

labels = {

    "English": {
        "home": "Home",
        "disease": "Disease Detection",
        "fertilizer": "Fertilizer Recommendation",
        "soil": "Soil Health",
        "irrigation": "Smart Irrigation",
        "chatbot": "AI Chatbot",
        "about": "About",
        "register": "👨‍🌾 Farmer Registration",
        "weather": "🌦 Live Weather",
        "city": "Select Your City",
        "temp": "Temperature",
        "humidity": "Humidity",
        "weather_text": "Weather",
        "wind": "Wind Speed"
    },

    "हिन्दी": {
        "home": "घर",
        "disease": "रोग पहचान",
        "fertilizer": "खाद सलाह",
        "soil": "मिट्टी जाँच",
        "irrigation": "सिंचाई सलाह",
        "chatbot": "एआई चैट",
        "about": "जानकारी",
        "register": "👨‍🌾 किसान पंजीकरण",
        "weather": "🌦 लाइव मौसम",
        "city": "अपना शहर चुनें",
        "temp": "तापमान",
        "humidity": "नमी",
        "weather_text": "मौसम",
        "wind": "हवा की गति"
    },

    "भोजपुरी": {
        "home": "घर",
        "disease": "रोग पहचान",
        "fertilizer": "खाद सलाह",
        "soil": "मिट्टी जांच",
        "irrigation": "सिंचाई सलाह",
        "chatbot": "एआई चैट",
        "about": "जानकारी",
        "register": "👨‍🌾 किसान रजिस्ट्रेशन",
        "weather": "🌦 जिंदा मौसम",
        "city": "अपना शहर चुनीं",
        "temp": "तापमान",
        "humidity": "नमी",
        "weather_text": "मौसम",
        "wind": "हवा के रफ्तार"
    },

    "अवधी": {
        "home": "घर",
        "disease": "रोग पहचान",
        "fertilizer": "खाद सलाह",
        "soil": "मिट्टी जाँच",
        "irrigation": "सिंचाई सलाह",
        "chatbot": "एआई चैट",
        "about": "जानकारी",
        "register": "👨‍🌾 किसान पंजीकरण",
        "weather": "🌦 जिंदा मौसम",
        "city": "अपना शहर चुनौ",
        "temp": "तापमान",
        "humidity": "नमी",
        "weather_text": "मौसम",
        "wind": "हवा की रफ्तार"
    }
}

# =========================================
# NAVIGATION
# =========================================

page = st.sidebar.radio(
    "Navigation",
    [
        labels[language]["home"],
        labels[language]["register"],
        labels[language]["disease"],
        labels[language]["fertilizer"],
        labels[language]["soil"],
        labels[language]["irrigation"],
        labels[language]["chatbot"],
        labels[language]["about"]
    ]
)

# =========================================
# HOME PAGE
# =========================================

if page == labels[language]["home"]:

    st.title("🌱 AI Farming Assistant")

    st.write("Upload crop image and get farming support.")
    st.markdown("---")

st.header("👨‍🌾 Farmer Registration")

farmer_name = st.text_input("Farmer Name")

farmer_mobile = st.text_input("Mobile Number")

farmer_village = st.text_input("Village")

farmer_crop = st.text_input("Main Crop")

if st.button("Save Farmer Data"):

    cursor.execute("""

    INSERT INTO farmers (name, mobile, village, crop)

    VALUES (?, ?, ?, ?)

    """, (

        farmer_name,
        farmer_mobile,
        farmer_village,
        farmer_crop
    ))

    conn.commit()

    st.success("Farmer Data Saved Successfully ✅")

    st.markdown("---")

    # =========================================
    # WEATHER SECTION
    # =========================================

    st.header(labels[language]["weather"])

    city = st.selectbox(
        labels[language]["city"],
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

    # =========================================
    # WEATHER API
    # =========================================

    api_key = st.secrets["WEATHER_API_KEY"]

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    weather_response = requests.get(weather_url)

    weather_data = weather_response.json()

    # =========================================
    # WEATHER DISPLAY
    # =========================================

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

        <h2 style="color:#1b5e20;">📍 {city}</h2>

        <h3>🌡 {labels[language]["temp"]}: {temperature} °C</h3>

        <h3>💧 {labels[language]["humidity"]}: {humidity}%</h3>

        <h3>☁ {labels[language]["weather_text"]}: {weather_condition.title()}</h3>

        <h3>🌬 {labels[language]["wind"]}: {wind_speed} m/s</h3>

        </div>
        """, unsafe_allow_html=True)

    else:
        st.error("Weather data not found.")
        # =========================================
# FARMER REGISTRATION
# =========================================

elif page == labels[language]["register"]:

    st.title(labels[language]["register"])

    farmer_name = st.text_input(
    "Farmer Name",
    key="farmer_name_input"
)

farmer_mobile = st.text_input(
    "Mobile Number",
    key="farmer_mobile_input"
)

farmer_village = st.text_input(
    "Village",
    key="farmer_village_input"
)

farmer_crop = st.text_input(
    "Main Crop",
    key="farmer_crop_input"
)
 farmer_image = st.file_uploader(
        "Upload Farmer Image",
        type=["jpg", "png", "jpeg"]
        key="farmer_image_upload"
    )

    if farmer_image is not None:

        st.image(farmer_image, width=200)

    if st.button("Register Farmer"
        key="register_farmer_btn"):

        image_name = ""

        if farmer_image is not None:

            image_name = farmer_image.name

        cursor.execute("""

        INSERT INTO farmers
        (name, mobile, village, crop, image)

        VALUES (?, ?, ?, ?, ?)

        """, (

            farmer_name,
            farmer_mobile,
            farmer_village,
            farmer_crop,
            image_name
        ))

        conn.commit()

        st.success("Farmer Registered Successfully ✅")

# =========================================
# DISEASE PAGE
# =========================================

elif page == labels[language]["disease"]:

    st.title("🦠 Disease Detection")

    uploaded_file = st.file_uploader(
        "Upload Crop Image",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_file:

        st.image(uploaded_file, width=300)

        st.success("Disease Detection System Working Successfully")

        if language == "English":

            st.warning("Cause: Leaf scorch due to heat stress.")

            st.info("Treatment: Use fungicide spray.")

            st.success("Fertilizer: Use balanced NPK fertilizer.")

        elif language == "हिन्दी":

            st.warning("कारण: अधिक गर्मी के कारण पत्ती झुलस गई।")

            st.info("उपचार: फफूंदनाशक दवा का छिड़काव करें।")

            st.success("खाद: संतुलित NPK खाद का उपयोग करें।")

        elif language == "भोजपुरी":

            st.warning("कारण: अधिक गर्मी से पत्ता झुलस गइल बा।")

            st.info("उपचार: फफूंद नाशक दवाई छिड़कीं।")

            st.success("खाद: संतुलित NPK खाद डालीं।")

        elif language == "अवधी":

            st.warning("कारण: अधिक गर्मी से पत्ती झुलस गई।")

            st.info("उपचार: फफूंदनाशक दवा छिड़कें।")

            st.success("खाद: संतुलित NPK खाद डालें।")

# =========================================
# FERTILIZER PAGE
# =========================================

elif page == labels[language]["fertilizer"]:

    st.title("🧪 Smart Fertilizer Recommendation")

    crop = st.selectbox(
        "Select Crop",
        ["Wheat", "Rice", "Sugarcane", "Maize"]
    )

    soil = st.selectbox(
        "Select Soil Type",
        ["Loamy", "Clay", "Sandy"]
    )

    if st.button("Get Recommendation"):

        st.success(f"Recommended Fertilizer for {crop}: NPK 20-20-20")

# =========================================
# SOIL PAGE
# =========================================

elif page == labels[language]["soil"]:

    st.title("🌱 Soil Health")

    ph = st.slider("Soil pH", 0.0, 14.0, 7.0)

    if ph < 6:

        st.warning("Soil is acidic.")

    elif ph > 8:

        st.warning("Soil is alkaline.")

    else:

        st.success("Soil health is good.")

# =========================================
# IRRIGATION PAGE
# =========================================

elif page == labels[language]["irrigation"]:

    st.title("💧 Smart Irrigation")

    moisture = st.slider("Soil Moisture", 0, 100, 50)

    if moisture < 40:

        st.error("Irrigation Needed")

    else:

        st.success("No Irrigation Needed")

# =========================================
# CHATBOT PAGE
# =========================================

elif page == labels[language]["chatbot"]:

    st.title("🤖 AI Farming Chatbot")

    user_question = st.text_input("Ask Farming Question")

    if user_question:

        if language == "English":

            st.success("Use organic compost and proper irrigation.")

        elif language == "हिन्दी":

            st.success("जैविक खाद और उचित सिंचाई का उपयोग करें।")

        elif language == "भोजपुरी":

            st.success("जैविक खाद अउर सही सिंचाई के उपयोग करीं।")

        elif language == "अवधी":

            st.success("जैविक खाद और सही सिंचाई का प्रयोग करें।")

# =========================================
# ABOUT PAGE
# =========================================

elif page == labels[language]["about"]:

    st.title("ℹ About")

    st.write("AI Farming Assistant helps farmers with smart agriculture solutions.")

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.markdown(
    "<center>Made with ❤️ for Farmers</center>",
    unsafe_allow_html=True
)
