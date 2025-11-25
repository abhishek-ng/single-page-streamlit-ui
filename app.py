import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import google.generativeai as genai
import base64
from dotenv import load_dotenv
import os

st.set_page_config(layout="wide")

# Load .env file
load_dotenv()

# Read API Key securely
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

st.title("PDF Text Extraction using Gemini")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("PDF Preview")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    pdf_bytes = None

    if uploaded_file:
        pdf_bytes = uploaded_file.read()
        pdf_viewer(pdf_bytes)

with col2:
    st.header("Gemini Extracted Text")

    if uploaded_file and pdf_bytes:
        # Encode PDF as base64 (required by Gemini for file input)
        pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")

        model = genai.GenerativeModel("gemini-pro-vision")


        with st.spinner("Extracting text using Gemini..."):
            response = model.generate_content(
                [
                    {
                        "mime_type": "application/pdf",
                        "data": pdf_b64
                    },
                    "Extract all readable text from this PDF. Return only clean text, no explanation."
                ]
            )

        extracted_text = response.text
        st.text_area("Text Extracted by Gemini", extracted_text, height=700)
