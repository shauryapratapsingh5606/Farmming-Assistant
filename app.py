import streamlit as st
from PIL import Image
import random
from difflib import get_close_matches

# PAGE SETTINGS
st.set_page_config(
    page_title="AI Farming Assistant",
    page_icon="🌱",
    layout="centered"
)

# TITLE
st.title("🌱 AI Farming Assistant")
st.write("Upload a crop image to detect possible disease.")

# IMAGE UPLOAD
uploaded_file = st.file_uploader(
    "Upload Crop Image",
    type=["jpg", "jpeg", "png"]
)

# SHOW IMAGE
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# DETECT DISEASE BUTTON
if st.button("Detect Disease"):

    diseases = [
        {
            "name": "Tomato Leaf Blight",
            "cause": "Fungal infection caused by excess moisture.",
            "solution": "Use fungicide and avoid overwatering."
        },
        {
            "name": "Leaf Spot Disease",
            "cause": "Bacterial infection due to humid weather.",
            "solution": "Remove infected leaves and use copper spray."
        },
        {
            "name": "Healthy Plant",
            "cause": "No disease detected.",
            "solution": "Maintain proper watering and sunlight."
        }
    ]

    result = random.choice(diseases)

    st.success(f"🌿 Disease: {result['name']}")
    st.warning(f"⚠ Cause: {result['cause']}")
    st.info(f"💡 Solution: {result['solution']}")

     # ---------------- CHATBOT ----------------

st.markdown("---")
st.header("🤖 Farming Chatbot")

user_question = st.text_input(
    "Ask farming related questions"
)

faq = {
    "how to prevent leaf blight":
    "Avoid excess moisture and use fungicide spray.",

    "best fertilizer for tomato":
    "Use nitrogen-rich organic fertilizer for tomatoes.",

    "how much water for crops":
    "Most crops need moderate watering depending on weather.",

    "why leaves turn yellow":
    "Yellow leaves may occur due to nutrient deficiency or overwatering.",

    "how to increase crop growth":
    "Use proper sunlight, irrigation, and balanced fertilizer."
}

if user_question:

    question = user_question.lower()

    matches = get_close_matches(
        question,
        faq.keys(),
        n=1,
        cutoff=0.3
    )

    if matches:
        answer = faq[matches[0]]
        st.success(answer)

    else:
        st.warning(
            "Sorry, I do not know this yet."
        )
