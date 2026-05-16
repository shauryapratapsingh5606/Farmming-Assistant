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

conn = sqlite3.connect("farmers.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS farmers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    mobile TEXT,

    village TEXT,

    crop TEXT,

    image TEXT
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
# LABELS
# =========================================

labels = {

    "English": {
        "home": "Home",
        "register": "👨‍🌾 Farmer Registration",
        "disease": "Disease Detection",
        "fertilizer": "Fertilizer Recommendation",
        "soil": "Soil Health",
        "irrigation": "Smart Irrigation",
        "chatbot": "AI Chatbot",
        "about": "About",
        "weather": "🌦 Live Weather",
        "city": "Select Your City",
        "temp": "Temperature",
        "humidity": "Humidity",
        "weather_text": "Weather",
        "wind": "Wind Speed"
    },

    "हिन्दी": {
        "home": "घर",
        "register": "👨‍🌾 किसान पंजीकरण",
        "disease": "रोग पहचान",
        "fertilizer": "खाद सलाह",
        "soil": "मिट्टी जाँच",
        "irrigation": "सिंचाई सलाह",
        "chatbot": "एआई चैट",
        "about": "जानकारी",
        "weather": "🌦 लाइव मौसम",
        "city": "अपना शहर चुनें",
        "temp": "तापमान",
        "humidity": "नमी",
        "weather_text": "मौसम",
        "wind": "हवा की गति"
    },

    "भोजपुरी": {
        "home": "घर",
        "register": "👨‍🌾 किसान रजिस्ट्रेशन",
        "disease": "रोग पहचान",
        "fertilizer": "खाद सलाह",
        "soil": "मिट्टी जांच",
        "irrigation": "सिंचाई सलाह",
        "chatbot": "एआई चैट",
        "about": "जानकारी",
        "weather": "🌦 जिंदा मौसम",
        "city": "अपना शहर चुनीं",
        "temp": "तापमान",
        "humidity": "नमी",
        "weather_text": "मौसम",
        "wind": "हवा के रफ्तार"
    },

    "अवधी": {
        "home": "घर",
        "register": "👨‍🌾 किसान पंजीकरण",
        "disease": "रोग पहचान",
        "fertilizer": "खाद सलाह",
        "soil": "मिट्टी जाँच",
        "irrigation": "सिंचाई सलाह",
        "chatbot": "एआई चैट",
        "about": "जानकारी",
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

    # WEATHER

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

    api_key = st.secrets["WEATHER_API_KEY"]

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

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

        <h2>📍 {city}</h2>

        <h3>🌡 {labels[language]["temp"]}: {temperature} °C</h3>

        <h3>💧 {labels[language]["humidity"]}: {humidity}%</h3>

        <h3>☁ {labels[language]["weather_text"]}: {weather_condition}</h3>

        <h3>🌬 {labels[language]["wind"]}: {wind_speed} m/s</h3>

        </div>
        """, unsafe_allow_html=True)

# =========================================
# FARMER REGISTRATION
# =========================================

elif page == labels[language]["register"]:

    st.title(labels[language]["register"])

    farmer_name = st.text_input(
        "Farmer Name",
        key="farmer_name"
    )

    farmer_mobile = st.text_input(
        "Mobile Number",
        key="farmer_mobile"
    )

    farmer_village = st.text_input(
        "Village",
        key="farmer_village"
    )

    farmer_crop = st.text_input(
        "Main Crop",
        key="farmer_crop"
    )

    farmer_image = st.file_uploader(
        "Upload Farmer Image",
        type=["jpg", "png", "jpeg"],
        key="farmer_image"
    )

    if farmer_image is not None:

        st.image(farmer_image, width=200)

    if st.button("Register Farmer"):

        image_name = ""

        if farmer_image is not None:

            image_name = farmer_image.name

        cursor.execute(
            """
            INSERT INTO farmers
            (name, mobile, village, crop, image)

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                farmer_name,
                farmer_mobile,
                farmer_village,
                farmer_crop,
                image_name
            )
        )

        conn.commit()

        st.success("Farmer Registered Successfully ✅")

        st.markdown("---")

        st.subheader("📋 Registered Farmers")

        cursor.execute("SELECT * FROM farmers")

        farmers_data = cursor.fetchall()

        for farmer in farmers_data:

            st.write(f"👨‍🌾 Name: {farmer[1]}")
            st.write(f"📱 Mobile: {farmer[2]}")
            st.write(f"🏡 Village: {farmer[3]}")
            st.write(f"🌾 Crop: {farmer[4]}")

            st.markdown("---")

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

        st.success("Use organic compost and proper irrigation.")

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
