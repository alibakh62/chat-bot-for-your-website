from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader

import os
from dotenv import load_dotenv

load_dotenv()

loader = DirectoryLoader(
    "websitecrawl/output",
    glob="**/*.txt",
    loader_cls=TextLoader,
)

documents = loader.load()

text_splitter = CharacterTextSplitter(
    chunk_size=1024,
    chunk_overlap=128,
)

texts = text_splitter.split_documents(documents)

persist_directory = "db"


vectordb = Chroma.from_documents(
    documents=texts,
	persist_directory=persist_directory,
	embeddings=OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")),
)

vectordb.persist()