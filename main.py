#create all embeddings, combine all answers and create a merged DB

import os 
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 
import time

from lc_base.chain import openai_chain
from lc_base.database import Data   
from lc_base.logs import save_log

# Store all reports into input_dir and the generated DB for all reports will be saved in output_dir
search_type = "stuff" #map_reduce, stuff
model_type = "gpt-4-1106-preview" #gpt-3.5-turbo, gpt-4-1106-preview
top_k = 70

input_dir = os.path.join("inputs", "policy")
output_dir = os.path.join("outputs", "faiss", "policy_eausa_stuff70")
combined_dir = os.path.join("outputs", "combined", "policy__eausa_stuff70", "faiss_index")

default_query = '''
Please generate a comprehensive summary of this document.
Ensure the summary is presented in a formal style, and if there are any contradictions or variations in the findings, 
address them appropriately. The summary should be approximately 1/6 of your input capacity and can be structured in paragraphs or bullet points.
'''

data = Data(inp_dir=input_dir, out_dir=output_dir)
data.check_output()
data.get_faiss_embeddings()

list_dir = os.listdir(output_dir)

comb_response = ''

for dir in list_dir:
    path = os.path.join(output_dir, dir, 'faiss_index')
    chain = openai_chain(inp_dir=path)
    
    print('Getting reponse for ' + str(dir))
    query = default_query
    start_time = time.time()
    response = chain.get_response(query, k=top_k, type=search_type, model_name=model_type)
    print(response)
    time_taken = time.time() - start_time
    save_log(file_path='logs/combined_policy.csv', query=query, response=response, model_name=model_type, 
             time_taken=time_taken, inp=input_dir, data=dir)
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
db.save_local(combined_dir)







