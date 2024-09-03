
# local-rag

# Retrieval-Augmented Generation (RAG) System
## Overview

This project implements a Retrieval-Augmented Generation (RAG) system designed to enhance the accuracy and relevance of generated responses by incorporating document retrieval directly into the generation process. By combining retrieved contextual information with a language model, the system can provide more informed and contextually accurate answers.
Purpose

The RAG system is particularly useful when you need to generate responses that are grounded in specific, pre-existing data. By retrieving relevant chunks of information from your data source, the model can produce answers that are not only contextually appropriate but also based on real data, improving reliability and trustworthiness.
Steps of RAG
1. Indexing

    Load Data: Import and load your data using Document Loaders.
    Split Text: Break down large documents into smaller, manageable chunks using text splitters. This makes the data easier to search and process.
    Store Data: Store and index the text chunks using a VectorStore and an Embeddings model, enabling efficient retrieval later.
![alt-text](https://github.com/LargeLanguageMan/llm-project-monks/blob/master/pics/rag1.png)
2. Retrieval and Generation

    Retrieve Data: Retrieve relevant data chunks from storage using a Retriever based on a user’s query.
    Generate Answer: Use a ChatModel or Large Language Model (LLM) to generate a response that incorporates both the user’s query and the retrieved data.


![alt-text](https://github.com/LargeLanguageMan/llm-project-monks/blob/master/pics/rag2.png)

## Installation

To set up the project, first, clone the repository and install the required Python packages by running:

bash

````
git clone https://github.com/LargeLanguageMan/llm-project-monks
cd llm-project-monks
pip install -r requirements.txt
````

## Usage
### Running a Query

    Load Documents: The program loads documents from the specified data directory.
    Split and Store: The documents are split into chunks and stored in a Chroma vector database.
    Query the Database: You can query the database by providing a text input, which will retrieve the most relevant chunks.
    Generate Response: The system then generates a response based on the retrieved data and the input query.

### Example Command

To run a query, use the following command:

bash

````
python rag.py "Your query text here"
````

This will process the query and output a response along with the sources used.
Project Structure

    text_embed.py: Handles text embedding.
    pdf_loader.py: Contains functions to load and process PDF documents.
    chunk_generator.py: Splits documents into smaller text chunks.
    store_embed.py: Adds the embedded chunks to the Chroma database.
    main.py: The main script to run the RAG process, including query handling and response generation.

Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

