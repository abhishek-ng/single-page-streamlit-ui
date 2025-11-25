import streamlit as st
import base64

st.title("PDF Upload & Preview")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # Read file as bytes
    pdf_bytes = uploaded_file.read()

    # Convert to base64 for embedding
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

    # Display PDF
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px"></iframe>'
    
    st.markdown(pdf_display, unsafe_allow_html=True)

    st.success("PDF loaded successfully!")
