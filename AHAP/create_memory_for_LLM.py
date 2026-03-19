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