import pandas as pd
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 

os.environ["OPENAI_API_KEY"] = "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"

folder = 'paper_csvs'

list_dirs = os.listdir(folder)

result = ''
for i in range(len(list_dirs)):
    path = os.path.join(folder, list_dirs[i])
    df = pd.read_csv(path)
    result += str(df['response'].iloc[0])

print(len(result))
#21000 words - consultation reports
#12988 words - academic papers

# Split the texts 
text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200, 
    length_function = len,
)
texts = text_splitter.split_text(result)

# Create Embedding
embedding = OpenAIEmbeddings()
db = FAISS.from_texts(texts, embedding)

# Save Embedding
db.save_local("paper_combined/faiss_index")