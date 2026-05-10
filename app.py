import streamlit as st
from PIL import Image
import random

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
