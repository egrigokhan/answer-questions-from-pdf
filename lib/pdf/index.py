from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

def loadAndChunkPDFFile(file_path):
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load()
    
    chain = load_qa_with_sources_chain(llm, chain_type="stuff")
    return chain({"input_documents": docs, "question": query}, return_only_outputs=True)["output_text"]
