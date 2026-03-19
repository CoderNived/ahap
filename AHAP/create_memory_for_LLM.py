# Step 1: Load raw PDF Data
# Step 2: Create Chunks
# Step 3: Create Vector Embeddings
# Step 4: Store Embeddings in FAISS

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import faiss
from langchain_community.document_loaders import PyPDFLoader

# Step 1: Load raw PDF Data
DATA_PATH = r"D:\dhanvantri.ai\AHAP\data\The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND (1).pdf"

def load_pdf_files(data_path):
    loader = PyPDFLoader(data_path)
    documents = loader.load()
    return documents

documents = load_pdf_files(DATA_PATH)
print("Length of Documents:", len(documents))

# Step 2: Create Chunks
def create_chunks(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500,
                                                   chunk_overlap = 50)
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks
text_chunks = create_chunks(documents)
print("Length of Text Chunks:", len(text_chunks))
# Step 3: Create Vector Embeddings
def create_embeddings(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_embeddings = embeddings.embed_documents([chunk.page_content for chunk in text_chunks])
    return vector_embeddings, embeddings
vector_embeddings, embeddings = create_embeddings(text_chunks)

print("Length of Vector Embeddings:", len(vector_embeddings))  # ✅ number of chunks
print("Dimension of Embeddings:", len(vector_embeddings[0]))   # ✅ vector size
# Step 4: Store Embeddings in FAISS