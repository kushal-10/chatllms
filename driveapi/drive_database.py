# Change this in gradio
import os
from driveapi.drive import drive_content
from driveapi.service import get_shared_folder_id

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 

# drive_shared_link = os.environ.get('DRIVE_LINK')
# shared_folder_id = get_shared_folder_id(drive_shared_link)

def create_chroma_db():
    drive_shared_link = os.environ.get('DRIVE_LINK')
    if drive_shared_link == None:
        return ""
    shared_folder_id = get_shared_folder_id(drive_shared_link)
    raw_text = drive_content(shared_folder_id)
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
