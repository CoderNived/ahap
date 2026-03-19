# Step 1: Load raw PDF Data
# Step 2: Create Chunks
# Step 3: Create Vector Embeddings
# Step 4: Store Embeddings in FAISS

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import faiss
# Step 1: Load raw PDF Data
DATA_PATH= r"D:\dhanvantri.ai\AHAP\data\The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND (1).pdf"
def load_pdf_files(data_path):
    loader = PyPDFLoader(data_path,
                         glob=*.pdf,
                         show_progress=True,
                         loader_cls=pyPDFLoader)
    documents = loader.load()
    return documents