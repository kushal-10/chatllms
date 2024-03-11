from driveapi.drive import process_pdf

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 

def create_dnd_database(file_list):
    raw_text = ''
    for pdf in file_list:
        raw_text += process_pdf(pdf)

    embedding = OpenAIEmbeddings()

    text_splitter = CharacterTextSplitter(        
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap  = 200, 
            length_function = len,
        )
    texts = text_splitter.split_text(raw_text)
    print('Length of text: ' + str(len(raw_text)))
    db = FAISS.from_texts(texts, embedding)
    
    return db
