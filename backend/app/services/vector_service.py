import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_FILE = "faiss.index"
TEXT_FILE = "texts.pkl"

try:
    index = faiss.read_index(INDEX_FILE)
    texts = pickle.load(open(TEXT_FILE, "rb"))
except:
    index = faiss.IndexFlatL2(384)
    texts = []

def save():
    faiss.write_index(index, INDEX_FILE)
    pickle.dump(texts, open(TEXT_FILE, "wb"))

def add(text):
    vec = model.encode([text])
    index.add(np.array(vec).astype("float32"))
    texts.append(text)
    save()

def search(query, k=3):
    if index.ntotal == 0:
        return []

    q = model.encode([query])
    D, I = index.search(np.array(q).astype("float32"), k)

    return [texts[i] for i in I[0] if i < len(texts)]