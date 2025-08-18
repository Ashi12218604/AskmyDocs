import os
import pickle
import streamlit as st
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

# --- Secrets and API Key Handling ---
# This block should be at the very top
# It checks for the Hugging Face token in Streamlit's secrets for deployment
if 'HUGGINGFACEHUB_API_TOKEN' in st.secrets:
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = st.secrets['HUGGINGFACEHUB_API_TOKEN']
# If not found (for local development), it falls back to a .env file
else:
    from dotenv import load_dotenv

    load_dotenv()

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="EchoDocs", page_icon="💡")
st.title("AskMyDocs 📈")
st.sidebar.title("Scheme Article URLs")

# --- URL Input Sidebar ---
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i + 1}")
    if url:
        urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store.pkl"
main_placeholder = st.empty()

# --- Main Logic: Processing URLs and Building Index ---
if process_url_clicked:
    if not urls or all(url == "" for url in urls):
        st.sidebar.error("Please enter at least one URL.")
    else:
        # 1. Load data from URLs
        loader = UnstructuredURLLoader(urls=urls)
        main_placeholder.text("Data Loading... Started... ✅")
        data = loader.load()

        # 2. Split text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
        )
        main_placeholder.text("Text Splitting... Started... ✅")
        docs = text_splitter.split_documents(data)

        # 3. Create embeddings using a free Hugging Face model
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # 4. Create FAISS vector store from documents and embeddings
        vectorstore = FAISS.from_documents(docs, embeddings)
        main_placeholder.text("Embedding Vector Building... Started... ✅")

        # [cite_start]5. Save the FAISS index to a local file for reuse [cite: 20, 27]
        with open(file_path, "wb") as f:
            pickle.dump(vectorstore, f)

        main_placeholder.text("Processing Complete! ✅")
        st.sidebar.success("URLs processed and indexed successfully!")
        # Clear the placeholder text after a short delay or leave a success message
        main_placeholder.empty()

# --- Question Answering Interface ---
query = st.text_input("Ask a question about the schemes:")

if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            # Load the saved FAISS index
            vectorstore = pickle.load(f)

            # Initialize the Hugging Face LLM for question answering
            llm = HuggingFaceHub(repo_id="google/flan-t5-large", task="text2text-generation",
                                 model_kwargs={"temperature": 0.7, "max_length": 512})
            # Create the QA chain
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())

            # Get the result
            result = chain({"question": query}, return_only_outputs=True)

            # Display the answer and sources
            st.header("Answer")
            st.write(result["answer"])

            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")
                for source in sources_list:
                    if source.strip():
                        st.write(source.strip())
    else:
        st.error("Please process the URLs first by clicking the button on the sidebar.")