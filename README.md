📄 AskMyDocs
<p align="center"> <img src="https://i.imgur.com/your-app-gif-url.gif" alt="AskMyDocs Demo GIF" width="800"/> </p>

AskMyDocs is an intelligent, conversational document analysis tool that allows you to chat with your documents. Upload PDFs or provide website URLs, and get instant answers, summaries, and insights from your content.

🔗 Live Demo Here

🎯 Project Purpose

This application was developed as a submission for the Haqdarshak Scheme Research Application assignment.

The goal was to build an automated tool to streamline the process of researching and understanding government schemes from various online sources. It leverages AI + ML technologies to make complex information more accessible and queryable.

✨ Key Features

📂 Multi-Source Input – Upload multiple PDF files or provide URLs for analysis.

💬 Conversational Q&A – Ask natural language questions and get context-based answers.

🔍 Source Verification – Each answer includes snippets from original documents.

🎨 Dynamic Theming – Toggle between Light and Dark modes.

💾 Session Management – Your chat history is preserved during the session.

🛠️ Tech Stack

Framework: Streamlit

LLM: Groq (LLaMA 3 – 8B)

Core Library: LangChain

Embeddings: Hugging Face (Sentence Transformers)

Vector Store: FAISS (Facebook AI Similarity Search)

File Processing: PyMuPDF (PDFs), Unstructured (URLs)

⚙️ How to Run Locally

Clone the Repository

git clone https://github.com/Ashi12218604/AskmyDocs.git
cd AskmyDocs


Create a Virtual Environment

python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate


Install Dependencies

pip install -r requirements.txt


Set Up API Key
Create a .env file in the project root and add your Groq API key:

GROQ_API_KEY="gsk_YourGroqApiKeyGoesHere"


Run the Application

streamlit run main.py


App will open at: http://localhost:8501

🚀 Future Work

📑 Export chat history to PDF/CSV

📌 Advanced metadata filtering (filter Q&A by source doc)

📂 Support for more file types (.docx, .txt)

🙏 Acknowledgements

Groq for blazing-fast LLM inference

Hugging Face for embeddings & models

LangChain for orchestration

Streamlit for an interactive front-end
