import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os

# API Key
api_key = "AIzaSyCzWmYUHD6i1rT6qWLpKVubDGpB4m8PDLg"

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks, api_key):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question, api_key):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("Reply: ", response["output_text"])

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
            user_input(user_question, api_key)
else:
    st.info("👆 Please upload and process your documents first!")
