📄 AskMyDocs 📝
<p align="center"> <img src="https://i.imgur.com/your-app-banner.png" alt="AskMyDocs Banner" width="800"/> </p> <p align="center"> <a href="https://echodocs.streamlit.app/"><img src="https://img.shields.io/badge/🚀 Live Demo-Click%20Here-brightgreen?style=for-the-badge" /></a> <a href="https://github.com/Ashi12218604/AskMyDocs/stargazers"><img src="https://img.shields.io/github/stars/Ashi12218604/AskMyDocs?style=for-the-badge" /></a> <a href="https://github.com/Ashi12218604/AskMyDocs/issues"><img src="https://img.shields.io/github/issues/Ashi12218604/AskMyDocs?style=for-the-badge&color=yellow" /></a> </p>
🎯 Project Purpose

An intelligent, conversational document analysis tool built for the Haqdarshak Scheme Research Application assignment.

✅ Helps streamline research on government schemes
✅ Uses AI/ML to make complex info queryable
✅ Works with PDFs + URLs

✨ Features

📂 Multi-Source Input → Upload PDFs or paste URLs

💬 Conversational Q&A → Ask in natural language

🔍 Source Verification → Snippets included with answers

🎨 Dynamic Theming → Light & Dark mode toggle

💾 Session Management → Save/reset chat history

<details> <summary>🛠️ Tech Stack (click to expand)</summary>

Framework: Streamlit

LLM: Groq (LLaMA 3 – 8B)

Core Library: LangChain

Embeddings: Hugging Face Sentence Transformers

Vector Store: FAISS

File Processing: PyMuPDF, Unstructured

</details>
⚙️ Run Locally
# 1. Clone the repo
git clone https://github.com/Ashi12218604/AskmyDocs.git
cd AskmyDocs

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key in .env
echo GROQ_API_KEY="your_api_key_here" > .env

# 5. Run the app
streamlit run main.py

🚀 Roadmap

 Export chat history to PDF/CSV

 Advanced metadata filtering

 Support .docx & .txt

📸 Demo
<p align="center"> <img src="https://i.imgur.com/your-demo-gif.gif" alt="AskMyDocs Demo" width="800"/> </p>
🙏 Acknowledgements

Groq – fast LLM inference

Hugging Face – embeddings/models

LangChain – orchestration

Streamlit – UI framework
