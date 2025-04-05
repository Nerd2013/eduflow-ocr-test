
import streamlit as st
from PIL import Image
import pytesseract

st.title("EduFlow OCR Test")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    text = pytesseract.image_to_string(image)
    st.subheader("Extracted Text")
    st.text(text if text.strip() else "No text detected.")
