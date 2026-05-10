import streamlit as st
from PIL import Image
import requests
from streamlit_mic_recorder import speech_to_text
import google.generativeai as genai

# PAGE SETTINGS
st.set_page_config(
    page_title="AI Farming Assistant",
    page_icon="🌱",
    layout="centered"
)

# CUSTOM CSS
st.markdown("""
<style>

body {
    background-color: #f1fff0;
}

.main {
    background: linear-gradient(to bottom, #f1fff0, #ffffff);
    padding: 2rem;
    border-radius: 20px;
}

/* TITLE */
h1 {
    color: #1b5e20;
    text-align: center;
    font-size: 52px;
    font-weight: bold;
}

/* SUBHEADINGS */
h2, h3 {
    color: #2e7d32;
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(90deg, #2e7d32, #43a047);
    color: white;
    border-radius: 14px;
    height: 3.2em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #1b5e20, #2e7d32);
    transform: scale(1.02);
    color: white;
}

/* INPUT BOX */
.stTextInput>div>div>input {
    border-radius: 12px;
    border: 2px solid #a5d6a7;
    padding: 10px;
}

/* FILE UPLOADER */
section[data-testid="stFileUploader"] {
    border: 2px dashed #66bb6a;
    padding: 20px;
    border-radius: 15px;
    background-color: #f8fff8;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #e8f5e9;
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
        "AI Chatbot",
        "About"
    ]
)

# TITLE
st.title("🌱 AI Farming Assistant")
st.write("Upload a crop image to detect possible disease.")

# GEMINI API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# HUGGING FACE API
API_URL = "https://router.huggingface.co/hf-inference/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
# DISEASE INFORMATION DATABASE

disease_info = {

    "rust": {
        "cause": "Rust fungus caused by wet conditions.",
        "treatment": "Spray Mancozeb or Copper Fungicide.",
        "organic": "Use neem oil spray every 7 days.",
        "prevention": "Avoid excess watering and improve airflow."
    },

    "blight": {
        "cause": "Blight spreads due to fungus and humidity.",
        "treatment": "Use Chlorothalonil fungicide.",
        "organic": "Remove infected leaves and use compost tea.",
        "prevention": "Keep leaves dry and maintain spacing."
    },

    "leaf scorch": {
        "cause": "Leaf scorch occurs due to heat or fungal infection.",
        "treatment": "Use balanced fertilizer and fungicide.",
        "organic": "Use organic compost and proper irrigation.",
        "prevention": "Avoid water stress and extreme heat."
    },

    "healthy": {
        "cause": "Your crop is healthy.",
        "treatment": "No treatment needed.",
        "organic": "Maintain good farming practices.",
        "prevention": "Continue regular monitoring."
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
                headers={
                    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}",
                    "Content-Type": "image/jpeg"
                },
                data=image_bytes
            )

            try:
                result = response.json()

                if isinstance(result, list):

                    disease = result[0]['label']
                    confidence = result[0]['score']

                    # RESULT CARD
                    st.markdown(f"""
                    <div style="
                    background: linear-gradient(135deg,#e8f5e9,#ffffff);
                    padding:25px;
                    border-radius:20px;
                    box-shadow:0px 4px 15px rgba(0,0,0,0.1);
                    margin-top:20px;
                    ">

                    <h2 style="color:#1b5e20;">
                    🌱 Disease Detected
                    </h2>

                    <h3 style="color:#d32f2f;">
                    {disease}
                    </h3>

                    <p style="font-size:18px;">
                    <b>Confidence Score:</b> {round(confidence * 100, 2)}%
                    </p>

                      </div>
                    """, unsafe_allow_html=True)

    found = False

    for key in disease_info:

        if key in disease.lower():

            info = disease_info[key]

            st.warning(f"Cause: {info['cause']}")

            st.info(f"Treatment: {info['treatment']}")

            st.success(f"Organic Solution: {info['organic']}")

            st.error(f"Prevention: {info['prevention']}")

           found = True

           break

if not found:

    st.warning("Disease information currently unavailable.")
        

                        st.markdown("""
                        <div style="
                        background-color:#fff3e0;
                        padding:18px;
                        border-radius:15px;
                        margin-top:10px;
                        ">

                        <h4>🦠 Cause</h4>
                        Fungal infection due to humidity and excess moisture.

                        <h4>💊 Treatment</h4>
                        Use Chlorothalonil or Mancozeb fungicide spray.

                        <h4>🌿 Organic Solution</h4>
                        Spray baking soda mixed with water weekly.

                        <h4>🛡 Prevention</h4>
                        Avoid overwatering and remove infected leaves.

                        <h4>🌱 Fertilizer Suggestion</h4>
                        Use balanced NPK fertilizer.

                        </div>
                        """, unsafe_allow_html=True)

                    # RUST
                    elif "rust" in disease.lower():

                        st.markdown("""
                        <div style="
                        background-color:#fff3e0;
                        padding:18px;
                        border-radius:15px;
                        margin-top:10px;
                        ">

                        <h4>🦠 Cause</h4>
                        Rust fungus caused by wet conditions.

                        <h4>💊 Treatment</h4>
                        Spray Mancozeb or Copper Fungicide every 7 days.

                        <h4>🌿 Organic Solution</h4>
                        Use Neem Oil spray on affected leaves.

                        <h4>🛡 Prevention</h4>
                        Avoid excess moisture and improve air circulation.

                        <h4>🌱 Fertilizer Suggestion</h4>
                        Use Potassium-rich fertilizer for stronger immunity.

                        </div>
                        """, unsafe_allow_html=True)

                    # HEALTHY
                    elif "healthy" in disease.lower():

                        st.markdown("""
                        <div style="
                        background-color:#e8f5e9;
                        padding:18px;
                        border-radius:15px;
                        margin-top:10px;
                        ">

                        <h3>✅ Plant is Healthy</h3>

                        Keep monitoring regularly and maintain proper nutrition.

                        🌱 Recommended:
                        Use organic compost and balanced fertilizer monthly.

                        </div>
                        """, unsafe_allow_html=True)

                    # OTHER
                    else:

                        st.markdown("""
                        <div style="
                        background-color:#fff3e0;
                        padding:18px;
                        border-radius:15px;
                        margin-top:10px;
                        ">

                        Disease information currently unavailable.

                        </div>
                        """, unsafe_allow_html=True)

                else:
                    st.error("API Error")
                    st.write(result)

            except Exception as e:
                st.error("Something went wrong.")
                st.write(e)

# CHATBOT SECTION
st.markdown("---")
st.header("🤖 Farming Chatbot")

# VOICE INPUT
voice_text = speech_to_text(
    language='en',
    use_container_width=True,
    just_once=True,
    key='voice'
)

# USER INPUT
user_question = st.text_input(
    "Ask farming related questions",
    value=voice_text if voice_text else ""
)

# AI RESPONSE
if user_question:

    prompt = f"""
    You are an agriculture expert.

    Support:
    - English
    - Hindi
    - Bhojpuri
    - Awadhi
    - Haryanvi
    - Punjabi
    - Marathi

    Give simple farming advice.

    User Question:
    {user_question}
    """

    try:
        response = model.generate_content(prompt)
        st.success(response.text)

    except Exception as e:
        st.error("Gemini AI Error")
        st.write(e)

# FOOTER
st.markdown("---")

st.markdown(
    "<center>Made with ❤️ for Farmers</center>",
    unsafe_allow_html=True
)
