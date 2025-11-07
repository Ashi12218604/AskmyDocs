import os
import logging
import streamlit as st
import fitz  # PyMuPDF
from dotenv import load_dotenv
import time
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq

# =====================================
# Streamlit Config
# =====================================
st.set_page_config(page_title="AskMyDocs", layout="wide", initial_sidebar_state="expanded")

# =====================================
# Dark Mode Styling
# =====================================
def apply_dark_mode_styles():
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


# =====================================
# Sidebar + Session State
# =====================================
st.sidebar.header("Settings")
dark_mode = st.sidebar.toggle("Enable Dark Mode", value=False)
if dark_mode:
    apply_dark_mode_styles()

st.title("AskMyDocs 📝")

# =====================================
# Load API Key
# =====================================
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", None)

if not GROQ_API_KEY:
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ Missing GROQ_API_KEY. Add it in Streamlit Secrets or .env file.")
    st.stop()

# =====================================
# Init States
# =====================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None

os.environ["TOKENIZERS_PARALLELISM"] = "false"

@st.cache_resource(show_spinner=False)
def get_embedder():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# =====================================
# Sidebar Inputs
# =====================================
if st.sidebar.button("Reset History"):
    st.session_state.messages = []
    st.session_state.faiss_index = None
    st.success("✅ History and index cleared.")
    st.rerun()

st.sidebar.header("Upload PDFs or Enter URLs")
uploaded_pdfs = st.sidebar.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
raw_urls = st.sidebar.text_area("Enter URLs (one per line)")
urls = [u.strip() for u in raw_urls.splitlines() if u.strip()]

# =====================================
# Process Documents
# =====================================
if st.sidebar.button("Process Data"):
    docs = []

    # --- Process PDFs ---
    if uploaded_pdfs:
        for pdf in uploaded_pdfs:
            try:
                size_mb = pdf.size / (1024 * 1024)
                if size_mb > 10:
                    st.warning(f"⚠️ {pdf.name} skipped (too large: {size_mb:.2f} MB)")
                    continue

                with fitz.open(stream=pdf.read(), filetype="pdf") as doc_pdf:
                    text = " ".join(page.get_text() for page in doc_pdf)
                    if text.strip():
                        docs.append(Document(page_content=text, metadata={"source": pdf.name}))
            except Exception as e:
                st.error(f"Error reading {pdf.name}: {e}")

    # --- Process URLs ---
    if urls:
        try:
            url_docs = []
            for url in urls:
                loader = WebBaseLoader(url)
                url_docs.extend(loader.load())
            docs.extend(url_docs)
        except Exception as e:
            st.error(f"Failed to load URLs: {e}")

    # --- Build Index ---
    if not docs:
        st.error("No valid content found to process.")
    else:
        with st.spinner("Processing documents... (please wait)"):
            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
            chunks = splitter.split_documents(docs)
            embedder = get_embedder()
            st.session_state.faiss_index = FAISS.from_documents(chunks, embedding=embedder)
            st.success("✅ Documents processed successfully!")


# =====================================
# Conversation History Display
# =====================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("Show Source Snippets"):
                for source in message["sources"]:
                    st.info(source)

# =====================================
# Chat Input / Q&A
# =====================================
prompt = st.chat_input("Ask a question about your documents...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.faiss_index is None:
        st.warning("⚠️ Please process documents first.")
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            faiss_index = st.session_state.faiss_index
            llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant")

            start_time = time.perf_counter()
            top_docs = faiss_index.similarity_search(prompt, k=4)
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            answer = chain.run(input_documents=top_docs, question=prompt)
            end_time = time.perf_counter()
            duration = end_time - start_time

            st.markdown(answer)
            st.caption(f"⏱️ Answer generated in {duration:.2f} seconds")

            # --- Display Sources ---
            sources_for_display = []
            for i, doc in enumerate(top_docs):
                source = doc.metadata.get("source", "Unknown Source")
                content = (doc.page_content or "").replace("$", "\\$")
                snippet = f"**Snippet {i + 1} from `{source}`:**\n\n{content[:400]}..."
                sources_for_display.append(snippet)

            with st.expander("Show Source Snippets"):
                for src in sources_for_display:
                    st.info(src)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources_for_display
            })
