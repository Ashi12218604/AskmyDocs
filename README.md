# AskmyDocs
AskMyDocs 📝
AskMyDocs is an intelligent, conversational document analysis tool that allows you to chat with your documents. Upload PDFs or provide website URLs, and get instant answers, summaries, and insights from your content.

🚀 Live Demo
You can access the live application here:
https://echodocs.streamlit.app/

✨ Key Features
Multi-Source Input: Upload multiple PDF files or provide a list of website URLs for analysis.

Conversational Q&A: Ask questions in natural language and get accurate answers based on the document content.

Source Verification: Each answer is accompanied by snippets from the original documents, allowing for easy verification.

Structured Summaries: Generate organized summaries based on key criteria like benefits, application processes, and eligibility.

Dynamic Theming: Switch between a clean light mode and a professional dark mode for a comfortable user experience.

Session Management: Your chat history is saved for your session, and you can easily reset the index and conversation to start fresh.

🛠️ Tech Stack
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

📸 Application Screenshot
(Note: You should replace the URL above with a direct link to a screenshot of your application. You can upload an image to a service like Imgur to get a link.)
