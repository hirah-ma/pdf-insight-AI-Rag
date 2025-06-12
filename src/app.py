import streamlit as st
import os
from dotenv import load_dotenv
from utils.pdf_processor import get_pdf_text, get_text_chunks, get_vector_store
from utils.ai_model import process_user_query

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Please set your GOOGLE_API_KEY in the .env file")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title="PDF Insight AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False

# Main UI
st.title("📚 PDF Insight AI")
st.markdown("""
### Your AI-Powered PDF Assistant

Transform your PDFs into interactive knowledge with our advanced AI assistant. Upload your documents and get instant, accurate answers to your questions.

#### Features:
- 📄 Process multiple PDF files
- 🔍 Smart document analysis
- 💡 Instant answers to your questions
- 🎯 Context-aware responses
""")

# File uploader in sidebar
with st.sidebar:
    st.title("📤 Upload & Process")
    st.markdown("---")
    pdf_docs = st.file_uploader("Choose your PDF files", accept_multiple_files=True, type=['pdf'])
    if st.button("🚀 Process Documents", type="primary") and pdf_docs:
        with st.spinner("Processing your documents..."):
            # Process PDFs
            raw_text = get_pdf_text(pdf_docs)
            text_chunks = get_text_chunks(raw_text)
            get_vector_store(text_chunks, api_key)
            st.session_state.processed = True
            st.success("✨ Documents processed successfully!")

# Main chat interface
if st.session_state.processed:
    st.markdown("---")
    st.subheader("💭 Ask Questions About Your Documents")
    user_question = st.text_input("Type your question here:", placeholder="What would you like to know?")
    if user_question:
        with st.spinner("🤔 Thinking..."):
            response = process_user_query(user_question, api_key)
            st.write("Reply: ", response)
else:
    st.info("👆 Please upload and process your documents first!") 