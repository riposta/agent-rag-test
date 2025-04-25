import openai
import faiss
import numpy as np
import threading

class Retriever:
    def __init__(self, openai_api_key, model="text-embedding-ada-002"):
        self.openai_api_key = openai_api_key
        self.model = model
        openai.api_key = openai_api_key
        self.index = None
        self.texts = []
        self.lock = threading.Lock()
        self.dimension = None
        self.client = openai.OpenAI(api_key=openai_api_key)

    def _get_openai_embedding(self, docs):

        if not docs or not isinstance(docs, str):
            text = [doc['text'] for doc in docs]
        else:
            text = docs
        response = self.client.embeddings.create(model=self.model, input=text)
        return response.data[0].embedding

    def clear(self):
        with self.lock:
            self.index = None
            self.texts = []
            self.dimension = None

    def add_documents(self, docs):
        embs = [self._get_openai_embedding(doc) for doc in docs]
        embs_np = np.array(embs).astype("float32")
        with self.lock:
            if self.index is None:
                self.dimension = embs_np.shape[1]
                self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(embs_np)
            self.texts.extend(docs)

    def get_top(self, query, k=1):
        emb = np.array([self._get_openai_embedding(query)]).astype("float32")
        with self.lock:
            if self.index is None or self.index.ntotal == 0:
                return [], None
            D, I = self.index.search(emb, k)
            return [self.texts[i] for i in I[0] if i < len(self.texts)], D[0][0]
