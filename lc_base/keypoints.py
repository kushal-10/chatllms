#Alternative to save_db + combine.py, create all embeddings and combine all answers

import os 
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 

from chain import openai_chain
from database import Data

# Store all reports into input_dir and the generated DB for all reports will be saved in output_dir
input_dir = os.path.join("inputs", "papers")
output_dir = os.path.join("outputs", "faiss", "papers")
combined_dir = os.path.join("outputs", "combined", "papers_4t_mapred10", "faiss_index")
search_type = "map_reduce" #map_reduce, stuff
model_type = "gpt-4-1106-preview" #gpt-3.5-turbo, gpt-4-1106-preview
top_k = 10
# Summarize the core theoretical frameworks and concepts presented in the paper in a very detailed way.
# I don't know the answer.
# 'What is the introduction, the main methodologies used and the conclusions of the given context? Please explain in a very detailed way.'
# I don't have the information to provide a detailed explanation of the introduction, main methodologies used, and conclusions of the given context. The text provided does not contain full sections of the document required to answer your question with the requested level of detail. To properly address this request, access to the complete document is necessary, including the specific sections that outline the introduction, detail the methodologies, and summarize the conclusions.

default_query = 'Please summarize the context in a very detailed way.'


# data = Data(inp_dir=input_dir, out_dir=output_dir)
# data.check_output()
# data.get_faiss_embeddings()

list_dir = os.listdir(output_dir)

comb_response = ''

for dir in list_dir:
    path = os.path.join(output_dir, dir, 'faiss_index')
    chain = openai_chain(inp_dir=path)
    
    print('Getting reponse for ' + str(dir))
    query = default_query
    response = chain.get_response(query, k=top_k, type=search_type, model_name=model_type)
    comb_response += str(response)
    print(response)

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
db.save_local(combined_dir)







