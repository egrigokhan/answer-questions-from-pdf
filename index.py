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
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import CharacterTextSplitter
import pathlib
import subprocess
import tempfile
import pickle
import os

from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI


def source_docs(github_repo):
    return list(get_github_docs(github_repo.split("/")[0], github_repo.split("/")[1]))


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
        return_only_outputs=True,
    )["output_text"]


def run(msg):
    return print_answer(msg)

def setup(config):
    os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
    os.environ["pdf_file"] = config["pdf_file"]

    loader = UnstructuredFileLoader(os.environ["pdf_file"])
    docs = loader.load()

    search_index(docs)
