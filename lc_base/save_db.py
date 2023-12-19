# Use this file directly to convert PDFs into FAISS embeddings and save their mapping, specify the desired input and outputs folder

from database import Data
import os

# Store all reports into inp_dir and the generated DB for all reports will be saved in out_dir
data = Data(inp_dir=os.path.join("inputs", "policy"), out_dir=os.path.join("outputs", "combined", "policy_eu_asia_usa"))
data.check_output()
data.get_combined_faiss_embedding()

#Length in Policy EU_Asia is 449198
#Length in policy Eu Asia USA is 967147