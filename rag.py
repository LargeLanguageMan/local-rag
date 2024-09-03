from chromadb.api.models.Collection import Document
from typing_extensions import Doc
from langchain_core import embeddings
from program.text_embed import text_embed
from program.pdf_loader import join_pages, load_documents
from program.chunk_generator import text_split          
import argparse
from langchain_community.llms.ollama import Ollama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
import os
import sys
import shutil


CHROMA_PATH = 'chroma'
DATA_PATH = "data"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    #test_chunks(splits)
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, nargs='?', default=None, help="The query text (optional).")
    parser.add_argument("--update", action="store_true", help="Update the database")
    parser.add_argument("--create", action="store_true",help="Create vector database")
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    query_text = args.query_text
    
    #init db first
    if not db_check() and not args.create:
        print("Your Chroma vector db doesn't exist, use --create")
        sys.exit(1)

    if args.create:
        print(f"Creating db at '{CHROMA_PATH}'. Now use --update for updating your files in the DB")
        Chroma(persist_directory=CHROMA_PATH,create_collection_if_not_exists=True,collection_name="my_rag_project", embedding_function=text_embed())
        print("✅ Vector db has been created")
    if args.reset:
        print("✨ Clearing Database")
        clear_database()
    if args.update:
        print("Updating db")
        documents = load_documents()
        chunks = text_split(documents)
        add_chunks(chunks)
    if args.query_text:
        print(f"Your Query is: '{query_text}'. Please be patient while I generate a response.")
        rag(query_text)
        

def db_check():
    if(os.path.exists(CHROMA_PATH)):
        return True
    else: return False


def add_chunks(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=text_embed()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks



def rag(query_text: str):
   
    #    # Prepare the DB.
    embedding_function = text_embed()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text





def test_chunks(splits: list):

# this is to test chunk size
 print(len(splits[0].page_content))
 i=0
 for chunk in splits:
     print("Chunk: " +str(i))
     print(chunk)
     i = i + 1


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == '__main__':
    main()
