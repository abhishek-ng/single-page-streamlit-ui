import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

st.title("PDF Upload & Preview (Edge Friendly)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    pdf_viewer(uploaded_file.read())
