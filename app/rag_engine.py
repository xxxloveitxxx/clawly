from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_hormozi_guardrails(framework: str) -> str:
    db = Chroma(persist_directory="/app/chroma_db", embedding_function=HuggingFaceEmbeddings())
    
    # Query the books for the specific framework rules
    query = f"Alex Hormozi rules and examples for {framework}, scarcity, and value equation."
    docs = db.similarity_search(query, k=3)
    
    return "\n\n".join([doc.page_content for doc in docs])
