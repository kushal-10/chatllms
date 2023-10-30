from database import Data

# 1 cent to create embeddings for 9 reports
# Store all reports into inp_dir and the generated DB for all reports will be saved in out_dir
data = Data(inp_dir='inputs', out_dir="outputs")
data.check_output()
data.get_faiss_embeddings()
