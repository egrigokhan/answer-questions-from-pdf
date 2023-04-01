# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iLKoiz_6MQnljz9Yzs_jHUfZKF0wax8F
"""

# Commented out IPython magic to ensure Python compatibility.
# %cd langchain-github-bot/

from langchain.llms import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import CharacterTextSplitter
import pickle
import os

from langchain.document_loaders import PyPDFLoader
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI

def search_index(source_docs):
    source_chunks = []
    splitter = CharacterTextSplitter(
        separator=" ", chunk_size=1024, chunk_overlap=0)
    for source in source_docs:
        for chunk in splitter.split_text(source.page_content):
            source_chunks.append(
                Document(page_content=chunk, metadata=source.metadata))

    with open("search_index.pickle", "wb") as f:
        pickle.dump(FAISS.from_documents(source_chunks, OpenAIEmbeddings()), f)


def print_answer(question):
    chain = load_qa_with_sources_chain(OpenAI(temperature=0))

    with open("search_index.pickle", "rb") as f:
        search_index = pickle.load(f)

    return chain(
        {
            "input_documents": search_index.similarity_search(question, k=4),
            "question": question,
        },
        return_only_outputs=False,
    )["output_text"]


def run(message, history):
    return print_answer(message)

def setup(config):
    os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
    os.environ["pdf_file"] = config["pdf_file"]

    # UnstructuredReader = download_loader("UnstructuredReader")

    # loader = UnstructuredReader()
    # docs = loader.load_data(file='Personal Information Form.pdf')
    # print(docs)

    loader = PyPDFLoader(os.environ["pdf_file"])
    docs = loader.load()

    search_index(docs)
