# 📘 AskMyDocs

AskMyDocs is a Document Question-Answering application powered by LangChain, FAISS, Hugging Face embeddings, and Groq LLMs. It allows users to upload PDFs and interactively query them using a conversational interface.

---

## 🚀Live Demo
👉 echo.streamlit.app

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
