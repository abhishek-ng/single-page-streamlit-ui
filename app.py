import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import google.generativeai as genai
import tempfile

st.set_page_config(layout="wide")

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("PDF Text Extraction using Gemini (Correct File Upload Method)")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("PDF Preview")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    temp_path = None

    if uploaded_file:
        # Write uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        pdf_viewer(open(temp_path, "rb").read())

with col2:
    st.header("Extracted Text")

    if uploaded_file and temp_path:
        with st.spinner("Uploading PDF to Gemini…"):
            uploaded_pdf = genai.upload_file(temp_path)

        model = genai.GenerativeModel("gemini-1.5-flash")

        with st.spinner("Extracting text…"):
            response = model.generate_content(
                [
                    uploaded_pdf,
                    "Extract all readable text from this PDF. Return only the plain text, no explanations."
                ]
            )

        extracted_text = response.text
        st.text_area("Extracted Text", extracted_text, height=700)
