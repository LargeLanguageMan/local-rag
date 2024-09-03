from chromadb.api.models.Collection import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def text_split(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=200,length_function =len , add_start_index=True,is_separator_regex=False
    )
    all_splits = text_splitter.split_documents(documents)
    return all_splits

# this is to test chunk size
# print(len(all_splits[0].page_content))
# i=0
# for chunk in all_splits:
#     print("Chunk: " +str(i))
#     print(chunk)
#     i = i + 1
