# 🔍 AskMyDocs – AI-Powered Document Q&A  

AskMyDocs is an **AI-driven document assistant** that allows you to upload PDFs, ask natural language questions, and receive context-aware answers.  
Built with **LangChain, FAISS, Hugging Face embeddings, and Streamlit**, it’s your personal knowledge retriever.  

---

## 🌟 Features  

- 📄 **Upload & Parse PDFs** (via PyMuPDF)  
- 🤖 **Ask Questions in Natural Language**  
- ⚡ **Fast Vector Search with FAISS**  
- 🧠 **Contextual Answers using Hugging Face models**  
- 🌍 **Streamlit Web App Interface**  
- 🔑 **GROQ API Integration**  

---

## 🖥️ Demo  

👉 **[Live Demo](https://your-streamlit-link.com)** (replace with your Streamlit Cloud link)  

![Demo Screenshot](demo.gif)  
*(Replace with your own screenshot or GIF)*  

---

## 🚀 Getting Started  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/Ashi12218604/AskmyDocs.git
cd AskmyDocs

**### 2️⃣ Create and activate a virtual environment**
# Linux / Mac
python -m venv venv
source venv/bin/activate  

# Windows
venv\Scripts\activate

**### 3️⃣ Install dependencies**
pip install -r requirements.txt
**
###4️⃣ Set up environment variables
**
Create a .env file in the project root and add your API key:

GROQ_API_KEY="your_api_key_here"

**### 5️⃣ Run the app**
streamlit run app.py

⚙️ Tech Stack

Python 3.9+

Streamlit – Interactive UI

LangChain – LLM Orchestration

FAISS – Vector Search

Hugging Face Transformers – Embeddings / Models

PyMuPDF – PDF Parsing

dotenv – Environment Management

📂 Project Structure
AskmyDocs/
│── app.py               # Streamlit main app
│── requirements.txt     # Dependencies
│── .env                 # API keys (not committed)
│── README.md            # Project documentation
│── /data                # Uploaded documents
│── /vectorstore         # FAISS index storage

🤝 Contributing

Contributions are welcome! 🎉

Fork the repo

Create your feature branch (git checkout -b feature-name)

Commit changes (git commit -m 'Added feature XYZ')

Push to branch (git push origin feature-name)

Open a Pull Request

📜 License

This project is licensed under the MIT License – see the LICENSE file for details.

⭐ Support

If you like this project, give it a ⭐ on GitHub!
It helps more people discover AskMyDocs 🚀

