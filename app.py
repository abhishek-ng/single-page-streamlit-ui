import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

st.title("PDF Upload & Preview")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    pdf_viewer(uploaded_file.read())
