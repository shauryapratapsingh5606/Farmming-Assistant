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
    background-color: #f4fff4;
}

.main {
    background-color: #f4fff4;
}

h1 {
    color: #2e7d32;
    text-align: center;
    font-size: 45px;
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
}

.css-1d391kg {
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
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

# HUGGING FACE API
API_URL = "https://router.huggingface.co/hf-inference/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"

headers = {
    "Authorization": "Bearer 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"
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

                    st.success(f"Detected Disease: {disease}")

                    st.info(
                        f"Confidence Score: {round(confidence * 100, 2)}%"
                    )

                    # Disease Causes
                    if "blight" in disease.lower():
                        st.warning(
                            "Cause: Fungal infection due to humidity and excess moisture."
                        )

                    elif "rust" in disease.lower():
                        st.warning(
                            "Cause: Rust fungus caused by wet conditions."
                        )

                    elif "healthy" in disease.lower():
                        st.success(
                            "Your crop appears healthy."
                        )

                    else:
                        st.warning(
                            "Cause information not available."
                        )

                else:
                    st.error("API Error")
                    st.write(result)

            except Exception as e:
                st.error("Something went wrong.")
                st.write(e)

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

    prompt = f"""
    You are an agriculture expert.
    Answer in simple language.
    Support Hindi and English.
    Give farming advice carefully.

    Question:
    {user_question}
    """

    response = model.generate_content(prompt)

    st.success(response.text)

   st.markdown("---")

st.markdown(
    "<center>Made with ❤️ for Farmers</center>",
    unsafe_allow_html=True
)
