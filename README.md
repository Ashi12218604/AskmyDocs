# AskmyDocs
AskMyDocs 📝
<p align="center">
<img src="https://www.google.com/search?q=https://i.imgur.com/your-app-gif-url.gif" alt="AskMyDocs Demo GIF" width="800"/>
</p>

AskMyDocs is an intelligent, conversational document analysis tool that allows you to chat with your documents. Upload PDFs or provide website URLs, and get instant answers, summaries, and insights from your content.

🚀 Live Demo
You can access the live application here:
https://echodocs.streamlit.app/

🎯 Project Purpose
This application was developed as a submission for the Haqdarshak Scheme Research Application assignment. The primary goal was to build an automated tool to streamline the process of researching and understanding government schemes from various online sources. It leverages modern AI and machine learning technologies to make complex information accessible and easy to query.

✨ Key Features
Multi-Source Input: Upload multiple PDF files or provide a list of website URLs for analysis.

Conversational Q&A: Ask questions in natural language and get accurate answers based on the document content.

Source Verification: Each answer is accompanied by snippets from the original documents, allowing for easy verification.

Dynamic Theming: Switch between a clean light mode and a professional dark mode.

Session Management: Your chat history is saved for your session, and you can easily reset the index to start fresh.

🛠️ Tech Stack
![Hugging Face](https://www.google.com/search?q=https://img.shields.io/badge/%25F0%259F%25A4% hugging%20face-FFD21E?style=for-the-badge)

Framework: Streamlit

Language Model (LLM): Groq (via llama3-8b-8192)

Core Libraries: LangChain

Embeddings: Hugging Face (sentence-transformers)

Vector Store: FAISS (Facebook AI Similarity Search)

File Processing: PyMuPDF for PDFs, Unstructured for URLs

⚙️ How to Run Locally
To run this project on your local machine, follow these steps:

1. Clone the Repository

git clone [https://github.com/Ashi12218604/AskmyDocs.git](https://github.com/Ashi12218604/AskmyDocs.git)
cd AskmyDocs

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies

pip install -r requirements.txt

4. Set Up Your API Key
Create a file named .env in the root of the project and add your Groq API key:

GROQ_API_KEY="gsk_YourGroqApiKeyGoesHere"

5. Run the Application

streamlit run main.py

The application will open in your web browser at http://localhost:8501.

🚀 Future Work
Export to PDF/CSV: Add functionality to download the chat history or generated summaries.

Advanced Metadata Filtering: Allow users to filter their questions by a specific source document.

Support for More File Types: Expand the application to handle .docx and .txt files.

🙏 Acknowledgements
This project was made possible by the powerful and freely accessible models from Groq and Hugging Face, and the incredible open-source libraries like LangChain and Streamlit.
