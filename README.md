📚 PDF Insight AI

An intelligent PDF document analyzer powered by Google's Gemini AI + LangChain. This application allows users to upload PDF documents and get instant, accurate answers to their questions about the content.

---

## 🌟 Demo

![PDF Insight AI Demo](video/v1.gif)
![LangChain Architecture](video/arch_animation.gif)
![User Interaction](video/chatflow.gif)

---

## 🚀 Skills & Technologies Showcased

### 🧠 AI & LLMs
- Retrieval-Augmented Generation (RAG) using LangChain
- Prompt engineering and context-aware Gemini Pro models
- Conversational agents with **Gemini 2.0 Flash**
- AI-powered **vector search** using FAISS

### 📚 Document Intelligence
- Text extraction using **PyPDF2**
- Recursive chunking with **LangChain TextSplitter**
- Embeddings via `GoogleGenerativeAIEmbeddings`

### ⚙️ Full Stack Development
- Interactive **Streamlit** UI for seamless user interaction
- Environment variable handling with **dotenv**
- Efficient session management using `st.session_state`
- Clean modular structure: `utils/pdf_processor.py`, `utils/ai_model.py`

### 🛡️ Security and Best Practices
- 🔐 API key management using `.env`
- 🔒 Secure, local-only document processing
- 📁 Vector DB saved and loaded locally with safe deserialization

---

## 🛠️ Features

- 📄 Process multiple PDF files
- 🔍 Smart document chunking and storage
- 💬 Ask questions about the uploaded content
- ⚡ Instant response with context-aware accuracy
- 🎯 RAG-based querying using Gemini
- 💾 Save and reload vector database

---

## 📦 Prerequisites

- Python 3.8 or higher
- Google API Key

---

## 📥 Installation

```bash
git clone https://github.com/yourusername/pdf-insight-ai.git
cd pdf-insight-ai
pip install -r requirements.txt
```

Add your API key to `.env`:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

---

## ▶️ Usage

```bash
streamlit run src/app.py
```

Then go to [http://localhost:8501](http://localhost:8501)

---

## 🧾 Project Structure

```
pdf-insight-ai/
├── src/
│   ├── utils/
│   │   ├── pdf_processor.py
│   │   └── ai_model.py
│   └── app.py
├── data/
│   └── vector_store/
├── video/
│   ├── v1.gif
│   ├── arch_animation.gif
│   └── chatflow.gif
├── .env
├── requirements.txt
└── README.md
```

---

## 🤝 Contributing

Contributions, feedback, and forks are welcome!


