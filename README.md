# 📘 AskMyDocs

AskMyDocs is an intelligent, conversational document analysis tool that allows you to chat with your documents. Upload PDFs or provide website URLs, and get instant answers, summaries, and insights from your content.

---

## 🚀Live Demo
👉 [echodocs.streamlit.app](https://echodocs.streamlit.app)

---
## ✨ Key Features
Multi-Source Input: Upload multiple PDF files or provide a list of website URLs for analysis.
Conversational Q&A: Ask questions in natural language and get accurate answers based on the document content.
Source Verification: Each answer is accompanied by snippets from the original documents, allowing for easy verification.
Dynamic Theming: Switch between a clean light mode and a professional dark mode. 
Session Management: Your chat history is saved for your session, and you can easily reset the index to start fresh.

---
## 🛠 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Ashi12218684/AskmyDocs.git
cd AskmyDocs
````

### 2️⃣ Create and activate a virtual environment

```bash
# Linux / Mac
python -m venv venv
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file in the project root and add your API key:

```
GROQ_API_KEY="your_api_key_here"
```

### 5️⃣ Run the app

```bash
streamlit run app.py
```

---

## ⚙ Tech Stack

* Python 3.9+
* Streamlit – Interactive UI
* LangChain – LLM Orchestration
* FAISS – Vector Search
* Hugging Face Transformers – Embeddings / Models
* PyMuPDF – PDF Parsing
* python-dotenv – Environment Management

---

## 📂 Project Structure

```
AskmyDocs/
│── app.py               # Streamlit main app
│── requirements.txt     # Python dependencies
│── .env.example         # Example environment variables
│── utils/               # Helper functions
│── data/                # Uploaded PDFs
│── vectorstore/         # FAISS index storage
```

---

## 🤝 Contribution

Contributions are welcome!

1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit changes
4. Push to your branch
5. Open a Pull Request

---
