import os 
os.environ["OPENAI_API_KEY"] = "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"
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 

from lc_base.chain import openai_chain
from lc_base.database import Data

# Store all reports into inp_dir and the generated DB for all reports will be saved in out_dir
data = Data(inp_dir='inputs', out_dir="outputs")
data.check_output()
data.get_faiss_embeddings()

out_dir = 'outputs'
list_dir = os.listdir(out_dir)

comb_response = ''

for dir in list_dir:
    path = os.path.join(out_dir, dir, 'faiss_index')
    chain = openai_chain(inp_dir=path)
    
    print('Getting reponse for ' + str(dir))
    query = 'What does this report talk about? Please explain in detail.'
    response = chain.get_response(query, k=10, type='stuff') # 'map_reduce' / 'stuff'
    comb_response += str(response)

# Split the texts 
text_splitter = CharacterTextSplitter(        
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200, 
    length_function = len,
)
texts = text_splitter.split_text(comb_response)

# Initialize OPENAI embeddings
embedding = OpenAIEmbeddings()

# Create Embedding
db = FAISS.from_texts(texts, embedding)

# Save Embedding
db.save_local(os.path.join('keypoints', "faiss_index"))







