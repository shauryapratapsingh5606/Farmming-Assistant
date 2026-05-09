import streamlit as st
from PIL import Image
import requests
import io

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI Farming Assistant",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 AI Farming Assistant")
st.write("Upload a crop image to detect disease using AI.")

# ---------------- HUGGING FACE API ----------------

API_URL = "https://api-inference.huggingface.co/models/microsoft/resnet-50"

headers = {
    "Authorization": "Bearer YOUR_HUGGINGFACE_TOKEN"
}

# ---------------- DISEASE INFO ----------------

disease_info = {
    "Tomato Early Blight": {
        "cause": "Fungal infection caused by Alternaria solani.",
        "solution": "Use fungicides and remove infected leaves."
    },
    "Tomato Late Blight": {
        "cause": "Caused by Phytophthora infestans fungus.",
        "solution": "Avoid excess moisture and spray fungicide."
    },
    "Healthy": {
        "cause": "No disease detected.",
        "solution": "Maintain proper watering and nutrition."
    }
}

# ---------------- IMAGE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload Crop Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Detect Disease"):

        with st.spinner("Detecting disease..."):

            image_bytes = uploaded_file.getvalue()

            response = requests.post(
                API_URL,
                headers=headers,
                data=image_bytes
            )
            if response.status_code != 200:
                st.error("API Error: " + response.text)
                st.stop()
            result = response.json()

            try:
                prediction = result[0]['label']
confidence = result[0]['score']

st.success(f"Prediction: {prediction}")
st.info(f"Confidence: {confidence:.2f}")

if "leaf" in prediction.lower():
    st.subheader("Possible Cause")
    st.write("The crop may be affected by a fungal or bacterial disease.")

    st.subheader("Recommended Solution")
    st.write("Remove infected leaves and use proper fungicide spray.")
else:
    st.subheader("Status")
    st.write("Plant condition appears normal.")

                st.success(f"Detected Disease: {disease}")
                st.info(f"Confidence: {confidence:.2f}")

                if disease in disease_info:

                    st.subheader("Cause")
                    st.write(disease_info[disease]["cause"])

                    st.subheader("Solution")
                    st.write(disease_info[disease]["solution"])

                else:
                    st.warning("Disease information not available.")

            except:
                st.error("Unable to detect disease. Try another image.")
