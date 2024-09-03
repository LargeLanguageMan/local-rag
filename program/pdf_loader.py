from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader


DATA_PATH = "data"

def load_documents():
    #for final project, change code to read all files in folder
    document_loaders = PyPDFDirectoryLoader(DATA_PATH)
    return document_loaders.load()

def join_pages(documents):
    page_arr = []
    for page in documents:
        page_arr.append(page)
    return page_arr
