import streamlit as st
from PIL import Image
import requests
from streamlit_mic_recorder import speech_to_text

# PAGE SETTINGS
st.set_page_config(
    page_title="AI Farming Assistant",
    page_icon="🌱",
    layout="centered"
)

# TITLE
st.title("🌱 AI Farming Assistant")
st.write("Upload a crop image to detect possible disease.")

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

# Chatbot Answers
if user_question:

    question = user_question.lower()

    if "fertilizer" in question:
        st.success(
            "Use nitrogen-rich fertilizer for better crop growth."
        )

    elif "water" in question:
        st.success(
            "Most crops need regular watering but avoid overwatering."
        )

    elif "disease" in question:
        st.success(
            "Upload crop image above to detect disease."
        )

    elif "pesticide" in question:
        st.success(
            "Use recommended pesticides carefully and follow safety guidelines."
        )

    else:
        st.info(
            "Please ask farming related questions."
        )
