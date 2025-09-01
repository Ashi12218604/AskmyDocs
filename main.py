import os
import shutil
import logging
import tempfile
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

# =========================
# Page Config (must be the first Streamlit command)
# =========================
st.set_page_config(page_title="AskMyDocs", layout="wide", initial_sidebar_state="expanded")


# =========================
# Custom CSS for Dark Mode
# =========================
def apply_dark_mode_styles():
    st.markdown("""
    <style>
        /* Base app background */
        .stApp {
            background-color: #111111;
        }
        /* Remove the white bar at the top */
        header {
            background-color: transparent !important;
        }
        /* Main content area */
        [data-testid="stAppViewContainer"] > .main {
            background-color: #1E1E1E;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #191919;
        }
        /* All Headers (h1, h2, h3) are now white */
        h1, h2, h3, h4 {
            color: #FFFFFF !important;
        }
        /* Generated text color */
        [data-testid="stChatMessage"] p {
            color: #00D1C1 !important; /* Vibrant Peacock Green/Teal */
        }
        /* Buttons */
        .stButton > button {
            background-color: #D32F2F; /* Red background */
            color: #FFFFFF; /* White text */
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
        }
        .stButton > button:hover {
            background-color: #B71C1C; /* Darker red on hover */
        }
        /* Chat Input Box */
        [data-testid="stChatInput"] {
            background-color: #191919;
        }
    </style>
    """, unsafe_allow_html=True)


# Sidebar: Dark mode toggle
st.sidebar.header("Settings")
dark_mode = st.sidebar.toggle("Enable Dark Mode", value=False)
if dark_mode:
    apply_dark_mode_styles()

st.title("AskMyDocs 📝")

# =========================
# Secrets / Environment
# =========================
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Missing GROQ_API_KEY. Add it in Streamlit Secrets (Cloud) or in a local .env file.")
    st.stop()

# =========================
# Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []
# --- FIX: Store the FAISS index in session state instead of a file ---
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None


# =========================
# Cached resources
# =========================
@st.cache_resource(show_spinner=False)
def get_embedder():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# =========================
# Sidebar Controls
# =========================
if st.sidebar.button("Reset History"):
    st.session_state.messages = []
    # --- FIX: Clear the index from session state ---
    st.session_state.faiss_index = None
    st.success("History and document index cleared.")
    st.rerun()

st.sidebar.header("Upload PDFs or Enter URLs")
uploaded_pdfs = st.sidebar.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
raw_urls = st.sidebar.text_area("Enter URLs (one per line)")
urls = [u.strip() for u in raw_urls.splitlines() if u.strip()]

# =========================
# Process Data
# =========================
if st.sidebar.button("Process Data"):
    # --- FIX: Clear old index from session state ---
    st.session_state.faiss_index = None

    docs = []
    if uploaded_pdfs:
        for pdf in uploaded_pdfs:
            try:
                with fitz.open(stream=pdf.read(), filetype="pdf") as doc_pdf:
                    text = " ".join([page.get_text() for page in doc_pdf])
                    if text.strip():
                        docs.append(Document(page_content=text, metadata={"source": pdf.name}))
            except Exception as e:
                st.error(f"Error reading PDF {getattr(pdf, 'name', 'uploaded file')}: {e}")
    if urls:
        try:
            url_docs = UnstructuredURLLoader(urls=urls).load()
            docs.extend(url_docs)
        except Exception as e:
            st.error(f"Failed to load URLs. Please check them and try again. Error: {e}")

    if not docs:
        st.error("No valid content found to process.")
    else:
        with st.spinner("Processing documents..."):
            splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            if not chunks:
                st.error("Could not extract any text from the provided documents. Please check the files/URLs.")
                st.stop()

            embedder = get_embedder()
            # --- FIX: Save the index directly to session state ---
            st.session_state.faiss_index = FAISS.from_documents(chunks, embedding=embedder)
            st.success("Documents processed successfully!")

# =========================
# Conversation History (UI)
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# Chat Input / Q&A
# =========================
prompt = st.chat_input("Ask a question about your documents...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- FIX: Check for the index in session state ---
    if st.session_state.faiss_index is None:
        st.warning("Please process your documents first using the sidebar.")
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            faiss_index = st.session_state.faiss_index
            llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama3-8b-8192")
            top_docs = faiss_index.similarity_search(prompt, k=3)
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            answer = chain.run(input_documents=top_docs, question=prompt)
            st.markdown(answer)

            with st.expander("Show Source Snippets"):
                for i, doc in enumerate(top_docs):
                    source = doc.metadata.get("source", "Unknown Source")
                    content = (doc.page_content or "").replace("$", "\\$")
                    st.markdown(f"**Snippet {i + 1} from `{source}`:**")
                    st.info(f"{content[:400]}...")

            st.session_state.messages.append({"role": "assistant", "content": answer})

