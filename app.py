import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Farming Assistant",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 Farming Assistant")

st.subheader("Crop Disease Detection System")

st.write("Upload a crop image to detect disease.")

uploaded_file = st.file_uploader(
    "Upload Crop Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Crop Image",
        use_container_width=True
    )

    if st.button("Detect Disease"):
        st.success("Disease detection will appear here.")

else:
    st.info("Please upload a crop image.")
  
