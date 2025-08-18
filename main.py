import os
import pickle
import logging
import streamlit as st
import fitz  # PyMuPDF
from dotenv import load_dotenv

from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq

# ---- Setup Logging ----
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    filemode="a",
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

# ---- Environment Variables ----
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# ---- Custom CSS for Dark Mode ----
def apply_dark_mode_styles():
    st.markdown("""
    <style>
        .stApp {
            background-color: #0f0f0f;
            color: #ffffff;
        }
        .stSidebar {
            background-color: #1a1a1a;
        }
        h1, h2, h3, h4 {
            color: #3B82F6; /* <-- CHANGED COLOR */
        }
        .stTextInput > div > div > input, .stTextArea textarea {
            background-color: #262626;
            color: #ffffff;
        }
        .stButton > button {
            background-color: #3B82F6; /* <-- CHANGED COLOR */
            color: #ffffff; /* <-- CHANGED for better contrast */
            font-weight: bold;
            border: none;
            border-radius: 6px;
        }
        .stButton > button:hover {
            background-color: #2563EB; /* <-- CHANGED hover color */
        }
    </style>
    """, unsafe_allow_html=True)

# ---- Page Config and Title ----
st.set_page_config(page_title="AskMyDocs", layout="wide")
# st.title("AskMyDocs 📝")

# # ---- Sidebar ----
# st.sidebar.header("Settings")
# --- CHANGED: Radio button is now a toggle switch ---
dark_mode = st.sidebar.toggle("Enable Dark Mode", value=True)

# ---- Page Config and Title ----
st.set_page_config(page_title="AskMyDocs", layout="wide")
st.title("AskMyDocs 📝")

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_path" not in st.session_state:
    st.session_state.file_path = "faiss_index.pkl"

# ---- Sidebar ----
st.sidebar.header("Settings")

# --- NEW: Clear/Reset Button ---
if st.sidebar.button("Reset History"):
    if os.path.exists(st.session_state.file_path):
        os.remove(st.session_state.file_path)
    st.session_state.messages = []
    st.success("History and document index cleared.")
    st.rerun()

st.sidebar.header("Upload PDFs or Enter URLs")
uploaded_pdfs = st.sidebar.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
raw_urls = st.sidebar.text_area("Enter URLs (one per line)")
urls = [u.strip() for u in raw_urls.splitlines() if u.strip()]

if st.sidebar.button("Process Data"):
    # Clear old index if it exists
    if os.path.exists(st.session_state.file_path):
        os.remove(st.session_state.file_path)

    docs = []
    # Process PDFs
    if uploaded_pdfs:
        for pdf in uploaded_pdfs:
            try:
                with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
                    text = " ".join([page.get_text() for page in doc])
                    if text.strip():
                        docs.append(Document(page_content=text, metadata={"source": pdf.name}))
            except Exception as e:
                st.error(f"Error reading PDF {pdf.name}: {e}")
        logging.info(f"Processed {len(uploaded_pdfs)} PDF(s).")

    # Process URLs
    if urls:
        try:
            url_docs = UnstructuredURLLoader(urls=urls).load()
            docs.extend(url_docs)
            logging.info(f"Loaded {len(urls)} URL(s).")
        except Exception as e:
            st.error(f"Failed to load URLs. Please check them and try again. Error: {e}")

    if not docs:
        st.error("No valid content found to process.")
    else:
        with st.spinner("Processing documents... This may take a moment."):
            splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            faiss_index = FAISS.from_documents(chunks, embedding=embedder)

            with open(st.session_state.file_path, "wb") as f:
                pickle.dump(faiss_index, f)

            st.success("Documents processed successfully!")
            logging.info("Vector index created and saved.")

# --- NEW: Display Conversation History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- NEW: Chat Input and Q&A Logic ---
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if index exists before generating response
    if not os.path.exists(st.session_state.file_path):
        st.warning("Please process your documents first using the sidebar.")
        st.stop()

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            with open(st.session_state.file_path, "rb") as f:
                faiss_index = pickle.load(f)

            llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama3-8b-8192")
            top_docs = faiss_index.similarity_search(prompt, k=4)
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            answer = chain.run(input_documents=top_docs, question=prompt)

            st.markdown(answer)

            # --- NEW: Show Source Snippets ---
            with st.expander("Show Source Snippets"):
                for i, doc in enumerate(top_docs):
                    source = doc.metadata.get('source', 'Unknown Source')
                    content = doc.page_content.replace('$', '\\$')  # Escape '$' for markdown
                    st.markdown(f"**Snippet {i + 1} from `{source}`:**")
                    st.info(f"{content[:400]}...")

            # Add assistant response to history
            full_response = answer
            st.session_state.messages.append({"role": "assistant", "content": full_response})