import os
import logging
import streamlit as st
import fitz  # PyMuPDF
from dotenv import load_dotenv
import time  # <-- ADDED TIME MODULE

# CORRECTED: UnstructuredURLLoader is in langchain_community
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq

# =========================
# Page Config
# =========================
st.set_page_config(page_title="AskMyDocs", layout="wide", initial_sidebar_state="expanded")


# =========================
# Custom CSS for Dark Mode
# =========================
def apply_dark_mode_styles():
    # Fixed indentation for the markdown block
    st.markdown("""
    <style>
        .stApp { background-color: #111111; }
        header { background-color: transparent !important; }
        [data-testid="stAppViewContainer"] > .main { background-color: #1E1E1E; }
        [data-testid="stSidebar"] { background-color: #191919; }
        [data-testid="stHeading"] h1 { color: #FFFFFF !important; }
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, h2, h3, h4 { color: #FFFFFF !important; }
        .stButton > button {
            background-color: #D32F2F; color: #FFFFFF; font-weight: bold;
            border: none; border-radius: 8px; padding: 10px 24px;
        }
        .stButton > button:hover { background-color: #B71C1C; }
        [data-testid="stChatInput"] { background-color: #191919; }
    </style>
    """, unsafe_allow_html=True)


# =========================
# Sidebar & State
# =========================
st.sidebar.header("Settings")
dark_mode = st.sidebar.toggle("Enable Dark Mode", value=False)
if dark_mode:
    apply_dark_mode_styles()

st.title("AskMyDocs 📝")

# Load API key
# Use st.secrets for deployment
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    # Fallback to .env for local development
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Missing GROQ_API_KEY. Add it in Streamlit Secrets or a local .env file.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None


@st.cache_resource(show_spinner=False)
def get_embedder():
    # Use a well-regarded, lightweight embedding model
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


if st.sidebar.button("Reset History"):
    st.session_state.messages = []
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
    docs = []
    if uploaded_pdfs:
        for pdf in uploaded_pdfs:
            try:
                # Read PDF content using PyMuPDF
                with fitz.open(stream=pdf.read(), filetype="pdf") as doc_pdf:
                    text = " ".join([page.get_text() for page in doc_pdf])
                    if text.strip():
                        docs.append(Document(page_content=text, metadata={"source": pdf.name}))
            except Exception as e:
                st.error(f"Error reading PDF {getattr(pdf, 'name', 'uploaded file')}: {e}")
    if urls:
        try:
            # Load URLs
            url_docs = UnstructuredURLLoader(urls=urls).load()
            docs.extend(url_docs)
        except Exception as e:
            st.error(f"Failed to load URLs. Please check them and try again. Error: {e}")

    if not docs:
        st.error("No valid content found to process.")
    else:
        with st.spinner("Processing documents... (this may take a moment)"):
            # Split documents into chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            if not chunks:
                st.error("Could not extract any text chunks from the documents.")
            else:
                # Create embeddings and FAISS index
                embedder = get_embedder()
                st.session_state.faiss_index = FAISS.from_documents(chunks, embedding=embedder)
                st.success("Documents processed successfully!")

# =========================
# Conversation History (UI)
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("Show Source Snippets"):
                for source in message["sources"]:
                    st.info(source)

# =========================
# Chat Input / Q&A
# =========================
prompt = st.chat_input("Ask a question about your documents...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.faiss_index is None:
        st.warning("Please process your documents first using the sidebar.")
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            faiss_index = st.session_state.faiss_index

            # --- MODEL UPDATED ---
            # Use a fast and capable model from Groq
            # gemma2-9b-it was decommissioned, using recommended replacement
            llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant")
            # --- END OF UPDATE ---

            # --- START TIMER ---
            start_time = time.perf_counter()

            # Search for relevant documents
            top_docs = faiss_index.similarity_search(prompt, k=4)  # Increased k for better context

            chain = load_qa_chain(llm=llm, chain_type="stuff")
            answer = chain.run(input_documents=top_docs, question=prompt)

            # --- END TIMER ---
            end_time = time.perf_counter()
            duration = end_time - start_time
            # --- END TIMER ---

            st.markdown(answer)

            # --- DISPLAY TIME TAKEN ---
            st.caption(f"Time taken to answer: {duration:.2f} seconds")
            # --- END DISPLAY ---

            # Format sources for display
            sources_for_display = []
            for i, doc in enumerate(top_docs):
                source = doc.metadata.get("source", "Unknown Source")
                # Clean content for display
                content = (doc.page_content or "").replace("$", "\\$")
                source_info = f"**Snippet {i + 1} from `{source}`:**\n\n{content[:400]}..."
                sources_for_display.append(source_info)

            with st.expander("Show Source Snippets"):
                for source_item in sources_for_display:
                    st.info(source_item)

            assistant_message = {"role": "assistant", "content": answer, "sources": sources_for_display}
            st.session_state.messages.append(assistant_message)

