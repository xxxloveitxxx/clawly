import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

print("🧠 Indexing Hormozi Books into Vector DB...")
docs = []
for book in os.listdir("/app/hormozi_books"):
    if book.endswith(".pdf"):
        loader = PyPDFLoader(f"/app/hormozi_books/{book}")
        docs.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# Save locally inside the Docker image
Chroma.from_documents(chunks, HuggingFaceEmbeddings(), persist_directory="/app/chroma_db")
print("✅ Hormozi Guardrails Indexed Successfully.")
