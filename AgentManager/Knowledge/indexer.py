import os
import yaml
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

from AgentManager.log import logger

import re
from typing import List

# URL to scrape
url = "https://www.paisabazaar.com/sbi-bank/"


base_dir = os.path.dirname(os.path.dirname(__file__))
config_path = os.path.join(base_dir, "config.yaml")

# Load YAML config
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

os.environ["GOOGLE_API_KEY"] = config["google"]["api_key"]

class Indexing:
    def __init__(self):

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config["embedding"]["model"]
            )
        logger.info("Embedding Model Initialized")
        
        self.text_splitter = SemanticChunker(
            self.embeddings
            )

        self.qdrant_client = QdrantClient(
            url=config["qdrant"]["url"],
            api_key = config["qdrant"]["api_key"]
        )
        logger.info("Qdrant Connection Setup Successfully")

        self.collection_name = config["embedding"]["collection_name"]

        # Check if collection exists
        collections = self.qdrant_client.get_collections().collections
        existing_names = [col.name for col in collections]

        if self.collection_name not in existing_names:
            logger.info(f"⚠️ Collection '{self.collection_name}' does not exist. Creating it now...")
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=768,
                    distance=Distance.COSINE
                )
            )
        else:
            logger.info(f"Collection '{self.collection_name}' already exists.")
            pass
        
        self.vector_store = QdrantVectorStore(
            client = self.qdrant_client,
            collection_name = config["qdrant"]["collection_name"],
            embedding = self.embeddings
        )
        logger.info("Vector Store Created Successfully")

        self.retriever = self.vector_store.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 3}
        )
    
    def add_embedding_to_vector_db(self, content: str, metadata: dict = None):
        clean_text = content.replace("\n", " ").replace("\t", " ")
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        chunks = self.text_splitter.create_documents([clean_text])

        if metadata:
            for chunk in chunks:
                if hasattr(chunk, "metadata"):
                    chunk.metadata.update(metadata)
                else:
                    chunk.metadata = metadata

        # Upload documents with metadata
        self.vector_store.add_documents(chunks, batch_size=32)
        print(f"✅ Embeddings uploaded successfully for Document to {self.collection_name}")
    
