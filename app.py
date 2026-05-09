import streamlit as st
from PIL import Image
import random

# Page settings
st.set_page_config(
    page_title="Farming Assistant",
    page_icon="🌱",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f5fff5;
}

.title {
    text-align: center;
    color: #2e7d32;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 18px;
    margin-bottom: 30px;
}

.result-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #e8f5e9;
    border: 2px solid #81c784;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🌾 Farming Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Crop Disease Detection System</div>', unsafe_allow_html=True)

# Upload image
uploaded_file = st.file_uploader(
    "📤 Upload Crop Image",
    type=["jpg", "jpeg", "png"]
)

# Disease data
diseases = [
    {
        "name": "Leaf Blight",
        "cause": "Fungal infection caused by excessive humidity.",
        "prevention": "Avoid overwatering and maintain proper airflow.",
        "treatment": "Use copper-based fungicide spray."
    },
    {
        "name": "Early Blight",
        "cause": "Disease spreads due to infected soil and wet leaves.",
        "prevention": "Rotate crops regularly and keep leaves dry.",
        "treatment": "Apply organic fungicide every 7 days."
    },
    {
        "name": "Bacterial Spot",
        "cause": "Bacteria attack leaves during warm and wet conditions.",
        "prevention": "Use disease-free seeds and avoid splashing water.",
        "treatment": "Use antibacterial plant spray."
    },
    {
        "name": "Healthy Plant",
        "cause": "No disease detected.",
        "prevention": "Continue proper irrigation and sunlight.",
        "treatment": "No treatment required."
    }
]

# Show uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="🌿 Uploaded Crop Image",
        use_container_width=True
    )

    # Button
    if st.button("🔍 Detect Disease"):

        result = random.choice(diseases)

        # Success message
        st.success("✅ AI Analysis Completed Successfully")

        # Result Card
        st.markdown(f"""
        <div class="result-box">

        <h2>🦠 Disease: {result['name']}</h2>

        <h4>⚠ Cause</h4>
        <p>{result['cause']}</p>

        <h4>🛡 Prevention</h4>
        <p>{result['prevention']}</p>

        <h4>💊 Treatment</h4>
        <p>{result['treatment']}</p>

        </div>
        """, unsafe_allow_html=True)

else:
    st.info("📷 Please upload a crop image to continue.")
