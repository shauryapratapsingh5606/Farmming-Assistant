import streamlit as st
from PIL import Image
import requests

# PAGE SETTINGS
st.set_page_config(
    page_title="AI Farming Assistant",
    page_icon="🌱",
    layout="centered"
)

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
                st.error("API Error")
                st.write(response.text)

            else:

                result = response.json()

                prediction = result[0]['label']
                confidence = result[0]['score']

                st.success(f"Prediction: {prediction}")
                st.info(f"Confidence: {confidence:.2f}")

                # SIMPLE AI ANALYSIS

                if "leaf" in prediction.lower():

                    st.subheader("Possible Cause")
                    st.write(
                        "The crop may be affected by fungal or bacterial infection."
                    )

                    st.subheader("Recommended Solution")
                    st.write(
                        "Remove infected leaves and spray proper fungicide."
                    )

                else:

                    st.subheader("Plant Status")
                    st.write("Plant appears mostly healthy.")
